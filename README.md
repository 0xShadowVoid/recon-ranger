# 🦅 ReconRanger - Universal Recon Toolkit Installer

> One-command installer for 60 professional recon tools (subfinder, amass, nuclei, sqlmap, dalfox, metasploit)  
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

## 🛠️ Complete Toolkit (63 Tools)

### 🌐 Recon & Subdomain Enumeration (7)
- **amass** - In-depth attack surface mapping
- **subfinder** - Fast subdomain discovery (30+ sources)
- **assetfinder** - Certificate Transparency subdomains
- **sublist3r** - OSINT-based subdomain enumeration
- **subdomainizer** - Find subdomains in external resources
- **github-subdomains** - GitHub commits/repos subdomains
- **bbot** - Recursive internet scanner

### 📡 DNS & Network Scanning (4)
- **dnsx** - Multi-purpose DNS toolkit
- **shuffledns** - MassDNS wrapper for brute-forcing
- **masscan** - High-speed port scanner
- **naabu** - Fast port scanner for recon

### 🔍 HTTP Probing & Fingerprinting (3)
- **httpx** - HTTP probing and fingerprinting
- **wafw00f** - WAF detection and identification
- **graphw00f** - GraphQL security testing

### 🕷️ Crawling & JavaScript Analysis (6)
- **katana** - Next-gen web crawler
- **gospider** - Fast web spider
- **linkfinder** - JavaScript endpoint discovery
- **jsfinder** - JavaScript secrets finder
- **jsluice** - JavaScript link extractor
- **jsleak** - JavaScript leak scanner

### 🔓 Content Discovery & Fuzzing (4)
- **ffuf** - Fast web fuzzer
- **dirsearch** - Directory brute-forcing
- **kiterunner** - Content discovery framework
- **cewl** - Custom wordlist generator

### 🔑 Parameter Discovery (2)
- **arjun** - HTTP parameter discovery
- **ParamSpider** - Parameter mining from archives

### 💉 XSS Scanners (3)
- **XSStrike** - Advanced XSS detection
- **dalfox** - Modern XSS scanner
- **XSpear** - XSS scanner with Selenium

### 🧪 Vulnerability Scanners (2)
- **nuclei** - Fast vulnerability scanner (10k+ templates)
- **nikto** - Web server scanner

### 💥 Exploitation Framework (1)
- **metasploit-framework** - Complete penetration testing framework

### 📦 Specialized Attack Tools

#### SQL/NoSQL Injection (3)
- **sqlmap** - Automatic SQL injection tool
- **ghauri** - SQL injection scanner
- **NoSQLMap** - NoSQL database injection

#### GraphQL (2)
- **GraphQLmap** - GraphQL security testing
- **graphw00f** - GraphQL fingerprinting

#### Directory Traversal (1)
- **dotdotpwn** - Path traversal fuzzer

#### Cloud Buckets (2)
- **S3Scanner** - AWS S3 bucket scanner
- **cloud_enum** - Multi-cloud resource enumeration

#### CMS Scanners (2)
- **wpscan** - WordPress security scanner
- **droopescan** - CMS scanner (Drupal, Joomla, etc.)

### 🌍 Subdomain Takeover (3)
- **subjack** - Subdomain takeover detection
- **subzy** - Fast subdomain takeover scanner
- **SubOver** - Subdomain takeover tool

### 🔎 OSINT & GitHub Hunting (5)
- **github-dorks** - GitHub sensitive data finder
- **githound** - GitHub secrets hunter
- **jsecret** - JavaScript secret finder
- **virustotalx** - VirusTotal intelligence tool
- **metabigor** - Network intelligence tool

### 🧰 Utilities & Helpers (6)
- **waybackurls** - URL fetcher from archives
- **gau** - GetAllUrls enumerator
- **anew** - Append new lines to files
- **interactsh** - Out-of-band interaction client
- **gf** - Pattern finder for grep
- **uro** - URL recon tool

### 🤖 Automation Frameworks (4)
- **ReconFTW** - Automated recon framework
- **AIDOR** - IDOR automation scanner
- **enumrust** - Rust-based enumeration tool
- **CVINDER** - CVE identifier and finder

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
| Utilities | 6 |
| Automation Frameworks | 4 |
| **TOTAL** | **60 unique tools** |

---

## 🧩 Architecture: Why So Simple?

| File | Lines | Purpose |
|------|-------|---------|
| `reconranger.py` | 34 | CLI entrypoint - delegates all work |
| `core/installer.py` | 200 | Installation logic + progress bars |
| `core/config.py` | 548 | All 60 tool definitions |
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
| `sudo python3 reconranger.py --all` | Install all 60 tools with progress bar |
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

Installing 60 tools...
Progress: 100%|████████████████████| 60/60
✓ amass
✓ subfinder
✓ httpx
...     

60/60 installed
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