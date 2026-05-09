# ReconRanger — Copilot Instructions

## Project Summary
ReconRanger is a bug bounty CLI tool manager written in Python.
It installs, organizes, and manages 76 recon tools across 15 categories.

## Key Files
- `reconranger.py` — CLI entry point. All argument parsing and dispatch lives here.
- `tools.json` — Source of truth for the tool registry. Alphabetically sorted.
- `core/config.py` — `CATEGORIES`, `TOOL_DEFINITIONS`, `VERSION`. Must stay in sync with `tools.json`.
- `core/installer.py` — Install handlers: `_install_go`, `_install_python`, `_install_git`, `_install_apt`, `_install_ruby`, `_install_cargo`.
- `core/system.py` — System dependency checks and Go path management.
- `core/keys.py` — API key wizard and env injection.

## Install Type Rules
- `go` — requires `package` field with full module path including `@latest`
- `python` — requires `package` field (pip package name); use `--break-system-packages`
- `git` — requires `repo`, `path`, and either `entrypoint` or `build_cmd`
- `apt` — requires `package` and `apt` fields (same value)
- `ruby` — requires `package` field (gem name); installer auto-installs ruby-full if missing
- `cargo` — requires either `package` (cargo install) or `repo`+`path`+`build_cmd` (git+build)

## Adding a Tool
1. Add entry to `tools.json` (alphabetical order, all required fields)
2. Add tool name to the correct category list in `core/config.py → CATEGORIES`
3. Optionally add full definition to `core/config.py → TOOL_DEFINITIONS`
4. Never duplicate a tool across categories

## Version
Current version is defined in `core/config.py → VERSION` and referenced in `reconranger.py`.
Update both when bumping the version.

## Style
- Python 3.8+ compatible
- No external dependencies beyond stdlib + tqdm + requests
- All installer methods return `bool` (True = success)
- Print user-facing output with `[✓]`, `[✗]`, `[→]`, `[!]` prefixes
- Use `logger.error/info/warning` for file logging, `print` for terminal output
