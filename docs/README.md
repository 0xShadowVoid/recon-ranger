# 🦅 ReconRanger v3.1 - Surgical Recon Toolkit for Linux
> **Made by 0xShadowVoid**

ReconRanger is a lightweight, surgical reconnaissance toolkit and manager that focuses on installing and orchestrating a curated set of high-quality recon tools.

Summary
-------
- **Version:** 3.1
- **Philosophy:** Install the right tools, not the most tools — surgical, reproducible recon workflows.
- **Platform:** Linux (Kali, Parrot, Ubuntu/Debian compatible). WSL is supported for testing.

Registry Summary
----------------
- **Total tools in registry:** 17
- **Categories present:** 6 (core, vuln, web, osint, utils, automation)
- **Core toolkit (8 tools):** bbot, subfinder, amass, httpx, nuclei, katana, ffuf, naabu

Quick Links
-----------
- Full documentation, guides, and reports: [docs/README.md](docs/README.md)
- Latest release: `v3.1`

Quick Start
-----------
Install prerequisites and fix system deps (run as non-root or via sudo when required):
```bash
python3 reconranger.py --fix-deps
```

Configure API keys (interactive):
```bash
python3 ApiKeyMaster.py --configure
python3 ApiKeyMaster.py --print-exports   # preview env exports (masked)
```

Install core toolkit (recommended):
```bash
python3 reconranger.py -c core
```

Useful Commands
---------------
- List tools: `python3 reconranger.py --list`
- Categories: `python3 reconranger.py --categories`
- Install specific tools: `python3 reconranger.py -t subfinder httpx`
- Check installation status: `python3 reconranger.py --check`

Why keep docs/ and root README
--------------------------------
- `README.md` (this file): short, friendly project landing for GitHub.
- `docs/`: full manuals, validation reports, and long-form generated artifacts (keeps repository root clean while retaining all documentation).

Security & Privacy
------------------
- Do NOT commit API keys. `ApiKeyMaster` stores keys under `~/.reconranger/` with strict permissions.
- If you use `--export` to write keys into shell profiles, be aware that plaintext keys in shell profiles are a security risk.

Contributing
------------
See the full contributor guide and developer workflows in [docs/README.md](docs/README.md#developer-workflows).

License
-------
This software is intended for authorized security testing and research. See LICENSE.txt for details.
# 🦅 ReconRanger v3.1 - Surgical Recon Toolkit for Linux
> **Made by 0xShadowVoid**

Python rewrite with a surgical core toolkit covering the vast majority of common recon workflows. Zero root required, auto-rollback protection, 5-minute installs. Install the curated core tools for focused, reproducible recon workflows.

---

## ✨ Features
- **Modular Tool Registry:** Add, edit, update, or delete tools via CLI without touching the code.
- **Surgical Core Toolkit:** Pre-configured with the best tools for modern recon (BBOT, Subfinder, Nuclei, etc.).
- **One-Click API Keys:** Centralized management for Chaos, GitHub, SecurityTrails, Netlas, Zoomeye, ShrewdEye, and VirusTotal.
- **Cross-Distro Support:** Optimized for **Kali Linux** and **Parrot OS** with auto-dependency fixing.
- **Global Installation:** Tools are installed globally to `/usr/local/bin` for ease of use.
- **Integrated PEGPON:** Includes the advanced PEGPON automation framework by default.
- **Robust Logging:** Detailed logs of every installation and error in the `logs/` directory.

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/0xShadowVoid/recon-ranger.git
cd recon-ranger

# Fix dependencies and setup environment
python3 reconranger.py --fix-deps
```

### 2. Configure API Keys
```bash
# Launch the configuration wizard
python3 reconranger.py --api

# Apply keys to tool configurations and shell environment
python3 reconranger.py --apply-keys
```

### 3. Install Tools
```bash
# Install the Core Toolkit (recommended)
python3 reconranger.py -c core

# Install everything in the registry
python3 reconranger.py --install-all

# Install specific tools by name
python3 reconranger.py -t subfinder bbot nuclei
```

---

## 🛠️ Tool Management
recon-ranger v3.1 makes it easy to maintain your own custom toolkit:
- **List Tools:** `python3 reconranger.py --list`
- **Add Tool:** `python3 reconranger.py --add-tool`
- **Delete Tool:** `python3 reconranger.py --delete-tool <name>`
- **Check Status:** `python3 reconranger.py --check`

---

## 📂 Project Structure
- `reconranger.py`: Main CLI entry point.
- `tools.json`: Dynamic registry of all tools.
- `core/`: Core modules for system, installation, and keys.
- `logs/`: Installation and error logs.

---

## 🔑 Supported API Providers
- **Chaos** [ProjectDiscovery]
- **GitHub** [Personal Access Tokens]
- **SecurityTrails** [DNS Intelligence]
- **Netlas** [Internet Scanning]
- **Zoomeye** [Cyberspace Search]
- **ShrewdEye** [Subdomain Intelligence]
- **VirusTotal** [Malware & Domain Intel]
- **Shodan** [IoT Search Engine]

---

## Future Features
- Go check file /docs/future_features.md

---

## 🏷️ Topics
`linux` `debian` `ubuntu` `kali` `security-tools` `vulnerability-scanning` `reconnaissance` `subdomain-enumeration` `parrot-os` `bug-bounty-hunting` `bug-bounty-tools`


---

## 📜 License
This project is for educational and ethical security testing purposes only.
