#!/usr/bin/env python3
"""
🔑 ApiKeyMaster v4.0 - SECURE Unified API Key Manager
✅ 600 permissions enforced on all key storage
✅ Automatic config generation for all 8 providers
✅ Timestamped audit logging
"""

import os
import sys
import json
import getpass
import re
from pathlib import Path
from typing import Dict
import datetime

class Colors:
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
    BLUE = '\033[94m'; CYAN = '\033[96m'; RESET = '\033[0m'; BOLD = '\033[1m'

class ApiKeyMaster:
    def __init__(self):
        self.config_dir = Path.home() / ".reconranger"
        self.config_file = self.config_dir / "api_keys.json"
        self.audit_log = self.config_dir / "audit.log"
        self.config_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.keys: Dict[str, str] = self._load_keys()
        
        self.providers = {
            "virustotal": {
                "env": "VT_API_KEY",
                "tool": "subfinder",
                "yaml_section": "virustotal",
                "description": "VirusTotal API (subdomain discovery)",
                "url": "https://www.virustotal.com/gui/user/PROFILE/apikey"
            },
            "securitytrails": {
                "env": "SECURITYTRAILS_API_KEY",
                "tool": "subfinder", 
                "yaml_section": "securitytrails",
                "description": "SecurityTrails API (historical DNS data)",
                "url": "https://securitytrails.com/app/account/api"
            },
            "binaryedge": {
                "env": "BINARYEDGE_API_KEY",
                "tool": "subfinder",
                "yaml_section": "binaryedge",
                "description": "BinaryEdge API (exposure data)",
                "url": "https://www.binaryedge.io/"
            },
            "shodan": {
                "env": "SHODAN_API_KEY",
                "tool": "shodan",
                "file_path": "~/.shodan/api_key",
                "description": "Shodan API (internet-wide scanning)",
                "url": "https://account.shodan.io/"
            },
            "github": {
                "env": "GITHUB_TOKEN",
                "tool": "githound",
                "yaml_path": "~/.githound/config.yaml",
                "description": "GitHub Personal Access Token (secrets hunting)",
                "url": "https://github.com/settings/tokens (repo scope required)"
            },
            "censys_id": {
                "env": "CENSYS_API_ID",
                "tool": "censys",
                "yaml_path": "~/.config/censys/censys.yml",
                "yaml_key": "api_id",
                "description": "Censys API ID",
                "url": "https://search.censys.io/account/api"
            },
            "censys_secret": {
                "env": "CENSYS_API_SECRET",
                "tool": "censys",
                "yaml_path": "~/.config/censys/censys.yml",
                "yaml_key": "api_secret",
                "description": "Censys API Secret",
                "url": "https://search.censys.io/account/api"
            },
            "whoxy": {
                "env": "WHOXY_API_KEY",
                "tool": "metabigor",
                "yaml_path": "~/.config/metabigor/config.yaml",
                "yaml_key": "whoxy",
                "description": "Whoxy API (reverse WHOIS)",
                "url": "https://whoxy.com/"
            }
        }
    
    def _load_keys(self) -> Dict:
        if self.config_file.exists():
            self.config_file.chmod(0o600)
            try:
                return json.loads(self.config_file.read_text())
            except Exception as e:
                print(f"{Colors.YELLOW}⚠ Error loading keys: {e}{Colors.RESET}")
                return {}
        return {}
    
    def _save_keys(self):
        self.config_file.write_text(json.dumps(self.keys, indent=2))
        self.config_file.chmod(0o600)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.audit_log.write_text(f"[{timestamp}] Keys saved to {self.config_file}\n", mode="a")
        print(f"\n{Colors.GREEN}✓{Colors.RESET} Keys saved securely to {self.config_file}")
        print(f"  {Colors.BLUE}Permissions: 600 (user-only){Colors.RESET}")
    
    def configure(self):
        print("\n" + f"{Colors.BLUE}{'🔐 API KEY CONFIGURATION WIZARD':^78}{Colors.RESET}")
        print("=" * 78)
        print("\n💡 Tips:")
        print("   • Get free API keys from URLs shown for each provider")
        print("   • Most providers offer free tiers sufficient for recon")
        print("   • Keys stored securely at ~/.reconranger/api_keys.json (600 perms)")
        print("   • Never commit API keys to version control!\n")
        
        updated = []
        for name, cfg in self.providers.items():
            current = self.keys.get(name, "NOT SET")
            mask = current[:4] + "*" * max(0, len(current) - 8) if current != "NOT SET" and len(current) > 8 else current
            
            print(f"\n{'─' * 78}")
            print(f"[{name.upper()}] - {cfg['description']}")
            print(f"  🔗 Get key: {cfg['url']}")
            print(f"  💾 Current: {mask}")
            
            if input("  Update key? (y/n): ").strip().lower() == 'y':
                key = getpass.getpass(f"  Enter {name} API key: ").strip()
                if key and not key.startswith(("your_", "ENTER_", "test_")):
                    self.keys[name] = key
                    updated.append(name)
                    print(f"  {Colors.GREEN}✓{Colors.RESET} Key accepted")
                else:
                    print(f"  {Colors.YELLOW}⚠{Colors.RESET} Skipped (empty or placeholder key)")
        
        if updated:
            self._save_keys()
            print("\n" + "=" * 78)
            print(f"{Colors.GREEN}✅{Colors.RESET} {len(updated)} key(s) updated successfully")
            print(f"\n💡 Next: Run '{Colors.YELLOW}python3 ApiKeyMaster.py --apply{Colors.RESET}' to configure tools")
        else:
            print("\n" + "=" * 78)
            print(f"{Colors.YELLOW}ℹ️{Colors.RESET} No keys updated")
    
    def apply_configs(self):
        """Apply keys to actual tool configuration files"""
        print("\n" + f"{Colors.BLUE}{'⚙️  APPLYING KEYS TO TOOL CONFIGURATIONS':^78}{Colors.RESET}")
        print("=" * 78 + "\n")
        
        applied = []
        
        # Subfinder config (handles multiple providers)
        subfinder_cfg = Path.home() / ".config" / "subfinder" / "config.yaml"
        subfinder_cfg.parent.mkdir(parents=True, exist_ok=True)
        
        if subfinder_cfg.exists():
            content = subfinder_cfg.read_text()
        else:
            content = "subfinder:\n  verbose: false\n  timeout: 30\n  max-dns-queries: 500\n"
        
        if "subfinder:" not in content:
            content = "subfinder:\n  verbose: false\n" + content
        
        for name in ["virustotal", "securitytrails", "binaryedge"]:
            if name in self.keys:
                key = self.keys[name]
                section = f"{name}:\n    - \"{key}\""
                pattern = f"{name}:\\n(?:\\s+-\\s+\"[^\"]*\"\\n?)+"
                content = re.sub(pattern, section, content, flags=re.MULTILINE)
                if f"\n{name}:" not in content and f" {name}:" not in content:
                    content = content.rstrip() + f"\n\n{section}\n"
                applied.append(f"subfinder ({name})")
        
        subfinder_cfg.write_text(content)
        subfinder_cfg.chmod(0o600)
        print(f"  {Colors.GREEN}✓{Colors.RESET} subfinder config updated: {subfinder_cfg}")
        
        # Shodan key
        if "shodan" in self.keys:
            shodan_cfg = Path.home() / ".shodan" / "api_key"
            shodan_cfg.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            shodan_cfg.write_text(self.keys["shodan"])
            shodan_cfg.chmod(0o600)
            applied.append("shodan")
            print(f"  {Colors.GREEN}✓{Colors.RESET} shodan key saved: {shodan_cfg}")
        
        # GitHub token for githound
        if "github" in self.keys:
            gh_cfg = Path.home() / ".githound" / "config.yaml"
            gh_cfg.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            gh_cfg.write_text(f"token: \"{self.keys['github']}\"\n")
            gh_cfg.chmod(0o600)
            applied.append("githound")
            print(f"  {Colors.GREEN}✓{Colors.RESET} githound config updated: {gh_cfg}")
        
        # Censys config
        if "censys_id" in self.keys or "censys_secret" in self.keys:
            censys_cfg = Path.home() / ".config" / "censys" / "censys.yml"
            censys_cfg.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            
            cfg = {}
            if censys_cfg.exists():
                try:
                    import yaml
                    cfg = yaml.safe_load(censys_cfg.read_text()) or {}
                except:
                    pass
            
            if "censys_id" in self.keys:
                cfg["api_id"] = self.keys["censys_id"]
            if "censys_secret" in self.keys:
                cfg["api_secret"] = self.keys["censys_secret"]
            
            try:
                import yaml
                censys_cfg.write_text(yaml.dump(cfg, default_flow_style=False))
                censys_cfg.chmod(0o600)
                applied.append("censys")
                print(f"  {Colors.GREEN}✓{Colors.RESET} censys config updated: {censys_cfg}")
            except ImportError:
                print(f"  {Colors.YELLOW}⚠{Colors.RESET} PyYAML not installed - manual config required")
        
        # Whoxy for metabigor
        if "whoxy" in self.keys:
            meta_cfg = Path.home() / ".config" / "metabigor" / "config.yaml"
            meta_cfg.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            meta_cfg.write_text(f"whoxy: \"{self.keys['whoxy']}\"\n")
            meta_cfg.chmod(0o600)
            applied.append("metabigor")
            print(f"  {Colors.GREEN}✓{Colors.RESET} metabigor config updated: {meta_cfg}")
        
        print("\n" + "=" * 78)
        if applied:
            print(f"{Colors.GREEN}✅{Colors.RESET} Successfully applied keys to {len(applied)} tool(s):")
            print(f"   {', '.join(applied)}")
            print(f"\n💡 Test: {Colors.YELLOW}subfinder -d example.com -sources virustotal,securitytrails{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}ℹ️{Colors.RESET} No keys to apply (configure keys first with --configure)")
    
    def list_keys(self):
        print("\n" + f"{Colors.BLUE}{'🔐 CONFIGURED API KEYS (MASKED)':^78}{Colors.RESET}")
        print("=" * 78 + "\n")
        
        if not self.keys:
            print("No API keys configured")
            print(f"\n💡 Run '{Colors.YELLOW}python3 ApiKeyMaster.py --configure{Colors.RESET}' to add keys")
            return
        
        print(f"{'Provider':<20} {'Tool':<15} {'Description':<35} {'Key (masked)'}")
        print("-" * 78)
        for name, key in sorted(self.keys.items()):
            mask = key[:4] + "*" * max(0, len(key) - 8) if len(key) > 8 else "*" * len(key)
            provider = self.providers.get(name, {})
            tool = provider.get("tool", "unknown")
            desc = provider.get("description", "")[:35]
            print(f"{name:<20} {tool:<15} {desc:<35} {mask}")
        
        print(f"\n{Colors.BLUE}Secure storage:{Colors.RESET} {self.config_file} {Colors.BLUE}(permissions: 600){Colors.RESET}")
        print(f"{Colors.RED}⚠️  SECURITY:{Colors.RESET} Never share this file or commit to git!")

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🔑 ApiKeyMaster - Secure API Key Manager for Recon Tools",
        epilog="""
Security Best Practices:
  • API keys stored with 600 permissions (user-only read/write)
  • Keys never logged in plaintext (masked in all output)
  • Configuration files also secured with 600 permissions
  • Always use read-only API keys where possible
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--configure", action="store_true", help="Interactive configuration wizard")
    parser.add_argument("--apply", action="store_true", help="Apply keys to tool configurations")
    parser.add_argument("--list", action="store_true", help="List masked keys")
    
    args = parser.parse_args()
    
    master = ApiKeyMaster()
    
    if args.configure:
        master.configure()
    elif args.apply:
        master.apply_configs()
    elif args.list:
        master.list_keys()
    else:
        parser.print_help()
        print("\n💡 Quick start:")
        print("   python3 ApiKeyMaster.py --configure   # Add API keys")
        print("   python3 ApiKeyMaster.py --apply       # Configure tools")

if __name__ == "__main__":
    main()