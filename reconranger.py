#!/usr/bin/env python3
"""ReconRanger CLI - Entry point only"""
import sys
import argparse
from core.installer import ReconRangerInstaller
from core.config import TOOL_DEFINITIONS

# Tool categories
CATEGORIES = {
    "recon": ["amass", "subfinder", "assetfinder", "sublist3r", "subdomainizer", "github-subdomains", "bbot"],
    "dns": ["dnsx", "shuffledns", "masscan", "naabu"],
    "http": ["httpx", "wafw00f", "graphw00f"],
    "crawl": ["katana", "gospider", "linkfinder", "jsfinder", "jsluice", "jsleak"],
    "fuzz": ["ffuf", "dirsearch", "kiterunner", "cewl"],
    "param": ["arjun", "paramspider"],
    "xss": ["xsstrike", "dalfox", "xspear"],
    "vuln": ["nuclei", "nikto"],
    "exploit": ["metasploit-framework"],
    "sql": ["sqlmap", "ghauri", "nosqlmap"],
    "graphql": ["graphqlmap", "graphw00f"],
    "traversal": ["dotdotpwn"],
    "cloud": ["s3scanner", "cloud_enum"],
    "cms": ["wpscan", "droopescan"],
    "takeover": ["subjack", "subzy", "subover"],
    "osint": ["github-dorks", "githound", "jsecret", "virustotalx", "metabigor"],
    "utils": ["waybackurls", "gau", "anew", "interactsh", "gf", "uro", "seclists"],
    "auto": ["reconftw", "aidor", "enumrust", "cvinder", "jeeves"],
    "core": ["httpx", "nuclei", "dalfox", "arjun", "ffuf", "waybackurls", "gau", "gf", "seclists", "subfinder", "naabu", "sqlmap", "wpscan", "interactsh", "kiterunner", "reconftw"]
}

def main():
    parser = argparse.ArgumentParser(description="🦅 Universal Recon Toolkit Installer")
    parser.add_argument("-t", "--tools", nargs="+", help="Specific tools to install/update")
    parser.add_argument("-c", "--category", help="Install all tools from category")
    parser.add_argument("-u", "--update", action="store_true", help="Update existing tools")
    parser.add_argument("-s", "--smart", action="store_true", help="Smart mode: skip installed, update outdated")
    parser.add_argument("-a", "--all", action="store_true", help="Install/Update ALL tools")
    parser.add_argument("-l", "--list", action="store_true", help="List available tools")
    parser.add_argument("--categories", action="store_true", help="List all categories")
    parser.add_argument("--links", action="store_true", help="Show tool repository links")
    
    args = parser.parse_args()
    
    if args.categories:
        print("\n📂 Available Categories:")
        for cat, tools in CATEGORIES.items():
            if cat == "core":
                print(f"  • {cat:15s} ({len(tools)} tools) ⭐ Top Hunters Core Set")
            else:
                print(f"  • {cat:15s} ({len(tools)} tools)")
        print(f"\n📖 Full tool list: TOOLS.md")
        print("💡 Use: python reconranger.py -c <category>")
        print("⭐ Tip: Use 'core' for the 15 essential tools top hunters use daily")
        return
    
    if args.links:
        print("\n🔗 Tool Repository Links:")
        for tool, cfg in sorted(TOOL_DEFINITIONS.items()):
            repo = cfg.get('repo', f'https://github.com/projectdiscovery/{tool}')
            print(f"  • {tool:20s}: {repo}")
        return
    
    if args.list:
        print("\n🛠️ Available Tools:")
        for tool, cfg in sorted(TOOL_DEFINITIONS.items()):
            print(f"  • {tool:20s} - {cfg['description']}")
        print(f"\n📊 Total: {len(TOOL_DEFINITIONS)} tools")
        print("📖 Full documentation: TOOLS.md")
        return
    
    # Handle category selection
    if args.category:
        if args.category.lower() in CATEGORIES:
            args.tools = CATEGORIES[args.category.lower()]
            print(f"📂 Installing {args.category} category tools: {', '.join(args.tools)}")
        else:
            print(f"❌ Unknown category: {args.category}")
            print("💡 Available categories:", ", ".join(CATEGORIES.keys()))
            sys.exit(1)
    
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