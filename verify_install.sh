#!/bin/bash
# verify_install.sh - Comprehensive tool verification with error logging

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'
ERROR_LOG="/var/log/reconranger_errors.log"

log_error() {
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$TIMESTAMP] VERIFICATION ERROR: $1" >> "$ERROR_LOG"
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔍 ReconRanger Installation Verification${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

TOOLS="amass subfinder httpx dnsx nuclei katana ffuf gospider assetfinder shuffledns naabu metabigor sublist3r cewl linkfinder cloud_enum githound virustotalx"

echo -e "\n${BLUE}Checking tool installations:${NC}"
MISSING=()
for tool in $TOOLS; do
  if command -v "$tool" &>/dev/null; then
    # Get version
    if "$tool" --version &>/dev/null 2>&1 | head -1 | grep -q "version\|Version"; then
      version=$("$tool" --version 2>&1 | head -1 | sed 's/.*version[[:space:]]*\([^ ]*\).*/\1/' | cut -c1-15) || version="installed"
    elif "$tool" -version &>/dev/null 2>&1; then
      version=$("$tool" -version 2>&1 | head -1 | cut -d' ' -f2- | cut -c1-15) || version="installed"
    else
      version="installed"
    fi
    echo -e "${GREEN}✓${NC} ${tool:22} ${version}"
  else
    echo -e "${RED}✗${NC} ${tool:22} NOT FOUND"
    MISSING+=("$tool")
    log_error "Tool missing: $tool"
  fi
done

echo -e "\n${BLUE}System environment:${NC}"
go_ver=$(go version 2>/dev/null | cut -d' ' -f3 || echo "NOT FOUND")
py_ver=$(python3 --version 2>/dev/null || echo "NOT FOUND")
node_ver=$(node --version 2>/dev/null || echo "NOT FOUND")
echo -e "  Go version:    ${go_ver}"
echo -e "  Python version:${py_ver}"
echo -e "  Node version:  ${node_ver}"

if [ "${go_ver}" = "NOT FOUND" ] || [[ ! "$go_ver" =~ ^go1\.(19|[2-9][0-9]) ]]; then
  echo -e "${RED}✗ Go 1.19+ required${NC}"
  log_error "Go version insufficient: $go_ver"
fi

echo -e "\n${BLUE}Critical dependencies:${NC}"
for dep in geckodriver firefox chromium; do
  if command -v "$dep" &>/dev/null; then
    echo -e "${GREEN}✓${NC} $dep"
  else
    echo -e "${YELLOW}⚠${NC} $dep (required for virustotalx)"
    if [ "$dep" = "geckodriver" ]; then
      log_error "geckodriver missing - required for virustotalx"
    fi
  fi
done

if [ ${#MISSING[@]} -eq 0 ]; then
  echo -e "\n${GREEN}✅ ALL TOOLS INSTALLED SUCCESSFULLY${NC}"
  echo -e "\n${BLUE}Quick test workflow:${NC}"
  echo -e "  subfinder -d example.com -silent | head -3 | httpx -silent -status-code"
else
  echo -e "\n${RED}⚠ ${#MISSING[@]} TOOL(S) MISSING:${NC} ${MISSING[*]}"
  echo -e "\n${YELLOW}Troubleshooting:${NC}"
  echo -e "  1. Re-run installer: sudo python3 reconranger.py --update -t ${MISSING[0]}"
  echo -e "  2. Check error log:  sudo tail -50 $ERROR_LOG"
  echo -e "  3. Verify Go env:    go env GOPATH GOBIN"
  exit 1
fi