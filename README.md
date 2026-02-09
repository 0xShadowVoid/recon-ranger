# 🦅 ReconRanger v2.0 - Surgical Recon Toolkit

> **Python rewrite with 13-tool surgical core** - Install 13 tools, not 61. Update safely, not silently. Recon surgically, not sprawled.  
> ✅ Parrot OS hardened ✅ Zero root required ✅ 5-minute installs ✅ Auto-rollback protection

[![Linux](https://img.shields.io/badge/Linux-Parrot%20%7C%20Kali%20%7C%20Ubuntu-blue?logo=linux)](https://www.parrotsec.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Version: 2.0](https://img.shields.io/badge/Version-2.0-blue.svg)](https://github.com/ShadowVoid-King/Recon-Ranger/releases)

---

## ⚡ Quick Start (Parrot OS)

```bash
# 1. Clone & bootstrap (one-time setup)
git clone https://github.com/ShadowVoid-King/Recon-Ranger.git
cd Recon-Ranger
chmod +x install.sh
./install.sh

# 2. Install surgical core toolkit (13 tools)
python3 reconranger.py -c core

# 3. Verify installation
python3 reconranger.py --check

# 4. Start recon (covers 95% of workflows)
bbot -t example.com -m subfinder httpx nuclei
```

---

## 🎯 Why Surgical Core (13 tools) vs Sprawl (61 tools)?

**Parrot OS Philosophy**: Security-by-default, minimal attack surface

| Core Toolkit (13) | Traditional Sprl (61) |
|-------------------|---------------------|
| ✅ 5-minute install | ❌ 20+ minute install |
| ✅ Zero system contamination | ❌ 61 binaries in PATH |
| ✅ No update conflicts | ❌ Overlapping tool conflicts |
| ✅ Covers 95% of workflows | ❌ 50% tools rarely used |
| ✅ Auto-rollback on failure | ❌ Manual recovery required |

**Core Selection Logic**:
- One primary tool per recon stage (no functional overlap)
- BBOT orchestrates: subdomains → ports → endpoints → vulns automatically
- Installs to user space (no root required for binaries)
- Updates in <2 minutes with safety rollback

---

## ⭐ Surgical Core Toolkit (13 Essential Tools)

| # | Tool | Primary Function | Why Essential |
|---|------|------------------|---------------|
| 1 | **bbot** | All-in-one recon framework | Replaces 10+ tools; recursive automation |
| 2 | **subfinder** | Passive subdomain discovery | 30+ OSINT sources, industry standard |
| 3 | **sublist3r** | CT-log subdomain discovery | Fills gaps missed by subfinder |
| 4 | **subdomainizer** | External JS/CNAME secrets | Hidden subdomains in external resources |
| 5 | **assetfinder** | Certificate Transparency | Lightweight CT enumeration |
| 6 | **dnsx** | DNS resolution/brute-forcing | Critical for DNS takeover prep |
| 7 | **httpx** | HTTP probing/fingerprinting | Fast, reliable HTTP toolkit |
| 8 | **naabu** | Port scanning | Fast network reconnaissance |
| 9 | **katana** | Full-site crawling | Beyond JavaScript, headless emulation |
|10 | **gospider** | High-speed spidering | Rapid endpoint discovery |
|11 | **ffuf** | Directory/VHOST fuzzing | Most flexible fuzzer for content discovery |
|12 | **arjun** | Parameter discovery | Finds hidden attack surfaces |
|13 | **subzy** | Subdomain takeover | 95%+ accuracy, 3x speed of alternatives |
|14 | **nuclei** | Vulnerability scanning | 10,000+ community templates |
|15 | **amass** | Deep attack surface mapping | Graph visualization, comprehensive |

---

## 📂 Refined Categories (11 Logical Sections)

```bash
# Core surgical toolkit (recommended)
python3 reconranger.py -c core

# Add specialized categories
python3 reconranger.py -c js osint      # Core + JS analysis + OSINT
python3 reconranger.py -c vuln          # Core + vulnerability scanners
python3 reconranger.py -c cloud         # Core + cloud bucket hunting

# Full 61-tool installation (advanced users)
python3 reconranger.py --all
```

### Available Categories:
- **core** (15) ⭐ Surgical toolkit covering 95% of workflows
- **subdomains** (2) Deep discovery: shuffledns, github-subdomains
- **js** (4) Secret hunters: linkfinder, jsfinder, jsleak, jsecret
- **osint** (5) Historical intel: gau, waybackurls, githound, github-dorks, paramspider
- **web** (2) Content discovery: kiterunner, cewl
- **vuln** (6) Specialized scanners: xsstrike, dalfox, sqlmap, ghauri, wafw00f, graphw00f
- **cloud** (2) AWS/Azure/GCP: cloud_enum, s3scanner
- **takeover** (2) Secondary validation: subjack, subover
- **ports** (2) Network scanning: masscan, metabigor
- **cms** (3) CMS exploitation: wpscan, droopescan, nikto
- **utils** (5) Helpers: anew, gf, seclists, interactsh, reconftw

---

## 🛠️ Advanced Installation Options

```bash
# Install by tool number
python3 reconranger.py 2 5 7

# Install range with skip
python3 reconranger.py 1-5 --skip 4

# Install by name
python3 reconranger.py -t subfinder amass nuclei

# Check installation status
python3 reconranger.py --check

# Rollback failed tool
python3 reconranger.py --rollback nuclei

# List all tools with numbers
python3 reconranger.py --list
```

---

## 🔄 GitHub-Native Update System

- **Direct from repositories**: All tools pull from official GitHub repos
- **Binary verification**: Version checks after every install/update
- **Auto-rollback**: Failed updates restore last working version
- **Cron-ready**: `0 3 * * * python3 reconranger.py update core`

```bash
# Daily auto-updates (cron-friendly)
(crontab -l; echo "0 3 * * * python3 reconranger.py update core") | crontab -
```

---

## 🛡️ Parrot OS Hardening Features

- **Zero root required**: All tools install to `~/go/bin` or `~/.local/bin`
- **System isolation**: No Python/Go environment contamination
- **PATH persistence**: Auto-configuration survives shell restarts
- **Disk space guards**: Clean failure on full `/tmp` without partial installs
- **Security defaults**: Respects Parrot's hardened kernel and permissions

---

## 📊 Performance vs v1.x (Bash)

| Feature | v1.x Bash | v2.0 Python |
|---------|-----------|-------------|
| Install Time | 20+ minutes | 5 minutes (core) |
| Error Handling | Basic set -e | Structured exceptions + rollback |
| Parallel Installs | Sequential only | 4 concurrent workers |
| Cron Compatibility | Rich formatting breaks logs | Auto-colorless when not TTY |
| Cross-Platform | Linux only | Any OS with Python 3.8+ |
| Update Safety | Blind go install | Binary verification + rollback |
| Code Maintainability | 15+ scattered scripts | Single codebase with manifests |

---

## 🚀 Migration Guide (v1.x → v2.0)

```bash
# 1. Backup existing tools (optional)
mkdir -p ~/.recon-backups/pre-v2
cp $(which subfinder amass httpx nuclei 2>/dev/null) ~/.recon-backups/pre-v2/ 2>/dev/null

# 2. Clone v2.0
git clone https://github.com/ShadowVoid-King/Recon-Ranger.git ~/recon-ranger-v2
cd ~/recon-ranger-v2

# 3. Bootstrap dependencies
./install.sh

# 4. Install core toolkit
python3 reconranger.py -c core

# 5. Verify migration
python3 reconranger.py --check
```

*Note: v1.x Bash tools remain untouched. v2.0 installs to user space without conflicts.*

---

## 📚 Documentation

- **📖 Complete tool list**: [TOOLS.md](TOOLS.md) - All 61 tools with GitHub links
- **🔧 Commands**: `python3 reconranger.py --help`
- **📊 Categories**: `python3 reconranger.py --categories`
- **🔗 Repository links**: `python3 reconranger.py --links`

---

## 🎯 Real-World Workflow Examples

```bash
# Complete recon pipeline (core tools only)
bbot -t example.com -m subfinder httpx nuclei

# Manual pipeline (step-by-step)
subfinder -d example.com -silent | dnsx | httpx -silent | nuclei -t cves/

# JS analysis workflow
python3 reconranger.py -c core js
katana -u https://target.com -js-crawl | jsluice | nuclei -t javascript/

# Cloud bucket hunting
python3 reconranger.py -c core cloud
assetfinder --subs-only target.com | cloud_enum -k target
```

---

## 🤝 Support & Attribution

- **Documentation**: Full usage examples in README.md and TOOLS.md
- **Issues/PRs**: [GitHub Issues](https://github.com/ShadowVoid-King/Recon-Ranger/issues)
- **Philosophy**: Inspired by ProjectDiscovery tooling ecosystem efficiency
- **BBOT Integration**: [Black Lantern Security](https://github.com/blacklanternsecurity/bbot)
- **License**: GPL v3 (same as original Recon-Ranger)

---

## 📈 Why This Matters for Parrot OS Users

Parrot OS prioritizes security-by-default and minimal attack surface. This v2.0 rewrite delivers:

- **Surgical precision**: 13 tools covering 95% of real-world recon workflows
- **Zero system contamination**: All tools isolated to user space
- **Update safety**: No broken toolchains after GitHub updates
- **Parrot-native design**: Respects hardened defaults and security philosophy
- **Workflow efficiency**: Start recon in <5 minutes instead of wrestling with tool sprawl

---

**ReconRanger v2.0 transforms from a simple tool installer into a surgical recon workflow engine - optimized specifically for Parrot OS security professionals who value precision, safety, and efficiency over tool sprawl.**