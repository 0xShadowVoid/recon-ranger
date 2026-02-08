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
            env = {**os.environ, "GOBIN": str(self.gobin), "GOPATH": str(Path.home() / "go")}
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd, env=env)
            return (r.returncode == 0, r.stderr if r.returncode else r.stdout)
        except Exception as e:
            return (False, str(e))

    def _is_installed(self, binary: str) -> bool:
        return shutil.which(binary) is not None

    def install_go(self, name: str, cfg: dict) -> bool:
        """Install Go tool via apt or go install"""
        binary = cfg["binary"]
        if cfg.get("apt"):
            ok, _ = self._run(["apt-get", "install", "-y", "-qq", cfg["apt"]], timeout=180)
            if ok and self._is_installed(binary):
                return True
        ok, err = self._run(["go", "install", "-v", f"{cfg['package']}@latest"], timeout=180)
        if ok:
            src = self.gobin / binary
            if src.exists():
                dst = self.bin_dir / binary
                if dst.exists():
                    dst.unlink()
                dst.symlink_to(src)
                return self._is_installed(binary)
        return False

    def install_python(self, name: str, cfg: dict) -> bool:
        """Install Python tool via pip"""
        py = sys.executable
        pkg = cfg["package"]
        flags = ["install", "-q", "--no-cache-dir"]
        if sys.version_info >= (3, 11):
            flags.insert(1, "--break-system-packages")
        ok, _ = self._run([py, "-m", "pip"] + flags + [pkg], timeout=120)
        return ok

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
            self._run(cfg["build_cmd"].split(), cwd=path, timeout=120)
        launcher = self.bin_dir / binary
        if "entrypoint" in cfg:
            launcher.write_text(f"#!/bin/bash\nexec {sys.executable} {cfg['entrypoint']} \"\$@\"\n")
        elif (path / binary).exists():
            if launcher.exists():
                launcher.unlink()
            launcher.symlink_to(path / binary)
        else:
            for f in path.rglob(binary):
                if launcher.exists():
                    launcher.unlink()
                launcher.symlink_to(f)
                break
        launcher.chmod(0o755)
        return self._is_installed(binary)

    def install_one(self, name: str, update=False) -> bool:
        """Install single tool"""
        cfg = self.tools[name]
        ttype = cfg["type"]
        if not update and self._is_installed(cfg["binary"]):
            return True
        methods = {
            "go": self.install_go,
            "python": self.install_python,
            "apt": self.install_apt,
            "git": self.install_git,
        }
        result = methods.get(ttype, lambda n, c: False)(name, cfg)
        if result and "post_install" in cfg:
            self._run(cfg["post_install"].split(), timeout=120)
        self.results[name] = result
        return result

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
        
        with tqdm(total=len(targets), desc="Progress") as pbar:
            for name in targets:
                ok = self.install_one(name, args.update)
                icon = "✓" if ok else "✗"
                color = Colors.GREEN if ok else Colors.RED
                print(f"{color}{icon}{Colors.RESET} {name:18}")
                pbar.update(1)
        
        ok = [n for n, r in self.results.items() if r]
        fail = [n for n, r in self.results.items() if not r]
        
        print(f"\n{Colors.GREEN}{len(ok)}/{len(targets)} installed{Colors.RESET}")
        if fail:
            print(f"{Colors.RED}Failed: {', '.join(fail)}{Colors.RESET}")
        print(f"\n{Colors.CYAN}Next: python3 ApiKeyMaster.py --configure{Colors.RESET}")