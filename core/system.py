"""System compatibility checks with input validation"""
import os
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Dict, List

class SystemChecker:
    def __init__(self):
        self.distro = self._detect_distro()
    
    def _detect_distro(self) -> Dict[str, str]:
        """Detect Linux distribution with validation"""
        try:
            with open("/etc/os-release") as f:
                lines = [line.strip() for line in f if line.strip()]
            
            # Validate file format
            if not any(line.startswith("ID=") for line in lines):
                raise RuntimeError("Invalid /etc/os-release format")
            
            info = {}
            for line in lines:
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    info[key] = value.strip('"')
            
            return {
                "id": info.get("ID", "unknown").lower(),
                "version": info.get("VERSION_ID", "unknown"),
                "name": info.get("NAME", "Linux"),
                "like": info.get("ID_LIKE", "")
            }
        except Exception as e:
            raise RuntimeError(f"Failed to detect OS: {e}")
    
    def is_debian_based(self) -> bool:
        """Check if system is Debian-based with validation"""
        distro_id = self.distro["id"]
        distro_like = self.distro["like"].lower()
        valid_ids = {"debian", "ubuntu", "kali", "parrot", "linuxmint", "pop", "mx"}
        return any(x in distro_like for x in ["debian", "ubuntu"]) or distro_id in valid_ids
    
    def check_python_version(self) -> None:
        """Validate Python version"""
        py_ver = platform.python_version()
        py_tuple = tuple(map(int, py_ver.split('.')[:2]))
        if py_tuple < (3, 8):
            raise RuntimeError(f"Python 3.8+ required (found {py_ver})")
    
    def check_go_version(self) -> str:
        """Validate Go version with proper error handling"""
        try:
            result = subprocess.run(["go", "version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError("Go command failed")
            
            import re
            match = re.search(r'go(\d+\.\d+\.?\d*)', result.stdout)
            if not match:
                raise RuntimeError("Invalid Go version format")
            
            version = match.group(1)
            major, minor = map(int, version.split('.')[:2])
            if major < 1 or (major == 1 and minor < 19):
                raise RuntimeError(f"Go 1.19+ required (found {version})")
            
            return version
        except FileNotFoundError:
            raise RuntimeError("Go is not installed or not in PATH. Please install Go 1.19+ from https://golang.org/dl/")
        except Exception as e:
            raise RuntimeError(f"Go version check failed: {e}")
    
    def check_disk_space(self, min_gb: float = 3.0) -> None:
        """Validate disk space availability"""
        free_gb = shutil.disk_usage("/").free / (2**30)
        if free_gb < min_gb:
            raise RuntimeError(f"Insufficient disk space: {free_gb:.1f}GB free (need {min_gb}GB+)")
    
    def check_internet(self) -> None:
        """Validate internet connectivity"""
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
        except OSError as e:
            raise RuntimeError(f"No internet connection: {e}")