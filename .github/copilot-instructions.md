# ReconRanger AI Coding Agent Instructions

## Project Overview

**ReconRanger v2.0** is a Python-based "surgical recon toolkit" that installs 15 core security tools (selected from 61 total tools) for website reconnaissance. The core philosophy: **install 13 essential tools, not 61**—eliminating bloat, update conflicts, and zero-root installation complexity.

**Key Innovation**: Surgical categorization prevents tool sprawl while maintaining coverage of all recon stages (subdomain discovery → port scanning → endpoint crawling → vulnerability scanning). The project emphasizes minimal installation footprint with automatic rollback protection.

---

## Architecture & Key Components

### Core Modules (`core/`)

- **`config.py`** (631 lines): Master tool registry defining all 61 tools with installation methods (Go, Python, Git, APT). Each tool entry includes: type, binary name, package/repo URL, description, example usage, and dependencies. The `CATEGORIES` dict maps 11 logical categories to tool lists.

- **`installer.py`** (578 lines): Installation orchestrator. Key responsibilities:
  - Multi-method installations: APT packages, Go binaries, Python packages, Git repos, custom build commands
  - Backup system: `~/.recon-backups/` stores tool backups before updates for rollback protection
  - Progress tracking via tqdm (with graceful fallback to plain text)
  - Handles sudo workflows (detects actual user home even when run with `sudo`)
  - Category-based batch installation

- **`system.py`** (98 lines): Cross-distro compatibility layer validating system requirements:
  - Linux distro detection (`/etc/os-release` parsing)
  - Python 3.8+ validation
  - Go 1.19+ verification (checks multiple common paths)
  - Debian/RPM-based system detection

- **`logger.py`** (50 lines): Centralized logging to `logs/` directory (not `/var/log/`)
  - Main log: `logs/reconranger.log`
  - Error log: `logs/reconranger_errors.log`
  - Dual output: file + stdout

### CLI Entry Point (`reconranger.py`)

Command dispatcher supporting multiple invocation styles:
- **Category install**: `python3 reconranger.py -c core` (15 tools), `python3 reconranger.py -c js osint` (additive)
- **Tool numbers**: `python3 reconranger.py 2 5 7` or `python3 reconranger.py 1-5 --skip 4` (range support)
- **Named tools**: `python3 reconranger.py -t subfinder amass nuclei`
- **Status**: `python3 reconranger.py --check` lists installed vs missing tools
- **Information**: `--list`, `--categories`, `--links`
- **Maintenance**: `-u` (update), `-s` (smart mode: install missing + update outdated), `--rollback <tool>`

---

## Data Flow & Integration Points

### Tool Installation Workflow

```
1. User runs: python3 reconranger.py -c core
2. CLI parser identifies category from CATEGORIES dict in config.py
3. ReconRangerInstaller._install_tools_list() iterates each tool
4. For each tool, installer._install_single_tool() routes by type:
   - APT: apt install (requires binary in apt field)
   - Go: go install github.com/... → binary placed in ~/go/bin/ then copied to /usr/local/bin/
   - Python: pip install package (if pip-installable)
   - Git: git clone repo → optional npm/pip install dependencies → optional build_cmd (go build)
   - Custom: Various fallbacks (Ruby gems, npm packages, Rust cargo)
5. Success: Binary verified in /usr/local/bin/{binary_name}
6. Backup: Old version backed up to ~/.recon-backups/{tool}-{timestamp}.bak
7. Status logged to logs/reconranger.log
```

### External Dependencies

- **Go (1.19+)**: Primary language for most tools (bbot, subfinder, httpx, nuclei, katana, etc.)
- **Python (3.8+)**: Runtime for sublist3r, arjun, and wrapper scripts
- **APT/YUM/DNF/Pacman**: OS package managers for initial system deps
- **GitHub**: Source of most tool repos (many ProjectDiscovery tools)
- **npm, Ruby, Rust**: Secondary build tools for specific tools (LinkFinder needs npm, some Ruby gems, Rust tools via cargo)

### Key Patterns in Tool Definitions

Tools in `TOOL_DEFINITIONS` follow standard schema but vary by installation method:

```python
# Simple APT-based tool (cewl)
"cewl": {"type": "apt", "package": "cewl", "binary": "cewl", "apt": "cewl", "description": "..."}

# Go package (subfinder)
"subfinder": {"type": "go", "package": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder", "binary": "subfinder", "apt": "subfinder"}

# Git repo with pip dependencies (LinkFinder)
"linkfinder": {"type": "git", "repo": "https://github.com/GerbenJavado/LinkFinder.git", 
               "path": "/opt/LinkFinder", "entrypoint": "/opt/LinkFinder/linkfinder.py", 
               "requirements": ["-r", "/opt/LinkFinder/requirements.txt"], "post_clone": "npm install --silent"}

# Tools often have post_install commands (nuclei updates templates)
"nuclei": {"post_install": "nuclei -ut -silent"}
```

---

## Developer Workflows & Common Tasks

### Adding a New Tool

1. **Identify tool type** (apt/go/python/git) and gather metadata (repo URL, binary name)
2. **Update `core/config.py`**: Add entry to `TOOL_DEFINITIONS` dict with required fields
3. **Assign category**: Add tool name to appropriate list in `CATEGORIES` dict
4. **Test**: `python3 reconranger.py -t {tool_name}` then `python3 reconranger.py --check`
5. **Document**: Add entry to TOOLS.md if user-facing

**Example (Go tool)**:
```python
"anew": {
    "type": "go",
    "package": "github.com/tomnomnom/anew",
    "binary": "anew",
    "apt": None,
    "description": "Tool for adding new lines to files, ignoring duplicates"
}
# Then add "anew" to CATEGORIES["utils"]
```


### Testing Installation & Error Checking

Install single tool:
```bash
python3 reconranger.py -t {tool_name}
```

After any install/update, check which tools succeeded and which failed:
```bash
python3 reconranger.py --check
```

This will list the names of tools that installed successfully and any failures:
```
✅ Installed: subfinder, httpx, nuclei, katana, ...
❌ Missing: arjun, katana, ...
```

For troubleshooting, review error logs:
```bash
tail -f logs/reconranger_errors.log
```

Rollback if failed:
```bash
python3 reconranger.py --rollback {tool_name}
```

### Cross-Distribution Support

Code checks distro in `core/system.py`. When adding OS-specific logic:
1. Check `SystemChecker.is_debian_based()` for Debian/Ubuntu/Kali
2. Fallback to detection via `/etc/os-release` parsing (see `_detect_distro()`)
3. Test on at least one other distro (RedHat/Arch/Fedora)

### Critical Workflows NOT in UI

- **Post-install setup**: Some tools need post-install scripts (e.g., `nuclei -ut` to update templates). See `post_install` field in tool configs.
- **Dependency management**: Tools with external deps (npm, Ruby) are handled in `post_clone` or `requirements` fields. Verify these run before binary is invoked.
- **Rollback mechanism**: Before installing/updating, installer backs up old binary to `~/.recon-backups/`. On failure, user can manually restore or use `--rollback` command.

---

## Project-Specific Conventions

1. **Binary Location Convention**: All executables install to `/usr/local/bin/{binary_name}`, checked via `Path("/usr/local/bin") / cfg["binary"]`

2. **Home Directory Detection**: Handles sudo: `os.environ.get('SUDO_USER')` → `/home/{actual_user}` instead of root's home

3. **Logging to User Space**: Logs stored in `./logs/` (relative to project), not `/var/log/`. Allows non-root usage.

4. **Category-First Mindset**: Always think in categories (core, js, osint, vuln, etc.) not individual tools. Core set solves 95% of use cases.

5. **Zero-Root by Default**: Most tools install to user space (`~/go/bin`) then copy to `/usr/local/bin/`. Only requires sudo for final binary placement, not compilation.

6. **Tqdm Progress UI**: Install progress shown via tqdm library with fallback to plain print if unavailable (see tqdm mock class in installer.py)

---

## Known Limitations & Gotchas

1. **Go Version Pinning**: Some tools require specific Go versions (e.g., dnsx needs 1.24.0). Check `go_version` field in tool config.

2. **APT Fallback**: If Go installation fails, some tools have APT packages as backup. See dual entries like `"apt": "subfinder"`.

3. **Post-Install Commands**: Tools like nuclei require `nuclei -ut` after installation. This blocks until templates download (~500MB).

4. **Git Clone Complexity**: LinkFinder requires npm install post-clone, SubDomainizer uses Python entrypoints. Each has custom handling in installer.

5. **Binary Naming Inconsistencies**: Some tool repos don't match binary names. Github repos may be `github-subdomains` but binary is `github-subdomains`. Check `binary` field carefully.

---

## File References for Common Tasks

| Task | Key File |
|------|----------|
| Add/update tool | [core/config.py](core/config.py#L15) – `TOOL_DEFINITIONS` dict |
| Modify install logic | [core/installer.py](core/installer.py#L1) – `_install_single_tool()` method |
| Cross-distro compatibility | [core/system.py](core/system.py#L1) – `SystemChecker` class |
| CLI commands | [reconranger.py](reconranger.py#L1) – argparse setup |
| Logging | [core/logger.py](core/logger.py#L1) – centralized logger |
| System bootstrap | [install.sh](install.sh#L1) – bash script for distro detection |

---


## Additional Documentation

If your project uses API key management (`ApiKeyMaster.py`) or orchestration scripts (`automation/`), consider documenting their workflows for future maintainers.
