import os
import logging
from logging.handlers import RotatingFileHandler

# LOG DIRECTORY

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "nids.log")

# LOGGER CONFIGURATION

def get_logger(name: str = "NIDS"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    logger.setLevel(logging.INFO)

    # FORMAT

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # FILE HANDLER (ROTATING)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # CONSOLE HANDLER
  
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # ADD HANDLERS

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# DEFAULT LOGGER INSTANCE

logger = get_logger()

# HELPER FUNCTIONS

def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(message: str):
    logger.error(message)

def setup_logger():
    return get_logger("NIDS")
