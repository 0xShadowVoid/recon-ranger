#!/usr/bin/env bash
# ReconRanger v4.0 — Bootstrap Installer
# Tested on: Kali, Parrot, Ubuntu, Debian, Arch, Fedora
set -euo pipefail

VERSION="4.0"
BOLD="\033[1m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

echo -e "${BOLD}ReconRanger v${VERSION} — Bootstrap Installer${RESET}"
echo "=================================================="

# ── Helpers ───────────────────────────────────────────────────────────────────
have() { command -v "$1" &>/dev/null; }

# ── Base packages (no Rust/Go/Ruby — installed separately below) ──────────────
install_base_deps() {
    local pkgs="python3 python3-pip python3-venv build-essential git curl wget"

    if have apt-get; then
        echo -e "${GREEN}[→] apt detected (Debian/Ubuntu/Kali/Parrot)${RESET}"
        apt-get update -qq
        # Install base packages, skipping failures
        apt-get install -y -q $pkgs || true
    elif have dnf; then
        echo -e "${GREEN}[→] dnf detected (Fedora/RHEL)${RESET}"
        dnf install -y python3 python3-pip git curl wget gcc make || true
    elif have yum; then
        echo -e "${GREEN}[→] yum detected (CentOS/RHEL)${RESET}"
        yum install -y python3 python3-pip git curl wget gcc make || true
    elif have pacman; then
        echo -e "${GREEN}[→] pacman detected (Arch)${RESET}"
        pacman -Syu --noconfirm python python-pip git curl wget base-devel || true
    else
        echo -e "${RED}[!] Unknown distro. Install manually: python3 pip git curl${RESET}"
        exit 1
    fi
}

# ── Go ────────────────────────────────────────────────────────────────────────
install_go() {
    if have go; then
        echo -e "${GREEN}[✓] go already installed: $(go version | awk '{print $3}')${RESET}"
        return
    fi
    echo -e "${GREEN}[→] Installing Go via official tarball…${RESET}"
    local GO_VER="1.23.4"
    local ARCH
    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64)  ARCH="amd64" ;;
        aarch64) ARCH="arm64" ;;
        armv6l)  ARCH="armv6l" ;;
        *)       ARCH="amd64" ;;
    esac
    local TARBALL="go${GO_VER}.linux-${ARCH}.tar.gz"
    local URL="https://go.dev/dl/${TARBALL}"

    curl -fsSL "$URL" -o "/tmp/${TARBALL}"
    rm -rf /usr/local/go
    tar -C /usr/local -xzf "/tmp/${TARBALL}"
    rm -f "/tmp/${TARBALL}"

    # Add to PATH for this session and for the installing user's shell
    export PATH=$PATH:/usr/local/go/bin
    for rc in /root/.bashrc /root/.zshrc /home/*/.bashrc /home/*/.zshrc; do
        [[ -f "$rc" ]] || continue
        grep -q '/usr/local/go/bin' "$rc" || echo 'export PATH=$PATH:/usr/local/go/bin' >> "$rc"
    done
    echo -e "${GREEN}[✓] go $(go version | awk '{print $3}')${RESET}"
}

# ── Go PATH for user bins ─────────────────────────────────────────────────────
setup_gopath() {
    local GOPATH_LINE='export GOPATH=$HOME/go'
    local PATH_LINE='export PATH=$PATH:$GOPATH/bin'
    mkdir -p ~/go/bin
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
    for rc in ~/.bashrc ~/.zshrc; do
        [[ -f "$rc" ]] || continue
        grep -q 'GOPATH' "$rc"      || echo "$GOPATH_LINE" >> "$rc"
        grep -q 'GOPATH/bin' "$rc"  || echo "$PATH_LINE"   >> "$rc"
    done
}

# ── Rust via rustup (avoids cargo/rustc apt conflicts) ────────────────────────
install_rust() {
    if have cargo; then
        echo -e "${GREEN}[✓] cargo already installed${RESET}"
        return
    fi
    echo -e "${GREEN}[→] Installing Rust via rustup (avoids apt conflicts)…${RESET}"
    # Remove conflicting apt packages if present
    if have apt-get; then
        apt-get remove -y -q cargo rustc 2>/dev/null || true
    fi
    curl -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
    export PATH="$HOME/.cargo/bin:$PATH"
    for rc in ~/.bashrc ~/.zshrc; do
        [[ -f "$rc" ]] || continue
        grep -q '\.cargo/bin' "$rc" || echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> "$rc"
    done
    echo -e "${GREEN}[✓] cargo $(cargo --version)${RESET}"
}

# ── Ruby ──────────────────────────────────────────────────────────────────────
install_ruby() {
    if have ruby && have gem; then
        echo -e "${GREEN}[✓] ruby already installed: $(ruby --version | awk '{print $2}')${RESET}"
        return
    fi
    echo -e "${GREEN}[→] Installing Ruby…${RESET}"
    if have apt-get; then
        # ruby-full has broken deps on some Kali versions — use ruby + ruby-dev instead
        apt-get install -y -q ruby ruby-dev 2>/dev/null || \
            apt-get install -y -q ruby-full 2>/dev/null || true
    elif have dnf;    then dnf install -y ruby ruby-devel || true
    elif have pacman; then pacman -S --noconfirm ruby || true
    fi
    if have gem; then
        echo -e "${GREEN}[✓] ruby $(ruby --version | awk '{print $2}')${RESET}"
    else
        echo -e "${YELLOW}[!] ruby/gem not installed — wpscan will not work.${RESET}"
    fi
}

# ── Python deps ───────────────────────────────────────────────────────────────
install_python_deps() {
    echo -e "${GREEN}[→] Installing Python dependencies…${RESET}"
    python3 -m pip install --upgrade pip --break-system-packages -q 2>/dev/null || \
        python3 -m pip install --upgrade pip -q || true
    python3 -m pip install --upgrade tqdm requests --break-system-packages -q 2>/dev/null || \
        python3 -m pip install --upgrade tqdm requests -q || true
}

# ── Root check ────────────────────────────────────────────────────────────────
if [[ $EUID -eq 0 ]]; then
    install_base_deps
    install_go
    install_ruby
else
    echo -e "${YELLOW}[!] Not running as root. Using sudo for system packages.${RESET}"
    sudo bash -c "
        $(declare -f have install_base_deps install_go install_ruby)
        install_base_deps
        install_go
        install_ruby
    "
fi

setup_gopath
install_rust
install_python_deps

# ── pdtm (optional) ───────────────────────────────────────────────────────────
if have go && ! have pdtm; then
    echo -e "${GREEN}[→] Installing pdtm…${RESET}"
    go install github.com/projectdiscovery/pdtm/cmd/pdtm@latest 2>/dev/null || true
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}Bootstrap complete!${RESET}"
echo ""
echo "Tool     Status"
echo "─────────────────────────────"
have python3 && echo "python3  $(python3 --version)" || echo "python3  ✗ MISSING"
have go      && echo "go       $(go version | awk '{print $3}')" || echo "go       ✗ MISSING"
have cargo   && echo "cargo    $(cargo --version 2>/dev/null)" || echo "cargo    ✗ MISSING"
have ruby    && echo "ruby     $(ruby --version | awk '{print $2}')" || echo "ruby     ✗ missing (wpscan disabled)"
have gem     && echo "gem      $(gem --version)" || true
echo ""
echo "Next steps:"
echo "  python3 reconranger.py -c core       # Install core toolkit"
echo "  python3 reconranger.py --categories  # List all categories"
echo "  python3 reconranger.py --check       # Check what's installed"