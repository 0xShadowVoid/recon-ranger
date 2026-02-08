"""Centralized logging with security controls"""
import logging
import os
from pathlib import Path

# Use local logs directory instead of /var/log
LOG_DIR = Path(__file__).parent.parent / "logs"
MAIN_LOG = LOG_DIR / "reconranger.log"
ERROR_LOG = LOG_DIR / "reconranger_errors.log"

def setup_logging():
    """Initialize secure logging"""
    # Ensure log directories exist with proper permissions
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    for log_path in [MAIN_LOG, ERROR_LOG]:
        if not log_path.exists():
            log_path.touch()
            os.chmod(log_path, 0o644)
    
    # Main logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(MAIN_LOG, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("ReconRanger")

def get_error_logger():
    """Get dedicated error logger"""
    logger = logging.getLogger("ReconRangerError")
    handler = logging.FileHandler(ERROR_LOG, encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
    return logger