import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(
    name: str,
    log_file: str = "/var/log/celery-weather-app/app.log",
    level=logging.INFO,
):
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # File Handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
