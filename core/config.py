"""Tool configuration - minimal, validated"""
from typing import Dict, Any, Optional

# Only essential fields required
TOOL_SCHEMA = {
    "type": str,
    "binary": str,
    "description": str,
}

# All 20 recon tools - kept simple
TOOL_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "amass": {
        "type": "go",
        "package": "github.com/owasp-amass/amass/v4/cmd/amass",
        "binary": "amass",
        "apt": "amass",
        "description": "In-depth attack surface mapping with graph visualization",
        "example": "amass enum -d target.com -o subs.txt",
    },
    "subfinder": {
        "type": "go",
        "package": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder",
        "binary": "subfinder",
        "apt": "subfinder",
        "description": "Fast subdomain discovery using 30+ passive sources",
        "example": "subfinder -d target.com -silent -o subs.txt",
    },
    "httpx": {
        "type": "go",
        "package": "github.com/projectdiscovery/httpx/cmd/httpx",
        "binary": "httpx",
        "apt": "httpx",
        "description": "HTTP toolkit for probing, fingerprinting, and crawling",
        "example": "cat subs.txt | httpx -silent -status-code",
    },
    "dnsx": {
        "type": "go",
        "package": "github.com/projectdiscovery/dnsx/cmd/dnsx",
        "binary": "dnsx",
        "apt": "dnsx",
        "description": "Multi-purpose DNS toolkit for enumeration and resolution",
        "example": "cat subs.txt | dnsx -a -resp -silent",
    },
    "nuclei": {
        "type": "go",
        "package": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei",
        "binary": "nuclei",
        "apt": "nuclei",
        "description": "Fast vulnerability scanner with 10,000+ community templates",
        "post_install": "nuclei -ut -silent",
        "example": "cat alive.txt | nuclei -t exposures/ -severity critical,high",
    },
    "katana": {
        "type": "go",
        "package": "github.com/projectdiscovery/katana/cmd/katana",
        "binary": "katana",
        "apt": "katana",
        "description": "Next-gen crawling and spidering framework",
        "example": "katana -u https://target.com -silent -depth 3 -js-crawl",
    },
    "ffuf": {
        "type": "go",
        "package": "github.com/ffuf/ffuf/v2",
        "binary": "ffuf",
        "apt": "ffuf",
        "description": "Fast web fuzzer for directory brute-forcing",
        "example": "ffuf -w wordlist.txt -u https://target.com/FUZZ",
    },
    "gospider": {
        "type": "go",
        "package": "github.com/jaeles-project/gospider",
        "binary": "gospider",
        "apt": None,
        "description": "Fast web spider for endpoint discovery",
        "example": "gospider -s https://target.com -o output",
    },
    "assetfinder": {
        "type": "go",
        "package": "github.com/tomnomnom/assetfinder",
        "binary": "assetfinder",
        "apt": None,
        "description": "Find subdomains from Certificate Transparency logs",
        "example": "assetfinder --subs-only target.com",
    },
    "shuffledns": {
        "type": "go",
        "package": "github.com/projectdiscovery/shuffledns/cmd/shuffledns",
        "binary": "shuffledns",
        "apt": "shuffledns",
        "description": "MassDNS wrapper for subdomain brute-forcing",
        "example": "shuffledns -list subs.txt -d target.com -r resolvers.txt",
    },
    "naabu": {
        "type": "go",
        "package": "github.com/projectdiscovery/naabu/v2/cmd/naabu",
        "binary": "naabu",
        "apt": "naabu",
        "description": "Fast port scanner for network reconnaissance",
        "example": "naabu -host target.com -p 80,443,8080,8443",
    },
    "metabigor": {
        "type": "go",
        "package": "github.com/j3ssie/metabigor",
        "binary": "metabigor",
        "apt": None,
        "description": "Network intelligence for ASN and IP range discovery",
        "example": "metabigor net -d target.com",
    },
    "sublist3r": {
        "type": "python",
        "package": "sublist3r==1.2.1",
        "binary": "sublist3r",
        "apt": None,
        "description": "Fast subdomain enumeration using OSINT sources",
        "example": "sublist3r -d target.com -o subs.txt",
    },
    "cewl": {
        "type": "apt",
        "package": "cewl",
        "binary": "cewl",
        "apt": "cewl",
        "description": "Custom wordlist generator from website spidering",
        "example": "cewl -d 2 -m 8 -w custom.txt https://target.com",
    },
    "subdomainizer": {
        "type": "git",
        "repo": "https://github.com/nsonaniya2010/SubDomainizer.git",
        "path": "/opt/SubDomainizer",
        "binary": "subdomainizer",
        "entrypoint": "/opt/SubDomainizer/SubDomainizer.py",
        "requirements": ["-r", "/opt/SubDomainizer/requirements.txt"],
        "description": "Find interesting subdomains and secrets in external resources",
        "example": "subdomainizer -u https://target.com -o results.txt",
    },
    "linkfinder": {
        "type": "git",
        "repo": "https://github.com/GerbenJavado/LinkFinder.git",
        "path": "/opt/LinkFinder",
        "binary": "linkfinder",
        "entrypoint": "/opt/LinkFinder/linkfinder.py",
        "requirements": ["-r", "/opt/LinkFinder/requirements.txt"],
        "post_clone": "npm install --silent",
        "description": "Discover hidden endpoints in JavaScript files",
        "example": "linkfinder -i https://target.com/main.js -o cli",
    },
    "cloud_enum": {
        "type": "python",
        "package": "cloud_enum",
        "binary": "cloud_enum",
        "apt": None,
        "description": "Multi-cloud OSINT for AWS/Azure/GCP public resources",
        "example": "cloud_enum -k target -t aws,azure,gcp",
    },
    "githound": {
        "type": "git",
        "repo": "https://github.com/twelvesec/githound.git",
        "path": "/opt/githound",
        "binary": "githound",
        "build_cmd": "go build -o githound .",
        "description": "GitHub secrets hunter and sensitive data finder",
        "example": "githound --org target-org --keywords api_key,password",
    },
    "virustotalx": {
        "type": "git",
        "repo": "https://github.com/orwagodfather/virustotalx.git",
        "path": "/opt/virustotalx",
        "binary": "virustotalx",
        "entrypoint": "/opt/virustotalx/virustotalx.py",
        "requirements": ["selenium", "requests", "beautifulsoup4", "colorama", "webdriver-manager"],
        "description": "VirusTotal intelligence tool for domain/IP/URL analysis",
        "example": "virustotalx -d target.com --api-key YOUR_VT_KEY",
    },
}

def get_tool(name: str) -> Optional[Dict[str, Any]]:
    """Get tool config by name"""
    return TOOL_DEFINITIONS.get(name)

def list_tools() -> list:
    """List all tool names"""
    return list(TOOL_DEFINITIONS.keys())