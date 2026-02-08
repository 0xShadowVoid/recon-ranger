#!/bin/bash
# update_tools.sh - One-command updater for all ReconRanger tools
# Logs errors to /var/log/reconranger_errors.log with timestamps

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'
ERROR_LOG="/var/log/reconranger_errors.log"

log_error() {
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$TIMESTAMP] ERROR: $1" >> "$ERROR_LOG"
  echo -e "${RED}[ERROR]${NC} $1"
}

# Check root
if [ "$EUID" -ne 0 ]; then
  log_error "update_tools.sh requires root privileges"
  echo -e "${RED}✗ This script requires root privileges${NC}"
  echo -e "  Run with: ${YELLOW}sudo ./update_tools.sh${NC}"
  exit 1
fi

# Verify reconranger.py exists
if [ ! -f "reconranger.py" ]; then
  log_error "reconranger.py not found in current directory"
  echo -e "${RED}✗ reconranger.py not found in current directory${NC}"
  echo -e "  Please run from ReconRanger installation directory"
  exit 1
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔄 ReconRanger Tool Updater${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${BLUE}Updating all ReconRanger tools...${NC}"
echo -e "${YELLOW}This will:${NC}"
echo -e "  • Pull latest versions from GitHub"
echo -e "  • Rebuild Go tools"
echo -e "  • Update Python packages"
echo -e "  • Refresh nuclei templates"
echo -e "\n${YELLOW}Press Ctrl+C to cancel within 5 seconds...${NC}"
sleep 5

# Run updater with error capture
if ! sudo python3 reconranger.py --update --all 2>&1 | tee -a /tmp/update_log.txt; then
  log_error "Tool update failed - see /tmp/update_log.txt for details"
  echo -e "\n${RED}✗ Tool update failed${NC}"
  echo -e "  Check error log: ${YELLOW}sudo tail -50 $ERROR_LOG${NC}"
  exit 1
fi

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Tool update complete${NC}"
echo -e "\n${BLUE}Verification:${NC}"
if [ -f "verify_install.sh" ]; then
  ./verify_install.sh
else
  echo -e "${YELLOW}⚠ verify_install.sh not found - run manually${NC}"
fi

# Show recent errors if any
if grep -q "ERROR" "$ERROR_LOG" 2>/dev/null; then
  echo -e "\n${YELLOW}⚠ Recent errors detected:${NC}"
  sudo tail -10 "$ERROR_LOG" | grep "ERROR"
  echo -e "\n${YELLOW}Full error log: $ERROR_LOG${NC}"
fi