import logging
import sys

# Configure logging format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console Handler
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)
        
    return logger
