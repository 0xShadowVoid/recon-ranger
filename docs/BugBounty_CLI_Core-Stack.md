# 0xShadowVoid — Bug Bounty CLI Stack 2026

---

## PASSIVE RECON

### bbot
- **Repo:** https://github.com/blacklanternsecurity/bbot
```bash
pip install bbot
```

### subfinder
- **Repo:** https://github.com/projectdiscovery/subfinder
```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### gau
- **Repo:** https://github.com/lc/gau
```bash
go install github.com/lc/gau/v2/cmd/gau@latest
```

---

## DNS RESOLUTION

### dnsx
- **Repo:** https://github.com/projectdiscovery/dnsx
```bash
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
```

### puredns
- **Repo:** https://github.com/d3mondev/puredns
```bash
go install github.com/d3mondev/puredns/v2@latest
```

---

## LIVE HOST PROBING

### httpx
- **Repo:** https://github.com/projectdiscovery/httpx
```bash
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### naabu
- **Repo:** https://github.com/projectdiscovery/naabu
```bash
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
```

### nmap
- **Repo:** https://github.com/nmap/nmap
```bash
sudo apt install nmap -y
```

---

## CRAWLING

### katana
- **Repo:** https://github.com/projectdiscovery/katana
```bash
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

### gospider
- **Repo:** https://github.com/jaeles-project/gospider
```bash
go install github.com/jaeles-project/gospider@latest
```

---

## FUZZING

### ffuf
- **Repo:** https://github.com/ffuf/ffuf
```bash
go install github.com/ffuf/ffuf/v2@latest
```

### feroxbuster
- **Repo:** https://github.com/epi052/feroxbuster
```bash
curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh | bash
# or
cargo install feroxbuster
```

### kiterunner
- **Repo:** https://github.com/assetnote/kiterunner
```bash
git clone https://github.com/assetnote/kiterunner.git
cd kiterunner
make build
sudo mv dist/kr /usr/local/bin/
```

---

## DIR DISCOVERY

### dirsearch
- **Repo:** https://github.com/maurosoria/dirsearch
```bash
pip install dirsearch
```

### GoBuster
- **Repo:** https://github.com/OJ/gobuster
```bash
go install github.com/OJ/gobuster/v3@latest
```

---

## PARAMETER DISCOVERY

### arjun
- **Repo:** https://github.com/s0md3v/Arjun
```bash
pip install arjun
```

### gf
- **Repo:** https://github.com/tomnomnom/gf
```bash
go install github.com/tomnomnom/gf@latest
# Install patterns
git clone https://github.com/tomnomnom/gf.git
cp -r gf/examples ~/.gf
# Extended patterns (recommended)
git clone https://github.com/1ndianl33t/Gf-Patterns ~/.gf-patterns
cp ~/.gf-patterns/*.json ~/.gf/
```

### ParamSpider
- **Repo:** https://github.com/devanshbatham/ParamSpider
```bash
pip install paramspider
```

---

## JS / SECRETS

### SecretFinder
- **Repo:** https://github.com/m4ll0k/SecretFinder
```bash
git clone https://github.com/m4ll0k/SecretFinder.git
cd SecretFinder
pip install -r requirements.txt
```

### LinkFinder
- **Repo:** https://github.com/GerbenJavado/LinkFinder
```bash
git clone https://github.com/GerbenJavado/LinkFinder.git
cd LinkFinder
pip install -r requirements.txt
python setup.py install
```

### jsluice
- **Repo:** https://github.com/BishopFox/jsluice
```bash
go install github.com/BishopFox/jsluice/cmd/jsluice@latest
```

### retire.js
- **Repo:** https://github.com/RetireJS/retire.js
```bash
npm install -g retire
```

### Gitleaks
- **Repo:** https://github.com/gitleaks/gitleaks
```bash
go install github.com/gitleaks/gitleaks/v8@latest
```

### truffleHog
- **Repo:** https://github.com/trufflesecurity/trufflehog
```bash
pip install trufflehog
# or binary
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
```

---

## GIT EXPOSURE

### git-dumper
- **Repo:** https://github.com/arthaud/git-dumper
```bash
pip install git-dumper
```

---

## ORIGIN IP

### hakoriginfinder
- **Repo:** https://github.com/hakluke/hakoriginfinder
```bash
go install github.com/hakluke/hakoriginfinder@latest
```

### CloudRip
- **Repo:** https://github.com/staxsum/CloudRip
```bash
git clone https://github.com/staxsum/CloudRip.git
cd CloudRip
pip install -r requirements.txt
```

---

## FINGERPRINTING

### wafw00f
- **Repo:** https://github.com/EnableSecurity/wafw00f
```bash
pip install wafw00f
```

### graphw00f
- **Repo:** https://github.com/dolevf/graphw00f
```bash
git clone https://github.com/dolevf/graphw00f.git
cd graphw00f
pip install -r requirements.txt
```

---

## VISUALIZATION

### GoWitness
- **Repo:** https://github.com/sensepost/gowitness
```bash
go install github.com/sensepost/gowitness@latest
```

---

## SCANNING

### nuclei
- **Repo:** https://github.com/projectdiscovery/nuclei
```bash
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
# Pull templates after install
nuclei -update-templates
```

---

## OOB INFRA

### Interactsh
- **Repo:** https://github.com/projectdiscovery/interactsh
```bash
go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
# Use projectdiscovery hosted server (no self-host needed)
interactsh-client
```

---

## EXPLOITATION

### sqlmap
- **Repo:** https://github.com/sqlmapproject/sqlmap
```bash
sudo apt install sqlmap -y
# or latest from source
git clone https://github.com/sqlmapproject/sqlmap.git
```

### SSRFmap
- **Repo:** https://github.com/swisskyrepo/SSRFmap
```bash
git clone https://github.com/swisskyrepo/SSRFmap.git
cd SSRFmap
pip install -r requirements.txt
```

---

## XSS

### Dalfox
- **Repo:** https://github.com/hahwul/dalfox
```bash
go install github.com/hahwul/dalfox/v2@latest
```

---

## JWT

### jwt_tool
- **Repo:** https://github.com/ticarpi/jwt_tool
```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
pip install -r requirements.txt
chmod +x jwt_tool.py
```

---

## CORS

### Corsy
- **Repo:** https://github.com/s0md3v/Corsy
```bash
git clone https://github.com/s0md3v/Corsy.git
cd Corsy
pip install -r requirements.txt
```

---

## TAKEOVER

### subzy
- **Repo:** https://github.com/PentestPad/subzy
```bash
go install github.com/PentestPad/subzy@latest
```

---

## PIPELINE UTILS

### jq
- **Repo:** https://github.com/jqlang/jq
```bash
sudo apt install jq -y
```

### anew
- **Repo:** https://github.com/tomnomnom/anew
```bash
go install github.com/tomnomnom/anew@latest
```

### notify
- **Repo:** https://github.com/projectdiscovery/notify
```bash
go install github.com/projectdiscovery/notify/cmd/notify@latest
# Configure provider (Slack/Discord/Telegram) in ~/.config/notify/provider-config.yaml
```

### uro
- **Repo:** https://github.com/s0md3v/uro
```bash
pip install uro
```

---

## GO PATH SETUP (required for all Go tools)

```bash
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
source ~/.bashrc
```

---

*Stack: 0xShadowVoid — 2026*

