#!/usr/bin/env python3
"""
ReconRanger v4.0 — Bug Bounty CLI Tool Manager
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
from core.config import VERSION, CATEGORIES, TOOL_DEFINITIONS

TOOLS_FILE = Path(__file__).parent / "tools.json"


def load_tools() -> dict:
    if not TOOLS_FILE.exists():
        return {}
    return json.loads(TOOLS_FILE.read_text())


def save_tools(tools: dict) -> None:
    TOOLS_FILE.write_text(json.dumps(tools, indent=2, sort_keys=True))


def main():
    tools       = load_tools()
    system      = SystemManager()
    key_manager = KeyManager()
    logger      = setup_logging()

    parser = argparse.ArgumentParser(
        description=f"ReconRanger v{VERSION} — Bug Bounty CLI Tool Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reconranger.py -c core               Install core toolkit (13 tools)
  reconranger.py -t subfinder httpx    Install specific tools
  reconranger.py --install-all         Install every tool in registry
  reconranger.py --list                List all tools with category/description
  reconranger.py --categories          Show categories and tool counts
  reconranger.py --check               Check which tools are installed
  reconranger.py --api                 Manage API keys
  reconranger.py --add-tool            Add a custom tool to the registry
  reconranger.py --edit-tool nuclei    Edit an existing tool entry
  reconranger.py --delete-tool oldtool Remove a tool from the registry
        """,
    )

    g_inst = parser.add_argument_group("Installation")
    g_inst.add_argument("-t", "--tools",       nargs="+", metavar="TOOL", help="Install specific tools by name")
    g_inst.add_argument("-c", "--category",    metavar="CAT",  help="Install all tools in a category")
    g_inst.add_argument("--install-all",       action="store_true", help="Install every tool in the registry")
    g_inst.add_argument("--check",             action="store_true", help="Show installation status for all tools")

    g_api = parser.add_argument_group("API Keys")
    g_api.add_argument("--api",                action="store_true", help="Launch API key configuration wizard")
    g_api.add_argument("--apply-keys",         action="store_true", help="Apply saved keys to tool configs and env")

    g_reg = parser.add_argument_group("Registry")
    g_reg.add_argument("--add-tool",           action="store_true", help="Add a new tool interactively")
    g_reg.add_argument("--edit-tool",          metavar="TOOL",      help="Edit an existing tool entry interactively")
    g_reg.add_argument("--delete-tool",        metavar="TOOL",      help="Delete a tool from the registry")
    g_reg.add_argument("-l", "--list",         action="store_true", help="List all tools")
    g_reg.add_argument("--categories",         action="store_true", help="List categories with tool counts")

    g_sys = parser.add_argument_group("System")
    g_sys.add_argument("--fix-deps",           action="store_true", help="Install/fix system dependencies")

    args = parser.parse_args()

    # ── Interactive menu (no args) ────────────────────────────────────────────
    if len(sys.argv) == 1:
        _interactive_menu(args)

    # ── System ────────────────────────────────────────────────────────────────
    if args.fix_deps:
        system.install_system_dependencies()
        system.check_go()
        return

    # ── API keys ──────────────────────────────────────────────────────────────
    if args.api:
        key_manager.wizard()
        return

    if args.apply_keys:
        key_manager.apply_to_env()
        return

    # ── Registry management ───────────────────────────────────────────────────
    if args.add_tool:
        _add_tool(tools)
        return

    if args.edit_tool:
        _edit_tool(tools, args.edit_tool)
        return

    if args.delete_tool:
        _delete_tool(tools, args.delete_tool)
        return

    if args.list:
        _print_list(tools)
        return

    if args.categories:
        _print_categories()
        return

    # ── Installation ──────────────────────────────────────────────────────────
    targets = []

    if args.install_all:
        targets = list(tools.keys())

    elif args.category:
        cat_tools = CATEGORIES.get(args.category)
        if cat_tools:
            targets = list(cat_tools)
            # Supplement registry from TOOL_DEFINITIONS for any missing entries
            for n in cat_tools:
                if n not in tools and n in TOOL_DEFINITIONS:
                    tools[n] = TOOL_DEFINITIONS[n]
        else:
            # Fall back to filtering tools.json by category field
            targets = [n for n, c in tools.items() if c.get("category") == args.category]
        if not targets:
            print(f"[!] Unknown category '{args.category}'. Run --categories to list valid ones.")
            return

    elif args.tools:
        targets = args.tools

    if targets:
        system.install_system_dependencies()
        system.check_go()
        installer = ReconRangerInstaller(tools)
        env       = key_manager.get_env_vars()

        ok_list, fail_list = [], []
        for t in targets:
            if installer.install_tool(t, env_vars=env):
                ok_list.append(t)
            else:
                fail_list.append(t)

        print(f"\n{'─'*50}")
        print(f"Requested : {len(targets)}")
        print(f"Succeeded : {len(ok_list)}")
        print(f"Failed    : {len(fail_list)}")
        if ok_list:
            print(f"  [✓] {', '.join(ok_list)}")
        if fail_list:
            print(f"  [✗] {', '.join(fail_list)}")
        return

    if args.check:
        _print_check(tools)
        return

    parser.print_help()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _interactive_menu(args):
    """Simple numbered menu shown when reconranger.py is invoked with no arguments."""
    print(f"\nReconRanger v{VERSION} — Interactive Mode")
    print("─" * 40)
    menu = [
        ("List all tools",        lambda: setattr(args, "list", True)),
        ("List categories",       lambda: setattr(args, "categories", True)),
        ("Install core toolkit",  lambda: setattr(args, "category", "core")),
        ("Install by category",   lambda: setattr(args, "category", input("  Category: ").strip())),
        ("Install specific tools",lambda: setattr(args, "tools", input("  Tools (space-separated): ").strip().split())),
        ("Check install status",  lambda: setattr(args, "check", True)),
        ("Manage API keys",       lambda: setattr(args, "api", True)),
        ("Exit",                  lambda: sys.exit(0)),
    ]
    for i, (label, _) in enumerate(menu, 1):
        print(f"  {i}) {label}")
    choice = input("\nChoice: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(menu):
        menu[int(choice) - 1][1]()
    else:
        print("Invalid choice.")
        sys.exit(1)


def _add_tool(tools: dict):
    print("\nAdd new tool to registry:")
    name    = input("  Name (slug): ").strip().lower()
    if not name:
        print("[!] Name required.")
        return
    ttype   = input("  Type [go/python/git/apt/ruby/cargo]: ").strip().lower()
    package = input("  Package / repo URL: ").strip()
    binary  = input("  Binary name: ").strip()
    desc    = input("  Description: ").strip()
    cat     = input("  Category: ").strip()
    example = input("  Example command: ").strip()

    entry = {"type": ttype, "binary": binary, "description": desc,
             "category": cat, "example": example}
    if ttype in ("go", "python", "ruby", "cargo"):
        entry["package"] = package
    elif ttype in ("git",):
        entry["repo"] = package
        entry["path"] = f"/opt/{name}"
        entry["entrypoint"] = f"/opt/{name}/{binary}.py"

    tools[name] = entry
    save_tools(tools)
    print(f"[✓] Added '{name}' to registry.")


def _edit_tool(tools: dict, name: str):
    if name not in tools:
        print(f"[✗] '{name}' not found in registry.")
        return

    entry = tools[name]
    print(f"\nEditing '{name}' — press Enter to keep current value.\n")
    editable = ["type", "package", "repo", "binary", "description",
                "category", "example", "path", "entrypoint", "post_install"]

    for field in editable:
        current = entry.get(field, "")
        val = input(f"  {field} [{current}]: ").strip()
        if val:
            entry[field] = val

    tools[name] = entry
    save_tools(tools)
    print(f"[✓] Updated '{name}'.")


def _delete_tool(tools: dict, name: str):
    if name not in tools:
        print(f"[✗] '{name}' not found.")
        return
    confirm = input(f"Delete '{name}'? [y/N]: ").strip().lower()
    if confirm == "y":
        del tools[name]
        save_tools(tools)
        print(f"[✓] Deleted '{name}'.")
    else:
        print("Cancelled.")


def _print_list(tools: dict):
    print(f"\nReconRanger Registry — {len(tools)} tools\n")
    print(f"{'#':<4} {'Name':<22} {'Category':<16} {'Type':<8} {'Description'}")
    print("─" * 90)
    for i, (name, cfg) in enumerate(sorted(tools.items()), 1):
        print(f"{i:<4} {name:<22} {cfg.get('category',''):<16} "
              f"{cfg.get('type',''):<8} {cfg.get('description','')[:45]}")


def _print_categories():
    print(f"\nAvailable Categories ({len(CATEGORIES)} total)\n")
    print(f"{'Category':<18} {'Tools':<6} {'Members'}")
    print("─" * 70)
    for cat, members in CATEGORIES.items():
        print(f"{cat:<18} {len(members):<6} {', '.join(members)}")


def _print_check(tools: dict):
    import shutil
    print(f"\nInstallation Status — {len(tools)} tools\n")
    print(f"{'Name':<22} {'Status':<14} {'Path'}")
    print("─" * 70)
    installed = 0
    for name, cfg in sorted(tools.items()):
        path = shutil.which(cfg.get("binary", name))
        if path:
            status = "[✓] Installed"
            installed += 1
        else:
            status = "[✗] Missing"
        print(f"{name:<22} {status:<14} {path or 'N/A'}")
    print(f"\n{installed}/{len(tools)} tools installed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")
        sys.exit(0)
