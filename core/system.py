"""System compatibility and dependency management - ReconRanger v3.1"""
import os
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Dict, List

class SystemManager:
    def __init__(self):
        self.distro = self._detect_distro()
    
    def _detect_distro(self) -> Dict[str, str]:
        """Detect Linux distribution with validation"""
        try:
            with open("/etc/os-release") as f:
                lines = [line.strip() for line in f if line.strip()]
            
            info = {}
            for line in lines:
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    info[key] = value.strip('"')
            
            return {
                "id": info.get("ID", "unknown").lower(),
                "version": info.get("VERSION_ID", "unknown"),
                "name": info.get("NAME", "Linux"),
                "like": info.get("ID_LIKE", "").lower()
            }
        except Exception:
            return {"id": "unknown", "version": "unknown", "name": "Linux", "like": ""}
    
    def is_debian_based(self) -> bool:
        distro_id = self.distro["id"]
        distro_like = self.distro["like"]
        valid_ids = {"debian", "ubuntu", "kali", "parrot", "linuxmint", "pop", "mx"}
        return any(x in distro_like for x in ["debian", "ubuntu"]) or distro_id in valid_ids

    def install_system_dependencies(self):
        """Install core dependencies for Python, Go, and Git tools"""
        if not self.is_debian_based():
            print("⚠️ Non-Debian based system detected. Manual dependency installation may be required.")
            return

        deps = [
            "git", "curl", "wget", "unzip", "tar", "build-essential",
            "python3", "python3-pip", "python3-venv", "libpcap-dev"
        ]
        
        print("⚙️ Installing system dependencies...")
        subprocess.run(["sudo", "apt-get", "update", "-qq"], check=False)
        subprocess.run(["sudo", "apt-get", "install", "-y", "-qq"] + deps, check=False)

    def check_go(self) -> bool:
        """Ensure Go is installed and version is >= 1.21"""
        go_path = shutil.which("go")
        if not go_path:
            return self.install_go()
        
        try:
            result = subprocess.run([go_path, "version"], capture_output=True, text=True)
            import re
            match = re.search(r'go(\d+\.\d+)', result.stdout)
            if match:
                version = float(match.group(1))
                if version < 1.21:
                    return self.install_go()
            return True
        except Exception:
            return self.install_go()

    def install_go(self) -> bool:
        """Install Go 1.22.x from official source"""
        print("🚀 Installing/Updating Go to latest stable version...")
        go_version = "1.22.2"
        go_tar = f"go{go_version}.linux-amd64.tar.gz"
        go_url = f"https://golang.org/dl/{go_tar}"
        
        try:
            subprocess.run(["wget", "-q", go_url, "-O", f"/tmp/{go_tar}"], check=True)
            subprocess.run(["sudo", "rm", "-rf", "/usr/local/go"], check=True)
            subprocess.run(["sudo", "tar", "-C", "/usr/local", "-xzf", f"/tmp/{go_tar}"], check=True)
            
            # Setup environment variables
            paths_to_add = [
                'export PATH=$PATH:/usr/local/go/bin',
                'export PATH=$PATH:$(go env GOPATH)/bin'
            ]
            
            home = Path.home()
            for shell_rc in [home / ".bashrc", home / ".zshrc"]:
                if shell_rc.exists():
                    content = shell_rc.read_text()
                    for p in paths_to_add:
                        if p not in content:
                            with open(shell_rc, "a") as f:
                                f.write(f"\n{p}\n")
            
            # Export for current session
            os.environ["PATH"] += ":/usr/local/go/bin"
            return True
        except Exception as e:
            print(f"❌ Failed to install Go: {e}")
            return False

    def ensure_global_path(self, binary_path: Path, binary_name: str):
        """Symlink binary to /usr/local/bin for global access"""
        target = Path("/usr/local/bin") / binary_name
        # If an existing file or symlink (including dangling symlinks) is
        # present at the target, remove it first so `ln -s` won't fail.
        try:
            if target.exists() or target.is_symlink():
                subprocess.run(["sudo", "rm", "-f", str(target)], check=True)
            subprocess.run(["sudo", "ln", "-s", str(binary_path), str(target)], check=True)
            subprocess.run(["sudo", "chmod", "+x", str(target)], check=True)
        except Exception as e:
            print(f"⚠️ Failed to create symlink for {binary_name}: {e}")
