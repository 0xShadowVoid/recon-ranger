#!/bin/bash
# ReconRanger v2.0 Bootstrapper
# One-time dependency setup for any Linux distribution

set -e

echo "🦅 ReconRanger v2.0 - Surgical Recon Toolkit"
echo "=========================================="

# Install system dependencies
echo "📦 Installing system dependencies..."
if command -v apt &> /dev/null; then
    echo "🔧 Detected Debian/Ubuntu-based system"
    if [[ $EUID -eq 0 ]]; then
        apt update
        apt install -y python3 python3-pip python3-venv golang-go build-essential git curl wget npm nodejs ruby-dev cargo
    else
        echo "ℹ️  Running as user - some packages may need sudo"
        echo "Please run: sudo apt update && sudo apt install -y python3 python3-pip python3-venv golang-go build-essential git curl wget npm nodejs ruby-dev cargo"
    fi
elif command -v yum &> /dev/null; then
    echo "🔧 Detected RedHat/CentOS/Fedora system"
    if [[ $EUID -eq 0 ]]; then
        yum update -y
        yum install -y python3 python3-pip python3-venv golang build-essential git curl wget npm nodejs ruby ruby-devel cargo
    else
        echo "ℹ️  Running as user - some packages may need sudo"
        echo "Please run: sudo yum update -y && sudo yum install -y python3 python3-pip python3-venv golang build-essential git curl wget npm nodejs ruby ruby-devel cargo"
    fi
elif command -v dnf &> /dev/null; then
    echo "🔧 Detected Fedora system"
    if [[ $EUID -eq 0 ]]; then
        dnf update -y
        dnf install -y python3 python3-pip python3-venv golang build-essential git curl wget npm nodejs ruby ruby-devel cargo
    else
        echo "ℹ️  Running as user - some packages may need sudo"
        echo "Please run: sudo dnf update -y && sudo dnf install -y python3 python3-pip python3-venv golang build-essential git curl wget npm nodejs ruby ruby-devel cargo"
    fi
elif command -v pacman &> /dev/null; then
    echo "🔧 Detected Arch Linux system"
    if [[ $EUID -eq 0 ]]; then
        pacman -Syu --noconfirm
        pacman -S --noconfirm python python-pip go base-devel git curl wget npm nodejs ruby rust
    else
        echo "ℹ️  Running as user - some packages may need sudo"
        echo "Please run: sudo pacman -Syu --noconfirm && sudo pacman -S --noconfirm python python-pip go base-devel git curl wget npm nodejs ruby rust"
    fi
else
    echo "⚠️  Unknown distribution. Please install manually:"
    echo "   - Python 3.8+ with pip and venv"
    echo "   - Go 1.19+"
    echo "   - Git, curl, wget"
    echo "   - Node.js, npm"
    echo "   - Ruby, gem"
    echo "   - Rust, cargo"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --user -q tqdm requests

# Setup Go environment for user
echo "🔧 Setting up Go environment..."

# Add GOPATH/bin to PATH if not present
if ! grep -q 'go/bin' ~/.bashrc; then
    echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
    echo 'export GOPATH=$HOME/go' >> ~/.bashrc
fi

# Create go directories
mkdir -p ~/go/bin

# Export for current session
export PATH=$PATH:~/go/bin
export GOPATH=$HOME/go

# Install pdtm for ProjectDiscovery tools
echo "📦 Installing pdtm (ProjectDiscovery Tool Manager)..."
if ! command -v pdtm &> /dev/null; then
    go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest
fi

echo ""
echo "✅ Bootstrap completed!"
echo ""
echo "🔧 Next steps:"
echo "   1. Install core toolkit: python3 reconranger.py -c core"
echo "   2. Verify installation: python3 reconranger.py --check"
echo "   3. Start recon: bbot -t example.com -m subfinder httpx nuclei"
echo ""
echo "📖 Documentation: TOOLS.md"
echo "🌟 Core toolkit covers 95% of recon workflows in <5 minutes!"
