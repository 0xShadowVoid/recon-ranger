#!/usr/bin/env python3
"""
🦅 ReconRanger v3.0 - Surgical Recon Toolkit & Tool Manager
Developed by 0xShadowVoid
"""

import sys
import json
import argparse
from pathlib import Path
from core.installer import ReconRangerInstaller
from core.system import SystemManager
from core.keys import KeyManager
from core.logger import setup_logging

# Load tool registry
TOOLS_FILE = Path(__file__).parent / "tools.json"
def load_tools():
    if not TOOLS_FILE.exists():
        return {}
    return json.loads(TOOLS_FILE.read_text())

def save_tools(tools):
    TOOLS_FILE.write_text(json.dumps(tools, indent=2))

def main():
    tools = load_tools()
    installer = ReconRangerInstaller(tools)
    system = SystemManager()
    key_manager = KeyManager()
    logger = setup_logging()

    parser = argparse.ArgumentParser(
        description="🦅 ReconRanger v3.0 - Surgical Recon Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reconranger --install-all              # Install all tools in registry
  reconranger -t subfinder amass         # Install specific tools
  reconranger --api                      # Manage API keys
  reconranger --add-tool                 # Add a new tool to registry
  reconranger --list                     # List all available tools
        """
    )

    # Tool Installation
    group_inst = parser.add_argument_group("Installation Options")
    group_inst.add_argument("-t", "--tools", nargs="+", help="Specific tools to install by name")
    group_inst.add_argument("-c", "--category", help="Install all tools from a category")
    group_inst.add_argument("--install-all", action="store_true", help="Install ALL tools in registry")
    group_inst.add_argument("--check", action="store_true", help="Check installation status of tools")

    # API Key Management
    group_api = parser.add_argument_group("API Key Management")
    group_api.add_argument("--api", action="store_true", help="Launch API key configuration wizard")
    group_api.add_argument("--apply-keys", action="store_true", help="Apply keys to tool config files and environment")

    # Tool Registry Management
    group_reg = parser.add_argument_group("Registry Management")
    group_reg.add_argument("--add-tool", action="store_true", help="Add a new tool to the registry")
    group_reg.add_argument("--edit-tool", help="Edit an existing tool in the registry")
    group_reg.add_argument("--delete-tool", help="Delete a tool from the registry")
    group_reg.add_argument("-l", "--list", action="store_true", help="List all tools in registry")

    # System
    group_sys = parser.add_argument_group("System")
    group_sys.add_argument("--fix-deps", action="store_true", help="Auto-fix system dependencies")

    args = parser.parse_args()

    # 1. System Fix
    if args.fix_deps:
        system.install_system_dependencies()
        system.check_go()
        return

    # 2. API Management
    if args.api:
        key_manager.wizard()
        return
    
    if args.apply_keys:
        key_manager.apply_to_env()
        return

    # 3. Registry Management
    if args.add_tool:
        name = input("Tool Name: ").strip().lower()
        ttype = input("Type (go/python/git/apt): ").strip().lower()
        package = input("Package/Repo URL: ").strip()
        binary = input("Binary Name: ").strip()
        desc = input("Description: ").strip()
        cat = input("Category: ").strip()
        tools[name] = {
            "type": ttype,
            "package": package,
            "binary": binary,
            "description": desc,
            "category": cat
        }
        save_tools(tools)
        print(f"✅ Added {name} to registry.")
        return

    if args.delete_tool:
        if args.delete_tool in tools:
            del tools[args.delete_tool]
            save_tools(tools)
            print(f"✅ Deleted {args.delete_tool}.")
        else:
            print("❌ Tool not found.")
        return

    if args.list:
        print(f"\n🛠️  ReconRanger Registry ({len(tools)} tools):")
        print(f"{'#':<3} {'Name':<18} {'Category':<12} {'Description'}")
        print("-" * 75)
        for i, (name, cfg) in enumerate(tools.items(), 1):
            print(f"{i:<3} {name:<18} {cfg['category']:<12} {cfg['description'][:40]}")
        return

    # 4. Installation Logic
    targets = []
    if args.install_all:
        targets = list(tools.keys())
    elif args.category:
        targets = [n for n, c in tools.items() if c['category'] == args.category]
    elif args.tools:
        targets = args.tools

    if targets:
        # Ensure dependencies first
        system.install_system_dependencies()
        system.check_go()
        
        env = key_manager.get_env_vars()
        for t in targets:
            installer.install_tool(t, env_vars=env)
        return

    if args.check:
        print(f"\n🔍 Installation Status:")
        print(f"{'Tool':<18} {'Status':<12} {'Path'}")
        print("-" * 50)
        for name, cfg in tools.items():
            import shutil
            path = shutil.which(cfg['binary'])
            status = "✅ Installed" if path else "❌ Missing"
            print(f"{name:<18} {status:<12} {path or 'N/A'}")
        return

    parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        sys.exit(0)
