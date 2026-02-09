#!/bin/bash
# ReconRanger v2.0 Bootstrapper
# One-time dependency setup for Parrot OS / Debian-based systems

set -e

echo "🦅 ReconRanger v2.0 - Surgical Recon Toolkit"
echo "=========================================="

# Check if running as root for system packages
if [[ $EUID -eq 0 ]]; then
    echo "⚠️  Running as root - installing system packages only"
    ROOT_MODE=true
else
    echo "✅ Running as user - tools will install to user space"
    ROOT_MODE=false
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
if $ROOT_MODE; then
    apt update
    apt install -y \
        python3 python3-pip python3-venv \
        golang-go build-essential \
        git curl wget \
        npm nodejs \
        ruby-dev \
        cargo
else
    echo "ℹ️  Please run: sudo apt update && sudo apt install -y python3 python3-pip python3-venv golang-go build-essential git curl wget npm nodejs ruby-dev cargo"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --user -q tqdm requests

# Setup Go environment for user
if ! $ROOT_MODE; then
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
fi

# Install pdtm for ProjectDiscovery tools (if not root)
if ! $ROOT_MODE; then
    echo "📦 Installing pdtm (ProjectDiscovery Tool Manager)..."
    if ! command -v pdtm &> /dev/null; then
        go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest
    fi
fi

echo ""
echo "✅ Bootstrap completed!"
echo ""
if $ROOT_MODE; then
    echo "🔧 Next steps:"
    echo "   1. Run as normal user: python3 reconranger.py -c core"
else
    echo "🔧 Next steps:"
    echo "   1. Install core toolkit: python3 reconranger.py -c core"
    echo "   2. Verify installation: python3 reconranger.py --check"
    echo "   3. Start recon: bbot -t example.com -m subfinder httpx nuclei"
fi
echo ""
echo "📖 Documentation: TOOLS.md"
echo "🌟 Core toolkit covers 95% of recon workflows in <5 minutes!"
