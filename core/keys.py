"""API Key Management - ReconRanger v3.0"""
import os
import json
import getpass
from pathlib import Path
from typing import Dict

class KeyManager:
    def __init__(self):
        self.config_dir = Path.home() / ".reconranger"
        self.config_file = self.config_dir / "keys.json"
        self.config_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.keys = self._load_keys()
        
        self.providers = {
            "chaos": {"env": "CHAOS_KEY", "url": "https://chaos.projectdiscovery.io/"},
            "github": {"env": "GITHUB_TOKEN", "url": "https://github.com/settings/tokens"},
            "securitytrails": {"env": "SECURITYTRAILS_KEY", "url": "https://securitytrails.com/"},
            "netlas": {"env": "NETLAS_API_KEY", "url": "https://docs.netlas.io/"},
            "zoomeye": {"env": "ZOOMEYE_API_KEY", "url": "https://www.zoomeye.ai/"},
            "shrewdeye": {"env": "SHREWDEYE_API_KEY", "url": "https://shrewdeye.app/"},
            "virustotal": {"env": "VT_API_KEY", "url": "https://www.virustotal.com/"},
            "shodan": {"env": "SHODAN_API_KEY", "url": "https://account.shodan.io/"}
        }

    def _load_keys(self) -> Dict:
        if self.config_file.exists():
            try:
                return json.loads(self.config_file.read_text())
            except:
                return {}
        return {}

    def save_keys(self):
        self.config_file.write_text(json.dumps(self.keys, indent=2))
        self.config_file.chmod(0o600)

    def wizard(self):
        print("\n🔐 API Key Configuration Wizard")
        print("Leave blank to keep current value.\n")
        for name, info in self.providers.items():
            current = self.keys.get(name, "Not Set")
            mask = current[:4] + "*" * (len(current)-4) if current != "Not Set" else current
            print(f"[{name.upper()}] Current: {mask}")
            print(f"🔗 Get key: {info['url']}")
            val = getpass.getpass(f"Enter {name} key: ").strip()
            if val:
                self.keys[name] = val
        self.save_keys()
        print("\n✅ Keys saved successfully.")

    def apply_to_env(self):
        """Export keys to shell profile for persistent use"""
        home = Path.home()
        for rc in [home / ".bashrc", home / ".zshrc"]:
            if rc.exists():
                content = rc.read_text()
                new_lines = []
                for name, info in self.providers.items():
                    if name in self.keys:
                        export_line = f'export {info["env"]}="{self.keys[name]}"'
                        # Remove existing export if present
                        content = "\n".join([line for line in content.splitlines() if not line.startswith(f'export {info["env"]}=')])
                        new_lines.append(export_line)
                
                if new_lines:
                    with open(rc, "w") as f:
                        f.write(content.strip() + "\n\n# ReconRanger API Keys\n" + "\n".join(new_lines) + "\n")
        
        print("🚀 API keys applied to shell profiles. Please restart your terminal or run 'source ~/.bashrc'.")

    def get_env_vars(self) -> Dict[str, str]:
        """Return dict of environment variables for current process use"""
        env = {}
        for name, info in self.providers.items():
            if name in self.keys:
                env[info["env"]] = self.keys[name]
        return env
