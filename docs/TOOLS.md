# 🛠️ ReconRanger - Complete Tool Documentation

> **60 professional security tools** organized by category with direct repository links

---

## Core

| Tool | Type | Install | Description |
|---|---|---|---|
| bbot | python | bbot | All-in-one recon framework (replaces 10+ tools; handles subdomains → ports → endpoints → vulns recursively) |
| subfinder | go | github.com/projectdiscovery/subfinder/v2/cmd/subfinder | Fast subdomain discovery using 30+ passive sources |
| sublist3r | python | sublist3r==1.0 | Fast subdomain enumeration using OSINT sources |
| subdomainizer | git | https://github.com/nsonaniya2010/SubDomainizer.git | Find interesting subdomains and secrets in external resources |
| assetfinder | go | github.com/tomnomnom/assetfinder | Find subdomains from Certificate Transparency logs |
| dnsx | go | github.com/projectdiscovery/dnsx/cmd/dnsx | Multi-purpose DNS toolkit for enumeration and resolution |
| httpx | go | github.com/projectdiscovery/httpx/cmd/httpx | HTTP toolkit for probing, fingerprinting, and crawling |
| naabu | go | github.com/projectdiscovery/naabu/v2/cmd/naabu | Fast port scanner for network reconnaissance |
| katana | go | github.com/projectdiscovery/katana/cmd/katana | Next-gen crawling and spidering framework |
| gospider | go | github.com/jaeles-project/gospider | Fast web spider for endpoint discovery |
| ffuf | go | github.com/ffuf/ffuf/v2 | Fast web fuzzer for directory brute-forcing |
| arjun | git | https://github.com/s0md3v/Arjun.git | HTTP parameter discovery suite |
| subzy | go | github.com/PentestPad/subzy | Fast subdomain takeover scanner |
| nuclei | go | github.com/projectdiscovery/nuclei/v3/cmd/nuclei | Fast vulnerability scanner with 10,000+ community templates |
| amass | go | github.com/owasp-amass/amass/v4/cmd/amass | In-depth attack surface mapping with graph visualization |

## Subdomains

| Tool | Type | Install | Description |
|---|---|---|---|
| shuffledns | go | github.com/projectdiscovery/shuffledns/cmd/shuffledns | MassDNS wrapper for subdomain brute-forcing |
| github-subdomains | go | github.com/gwen001/github-subdomains | Find subdomains from GitHub commits and repos |

## Js

| Tool | Type | Install | Description |
|---|---|---|---|
| linkfinder | git | https://github.com/GerbenJavado/LinkFinder.git | Discover hidden endpoints in JavaScript files |
| jsfinder | git | https://github.com/0x240x23elu/jsfinder.git | JavaScript secrets finder |
| jsleak | git | https://github.com/003random/jsleak.git | JavaScript leak scanner |
| jsecret | git | https://github.com/raoufmaklouf/jsecret.git | JavaScript secret and API key finder |
| jsluice | go | github.com/BishopFox/jsluice/cmd/jsluice | JavaScript link extractor |

## Osint

| Tool | Type | Install | Description |
|---|---|---|---|
| gau | go | github.com/lc/gau/v2/cmd/gau | GetAllUrls - URL enumerator from multiple sources |
| waybackurls | go | github.com/tomnomnom/waybackurls | Fetch URLs from Wayback Machine and Common Crawl |
| githound | git | https://github.com/tillson/git-hound.git | GitHub secrets hunter and sensitive data finder |
| github-dorks | git | https://github.com/techgaun/github-dorks.git | GitHub dorking for sensitive data exposure |
| paramspider | git | https://github.com/devanshbatham/ParamSpider.git | Mine parameters from web archives |
| virustotalx | git | https://github.com/ru3y7/virustotalx.git | VirusTotal intelligence tool for domain/IP/URL analysis |
| jeeves | git | https://github.com/ferreiraklet/Jeeves.git | OSINT automation tool for reconnaissance |

## Web

| Tool | Type | Install | Description |
|---|---|---|---|
| kiterunner | git | https://github.com/assetnote/kiterunner.git | Content discovery framework |
| cewl | apt | cewl | Custom wordlist generator from website spidering |

## Vuln

| Tool | Type | Install | Description |
|---|---|---|---|
| xsstrike | git | https://github.com/s0md3v/XSStrike.git | Advanced XSS detection suite |
| dalfox | go | github.com/dalfox/dalfox/v2 | Modern XSS scanner and parameter analyzer |
| sqlmap | git | https://github.com/sqlmapproject/sqlmap.git | Automatic SQL injection and database takeover tool |
| ghauri | git | https://github.com/r0oth3x49/ghauri.git | SQL injection scanner |
| wafw00f | git | https://github.com/EnableSecurity/wafw00f.git | WAF detection and identification |
| graphw00f | git | https://github.com/dolevf/graphw00f.git | GraphQL fingerprinting |
| dotdotpwn | git | https://github.com/wireghoul/dotdotpwn.git | Path traversal fuzzer |
| graphqlmap | git | https://github.com/swisskyrepo/GraphQLmap.git | GraphQL security testing |
| nosqlmap | git | https://github.com/codingo/NoSQLMap.git | NoSQL database injection |
| cvinder | git | https://github.com/3a7/CVINDER.git | CVE identifier and vulnerability finder |
| aidor | git | https://github.com/abdulahadtheCyber-pixel/AIDOR.git | Automated Insecure Direct Object Reference scanner |
| xspear | ruby | XSpear | XSS scanner with Selenium |
| metasploit-framework | git | https://github.com/rapid7/metasploit-framework.git | Complete penetration testing framework |

## Cloud

| Tool | Type | Install | Description |
|---|---|---|---|
| cloud_enum | python | cloud_enum | Multi-cloud OSINT for AWS/Azure/GCP public resources |
| s3scanner | git | https://github.com/sa7mon/S3Scanner.git | AWS S3 bucket scanner |

## Takeover

| Tool | Type | Install | Description |
|---|---|---|---|
| subjack | git | https://github.com/haccer/subjack.git | Subdomain takeover tool |

## Ports

| Tool | Type | Install | Description |
|---|---|---|---|
| masscan | git | https://github.com/robertdavidgraham/masscan.git | High-speed port scanner |
| metabigor | go | github.com/j3ssie/metabigor | Network intelligence for ASN and IP range discovery |

## Cms

| Tool | Type | Install | Description |
|---|---|---|---|
| wpscan | ruby | wpscan | WordPress security scanner |
| droopescan | git | https://github.com/droope/droopescan.git | CMS scanner for Drupal and related platforms |
| nikto | apt | nikto | Web server scanner |

## Utils

| Tool | Type | Install | Description |
|---|---|---|---|
| anew | go | github.com/tomnomnom/anew | Append new lines to files, useful for collecting output |
| gf | go | github.com/tomnomnom/gf | Pattern finder for grep |
| seclists | git | https://github.com/danielmiessler/SecLists.git | Collection of security wordlists |
| interactsh | go | github.com/projectdiscovery/interactsh/cmd/interactsh-client | Out-of-band interaction client for blind testing |
| reconftw | git | https://github.com/six2dez/reconftw.git | Automated recon framework |
| uro | go | github.com/s0md3v/uro | URL recon tool |
| enumrust | cargo | https://github.com/KingOfBugbounty/enumrust.git | Rust-based enumeration tool |
| dirsearch | git | https://github.com/maurosoria/dirsearch.git | Directory brute-forcing |
