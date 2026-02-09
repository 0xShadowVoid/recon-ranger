#!/usr/bin/env python3
"""ReconRanger v2.0 CLI - Surgical Recon Toolkit"""
import sys
import argparse
from core.installer import ReconRangerInstaller
from core.config import TOOL_DEFINITIONS, CATEGORIES

def main():
    parser = argparse.ArgumentParser(
        description="🦅 ReconRanger v2.0 - Surgical Recon Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python reconranger.py -c core              # Install 13 core tools
  sudo python reconranger.py -c js osint          # Install core + JS + OSINT
  sudo python reconranger.py 2 5 7                 # Install tools by number
  sudo python reconranger.py 1-5 --skip 4         # Install range 1-5 skipping #4
  sudo python reconranger.py -t subfinder amass    # Install specific tools by name
  python reconranger.py --list                    # List all tools with numbers
  python reconranger.py --categories              # Show categories
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
        print(f"\n📖 Full tool list: python reconranger.py --list")
        print("💡 Use: python reconranger.py -c <category>")
        print("⭐ Tip: Use 'core' for the 13 essential tools covering 95% of recon workflows")
        return
    
    if args.list:
        print(f"\n🛠️ Available Tools ({len(TOOL_DEFINITIONS)} total):")
        print(f"{'#':3s} {'Tool':20s} {'Description':40s}")
        print("-" * 70)
        for i, (tool, cfg) in enumerate(sorted(TOOL_DEFINITIONS.items()), 1):
            desc = cfg['description'][:37] + "..." if len(cfg['description']) > 40 else cfg['description']
            print(f"{i:3d} {tool:20s} {desc:40s}")
        print(f"\n📊 Total: {len(TOOL_DEFINITIONS)} tools")
        print("📖 Full documentation: TOOLS.md")
        return
    
    if args.links:
        print("\n🔗 Tool Repository Links:")
        for tool, cfg in sorted(TOOL_DEFINITIONS.items()):
            repo = cfg.get('repo', f'https://github.com/projectdiscovery/{tool}')
            print(f"  • {tool:20s}: {repo}")
        return
    
    if args.check:
        installer = ReconRangerInstaller(TOOL_DEFINITIONS)
        print("\n� Checking Installation Status:")
        print(f"{'Tool':20s} {'Status':10s} {'Path':50s}")
        print("-" * 85)
        
        installed_count = 0
        for tool, cfg in sorted(TOOL_DEFINITIONS.items()):
            binary = cfg.get('binary', tool)
            if installer._is_installed(binary):
                status = "✓ Installed"
                path = installer._find_binary_path(binary)
                installed_count += 1
            else:
                status = "✗ Missing"
                path = "N/A"
            print(f"{tool:20s} {status:10s} {path:50s}")
        
        print(f"\n📊 Summary: {installed_count}/{len(TOOL_DEFINITIONS)} tools installed")
        return
    
    if args.rollback:
        installer = ReconRangerInstaller(TOOL_DEFINITIONS)
        if args.rollback in TOOL_DEFINITIONS:
            installer.rollback_tool(args.rollback)
        else:
            print(f"❌ Unknown tool: {args.rollback}")
        return
    
    # Validate installation arguments
    if not any([args.tools, args.category, args.all, args.numbers]):
        parser.print_help()
        print("\n❌ No installation target specified")
        return
    
    installer = ReconRangerInstaller(TOOL_DEFINITIONS)
    
    # Handle different installation modes
    success = False
    
    if args.category:
        success = installer.install_category(args.category)
    elif args.numbers:
        # Check if it's a range (X-Y) or individual numbers
        if len(args.numbers) == 2 and len(sys.argv) > 2 and '-' in sys.argv[sys.argv.index(args.numbers[0])-1]:
            # Range mode
            start, end = args.numbers
            success = installer.install_range(start, end, args.skip)
        else:
            # Individual numbers mode
            success = installer.install_multiple_tools(args.numbers)
    elif args.tools:
        success = installer._install_tools_list(args.tools)
    elif args.all:
        all_tools = list(TOOL_DEFINITIONS.keys())
        success = installer._install_tools_list(all_tools)
    
    if success:
        print(f"\n{Colors.GREEN}✅ Installation completed successfully!{Colors.RESET}")
        print(f"{Colors.CYAN}Next: Run 'python reconranger.py --check' to verify installation{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}❌ Installation completed with errors{Colors.RESET}")
        print(f"{Colors.YELLOW}Check logs in ~/.reconranger/logs/ for details{Colors.RESET}")

class Colors:
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
    BLUE = '\033[94m'; CYAN = '\033[96m'; RESET = '\033[0m'; BOLD = '\033[1m'

if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    main()