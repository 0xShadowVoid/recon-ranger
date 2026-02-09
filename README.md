# 🦅 ReconRanger - Universal Recon Toolkit Installer

> One-command installer for 61 professional recon tools (subfinder, amass, nuclei, sqlmap, dalfox, metasploit, jeeves)  
> ✅ Works on Debian/Ubuntu/Kali/Parrot/Mint ✅ GPL v3 Licensed ✅ Progress bars

[![Linux](https://img.shields.io/badge/Linux-Debian%20%7C%20Ubuntu%20%7C%20Kali%20%7C%20Parrot-blue?logo=linux)](https://www.debian.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
sudo apt update && sudo apt install -y git python3 python3-pip golang-go nodejs npm

# 2. Clone & install ALL tools
git clone https://github.com/ShadowVoid-King/Recon-Ranger
cd Recon-Ranger
sudo python3 reconranger.py --all

# 3. Configure API keys
python3 ApiKeyMaster.py --configure
python3 ApiKeyMaster.py --apply

# 4. Verify installation
./verify_install.sh
```

---

## 🛠️ Complete Toolkit (61 Tools)

**📖 [View complete tool documentation → TOOLS.md](TOOLS.md)**

### Quick Categories
- **Recon & Subdomains** (7): amass, subfinder, assetfinder, sublist3r, subdomainizer, github-subdomains, bbot
- **DNS & Network** (4): dnsx, shuffledns, masscan, naabu  
- **HTTP/Fingerprinting** (3): httpx, wafw00f, graphw00f
- **Crawling/JavaScript** (6): katana, gospider, linkfinder, jsfinder, jsluice, jsleak
- **Content Discovery** (4): ffuf, dirsearch, kiterunner, cewl
- **Parameter Discovery** (2): arjun, paramspider
- **XSS Scanners** (3): xsstrike, dalfox, xspear
- **Vulnerability Scanners** (2): nuclei, nikto
- **Exploitation** (1): metasploit-framework
- **SQL/NoSQL** (3): sqlmap, ghauri, nosqlmap
- **GraphQL** (2): graphqlmap, graphw00f
- **Directory Traversal** (1): dotdotpwn
- **Cloud Buckets** (2): s3scanner, cloud_enum
- **CMS Scanners** (2): wpscan, droopescan
- **Subdomain Takeover** (3): subjack, subzy, subover
- **OSINT/GitHub** (5): github-dorks, githound, jsecret, virustotalx, metabigor
- **Utilities** (7): waybackurls, gau, anew, interactsh, gf, uro, seclists
- **Automation** (5): reconftw, aidor, enumrust, cvinder, jeeves

---

## 📊 Tool Distribution

| Category | Tools |
|----------|-------|
| Recon & Subdomains | 7 |
| DNS & Network | 4 |
| HTTP/Fingerprinting | 3 |
| Crawling/JS Analysis | 6 |
| Content Discovery | 4 |
| Parameter Discovery | 2 |
| XSS Scanners | 3 |
| Vulnerability Scanners | 2 |
| Exploitation Framework | 1 |
| SQL/NoSQL Injection | 3 |
| GraphQL | 2 |
| Directory Traversal | 1 |
| Cloud Buckets | 2 |
| CMS Scanners | 2 |
| Subdomain Takeover | 3 |
| OSINT/GitHub | 5 |
| Utilities | 7 |
| Automation Frameworks | 5 |
| **TOTAL** | **61 unique tools** |

---

## 🧩 Architecture: Why So Simple?

| File | Lines | Purpose |
|------|-------|---------|
| `reconranger.py` | 34 | CLI entrypoint - delegates all work |
| `core/installer.py` | 200 | Installation logic + progress bars |
| `core/config.py` | 560 | All 61 tool definitions |
| `core/system.py` | 85 | System checks |
| `core/logger.py` | 40 | Logging setup |

**Why modular?**
- Easy to test individual components
- Swap installers without touching CLI
- Add new tools by editing just `config.py`

---

## 🛡️ Why Validation?

You asked why we need validation for a one-time install script. Here's why:

| Without Validation | With Validation |
|-------------------|-----------------|
| Invalid tool names crash midway | Caught before any install starts |
| Wrong Python version fails cryptically | Clear "Python 3.8+ required" message |
| Git clone fails silently | Progress stops, error logged |
| Missing Go breaks 12 tools | Detected upfront, single error |
| Full disk mid-install | Checked first, no partial installs |

**It's about failing fast with clear messages**, not preventing attacks.

---

## 🧰 Commands

| Command | Description |
|---------|-------------|
| `sudo python3 reconranger.py --all` | Install all 61 tools with progress bar |
| `sudo python3 reconranger.py -t subfinder httpx` | Install specific tools |
| `sudo python3 reconranger.py --update --all` | Update all tools |
| `python3 reconranger.py --list` | List available tools |
| `python3 ApiKeyMaster.py --configure` | Setup API keys interactively |
| `python3 ApiKeyMaster.py --apply` | Apply keys to tool configs |
| `./verify_install.sh` | Check all tool versions |

---

## 📊 Progress Bars

Install shows real-time progress:

```
Checking system...
✓ Python OK, Go 1.21

Installing 61 tools...
Progress: 100%|████████████████████| 61/61
✓ amass
✓ subfinder
✓ httpx
...     

61/61 installed
Next: python3 ApiKeyMaster.py --configure
```

Installs `tqdm` automatically, or uses simple fallback.

---

## 🔒 API Key Security

Keys stored at `~/.reconranger/api_keys.json` with **600 permissions**:

```bash
# Verify permissions (MUST show -rw-------):
ls -l ~/.reconranger/api_keys.json

# CORRECT OUTPUT:
# -rw------- 1 youruser youruser 420 Feb 8 14:30 /home/youruser/.reconranger/api_keys.json
```

✅ `ApiKeyMaster.py` enforces 600 permissions  
✅ `.gitignore` excludes `~/.reconranger/`

---

## ⚙️ Tool Examples

```bash
# Full recon pipeline
subfinder -d target.com -silent | httpx -silent -status-code | nuclei -t exposures/

# Cloud enumeration
cloud_enum -k target -t aws,azure,gcp

# GitHub secrets (needs token)
githound --org target-org --keywords api_key,password

# JS endpoint discovery
katana -u https://target.com -js-crawl | grep "\.js$" | xargs -I {} linkfinder -i {} -o cli
```

---

## 📜 License

Copyright (C) 2026 Mohamed Sayed  
GNU General Public License v3.0 - See [LICENSE](LICENSE.txt) file

---

## ⚠️ Legal Notice

Use **only** on systems you own or have explicit written permission to test.