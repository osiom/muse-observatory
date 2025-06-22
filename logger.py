import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Get current date for log filename
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"logs/muse_observatory_{current_date}.log"

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # File handler - writes to log file
        logging.FileHandler(log_filename),
        # Stream handler - writes to console
        logging.StreamHandler(),
    ],
)


def get_logger(name: str):
    """
    Get a logger with the specified name.

    Args:
        name (str): Name for the logger, typically __name__ of the calling module

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    return logger
