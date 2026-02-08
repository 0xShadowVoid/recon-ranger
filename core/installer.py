"""Simple installer with progress bars - kept short"""
import os, sys, shutil, subprocess, tempfile, re
from pathlib import Path
from typing import Dict, Tuple
from core.system import SystemChecker
from core.logger import setup_logging, get_error_logger

try:
    from tqdm import tqdm
except ImportError:
    class tqdm:
        def __init__(self, iterable=None, total=None, desc=''):
            self.iterable = iterable
            self.total, self.desc = total, desc
            self.n = 0
        def __iter__(self):
            print(f"Installing {self.desc}...")
            for item in self.iterable:
                yield item
                self.n += 1
        def update(self, n=1):
            pass
        def close(self):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

logger = setup_logging()
error_logger = get_error_logger()

class Colors:
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
    BLUE = '\033[94m'; CYAN = '\033[96m'; RESET = '\033[0m'; BOLD = '\033[1m'

class ReconRangerInstaller:
    def __init__(self, tools: Dict):
        self.tools = tools
        self.gobin = Path.home() / "go" / "bin"
        self.bin_dir = Path("/usr/local/bin")
        self.system = SystemChecker()
        self.results = {}

    def _run(self, cmd: list, cwd=None, timeout=300) -> Tuple[bool, str]:
        """Execute command, return (success, output)"""
        try:
            env = {
                **os.environ, 
                "GOBIN": str(self.gobin), 
                "GOPATH": str(Path.home() / "go"),
                "GOPROXY": "https://proxy.golang.org,direct",
                "GOSUMDB": "sum.golang.org",
                "CGO_ENABLED": "0"
            }
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd, env=env)
            return (r.returncode == 0, r.stderr if r.returncode else r.stdout)
        except subprocess.TimeoutExpired as e:
            error_logger.error(f"Command timed out: {' '.join(cmd)}")
            return (False, f"Timeout after {timeout}s")
        except Exception as e:
            error_logger.error(f"Command failed: {' '.join(cmd)} - {str(e)}")
            return (False, str(e))

    def _is_installed(self, binary: str) -> bool:
        """Check if binary exists in PATH or common locations"""
        if shutil.which(binary):
            return True
        # Check common locations
        for path in [self.gobin / binary, self.bin_dir / binary, Path.home() / ".local" / "bin" / binary]:
            if path.exists():
                return True
        return False

    def _get_version(self, binary: str) -> str:
        """Get installed version of a tool"""
        # Find the binary path
        binary_path = shutil.which(binary)
        if not binary_path:
            for path in [self.gobin / binary, self.bin_dir / binary, Path.home() / ".local" / "bin" / binary]:
                if path.exists():
                    binary_path = str(path)
                    break
        if not binary_path:
            return None
        
        # Try common version flags
        version_flags = ['--version', '-version', '-V', '-v']
        for flag in version_flags:
            try:
                result = subprocess.run([binary_path, flag], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    output = result.stdout or result.stderr
                    # Extract version number using regex
                    version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', output)
                    if version_match:
                        return version_match.group(1)
            except:
                continue
        return None

    def _needs_update(self, name: str, cfg: dict) -> bool:
        """Check if tool needs update - for now always update if installed via go/pip/git"""
        ttype = cfg.get("type")
        if ttype == "go":
            # Go tools installed via @latest always get latest
            return True
        elif ttype == "python":
            # Python tools - pip will handle updates
            return True
        elif ttype == "git":
            # Git tools - pull will get latest
            return True
        elif ttype == "apt":
            # APT tools - let apt decide
            return True
        return False

    def install_go(self, name: str, cfg: dict) -> bool:
        """Install Go tool via apt or go install"""
        binary = cfg["binary"]
        if cfg.get("apt"):
            ok, _ = self._run(["apt-get", "install", "-y", "-qq", cfg["apt"]], timeout=180)
            if ok and self._is_installed(binary):
                return True
        # Ensure go bin directory exists
        self.gobin.mkdir(parents=True, exist_ok=True)
        # Run go install with longer timeout for large tools
        print(f"    Downloading {name}...", end="", flush=True)
        ok, err = self._run(["go", "install", f"{cfg['package']}@latest"], timeout=600)
        if not ok:
            error_logger.error(f"Failed to install {name}: {err}")
            print(f"\r    {name} failed: {err[:100]}")
            return False
        print(f"\r    {name} compiled ")
        if ok:
            src = self.gobin / binary
            if src.exists():
                dst = self.bin_dir / binary
                # Copy instead of symlink for reliability
                if dst.exists():
                    dst.unlink()
                shutil.copy2(src, dst)
                dst.chmod(0o755)
                return self._is_installed(binary)
            else:
                # Binary might be in GOPATH/bin directly
                for alt_src in [Path.home() / "go" / "bin" / binary, Path("/root/go/bin") / binary]:
                    if alt_src.exists():
                        dst = self.bin_dir / binary
                        if dst.exists():
                            dst.unlink()
                        shutil.copy2(alt_src, dst)
                        dst.chmod(0o755)
                        return self._is_installed(binary)
        return False

    def install_python(self, name: str, cfg: dict) -> bool:
        """Install Python tool via pip"""
        py = sys.executable
        pkg = cfg["package"]
        binary = cfg["binary"]
        flags = ["install", "-q", "--no-cache-dir"]
        if sys.version_info >= (3, 11):
            flags.insert(1, "--break-system-packages")
        ok, _ = self._run([py, "-m", "pip"] + flags + [pkg], timeout=120)
        if ok:
            # Check if binary is now available
            if self._is_installed(binary):
                return True
            # Try to find and link the module as executable
            try:
                result = subprocess.run([py, "-c", f"import {binary}; print({binary}.__file__)"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    module_path = Path(result.stdout.strip())
                    # Create a launcher script
                    launcher = self.bin_dir / binary
                    launcher.write_text(f"#!/usr/bin/env python3\nimport sys\nimport {binary}\nif hasattr({binary}, 'main'):\n    {binary}.main()\nelse:\n    print('Module {binary} has no main function')\n")
                    launcher.chmod(0o755)
                    return True
            except:
                pass
        return ok and self._is_installed(binary)

    def install_apt(self, name: str, cfg: dict) -> bool:
        """Install via apt"""
        ok, _ = self._run(["apt-get", "install", "-y", "-qq", cfg["apt"]], timeout=180)
        return ok and self._is_installed(cfg["binary"])

    def install_git(self, name: str, cfg: dict) -> bool:
        """Install from git repo"""
        path = Path(cfg["path"])
        binary = cfg["binary"]
        if path.exists():
            self._run(["git", "-C", str(path), "pull", "--quiet"], timeout=60)
        else:
            ok, _ = self._run(["git", "clone", "--depth", "1", "--quiet", cfg["repo"], str(path)], timeout=180)
            if not ok:
                return False
        if "requirements" in cfg:
            py = sys.executable
            flags = ["install", "-q"]
            if sys.version_info >= (3, 11):
                flags.append("--break-system-packages")
            reqs = cfg["requirements"]
            if reqs[0] == "-r":
                self._run([py, "-m", "pip"] + flags + reqs, timeout=120)
            else:
                self._run([py, "-m", "pip"] + flags + reqs, timeout=120)
        if "post_clone" in cfg:
            self._run(cfg["post_clone"].split(), cwd=path, timeout=120)
        if "build_cmd" in cfg:
            # Use Go environment for build commands
            build_env = {**os.environ, "GOBIN": str(self.gobin), "GOPATH": str(Path.home() / "go")}
            subprocess.run(cfg["build_cmd"].split(), cwd=path, timeout=120, env=build_env)
        launcher = self.bin_dir / binary
        if "entrypoint" in cfg:
            launcher.write_text(f"#!/bin/bash\nexec {sys.executable} {cfg['entrypoint']} \"\$@\"\n")
        elif (path / binary).exists():
            if launcher.exists():
                launcher.unlink()
            # Copy instead of symlink for reliability
            shutil.copy2(path / binary, launcher)
        else:
            for f in path.rglob(binary):
                if launcher.exists():
                    launcher.unlink()
                shutil.copy2(f, launcher)
                break
        launcher.chmod(0o755)
        return self._is_installed(binary)

    def install_one(self, name: str, update=False, smart=False) -> str:
        """Install single tool, returns status: 'installed', 'updated', 'skipped', 'failed'"""
        cfg = self.tools[name]
        ttype = cfg["type"]
        binary = cfg["binary"]
        
        is_installed = self._is_installed(binary)
        
        # Smart mode: skip if installed and no update needed
        if smart and is_installed and not update:
            if not self._needs_update(name, cfg):
                return 'skipped'
        
        # Normal mode: skip if already installed and not forcing update
        if not update and not smart and is_installed:
            return 'skipped'
        
        # Determine if this is an update or fresh install
        is_update = is_installed and (update or smart)
        
        methods = {
            "go": self.install_go,
            "python": self.install_python,
            "apt": self.install_apt,
            "git": self.install_git,
        }
        
        result = methods.get(ttype, lambda n, c: False)(name, cfg)
        
        if result and "post_install" in cfg:
            self._run(cfg["post_install"].split(), timeout=120)
        
        if result:
            return 'updated' if is_update else 'installed'
        else:
            return 'failed'

    def run(self, args):
        """Main install flow with progress bar"""
        if args.tools:
            invalid = [t for t in args.tools if t not in self.tools]
            if invalid:
                print(f"{Colors.RED}Unknown: {', '.join(invalid)}{Colors.RESET}")
                sys.exit(1)
        
        print(f"{Colors.BLUE}Checking system...{Colors.RESET}")
        self.system.check_python_version()
        go_ver = self.system.check_go_version()
        print(f"{Colors.GREEN}✓ Python OK, Go {go_ver}{Colors.RESET}")
        self.system.check_disk_space()
        self.system.check_internet()
        
        if os.geteuid() != 0:
            print(f"{Colors.RED}✗ Run with sudo{Colors.RESET}")
            sys.exit(1)
        
        if args.all:
            targets = list(self.tools.keys())
        elif args.tools:
            targets = args.tools
        else:
            print(f"\n{Colors.CYAN}Tools:{Colors.RESET}")
            for i, (name, cfg) in enumerate(self.tools.items(), 1):
                print(f"  {i}. {name:18} {cfg['description'][:45]}")
            print(f"\nSelect (1-{len(self.tools)}) or 'all': ", end="")
            choice = input().strip().lower()
            if choice == "all":
                targets = list(self.tools.keys())
            else:
                try:
                    idx = int(choice) - 1
                    targets = [list(self.tools.keys())[idx]]
                except:
                    print("Invalid")
                    sys.exit(1)
        
        print(f"\n{Colors.BLUE}Installing {len(targets)} tools...{Colors.RESET}\n")
        
        # Track results by status
        installed = []
        updated = []
        skipped = []
        failed = []
        
        with tqdm(total=len(targets), desc="Progress") as pbar:
            for name in targets:
                status = self.install_one(name, args.update, args.smart)
                
                if status == 'installed':
                    icon, color = "✓", Colors.GREEN
                    installed.append(name)
                elif status == 'updated':
                    icon, color = "↻", Colors.YELLOW
                    updated.append(name)
                elif status == 'skipped':
                    icon, color = "⊘", Colors.CYAN
                    skipped.append(name)
                else:  # failed
                    icon, color = "✗", Colors.RED
                    failed.append(name)
                
                print(f"{color}{icon}{Colors.RESET} {name:18}")
                pbar.update(1)
        
        # Summary
        total = len(targets)
        print(f"\n{Colors.GREEN}✓ Installed: {len(installed)}{Colors.RESET}")
        if updated:
            print(f"{Colors.YELLOW}↻ Updated: {len(updated)}{Colors.RESET}")
        if skipped:
            print(f"{Colors.CYAN}⊘ Skipped (already installed): {len(skipped)}{Colors.RESET}")
        if failed:
            print(f"{Colors.RED}✗ Failed: {', '.join(failed)}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}Next: python3 ApiKeyMaster.py --configure{Colors.RESET}")