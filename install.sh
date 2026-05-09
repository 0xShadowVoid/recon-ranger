#!/usr/bin/env bash
# ReconRanger v4.0 — Bootstrap Installer
# Run once to install system dependencies, then use reconranger.py for tools.
set -euo pipefail

VERSION="4.0"
BOLD="\033[1m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

echo -e "${BOLD}ReconRanger v${VERSION} — Bootstrap Installer${RESET}"
echo "=================================================="

# ── Detect package manager ────────────────────────────────────────────────────
install_deps() {
    local pkgs="python3 python3-pip python3-venv golang-go build-essential git curl wget ruby-full cargo rustup"

    if command -v apt-get &>/dev/null; then
        echo -e "${GREEN}[→] apt detected (Debian/Ubuntu/Kali/Parrot)${RESET}"
        apt-get update -qq
        apt-get install -y -q $pkgs
    elif command -v dnf &>/dev/null; then
        echo -e "${GREEN}[→] dnf detected (Fedora/RHEL)${RESET}"
        dnf install -y python3 python3-pip golang git curl wget ruby ruby-devel cargo rust
    elif command -v yum &>/dev/null; then
        echo -e "${GREEN}[→] yum detected (CentOS/RHEL)${RESET}"
        yum install -y python3 python3-pip golang git curl wget ruby ruby-devel cargo rust
    elif command -v pacman &>/dev/null; then
        echo -e "${GREEN}[→] pacman detected (Arch)${RESET}"
        pacman -Syu --noconfirm python python-pip go git curl wget ruby rust
    else
        echo -e "${RED}[!] Unknown distro. Install manually: python3 pip go git ruby cargo${RESET}"
        exit 1
    fi
}

# ── Root check ────────────────────────────────────────────────────────────────
if [[ $EUID -eq 0 ]]; then
    install_deps
else
    echo -e "${YELLOW}[!] Not running as root. Trying sudo…${RESET}"
    sudo bash -c "$(declare -f install_deps); install_deps"
fi

# ── Python deps ───────────────────────────────────────────────────────────────
echo -e "${GREEN}[→] Installing Python dependencies…${RESET}"
python3 -m pip install --upgrade pip --break-system-packages -q
python3 -m pip install --upgrade tqdm requests --break-system-packages -q

# ── Go environment ────────────────────────────────────────────────────────────
echo -e "${GREEN}[→] Configuring Go environment…${RESET}"
GOPATH_LINE='export GOPATH=$HOME/go'
PATH_LINE='export PATH=$PATH:$GOPATH/bin'

for rc in ~/.bashrc ~/.zshrc; do
    [[ -f "$rc" ]] || continue
    grep -q 'GOPATH' "$rc" || echo "$GOPATH_LINE" >> "$rc"
    grep -q 'GOPATH/bin' "$rc" || echo "$PATH_LINE" >> "$rc"
done

mkdir -p ~/go/bin
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# ── Verify Go ─────────────────────────────────────────────────────────────────
if ! command -v go &>/dev/null; then
    echo -e "${RED}[✗] go not found after install. Add it to PATH manually.${RESET}"
else
    echo -e "${GREEN}[✓] go $(go version | awk '{print $3}')${RESET}"
fi

# ── Verify Python ─────────────────────────────────────────────────────────────
echo -e "${GREEN}[✓] python $(python3 --version)${RESET}"

# ── pdtm (optional, ProjectDiscovery tool manager) ────────────────────────────
if command -v go &>/dev/null && ! command -v pdtm &>/dev/null; then
    echo -e "${GREEN}[→] Installing pdtm (ProjectDiscovery Tool Manager)…${RESET}"
    go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest 2>/dev/null || true
fi

echo ""
echo -e "${BOLD}${GREEN}Bootstrap complete!${RESET}"
echo ""
echo "Next steps:"
echo "  python3 reconranger.py -c core       # Install core toolkit (13 tools)"
echo "  python3 reconranger.py --categories  # List all categories"
echo "  python3 reconranger.py --list        # Browse full tool registry"
echo "  python3 reconranger.py --check       # Check what's installed"
echo ""
echo "Docs: docs/README.md | Full stack: docs/BugBounty_CLI_Core-Stack.md"
