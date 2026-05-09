"""Modular Tool Installer — ReconRanger v4.0"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
try:
    from system import SystemManager
    from logger import setup_logging
except ImportError:
    from core.system import SystemManager
    from core.logger import setup_logging

logger = setup_logging()


class Colors:
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BLUE   = "\033[94m"
    RESET  = "\033[0m"


class ReconRangerInstaller:
    def __init__(self, tools_config: Dict):
        self.tools   = tools_config
        self.system  = SystemManager()
        self.bin_dir = Path("/usr/local/bin")
        self.opt_dir = Path("/opt")
        self.go_bin  = self._detect_go_bin()

    # ── helpers ───────────────────────────────────────────────────────────────

    def _detect_go_bin(self) -> Path:
        try:
            res = subprocess.run(["go", "env", "GOPATH"], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                return Path(res.stdout.strip()) / "bin"
        except Exception:
            pass
        return Path.home() / "go" / "bin"

    def _run_cmd(self, cmd: List[str], cwd: Optional[Path] = None,
                 env: Optional[Dict] = None) -> bool:
        try:
            result = subprocess.run(
                cmd,
                cwd=str(cwd) if cwd else None,
                env={**os.environ, **(env or {})},
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logger.error(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
                return False
            return True
        except Exception as e:
            logger.error(f"Exception running {' '.join(cmd)}: {e}")
            return False

    # ── public ────────────────────────────────────────────────────────────────

    def install_tool(self, name: str, env_vars: Optional[Dict] = None) -> bool:
        if name not in self.tools:
            print(f"{Colors.RED}[✗] {name} not found in registry.{Colors.RESET}")
            return False

        cfg   = self.tools[name]
        ttype = cfg.get("type")
        print(f"{Colors.BLUE}[→] Installing {name} ({ttype})…{Colors.RESET}")

        dispatch = {
            "go":     self._install_go,
            "python": self._install_python,
            "git":    self._install_git,
            "apt":    self._install_apt,
            "ruby":   self._install_ruby,
            "cargo":  self._install_cargo,
        }

        handler = dispatch.get(ttype)
        if not handler:
            print(f"{Colors.RED}[✗] Unknown install type '{ttype}' for {name}.{Colors.RESET}")
            return False

        success = handler(name, cfg)

        if success:
            post = cfg.get("post_install")
            if post:
                print(f"  [⚙] Running post-install for {name}…")
                self._run_cmd(post.split(), env=env_vars)
            print(f"{Colors.GREEN}[✓] {name} installed.{Colors.RESET}")
            logger.info(f"Installed {name}")
        else:
            print(f"{Colors.RED}[✗] Failed to install {name}. See logs/error.log{Colors.RESET}")
            logger.error(f"Failed to install {name}")

        return success

    # ── installers ────────────────────────────────────────────────────────────

    def _install_go(self, name: str, cfg: Dict) -> bool:
        package = cfg["package"]
        if "@" not in package:
            package = f"{package}@latest"
        binary = cfg["binary"]
        if not self._run_cmd(["go", "install", package]):
            return False
        src = self.go_bin / binary
        if src.exists():
            self.system.ensure_global_path(src, binary)
            return True
        # binary not found — still consider success (some tools use different names)
        logger.warning(f"go install succeeded but binary '{binary}' not found in {self.go_bin}")
        return True

    def _install_python(self, name: str, cfg: Dict) -> bool:
        package = cfg["package"]
        binary  = cfg["binary"]
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade",
               package, "--break-system-packages"]
        if not self._run_cmd(cmd):
            return False
        pip_bin = shutil.which(binary)
        if pip_bin:
            self.system.ensure_global_path(Path(pip_bin), binary)
        return True

    def _install_git(self, name: str, cfg: Dict) -> bool:
        repo   = cfg["repo"]
        path   = Path(cfg["path"])
        binary = cfg["binary"]

        # Ensure parent dir exists
        try:
            subprocess.run(["mkdir", "-p", str(path.parent)], check=True)
        except Exception:
            pass

        # Wipe and re-clone for idempotency
        if path.exists():
            shutil.rmtree(path)

        if not self._run_cmd(["git", "clone", "--depth", "1", repo, str(path)]):
            return False

        # Python requirements
        if "requirements" in cfg:
            req_cmd = ([sys.executable, "-m", "pip", "install"]
                       + cfg["requirements"]
                       + ["--break-system-packages"])
            self._run_cmd(req_cmd, cwd=path)

        # Build step (go/make/cargo inside a git repo)
        if "build_cmd" in cfg:
            self._run_cmd(cfg["build_cmd"].split(), cwd=path)

        # post_clone shell command (e.g. ./install.sh)
        if "post_clone" in cfg:
            self._run_cmd(cfg["post_clone"].split(), cwd=path)

        # Wire up the binary
        if "entrypoint" in cfg:
            entry = Path(cfg["entrypoint"])
            self.system.ensure_global_path(entry, binary)
            return True

        # Look for binary in the cloned directory
        for candidate in [path / binary, path / "dist" / binary, path / "bin" / binary]:
            if candidate.exists():
                self.system.ensure_global_path(candidate, binary)
                return True

        # Last resort: maybe it landed on PATH after build
        if shutil.which(binary):
            return True

        logger.warning(f"git install for {name}: binary '{binary}' not located after clone/build")
        return False

    def _install_apt(self, name: str, cfg: Dict) -> bool:
        pkg = cfg.get("apt") or cfg.get("package")
        return self._run_cmd(["apt-get", "install", "-y", "-q", pkg])

    def _install_ruby(self, name: str, cfg: Dict) -> bool:
        """Install a RubyGem. Ensures ruby and gem are present first."""
        gem = shutil.which("gem")
        if not gem:
            print(f"  [!] gem not found — installing ruby-full…")
            if not self._run_cmd(["apt-get", "install", "-y", "-q", "ruby-full"]):
                return False
            gem = shutil.which("gem")
            if not gem:
                logger.error("gem still not available after apt install ruby-full")
                return False

        package = cfg["package"]
        binary  = cfg["binary"]

        if not self._run_cmd([gem, "install", package, "--no-document"]):
            return False

        gem_bin = shutil.which(binary)
        if gem_bin:
            self.system.ensure_global_path(Path(gem_bin), binary)
        return True

    def _install_cargo(self, name: str, cfg: Dict) -> bool:
        """Install via cargo install <package> or build from a cloned git repo."""
        cargo = shutil.which("cargo")
        if not cargo:
            print(f"  [!] cargo not found — installing rustup…")
            # Install via rustup non-interactively
            rustup_init = "/tmp/rustup-init.sh"
            if self._run_cmd(["curl", "-sSf", "https://sh.rustup.rs", "-o", rustup_init]):
                self._run_cmd(["sh", rustup_init, "-y", "--no-modify-path"])
                # Add cargo to PATH for this session
                cargo_home = Path.home() / ".cargo" / "bin"
                os.environ["PATH"] = str(cargo_home) + ":" + os.environ.get("PATH", "")
                cargo = shutil.which("cargo")
            if not cargo:
                logger.error("cargo still not available after rustup install")
                return False

        binary = cfg["binary"]

        # Repo-based build (cargo build --release inside a cloned dir)
        if "repo" in cfg:
            path = Path(cfg["path"])
            if path.exists():
                shutil.rmtree(path)
            if not self._run_cmd(["git", "clone", "--depth", "1", cfg["repo"], str(path)]):
                return False
            build_cmd = cfg.get("build_cmd", "cargo build --release").split()
            if not self._run_cmd(build_cmd, cwd=path):
                return False
            for candidate in [path / "target" / "release" / binary, path / binary]:
                if candidate.exists():
                    self.system.ensure_global_path(candidate, binary)
                    return True
            return False

        # Package install (cargo install <package>)
        package = cfg["package"]
        if not self._run_cmd([cargo, "install", package]):
            return False
        cargo_bin = Path.home() / ".cargo" / "bin" / binary
        if cargo_bin.exists():
            self.system.ensure_global_path(cargo_bin, binary)
        return True