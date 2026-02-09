"""Simple installer with progress bars - v2.0 surgical toolkit"""
import os, sys, shutil, subprocess, tempfile, re
from pathlib import Path
from typing import Dict, Tuple, List
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
        # Use actual user's home directory even when running with sudo
        actual_home = os.environ.get('SUDO_USER')
        if actual_home:
            self.user_home = Path(f"/home/{actual_home}")
        else:
            self.user_home = Path.home()
        
        self.gobin = self.user_home / "go" / "bin"
        self.bin_dir = Path("/usr/local/bin")
        self.system = SystemChecker()
        self.results = {}
        
        # v2.0: Add backup directory for rollback protection
        self.backup_dir = self.user_home / ".recon-backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def install_category(self, category: str) -> bool:
        """Install all tools from a category"""
        from core.config import CATEGORIES
        if category not in CATEGORIES:
            print(f"{Colors.RED}❌ Unknown category: {category}{Colors.RESET}")
            print(f"{Colors.CYAN}Available categories: {', '.join(CATEGORIES.keys())}{Colors.RESET}")
            return False
            
        tools_to_install = CATEGORIES[category]
        print(f"{Colors.BLUE}📂 Installing {category} category ({len(tools_to_install)} tools){Colors.RESET}")
        return self._install_tools_list(tools_to_install)
        
    def install_multiple_tools(self, numbers: List[int]) -> bool:
        """Install tools by number (1-indexed)"""
        tool_list = list(self.tools.keys())
        tools_to_install = []
        
        for num in numbers:
            if 1 <= num <= len(tool_list):
                tool_name = tool_list[num - 1]
                tools_to_install.append(tool_name)
            else:
                print(f"{Colors.YELLOW}⚠️ Tool #{num} not found (1-{len(tool_list)}){Colors.RESET}")
                
        if not tools_to_install:
            print(f"{Colors.RED}❌ No valid tools specified{Colors.RESET}")
            return False
            
        print(f"{Colors.BLUE}🔧 Installing {len(tools_to_install)} tools by number{Colors.RESET}")
        return self._install_tools_list(tools_to_install)
        
    def install_range(self, start: int, end: int, skip: List[int] = None) -> bool:
        """Install tools in a range, optionally skipping some"""
        tool_list = list(self.tools.keys())
        skip = skip or []
        
        if start < 1 or end > len(tool_list) or start > end:
            print(f"{Colors.RED}❌ Invalid range: {start}-{end} (1-{len(tool_list)}){Colors.RESET}")
            return False
            
        tools_to_install = []
        for i in range(start, end + 1):
            if i not in skip:
                tool_name = tool_list[i - 1]
                tools_to_install.append(tool_name)
                
        if not tools_to_install:
            print(f"{Colors.RED}❌ No tools to install in range {start}-{end}{Colors.RESET}")
            return False
            
        skip_str = f" (skipping {skip})" if skip else ""
        print(f"{Colors.BLUE}🔧 Installing range {start}-{end}{skip_str}: {len(tools_to_install)} tools{Colors.RESET}")
        return self._install_tools_list(tools_to_install)
        
    def _install_tools_list(self, tools_to_install: List[str]) -> bool:
        """Internal method to install a list of tools"""
        success_list = []
        failed_list = []
        
        with tqdm(total=len(tools_to_install), desc="Installing tools", unit="tool") as pbar:
            for tool_name in tools_to_install:
                if tool_name not in self.tools:
                    print(f"{Colors.YELLOW}⚠️ Tool '{tool_name}' not found in configuration{Colors.RESET}")
                    failed_list.append(tool_name)
                    pbar.update(1)
                    continue
                    
                # Backup existing binary if it exists
                self._backup_tool(tool_name)
                
                # Install using install_one method
                status = self.install_one(tool_name, update=False, smart=False)
                if status in ['installed', 'updated']:
                    success_list.append(tool_name)
                    self.results[tool_name] = True
                else:
                    failed_list.append(tool_name)
                    self.results[tool_name] = False
                    
                pbar.update(1)
                
        # Summary
        print(f"\n{Colors.GREEN}✅ Successfully installed: {', '.join(success_list) if success_list else 'None'}{Colors.RESET}")
        if failed_list:
            print(f"{Colors.RED}❌ Failed: {', '.join(failed_list)}{Colors.RESET}")
            
        return len(failed_list) == 0
        
    def _backup_tool(self, tool_name: str):
        """Create timestamped backup before installation"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Find existing binary
        tool_config = self.tools[tool_name]
        binary_name = tool_config.get('binary', tool_name)
        
        # Check common locations
        locations = [
            self.gobin / binary_name,
            self.bin_dir / binary_name,
            Path(f"/usr/bin/{binary_name}"),
            Path(f"/usr/local/bin/{binary_name}")
        ]
        
        for location in locations:
            if location.exists():
                backup_path = self.backup_dir / f"{binary_name}_{timestamp}"
                try:
                    shutil.copy2(location, backup_path)
                    logger.info(f"Backed up {binary_name} to {backup_path}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to backup {binary_name}: {e}")
                    
    def rollback_tool(self, tool_name: str) -> bool:
        """Rollback a tool to the last backup"""
        tool_config = self.tools[tool_name]
        binary_name = tool_config.get('binary', tool_name)
        
        # Find latest backup
        backups = list(self.backup_dir.glob(f"{binary_name}_*"))
        if not backups:
            print(f"{Colors.YELLOW}⚠️ No backup found for {binary_name}{Colors.RESET}")
            return False
            
        latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
        
        # Restore backup
        target_location = self.gobin / binary_name
        try:
            shutil.copy2(latest_backup, target_location)
            os.chmod(target_location, 0o755)
            print(f"{Colors.GREEN}✅ Rolled back {binary_name} to backup from {latest_backup.name}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to rollback {binary_name}: {e}{Colors.RESET}")
            return False

    def _find_go(self) -> str:
        """Find Go binary in common locations"""
        for path in ["/usr/local/go/bin/go", "/usr/local/bin/go", "/usr/bin/go", shutil.which("go")]:
            if path and Path(path).exists():
                return path
        return "go"  # Fallback to PATH

    def _run(self, cmd: list, cwd=None, timeout=300) -> Tuple[bool, str]:
        """Execute command, return (success, output)"""
        try:
            # Replace 'go' with full path if it's the first argument
            if cmd and cmd[0] == "go":
                cmd[0] = self._find_go()
            
            env = {
                **os.environ, 
                "GOBIN": str(self.gobin), 
                "GOPATH": str(self.user_home / "go"),
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

    def _find_binary_path(self, binary: str) -> str:
        """Find the path of an installed binary"""
        # Check common locations in order
        for path in [self.gobin / binary, self.bin_dir / binary, Path.home() / ".local" / "bin" / binary]:
            if path.exists():
                return str(path)
        
        # Check system PATH
        system_path = shutil.which(binary)
        if system_path:
            return system_path
            
        return "Not found"

    def _is_installed(self, binary: str) -> bool:
        """Check if binary exists in PATH or common locations"""
        if shutil.which(binary):
            return True
        # Check common locations
        for path in [self.gobin / binary, self.bin_dir / binary, Path.home() / ".local" / "bin" / binary]:
            if path.exists():
                return True
        return False

    def _install_single_tool(self, tool_name: str) -> bool:
        """Install a single tool using the existing install_one method"""
        try:
            status = self.install_one(tool_name, update=False, smart=False)
            return status in ['installed', 'updated']
        except Exception as e:
            error_logger.error(f"Failed to install {tool_name}: {e}")
            return False

    def install_go(self, name: str, cfg: dict) -> bool:
        """Install Go tool via apt or go install"""
        binary = cfg["binary"]
        
        # Try apt only if available and quick
        if cfg.get("apt"):
            ok, _ = self._run(["apt-cache", "show", cfg["apt"]], timeout=10)
            if ok:
                ok, _ = self._run(["apt-get", "install", "-y", "-qq", cfg["apt"]], timeout=60)
                if ok and self._is_installed(binary):
                    return True
        
        # Ensure go bin directory exists
        self.gobin.mkdir(parents=True, exist_ok=True)
        
        # Run go install with longer timeout for large tools
        print(f"    Downloading {name}...", end="", flush=True)
        package = cfg['package']
        # Don't add @latest if package already has version
        if '@' not in package:
            package = f"{package}@latest"
        ok, err = self._run(["go", "install", package], timeout=600)
        if not ok:
            error_logger.error(f"Failed to install {name}: {err}")
            print(f"\r    {name} failed: {err[:100]}")
            return False
        print(f"\r    {name} compiled ")
        
        # Copy binary to /usr/local/bin
        src = self.gobin / binary
        if src.exists():
            dst = self.bin_dir / binary
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
        print(f"    Installing {pkg} via pip...", end="", flush=True)
        ok, err = self._run([py, "-m", "pip"] + flags + [pkg], timeout=120)
        if not ok:
            print(f"\r    {name} pip failed: {err[:100]}")
            error_logger.error(f"pip install failed for {name}: {err}")
            return False
        if self._is_installed(binary):
            print(f"\r    {name} installed ")
            return True
        # Try to create launcher
        try:
            result = subprocess.run([py, "-c", f"import {binary}; print({binary}.__file__)"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                launcher = self.bin_dir / binary
                launcher.write_text(f"#!/usr/bin/env python3\nimport sys\nimport {binary}\nif hasattr({binary}, 'main'):\n    {binary}.main()\nelse:\n    print('Module {binary} has no main function')\n")
                launcher.chmod(0o755)
                print(f"\r    {name} launcher created ")
                return True
        except Exception as e:
            error_logger.error(f"Failed to create launcher for {name}: {e}")
        print(f"\r    {name} not found after install")
        return False

    def install_apt(self, name: str, cfg: dict) -> bool:
        """Install via apt"""
        ok, _ = self._run(["apt-get", "install", "-y", "-qq", cfg["apt"]], timeout=180)
        return ok and self._is_installed(cfg["binary"])

    def install_git(self, name: str, cfg: dict) -> bool:
        """Install from git repo"""
        path = Path(cfg["path"])
        binary = cfg["binary"]
        
        # Prevent git from prompting for credentials
        env = {
            **os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GOBIN": str(self.gobin),
            "GOPATH": str(self.user_home / "go"),
        }
        
        print(f"    Cloning {name}...", end="", flush=True)
        if path.exists():
            subprocess.run(["git", "-C", str(path), "pull", "--quiet"], 
                        timeout=60, env=env, capture_output=True)
        else:
            result = subprocess.run(["git", "clone", "--depth", "1", cfg["repo"], str(path)], 
                                   timeout=180, env=env, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"\r    {name} clone failed: {result.stderr[:100]}")
                error_logger.error(f"Failed to clone {name}: {result.stderr}")
                return False
        print(f"\r    {name} cloned ")
        
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
            # Use _run method to get proper Go path and environment
            print(f"    Building {name}...", end="", flush=True)
            build_cmd = cfg["build_cmd"].split()
            ok, err = self._run(build_cmd, cwd=path, timeout=120)
            if not ok:
                print(f"\r    {name} build failed: {err[:100]}")
                error_logger.error(f"Build failed for {name}: {err}")
                return False
            print(f"\r    {name} built ")
        
        launcher = self.bin_dir / binary
        launcher_created = False
        
        if "entrypoint" in cfg:
            launcher.write_text(f"#!/bin/bash\nexec {sys.executable} {cfg['entrypoint']} \"\$@\"\n")
            launcher_created = True
        elif (path / binary).exists():
            if launcher.exists():
                launcher.unlink()
            # Copy instead of symlink for reliability
            shutil.copy2(path / binary, launcher)
            launcher_created = True
        else:
            # Search for binary in the repo
            for f in path.rglob(binary):
                if launcher.exists():
                    launcher.unlink()
                shutil.copy2(f, launcher)
                launcher_created = True
                break
        
        if launcher_created:
            launcher.chmod(0o755)
            print(f"    {name} installed ")
        else:
            print(f"    {name}: binary not found in {path}")
            error_logger.error(f"Could not create launcher for {name}, binary not found in {path}")
            return False
            
        return self._is_installed(binary)

    def install_ruby(self, name: str, cfg: dict) -> bool:
        """Install Ruby gem"""
        gem = cfg["package"]
        binary = cfg["binary"]
        print(f"    Installing {gem} via gem...", end="", flush=True)
        ok, err = self._run(["gem", "install", gem], timeout=120)
        if not ok:
            print(f"\r    {name} gem failed: {err[:100]}")
            error_logger.error(f"gem install failed for {name}: {err}")
            return False
        if self._is_installed(binary):
            print(f"\r    {name} installed ")
            return True
        print(f"\r    {name} not found after install")
        return False

    def install_cargo(self, name: str, cfg: dict) -> bool:
        """Install Rust crate via cargo"""
        package = cfg.get("package", name)
        binary = cfg["binary"]
        print(f"    Installing {package} via cargo...", end="", flush=True)
        ok, err = self._run(["cargo", "install", package], timeout=300)
        if not ok:
            print(f"\r    {name} cargo failed: {err[:100]}")
            error_logger.error(f"cargo install failed for {name}: {err}")
            return False
        
        # Check common cargo bin locations
        cargo_bin = Path.home() / ".cargo" / "bin" / binary
        if cargo_bin.exists():
            # Copy to system bin
            dst = self.bin_dir / binary
            if dst.exists():
                dst.unlink()
            shutil.copy2(cargo_bin, dst)
            dst.chmod(0o755)
            print(f"\r    {name} installed ")
            return True
        print(f"\r    {name} not found after install")
        return False

    def install_one(self, name: str, update=False, smart=False) -> str:
        """Install single tool, returns status: 'installed', 'updated', 'skipped', 'failed'"""
        cfg = self.tools[name]
        ttype = cfg["type"]
        binary = cfg["binary"]
        
        is_installed = self._is_installed(binary)
        
        # Smart mode: skip if installed and no update needed
        if smart and is_installed and not update:
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
            "ruby": self.install_ruby,
            "cargo": self.install_cargo,
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
        
        # No sudo required for v2.0 - tools install to user space
        
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
        
        print(f"\n{Colors.CYAN}Next: python3 reconranger.py --check{Colors.RESET}")
