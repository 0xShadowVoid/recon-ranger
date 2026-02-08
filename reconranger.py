#!/usr/bin/env python3
"""ReconRanger CLI - Entry point only"""
import sys
import argparse
from core.installer import ReconRangerInstaller
from core.config import TOOL_DEFINITIONS

def main():
    parser = argparse.ArgumentParser(description="🦅 Universal Recon Toolkit Installer")
    parser.add_argument("-t", "--tools", nargs="+", help="Specific tools to install/update")
    parser.add_argument("-u", "--update", action="store_true", help="Update existing tools")
    parser.add_argument("-s", "--smart", action="store_true", help="Smart mode: skip installed, update outdated")
    parser.add_argument("-a", "--all", action="store_true", help="Install/Update ALL tools")
    parser.add_argument("-l", "--list", action="store_true", help="List available tools")
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable tools:")
        for tool, cfg in sorted(TOOL_DEFINITIONS.items()):
            print(f"  • {tool:22s} - {cfg['description']}")
        return
    
    if args.update and not (args.tools or args.all):
        print("✗ --update requires -t or --all")
        sys.exit(1)
    
    installer = ReconRangerInstaller(TOOL_DEFINITIONS)
    installer.run(args)

if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    main()