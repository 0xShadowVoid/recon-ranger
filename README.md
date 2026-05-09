<div align="center">

# 🦅 ReconRanger

**Bug Bounty CLI Tool Manager — v4.0**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Tools](https://img.shields.io/badge/Tools-76-orange?style=flat-square)](tools.json)
[![Categories](https://img.shields.io/badge/Categories-15-purple?style=flat-square)](tools.json)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square&logo=linux)](https://github.com/0xShadowVoid/recon-ranger)

Install, manage, and organize 76 bug bounty recon tools — by name, category, or full-stack — from a single CLI.

</div>

---

## Features

- Install tools by name, category, or `--install-all`
- Supports `go`, `python`, `apt`, `git`, `ruby`, and `cargo` install types
- Automatic dependency resolution (Go env, pip flags, Ruby gems, Rust/Cargo)
- API key wizard for tools that require tokens (Shodan, GitHub, VT, etc.)
- Live install status check (`--check`)
- Registry management: add, edit, delete tools from `tools.json`
- Real-time alerts via `notify` (Slack / Discord / Telegram)
- 15 categories covering every bug bounty recon phase

---

## Quick Start

```bash
git clone https://github.com/0xShadowVoid/recon-ranger
cd recon-ranger
chmod +x install.sh && sudo ./install.sh   # Install system deps once
python3 reconranger.py -c core             # Install core toolkit
python3 reconranger.py --check             # Verify installs
```

---

## Usage

```
python3 reconranger.py [OPTIONS]

Installation:
  -t, --tools TOOL [TOOL ...]   Install specific tools by name
  -c, --category CAT            Install all tools in a category
  --install-all                 Install every tool in the registry
  --check                       Show installation status for all tools

API Keys:
  --api                         Launch API key configuration wizard
  --apply-keys                  Apply saved keys to tool configs

Registry:
  --add-tool                    Add a new tool interactively
  --edit-tool TOOL              Edit an existing tool entry
  --delete-tool TOOL            Remove a tool from the registry
  -l, --list                    List all tools with category and description
  --categories                  Show all categories and their tool counts

System:
  --fix-deps                    Install / repair system dependencies
```

### Examples

```bash
# Core toolkit — covers 95% of recon workflows
python3 reconranger.py -c core

# Install by category
python3 reconranger.py -c secrets
python3 reconranger.py -c fuzzing
python3 reconranger.py -c js

# Install specific tools
python3 reconranger.py -t subfinder httpx nuclei dalfox

# Full install (all 76 tools)
python3 reconranger.py --install-all

# API key setup (Shodan, GitHub, VirusTotal, etc.)
python3 reconranger.py --api

# Check what's installed
python3 reconranger.py --check

# Edit a tool definition
python3 reconranger.py --edit-tool nuclei

# Add a custom tool
python3 reconranger.py --add-tool
```

---

## Categories

| Category | Count | Purpose |
|----------|-------|---------|
| `core` | 13 | Essential tools for any bug hunt — subdomains, probing, crawling, scanning |
| `subdomains` | 3 | Extended subdomain discovery |
| `ports` | 4 | Port scanning and network mapping |
| `fuzzing` | 5 | Directory, file, and API route discovery |
| `web` | 4 | Parameter discovery and wordlist generation |
| `js` | 5 | JavaScript analysis — endpoints, secrets, links |
| `secrets` | 5 | Secret scanning across code, git history, and live sites |
| `osint` | 5 | Historical URL data, GitHub dorking, OSINT automation |
| `vuln` | 13 | Vulnerability testing — XSS, SQLi, SSRF, CORS, JWT, NoSQL |
| `cloud` | 2 | AWS, Azure, and GCP misconfiguration scanning |
| `takeover` | 2 | Subdomain takeover detection |
| `cms` | 3 | WordPress, Drupal, and generic web server scanning |
| `fingerprinting` | 4 | WAF detection, GraphQL engine ID, screenshots, origin IP |
| `automation` | 2 | Full-pipeline recon automation frameworks |
| `utils` | 7 | Pipeline tools, wordlists, alerting, deduplication |

---

## Tool Table

### Core

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `amass` | go | In-depth attack surface mapping and graph visualization | `amass enum -d target.com -o subs.txt` |
| `assetfinder` | go | Find subdomains from Certificate Transparency logs | `assetfinder --subs-only target.com` |
| `bbot` | python | All-in-one recon framework: subdomains, ports, endpoints, vulns in one run | `bbot -t example.com -m subfinder httpx nuclei` |
| `dnsx` | go | Multi-purpose DNS toolkit for resolution, enumeration, and brute-force | `cat subs.txt | dnsx -a -resp -silent` |
| `ffuf` | go | Fast web fuzzer for directories, files, and parameters | `ffuf -w wordlist.txt -u https://target.com/FUZZ` |
| `gospider` | go | Fast web spider for endpoint and link discovery | `gospider -s https://target.com -o output` |
| `httpx` | go | HTTP probing toolkit: live host detection, status codes, titles, and tech detection | `cat subs.txt | httpx -silent -status-code -title -tech-detect` |
| `katana` | go | Next-gen crawling framework with JavaScript rendering and passive mode | `katana -u https://target.com -depth 3 -js-crawl -silent` |
| `naabu` | go | Fast SYN/CONNECT port scanner built for recon pipelines | `naabu -host target.com -top-ports 1000 -silent` |
| `nuclei` | go | Template-based vulnerability scanner with 9000+ community templates | `cat alive.txt | nuclei -t exposures/ -severity critical,high` |
| `subdomainizer` | git | Find subdomains and secrets buried in JavaScript and external resources | `subdomainizer -u https://target.com -o results.txt` |
| `subfinder` | go | Passive subdomain discovery using 30+ sources including Shodan and VirusTotal | `subfinder -d target.com -silent -all -o subs.txt` |
| `sublist3r` | python | Subdomain enumeration via OSINT: Google, Bing, DNSdumpster, and more | `sublist3r -d target.com -o subs.txt` |

### Subdomains

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `github-subdomains` | go | Find subdomains leaked in GitHub commits and repository content | `github-subdomains -d target.com -t GITHUB_TOKEN` |
| `puredns` | go | Reliable subdomain brute-force with wildcard filtering via massdns | `puredns bruteforce wordlist.txt target.com` |
| `shuffledns` | go | MassDNS wrapper for mass subdomain brute-forcing and resolution | `shuffledns -list subs.txt -d target.com -r resolvers.txt` |

### Ports

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `masscan` | git | Internet-scale port scanner — all 65535 ports in minutes | `masscan -p1-65535 --rate=10000 target.com` |
| `metabigor` | go | Network intelligence: ASN lookup, IP range discovery, and CIDR enumeration | `metabigor net -d target.com` |
| `nmap` | apt | Industry-standard network discovery, port scanning, and service detection | `nmap -sV -sC -p- target.com` |

### Fuzzing

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `dirsearch` | git | Web path discovery by brute-forcing directories and files | `dirsearch -u https://target.com` |
| `feroxbuster` | cargo | Fast, recursive content discovery tool written in Rust | `feroxbuster -u https://target.com -w wordlist.txt --depth 3` |
| `gobuster` | go | Directory, DNS, and vhost brute-forcing tool | `gobuster dir -u https://target.com -w wordlist.txt` |
| `kiterunner` | git | Context-aware API route discovery using real-world API wordlists | `kr scan https://target.com -w routes-small.kite` |

### Web

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `arjun` | python | HTTP parameter discovery suite | `arjun -u https://target.com` |
| `cewl` | apt | Custom wordlist generator built by spidering a target website | `cewl -d 2 -m 8 -w custom.txt https://target.com` |
| `paramspider` | python | Mine parameterised URLs from web archives for fuzzing and injection testing | `paramspider -d target.com` |
| `x8` | cargo | Hidden HTTP parameter discovery written in Rust — fast and precise | `x8 -u https://target.com/ -w wordlist.txt` |

### Js

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `jsecret` | git | Extract API keys and secrets embedded in JavaScript files | `jsecret -u https://target.com` |
| `jsfinder` | git | Extract URLs and subdomains from JavaScript files | `python3 JSFinder.py -u https://target.com` |
| `jsleak` | go | Scan JavaScript files for secrets, endpoints, and sensitive strings | `cat js_urls.txt | jsleak` |
| `jsluice` | go | Extract URLs, paths, and secrets from JavaScript source at scale | `cat js_files.txt | jsluice urls` |
| `linkfinder` | git | Discover hidden endpoints and parameters in JavaScript files | `python3 linkfinder.py -i https://target.com/main.js -o cli` |

### Secrets

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `git-dumper` | python | Dump an exposed .git directory from a web server | `git-dumper https://target.com/.git ./output` |
| `githound` | git | GitHub secrets hunter — scans repos for leaked credentials and keys | `githound --org target-org --keywords api_key,secret` |
| `gitleaks` | go | Scan git repos, files, and directories for hardcoded secrets | `gitleaks detect --source . -v` |
| `secretfinder` | git | Regex-based API key and secret scanner across JavaScript and HTML | `python3 SecretFinder.py -i https://target.com/main.js -o cli` |
| `trufflehog` | go | Deep secret scanning across git history, S3, filesystems, and more | `trufflehog git https://github.com/target/repo --only-verified` |

### Osint

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `gau` | go | Fetch known URLs from AlienVault OTX, Wayback Machine, and Common Crawl | `gau example.com` |
| `github-dorks` | git | GitHub dorking tool to surface sensitive data in public repositories | `github-dorks -u target-org` |
| `jeeves` | git | OSINT automation tool for passive reconnaissance | `python3 jeeves.py -d target.com` |
| `virustotalx` | git | VirusTotal intelligence for domain, IP, URL, and file analysis | `virustotalx -d target.com --api-key VT_KEY` |
| `waybackurls` | go | Fetch all archived URLs for a domain from the Wayback Machine | `echo example.com | waybackurls` |

### Vuln

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `aidor` | git | Automated Insecure Direct Object Reference scanner | `aidor -u https://target.com` |
| `corsy` | git | CORS misconfiguration scanner | `python3 corsy.py -u https://target.com` |
| `cvinder` | git | CVE identifier and vulnerability finder | `cvinder -d target.com` |
| `dalfox` | go | Modern XSS scanner and parameter analyzer | `dalfox url https://target.com` |
| `dotdotpwn` | git | Directory traversal and path traversal fuzzer | `perl dotdotpwn.pl -h https://target.com` |
| `ghauri` | git | Advanced SQL injection detection and exploitation tool | `python3 ghauri.py -u https://target.com` |
| `graphqlmap` | git | GraphQL endpoint enumeration and injection testing | `python3 graphqlmap.py -u https://target.com/graphql` |
| `jwt_tool` | git | Test, tamper, and crack JSON Web Tokens for auth bypass vulnerabilities | `python3 jwt_tool.py <JWT> -T` |
| `metasploit-framework` | git | Full-featured penetration testing and exploitation framework | `msfconsole` |
| `nosqlmap` | git | Automated NoSQL injection and exploitation tool for MongoDB, CouchDB, and Redis | `python3 nosqlmap.py -u https://target.com` |
| `sqlmap` | git | Automated SQL injection detection and database takeover | `sqlmap -u 'https://target.com/search?q=test' --batch --dbs` |
| `ssrfmap` | git | Automatic SSRF detection and exploitation — supports 17 payloads | `python3 ssrfmap.py -r request.txt -p url` |
| `xsstrike` | git | Advanced XSS detection with DOM analysis, fuzzing, and WAF bypass | `python3 xsstrike.py -u 'https://target.com/search?q=test'` |

### Cloud

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `cloud_enum` | python | Multi-cloud OSINT tool for AWS, Azure, and GCP public resource discovery | `cloud_enum -k target -t aws,azure,gcp` |
| `s3scanner` | python | Find and enumerate misconfigured open S3 buckets | `s3scanner scan --bucket target-bucket` |

### Takeover

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `subjack` | git | Subdomain takeover detection across 50+ services | `subjack -w subs.txt -t 100 -timeout 30` |
| `subzy` | go | Fast subdomain takeover checker against 100+ fingerprint signatures | `subzy run --targets subs.txt` |

### Cms

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `droopescan` | python | CMS scanner for Drupal, SilverStripe, WordPress, and Joomla | `droopescan scan drupal -u https://target.com` |
| `nikto` | apt | Web server misconfiguration and known vulnerability scanner | `nikto -h https://target.com` |
| `wpscan` | ruby | WordPress security scanner — themes, plugins, users, and CVEs | `wpscan --url https://target.com --enumerate vp,vt,u` |

### Fingerprinting

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `gowitness` | go | Web screenshot utility for visual recon of live hosts at scale | `gowitness scan file -f alive.txt --screenshot-path ./screens` |
| `graphw00f` | git | GraphQL server engine fingerprinting and detection | `graphw00f -t https://target.com/graphql` |
| `hakoriginfinder` | go | Discover the origin IP address behind CDN and WAF providers | `echo target.com | hakoriginfinder` |
| `wafw00f` | python | WAF detection and fingerprinting — identifies 180+ WAF products | `wafw00f https://target.com` |

### Automation

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `pegpon` | git | Bash-based automation for subdomain enumeration, fuzzing, and web recon | `pegpon -d example.com` |
| `reconftw` | git | Full-cycle recon automation wrapping 35+ tools into one workflow | `./reconftw.sh -d target.com -a` |

### Utils

| Tool | Install Type | Description | Example |
|------|-------------|-------------|---------|
| `anew` | go | Append new unique lines to a file, de-duplicating on the fly | `cat new.txt | anew all.txt` |
| `enumrust` | cargo | Rust-based fast subdomain and host enumeration | `./enumrust target.com` |
| `gf` | go | Grep wrapper with named pattern sets for bug bounty workflows | `cat urls.txt | gf sqli` |
| `interactsh` | go | Out-of-band interaction client for blind SSRF, XXE, and OOB vulnerability detection | `interactsh-client -v` |
| `notify` | go | Stream tool output as real-time alerts to Slack, Discord, or Telegram | `subfinder -d target.com | notify -silent` |
| `seclists` | git | Daniel Miessler's curated wordlist collection for all recon phases | `ffuf -w /opt/seclists/Discovery/Web-Content/common.txt -u https://target.com/FUZZ` |
| `uro` | python | Deduplicate and clean URL lists by stripping redundant parameters | `cat urls.txt | uro` |

---

## API Keys

The following tools require API keys to function fully. Run `python3 reconranger.py --api` to configure them.

| Tool | Key Required | Get It |
|------|-------------|--------|
| `subfinder` | Shodan, Censys, GitHub, VirusTotal | [projectdiscovery/subfinder](https://github.com/projectdiscovery/subfinder/blob/master/v2/README.md#post-installation-instructions) |
| `amass` | Many sources | [owasp-amass/amass](https://github.com/owasp-amass/amass/blob/master/doc/user_guide.md#configuration-file) |
| `github-subdomains` | GitHub Token | [github.com/settings/tokens](https://github.com/settings/tokens) |
| `githound` | GitHub Token | [github.com/settings/tokens](https://github.com/settings/tokens) |
| `virustotalx` | VirusTotal API | [virustotal.com/gui/my-apikey](https://www.virustotal.com/gui/my-apikey) |
| `wpscan` | WPScan Token | [wpscan.com/register](https://wpscan.com/register) |
| `bbot` | Shodan, GitHub, Censys | [bbot docs](https://www.blacklanternsecurity.com/bbot/Scanning/configuration/) |

---

## Typical Bug Bounty Workflow

```bash
# 1. Subdomain enumeration
subfinder -d target.com -silent -all | anew subs.txt
amass enum -d target.com >> subs.txt

# 2. DNS resolution + live host probing
cat subs.txt | dnsx -a -resp -silent | anew resolved.txt
cat resolved.txt | httpx -silent -status-code -title -tech-detect | anew alive.txt

# 3. Port scan live hosts
cat alive.txt | naabu -top-ports 1000 -silent

# 4. Crawl and extract URLs
katana -u https://target.com -depth 3 -js-crawl -silent | anew urls.txt
cat subs.txt | gau | anew urls.txt

# 5. Parameter discovery
cat urls.txt | gf sqli | anew sqli_candidates.txt
cat urls.txt | gf xss  | anew xss_candidates.txt

# 6. Vulnerability scanning
cat alive.txt | nuclei -t exposures/ -t cves/ -severity critical,high

# 7. Targeted testing
dalfox url https://target.com          # XSS
sqlmap -u 'https://target.com?id=1'   # SQLi
python3 corsy.py -u https://target.com # CORS
```

---

## Requirements

- Python 3.8+
- Go 1.21+
- Git
- Ruby (for wpscan)
- Rust/Cargo (for feroxbuster, x8, enumrust)
- Debian/Ubuntu/Kali/Parrot/Arch/Fedora Linux

Run `sudo ./install.sh` to satisfy all system requirements automatically.

---

## File Structure

```
recon-ranger/
├── reconranger.py          # Main CLI entry point
├── install.sh              # One-time system bootstrap
├── tools.json              # Full tool registry (source of truth)
├── requirements.txt        # Python dependencies for reconranger itself
├── core/
│   ├── config.py           # CATEGORIES, TOOL_DEFINITIONS, VERSION
│   ├── installer.py        # go / python / git / apt / ruby / cargo handlers
│   ├── system.py           # System dependency checks
│   ├── keys.py             # API key management
│   └── logger.py           # Logging setup
└── docs/
    ├── TOOLS.md             # Full tool reference table
    ├── BugBounty_CLI_Core-Stack.md  # Curated core stack breakdown
    └── future_features.md   # Roadmap
```

---

## Contributing

1. Fork the repo
2. Add your tool to `tools.json` following the existing schema
3. Add it to the correct category in `core/config.py → CATEGORIES`
4. Open a PR with a short description of the tool and why it belongs

---

## Disclaimer

ReconRanger is for authorized security testing and bug bounty programs only. You are responsible for how you use this tool. Only test targets you have explicit permission to test.

---

<div align="center">

Made by [0xShadowVoid](https://github.com/0xShadowVoid)

</div>
