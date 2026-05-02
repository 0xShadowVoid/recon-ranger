"""Centralized logging - ReconRanger v3.1"""
import logging
import os
from pathlib import Path

# Use local logs directory
LOG_DIR = Path(__file__).parent.parent / "logs"
MAIN_LOG = LOG_DIR / "install.log"
ERROR_LOG = LOG_DIR / "error.log"

def setup_logging():
    """Initialize secure logging"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    for log_path in [MAIN_LOG, ERROR_LOG]:
        if not log_path.exists():
            log_path.touch()
            os.chmod(log_path, 0o644)
    
    logger = logging.getLogger("ReconRanger")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Main log handler
        fh = logging.FileHandler(MAIN_LOG, encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s'))
        
        # Error log handler
        eh = logging.FileHandler(ERROR_LOG, encoding='utf-8')
        eh.setLevel(logging.ERROR)
        eh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s'))
        
        logger.addHandler(fh)
        logger.addHandler(eh)
    
    return logger
