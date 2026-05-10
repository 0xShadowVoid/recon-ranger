#!/usr/bin/env python3
"""
ReconRanger v4.0 — Bug Bounty CLI Tool Manager
Developed by 0xShadowVoid
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Works from any directory, flat or core/ structure
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from installer import ReconRangerInstaller
    from system import SystemManager
    from keys import KeyManager
    from logger import setup_logging
    from config import VERSION, get_categories, get_tools
except ImportError:
    from core.installer import ReconRangerInstaller
    from core.system import SystemManager
    from core.keys import KeyManager
    from core.logger import setup_logging
    from core.config import VERSION, get_categories, get_tools

TOOLS_FILE = Path(__file__).parent / "tools.json"


def load_json() -> dict:
    if not TOOLS_FILE.exists():
        return {}
    return json.loads(TOOLS_FILE.read_text())


def save_json(data: dict) -> None:
    TOOLS_FILE.write_text(json.dumps(data, indent=2))


def get_tool_registry() -> dict:
    """All tools — strips _categories and other _ keys."""
    return {k: v for k, v in load_json().items() if not k.startswith("_")}


def main():
    CATEGORIES = get_categories()
    tools      = get_tool_registry()
    system     = SystemManager()
    key_mgr    = KeyManager()
    logger     = setup_logging()

    parser = argparse.ArgumentParser(
        description=f"ReconRanger v{VERSION} — Bug Bounty CLI Tool Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reconranger.py -c core               Install full stack (38 tools)
  reconranger.py -t subfinder httpx    Install specific tools
  reconranger.py --install-all         Install every tool in registry
  reconranger.py --list                List all tools
  reconranger.py --categories          Show categories and counts
  reconranger.py --check               Check which tools are installed
  reconranger.py --add-tool            Add a tool (updates tools.json only)
  reconranger.py --add-category        Add / extend a category
  reconranger.py --edit-tool nuclei    Edit an existing tool entry
  reconranger.py --delete-tool NAME    Remove a tool from the registry
  reconranger.py --api                 Manage API keys
        """,
    )

    g_inst = parser.add_argument_group("Installation")
    g_inst.add_argument("-t", "--tools",       nargs="+", metavar="TOOL")
    g_inst.add_argument("-c", "--category",    metavar="CAT")
    g_inst.add_argument("--install-all",       action="store_true")
    g_inst.add_argument("--check",             action="store_true")

    g_api = parser.add_argument_group("API Keys")
    g_api.add_argument("--api",                action="store_true")
    g_api.add_argument("--apply-keys",         action="store_true")

    g_reg = parser.add_argument_group("Registry")
    g_reg.add_argument("--add-tool",           action="store_true", help="Add a new tool (tools.json only)")
    g_reg.add_argument("--add-category",       action="store_true", help="Add a new category or extend existing one")
    g_reg.add_argument("--edit-tool",          metavar="TOOL",      help="Edit an existing tool entry")
    g_reg.add_argument("--delete-tool",        metavar="TOOL",      help="Delete a tool from the registry")
    g_reg.add_argument("-l", "--list",         action="store_true")
    g_reg.add_argument("--categories",         action="store_true")

    g_sys = parser.add_argument_group("System")
    g_sys.add_argument("--fix-deps",           action="store_true")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        _interactive_menu(args)

    if args.fix_deps:
        system.install_system_dependencies()
        system.check_go()
        return

    if args.api:
        key_mgr.wizard()
        return

    if args.apply_keys:
        key_mgr.apply_to_env()
        return

    if args.add_tool:
        _add_tool()
        return

    if args.add_category:
        _add_category()
        return

    if args.edit_tool:
        _edit_tool(args.edit_tool)
        return

    if args.delete_tool:
        _delete_tool(args.delete_tool)
        return

    if args.list:
        _print_list(tools)
        return

    if args.categories:
        _print_categories(CATEGORIES)
        return

    if args.check:
        _print_check(tools)
        return

    # ── Installation ──────────────────────────────────────────────────────────
    targets = []

    if args.install_all:
        targets = list(tools.keys())

    elif args.category:
        targets = CATEGORIES.get(args.category)
        if not targets:
            # Fallback: filter tools.json by category field
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
        env       = key_mgr.get_env_vars()

        ok, fail = [], []
        for t in targets:
            if installer.install_tool(t, env_vars=env):
                ok.append(t)
            else:
                fail.append(t)

        print(f"\n{'─'*50}")
        print(f"Requested : {len(targets)}")
        print(f"Succeeded : {len(ok)}")
        print(f"Failed    : {len(fail)}")
        if ok:   print(f"  [✓] {', '.join(ok)}")
        if fail: print(f"  [✗] {', '.join(fail)}")
        return

    parser.print_help()


# ── Registry helpers — ALL touch only tools.json ─────────────────────────────

def _add_tool():
    """Add a tool to tools.json and optionally to a category — no Python editing needed."""
    print("\nAdd new tool — only tools.json will be updated.\n")

    name = input("  Tool name (slug, e.g. 'mytool'): ").strip().lower()
    if not name:
        print("[!] Name required."); return

    ttype   = input("  Install type [go/python/git/apt/ruby/cargo]: ").strip().lower()
    binary  = input("  Binary name: ").strip()
    desc    = input("  Description: ").strip()
    example = input("  Example command: ").strip()

    entry: dict = {"type": ttype, "binary": binary, "description": desc, "example": example}

    if ttype in ("go", "python", "ruby"):
        entry["package"] = input("  Package (pip name / go module): ").strip()
    elif ttype == "apt":
        pkg = input("  Apt package name: ").strip()
        entry["package"] = pkg
        entry["apt"]     = pkg
    elif ttype in ("git", "cargo"):
        entry["repo"]       = input("  Git repo URL: ").strip()
        entry["path"]       = f"/opt/{name}"
        entry["entrypoint"] = f"/opt/{name}/{binary}.py"
        if ttype == "cargo":
            entry["build_cmd"] = "cargo build --release"

    # Optional: assign to category
    cat = input("  Category (leave blank to skip): ").strip().lower()

    data = load_json()
    data[name] = entry

    if cat:
        cats = data.get("_categories", {})
        cats.setdefault(cat, [])
        if name not in cats[cat]:
            cats[cat].append(name)
        data["_categories"] = cats

    save_json(data)
    print(f"\n[✓] '{name}' added to tools.json" + (f" under category '{cat}'" if cat else "") + ".")
    print("    No Python files were modified.")


def _add_category():
    """Add a new category or append tools to an existing one — tools.json only."""
    print("\nAdd / extend category — only tools.json will be updated.\n")

    data = load_json()
    cats = data.get("_categories", {})

    existing = list(cats.keys())
    if existing:
        print(f"  Existing categories: {', '.join(existing)}\n")

    cat = input("  Category name (new or existing): ").strip().lower()
    if not cat:
        print("[!] Name required."); return

    current = cats.get(cat, [])
    print(f"  Current tools in '{cat}': {', '.join(current) if current else 'none'}")

    raw = input("  Tools to add (space-separated): ").strip()
    additions = [t.strip() for t in raw.split() if t.strip()]

    registry = {k for k in data if not k.startswith("_")}
    not_found = [t for t in additions if t not in registry]
    if not_found:
        print(f"  [!] Not in registry (will add anyway): {', '.join(not_found)}")

    for t in additions:
        if t not in current:
            current.append(t)

    cats[cat] = current
    data["_categories"] = cats
    save_json(data)
    print(f"\n[✓] Category '{cat}' now has {len(current)} tools.")
    print("    No Python files were modified.")


def _edit_tool(name: str):
    data  = load_json()
    tools = {k: v for k, v in data.items() if not k.startswith("_")}

    if name not in tools:
        print(f"[✗] '{name}' not found."); return

    entry = tools[name]
    print(f"\nEditing '{name}' — press Enter to keep current value.\n")

    for field in ["type", "package", "repo", "binary", "description",
                  "category", "example", "path", "entrypoint", "post_install"]:
        current = entry.get(field, "")
        val = input(f"  {field} [{current}]: ").strip()
        if val:
            entry[field] = val

    data[name] = entry
    save_json(data)
    print(f"[✓] '{name}' updated.")


def _delete_tool(name: str):
    data = load_json()
    if name not in data:
        print(f"[✗] '{name}' not found."); return

    confirm = input(f"Delete '{name}'? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Cancelled."); return

    del data[name]

    # Also remove from any category lists
    cats = data.get("_categories", {})
    for members in cats.values():
        if name in members:
            members.remove(name)
    data["_categories"] = cats

    save_json(data)
    print(f"[✓] '{name}' deleted from registry and all categories.")


def _print_list(tools: dict):
    print(f"\nReconRanger Registry — {len(tools)} tools\n")
    print(f"{'#':<4} {'Name':<22} {'Category':<16} {'Type':<8} Description")
    print("─" * 90)
    for i, (name, cfg) in enumerate(sorted(tools.items()), 1):
        cat  = cfg.get("category", "")
        t    = cfg.get("type", "")
        desc = cfg.get("description", "")[:45]
        print(f"{i:<4} {name:<22} {cat:<16} {t:<8} {desc}")


def _print_categories(cats: dict):
    print(f"\nAvailable Categories ({len(cats)} total)\n")
    print(f"{'Category':<18} {'Tools':<6} Members")
    print("─" * 70)
    for cat, members in cats.items():
        print(f"{cat:<18} {len(members):<6} {', '.join(members)}")


def _print_check(tools: dict):
    import shutil
    print(f"\nInstallation Status — {len(tools)} tools\n")
    print(f"{'Name':<22} {'Status':<14} Path")
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


def _interactive_menu(args):
    print(f"\nReconRanger v{VERSION} — Interactive Mode")
    print("─" * 40)
    menu = [
        ("List all tools",          lambda: setattr(args, "list", True)),
        ("List categories",         lambda: setattr(args, "categories", True)),
        ("Install full stack",      lambda: setattr(args, "category", "core")),
        ("Install by category",     lambda: setattr(args, "category", input("  Category: ").strip())),
        ("Install specific tools",  lambda: setattr(args, "tools", input("  Tools (space-separated): ").strip().split())),
        ("Check install status",    lambda: setattr(args, "check", True)),
        ("Add a tool",              lambda: _add_tool()),
        ("Add / extend a category", lambda: _add_category()),
        ("Manage API keys",         lambda: setattr(args, "api", True)),
        ("Exit",                    lambda: sys.exit(0)),
    ]
    for i, (label, _) in enumerate(menu, 1):
        print(f"  {i}) {label}")
    choice = input("\nChoice: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(menu):
        label, fn = menu[int(choice) - 1]
        if label in ("Add a tool", "Add / extend a category"):
            fn()
            sys.exit(0)
        fn()
    else:
        print("Invalid choice.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")
        sys.exit(0)
