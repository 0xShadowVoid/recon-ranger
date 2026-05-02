# 🦅 ReconRanger v3.0 - Surgical Recon Toolkit for Linux
> **Made by 0xShadowVoid**

Python rewrite with 13-tool surgical core covering 95% of recon workflows. Zero root required, auto-rollback protection, 5-minute installs. Install 13 tools, not 61. Recon surgically, not sprawled. Transforms from simple tool installer into surgical recon workflow engine - optimized for Linux.

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
git clone https://github.com/0xShadowVoid/Recon-Ranger.git
cd Recon-Ranger

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
Recon-Ranger v3.0 makes it easy to maintain your own custom toolkit:
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

## 🏷️ Topics
`linux` `debian` `ubuntu` `kali` `security-tools` `vulnerability-scanning` `reconnaissance` `subdomain-enumeration` `parrot-os` `bug-bounty-hunting` `bug-bounty-tools`

---

## 📜 License
This project is for educational and ethical security testing purposes only.
