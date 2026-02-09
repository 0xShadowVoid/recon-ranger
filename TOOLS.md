# 🛠️ ReconRanger - Complete Tool Documentation

> **61 professional security tools** organized by category with direct repository links

---

## 📂 Installation Commands

```bash
# Install all tools
sudo python reconranger.py --all

# Install by category
sudo python reconranger.py -c recon
sudo python reconranger.py -c dns
sudo python reconranger.py -c http

# Install specific tools
sudo python reconranger.py -t subfinder amass nuclei

# List categories
python reconranger.py --categories

# List all tools
python reconranger.py --list

# Show repository links
python reconranger.py --links
```

---

## 🌐 Recon & Subdomain Enumeration (7)

| Tool | Description | Repository |
|-------|-------------|------------|
| **amass** | In-depth attack surface mapping | [owasp-amass/amass](https://github.com/owasp-amass/amass) |
| **subfinder** | Fast subdomain discovery (30+ sources) | [projectdiscovery/subfinder](https://github.com/projectdiscovery/subfinder) |
| **assetfinder** | Certificate Transparency subdomains | [tomnomnom/assetfinder](https://github.com/tomnomnom/assetfinder) |
| **sublist3r** | OSINT-based subdomain enumeration | [aboul3la/Sublist3r](https://github.com/aboul3la/Sublist3r) |
| **subdomainizer** | Find subdomains in external resources | [nsonaniya2010/SubDomainizer](https://github.com/nsonaniya2010/SubDomainizer) |
| **github-subdomains** | GitHub commits/repos subdomains | [gwen001/github-subdomains](https://github.com/gwen001/github-subdomains) |
| **bbot** | Recursive internet scanner | [blacklanternsecurity/bbot](https://github.com/blacklanternsecurity/bbot) |

---

## 📡 DNS & Network Scanning (4)

| Tool | Description | Repository |
|-------|-------------|------------|
| **dnsx** | Multi-purpose DNS toolkit | [projectdiscovery/dnsx](https://github.com/projectdiscovery/dnsx) |
| **shuffledns** | MassDNS wrapper for brute-forcing | [projectdiscovery/shuffledns](https://github.com/projectdiscovery/shuffledns) |
| **masscan** | High-speed port scanner | [robertdavidgraham/masscan](https://github.com/robertdavidgraham/masscan) |
| **naabu** | Fast port scanner for recon | [projectdiscovery/naabu](https://github.com/projectdiscovery/naabu) |

---

## 🔍 HTTP Probing & Fingerprinting (3)

| Tool | Description | Repository |
|-------|-------------|------------|
| **httpx** | HTTP probing and fingerprinting | [projectdiscovery/httpx](https://github.com/projectdiscovery/httpx) |
| **wafw00f** | WAF detection and identification | [EnableSecurity/wafw00f](https://github.com/EnableSecurity/wafw00f) |
| **graphw00f** | GraphQL fingerprinting | [dolevf/graphw00f](https://github.com/dolevf/graphw00f) |

---

## 🕷️ Crawling & JavaScript Analysis (6)

| Tool | Description | Repository |
|-------|-------------|------------|
| **katana** | Next-gen web crawler | [projectdiscovery/katana](https://github.com/projectdiscovery/katana) |
| **gospider** | Fast web spider | [jaeles-project/gospider](https://github.com/jaeles-project/gospider) |
| **linkfinder** | JavaScript endpoint discovery | [GerbenJavado/LinkFinder](https://github.com/GerbenJavado/LinkFinder) |
| **jsfinder** | JavaScript secrets finder | [0x240x23elu/jsfinder](https://github.com/0x240x23elu/jsfinder) |
| **jsluice** | JavaScript link extractor | [BishopFox/jsluice](https://github.com/BishopFox/jsluice) |
| **jsleak** | JavaScript leak scanner | [003random/jsleak](https://github.com/003random/jsleak) |

---

## 🔓 Content Discovery & Fuzzing (4)

| Tool | Description | Repository |
|-------|-------------|------------|
| **ffuf** | Fast web fuzzer | [ffuf/ffuf](https://github.com/ffuf/ffuf) |
| **dirsearch** | Directory brute-forcing | [maurosoria/dirsearch](https://github.com/maurosoria/dirsearch) |
| **kiterunner** | Content discovery framework | [assetnote/kiterunner](https://github.com/assetnote/kiterunner) |
| **cewl** | Custom wordlist generator | [digininja/CeWL](https://github.com/digininja/CeWL) |

---

## 🔑 Parameter Discovery (2)

| Tool | Description | Repository |
|-------|-------------|------------|
| **arjun** | HTTP parameter discovery | [s0md3v/Arjun](https://github.com/s0md3v/Arjun) |
| **paramspider** | Parameter mining from archives | [devanshbatham/ParamSpider](https://github.com/devanshbatham/ParamSpider) |

---

## 💉 XSS Scanners (3)

| Tool | Description | Repository |
|-------|-------------|------------|
| **xsstrike** | Advanced XSS detection | [s0md3v/XSStrike](https://github.com/s0md3v/XSStrike) |
| **dalfox** | Modern XSS scanner | [dalfox/dalfox](https://github.com/dalfox/dalfox) |
| **xspear** | XSS scanner with Selenium | [hahwul/XSpear](https://github.com/hahwul/XSpear) |

---

## 🧪 Vulnerability Scanners (2)

| Tool | Description | Repository |
|-------|-------------|------------|
| **nuclei** | Fast vulnerability scanner (10k+ templates) | [projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei) |
| **nikto** | Web server scanner | [sullo/nikto](https://github.com/sullo/nikto) |

---

## 💥 Exploitation Framework (1)

| Tool | Description | Repository |
|-------|-------------|------------|
| **metasploit-framework** | Complete penetration testing framework | [rapid7/metasploit-framework](https://github.com/rapid7/metasploit-framework) |

---

## 📦 Specialized Attack Tools

### SQL/NoSQL Injection (3)

| Tool | Description | Repository |
|-------|-------------|------------|
| **sqlmap** | Automatic SQL injection tool | [sqlmapproject/sqlmap](https://github.com/sqlmapproject/sqlmap) |
| **ghauri** | SQL injection scanner | [r0oth3x49/ghauri](https://github.com/r0oth3x49/ghauri) |
| **nosqlmap** | NoSQL database injection | [codingo/NoSQLMap](https://github.com/codingo/NoSQLMap) |

### GraphQL (2)

| Tool | Description | Repository |
|-------|-------------|------------|
| **graphqlmap** | GraphQL security testing | [swisskyrepo/GraphQLmap](https://github.com/swisskyrepo/GraphQLmap) |
| **graphw00f** | GraphQL fingerprinting | [dolevf/graphw00f](https://github.com/dolevf/graphw00f) |

### Directory Traversal (1)

| Tool | Description | Repository |
|-------|-------------|------------|
| **dotdotpwn** | Path traversal fuzzer | [wireghoul/dotdotpwn](https://github.com/wireghoul/dotdotpwn) |

### Cloud Buckets (2)

| Tool | Description | Repository |
|-------|-------------|------------|
| **s3scanner** | AWS S3 bucket scanner | [sa7mon/S3Scanner](https://github.com/sa7mon/S3Scanner) |
| **cloud_enum** | Multi-cloud resource enumeration | [initstring/cloud_enum](https://github.com/initstring/cloud_enum) |

### CMS Scanners (2)

| Tool | Description | Repository |
|-------|-------------|------------|
| **wpscan** | WordPress security scanner | [wpscanteam/wpscan](https://github.com/wpscanteam/wpscan) |
| **droopescan** | CMS scanner (Drupal, Joomla, etc.) | [droope/droopescan](https://github.com/droope/droopescan) |

---

## 🌍 Subdomain Takeover (3)

| Tool | Description | Repository |
|-------|-------------|------------|
| **subjack** | Subdomain takeover detection | [haccer/subjack](https://github.com/haccer/subjack) |
| **subzy** | Fast subdomain takeover scanner | [LukaSikic/subzy](https://github.com/LukaSikic/subzy) |
| **subover** | Subdomain takeover tool | [Ice3man543/SubOver](https://github.com/Ice3man543/SubOver) |

---

## 🔎 OSINT & GitHub Hunting (5)

| Tool | Description | Repository |
|-------|-------------|------------|
| **github-dorks** | GitHub sensitive data finder | [techgaun/github-dorks](https://github.com/techgaun/github-dorks) |
| **githound** | GitHub secrets hunter | [tillson/git-hound](https://github.com/tillson/git-hound) |
| **jsecret** | JavaScript secret finder | [raoufmaklouf/jsecret](https://github.com/raoufmaklouf/jsecret) |
| **virustotalx** | VirusTotal intelligence tool | [ru3y7/virustotalx](https://github.com/ru3y7/virustotalx) |
| **metabigor** | Network intelligence tool | [j3ssie/metabigor](https://github.com/j3ssie/metabigor) |

---

## 🧰 Utilities & Helpers (7)

| Tool | Description | Repository |
|-------|-------------|------------|
| **waybackurls** | URL fetcher from archives | [tomnomnom/waybackurls](https://github.com/tomnomnom/waybackurls) |
| **gau** | GetAllUrls enumerator | [lc/gau](https://github.com/lc/gau) |
| **anew** | Append new lines to files | [tomnomnom/anew](https://github.com/tomnomnom/anew) |
| **interactsh** | Out-of-band interaction client | [projectdiscovery/interactsh](https://github.com/projectdiscovery/interactsh) |
| **gf** | Pattern finder for grep | [tomnomnom/gf](https://github.com/tomnomnom/gf) |
| **uro** | URL recon tool | [s0md3v/uro](https://github.com/s0md3v/uro) |
| **seclists** | Collection of security wordlists | [danielmiessler/SecLists](https://github.com/danielmiessler/SecLists) |

---

## 🤖 Automation Frameworks (5)

| Tool | Description | Repository |
|-------|-------------|------------|
| **reconftw** | Automated recon framework | [six2dez/reconftw](https://github.com/six2dez/reconftw) |
| **aidor** | IDOR automation scanner | [abdulahadtheCyber-pixel/AIDOR](https://github.com/abdulahadtheCyber-pixel/AIDOR) |
| **enumrust** | Rust-based enumeration tool | [KingOfBugbounty/enumrust](https://github.com/KingOfBugbounty/enumrust) |
| **cvinder** | CVE identifier and finder | [3a7/CVINDER](https://github.com/3a7/CVINDER) |
| **jeeves** | OSINT automation tool | [ferreiraklet/Jeeves](https://github.com/ferreiraklet/Jeeves) |

---

## 📊 Summary

- **Total Tools**: 61
- **Categories**: 18
- **Languages**: Go, Python, Ruby, Rust, Perl, Shell
- **Installation Methods**: go install, git clone, pip install, apt install, gem install, cargo build

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ShadowVoid-King/Recon-Ranger
cd Recon-Ranger

# Install all tools
sudo python reconranger.py --all

# Or install by category
sudo python reconranger.py -c recon
sudo python reconranger.py -c vuln
sudo python reconranger.py -c xss
```

---

*Last updated: February 2026*
