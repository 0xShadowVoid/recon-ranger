"""Modular Tool Installer - ReconRanger v3.0"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from core.system import SystemManager
from core.logger import setup_logging

logger = setup_logging()

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

class ReconRangerInstaller:
    def __init__(self, tools_config: Dict):
        self.tools = tools_config
        self.system = SystemManager()
        self.bin_dir = Path("/usr/local/bin")
        self.opt_dir = Path("/opt")
        self.go_bin = Path.home() / "go" / "bin"

    def _run_cmd(self, cmd: List[str], cwd: Optional[Path] = None, env: Optional[Dict] = None) -> bool:
        try:
            result = subprocess.run(
                cmd, 
                cwd=str(cwd) if cwd else None, 
                env={**os.environ, **(env or {})},
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                logger.error(f"Command failed: {' '.join(cmd)}\nError: {result.stderr}")
                return False
            return True
        except Exception as e:
            logger.error(f"Exception running command {' '.join(cmd)}: {e}")
            return False

    def install_tool(self, name: str, env_vars: Optional[Dict] = None) -> bool:
        if name not in self.tools:
            print(f"{Colors.RED}❌ Tool {name} not found in registry.{Colors.RESET}")
            return False

        cfg = self.tools[name]
        ttype = cfg.get("type")
        print(f"{Colors.BLUE}🔧 Installing {name}...{Colors.RESET}")

        success = False
        if ttype == "go":
            success = self._install_go(name, cfg)
        elif ttype == "python":
            success = self._install_python(name, cfg)
        elif ttype == "git":
            success = self._install_git(name, cfg)
        elif ttype == "apt":
            success = self._install_apt(name, cfg)
        
        if success:
            if "post_install" in cfg:
                print(f"  ⚙️ Running post-install for {name}...")
                self._run_cmd(cfg["post_install"].split(), env=env_vars)
            print(f"{Colors.GREEN}✅ {name} installed successfully.{Colors.RESET}")
            logger.info(f"Successfully installed {name}")
        else:
            print(f"{Colors.RED}❌ Failed to install {name}. Check logs/error.log{Colors.RESET}")
            logger.error(f"Failed to install {name}")
        
        return success

    def _install_go(self, name: str, cfg: Dict) -> bool:
        package = cfg["package"]
        binary = cfg["binary"]
        if self._run_cmd(["go", "install", package]):
            src = self.go_bin / binary
            if src.exists():
                self.system.ensure_global_path(src, binary)
                return True
        return False

    def _install_python(self, name: str, cfg: Dict) -> bool:
        package = cfg["package"]
        binary = cfg["binary"]
        if self._run_cmd([sys.executable, "-m", "pip", "install", "--upgrade", package, "--break-system-packages"]):
            # Pip usually puts binaries in /usr/local/bin or ~/.local/bin
            # We'll try to find it and ensure it's linked
            pip_bin = shutil.which(binary)
            if pip_bin:
                self.system.ensure_global_path(Path(pip_bin), binary)
                return True
        return False

    def _install_git(self, name: str, cfg: Dict) -> bool:
        repo = cfg["repo"]
        path = Path(cfg["path"])
        binary = cfg["binary"]
        
        # Ensure parent directory exists and is writable
        try:
            subprocess.run(["sudo", "mkdir", "-p", str(path.parent)], check=True)
            subprocess.run(["sudo", "chown", os.environ.get("USER", "root"), str(path.parent)], check=True)
        except: pass

        if path.exists():
            shutil.rmtree(path)
        
        if self._run_cmd(["git", "clone", "--depth", "1", repo, str(path)]):
            if "requirements" in cfg:
                req_cmd = [sys.executable, "-m", "pip", "install"] + cfg["requirements"] + ["--break-system-packages"]
                self._run_cmd(req_cmd, cwd=path)
            
            if "build_cmd" in cfg:
                self._run_cmd(cfg["build_cmd"].split(), cwd=path)
            
            if "entrypoint" in cfg:
                entry = Path(cfg["entrypoint"])
                self.system.ensure_global_path(entry, binary)
                return True
            elif (path / binary).exists():
                self.system.ensure_global_path(path / binary, binary)
                return True
        return False

    def _install_apt(self, name: str, cfg: Dict) -> bool:
        pkg = cfg["package"]
        return self._run_cmd(["sudo", "apt-get", "install", "-y", pkg])
