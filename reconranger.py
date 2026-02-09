#!/usr/bin/env python3
"""ReconRanger v2.0 CLI - Surgical Recon Toolkit"""
import sys
import argparse
from core.installer import ReconRangerInstaller
from core.config import TOOL_DEFINITIONS, CATEGORIES
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="🦅 ReconRanger v2.0 - Surgical Recon Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 reconranger.py -c core              # Install 13 core tools
  python3 reconranger.py -c js osint          # Install core + JS + OSINT
  python3 reconranger.py 2 5 7                 # Install tools by number
  python3 reconranger.py 1-5 --skip 4         # Install range 1-5 skipping #4
  python3 reconranger.py -t subfinder amass    # Install specific tools by name
  python3 reconranger.py --list                    # List all tools with numbers
  python3 reconranger.py --categories              # Show categories
        """
    )
    
    # Installation options
    parser.add_argument("-t", "--tools", nargs="+", help="Specific tools to install/update by name")
    parser.add_argument("-c", "--category", help="Install all tools from category")
    parser.add_argument("-u", "--update", action="store_true", help="Update existing tools")
    parser.add_argument("-s", "--smart", action="store_true", help="Smart mode: skip installed, update outdated")
    parser.add_argument("-a", "--all", action="store_true", help="Install/Update ALL tools")
    
    # v2.0 new options
    parser.add_argument("numbers", nargs="*", type=int, help="Tool numbers (space-separated) or range (X-Y)")
    parser.add_argument("--skip", type=int, nargs="+", help="Skip specific tool numbers when using range")
    parser.add_argument("--rollback", help="Rollback specific tool to backup")
    
    # Information options
    parser.add_argument("-l", "--list", action="store_true", help="List available tools with numbers")
    parser.add_argument("--categories", action="store_true", help="List all categories")
    parser.add_argument("--links", action="store_true", help="Show tool repository links")
    parser.add_argument("--check", action="store_true", help="Check installation status")
    
    args = parser.parse_args()
    
    # Handle information commands first
    if args.categories:
        print("\n📂 Available Categories:")
        for cat, tools in CATEGORIES.items():
            if cat == "core":
                print(f"  • {cat:15s} ({len(tools)} tools) ⭐ Surgical Core Set")
            else:
                print(f"  • {cat:15s} ({len(tools)} tools)")
        return
    
    if args.list:
        print(f"\n🛠️ Available Tools ({len(TOOL_DEFINITIONS)} total):")
        for i, (name, cfg) in enumerate(TOOL_DEFINITIONS.items(), 1):
            binary_path = Path("/usr/local/bin") / cfg["binary"]
            status = "✓" if binary_path.exists() else " "
            print(f"  {i:2}. {name:20} {cfg['description'][:40]} {status}")
        return
    
    if args.links:
        print(f"\n🔗 Tool Repository Links:")
        for name, cfg in TOOL_DEFINITIONS.items():
            if cfg.get("repo"):
                print(f"  {name:20} {cfg['repo']}")
        return
    
    if args.check:
        print(f"\n🔍 Installation Status Check:")
        installed = []
        missing = []
        for name, cfg in TOOL_DEFINITIONS.items():
            binary = cfg["binary"]
            binary_path = Path("/usr/local/bin") / binary
            if binary_path.exists():
                installed.append(name)
            else:
                missing.append(name)
        
        print(f"✅ Installed: {len(installed)}/{len(TOOL_DEFINITIONS)} tools")
        if missing:
            print(f"❌ Missing: {', '.join(missing)}")
        else:
            print("🎉 All tools installed!")
        return
    
    if args.rollback:
        installer = ReconRangerInstaller(TOOL_DEFINITIONS)
        success = installer.rollback_tool(args.rollback)
        sys.exit(0 if success else 1)
    
    # Installation commands
    installer = ReconRangerInstaller(TOOL_DEFINITIONS)
    
    if args.category:
        success = installer.install_category(args.category)
        sys.exit(0 if success else 1)
    
    if args.tools:
        success = installer.install_multiple_tools(args.tools)
        sys.exit(0 if success else 1)
    
    if args.numbers:
        # Handle range vs individual numbers
        if len(args.numbers) == 2 and args.skip is None:
            # Likely a range (X-Y)
            start, end = args.numbers
            success = installer.install_range(start, end)
        elif len(args.numbers) == 2 and args.skip is not None:
            # Range with skip
            start, end = args.numbers
            success = installer.install_range(start, end, args.skip)
        else:
            # Individual numbers
            success = installer.install_multiple_tools(args.numbers)
        sys.exit(0 if success else 1)
    
    if args.all:
        success = installer.run(args)
        sys.exit(0 if success else 1)
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    main()
