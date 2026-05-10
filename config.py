"""ReconRanger v4.0 — config.py
Single source of truth is tools.json.
Categories and tool definitions are loaded from there at runtime.
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

VERSION     = "4.0"
DESCRIPTION = "ReconRanger v4.0 — Bug Bounty CLI Tool Manager"

_TOOLS_FILE = Path(__file__).parent.parent / "tools.json"


def _load() -> dict:
    if not _TOOLS_FILE.exists():
        return {}
    return json.loads(_TOOLS_FILE.read_text())


def get_categories() -> Dict[str, List[str]]:
    """Return categories dict from tools.json _categories key."""
    return _load().get("_categories", {})


def get_tools() -> Dict[str, Any]:
    """Return all tool definitions (excludes _categories key)."""
    data = _load()
    return {k: v for k, v in data.items() if not k.startswith("_")}


def get_tool(name: str) -> Optional[Dict[str, Any]]:
    return get_tools().get(name)


def list_tools() -> List[str]:
    return list(get_tools().keys())


# Backwards-compatible aliases so installer.py / reconranger.py
# still work without changes to their import lines.
CATEGORIES       = get_categories()
TOOL_DEFINITIONS = get_tools()