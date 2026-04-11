"""Logging configuration and setup for the Mood Tracker backend application."""

__all__ = ["setup_logging", "logging_settings"]

import logging
import os
from datetime import datetime

from pydantic import BaseModel

from app.src.settings import settings


class LoggingSettings(BaseModel):
    """Pydantic model holding all logging-related configuration values."""

    APP_NAME: str = settings.APP_NAME
    FILE_NAME: str = f"{APP_NAME}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"
    LOG_DIR: str = "logs"
    ENABLE_SQLALCHEMY_LOGGING: bool = True
    LOG_LEVEL: int = logging.DEBUG
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


logging_settings: LoggingSettings = LoggingSettings()


def setup_logging(logging_settings: LoggingSettings = logging_settings):
    """Configure file and console logging handlers and return the application logger."""
    if not os.path.exists(logging_settings.LOG_DIR):
        os.makedirs(logging_settings.LOG_DIR)

    # Set log file name with current date
    log_filename = os.path.join(logging_settings.LOG_DIR, logging_settings.FILE_NAME)

    # Basic configuration for logging
    logging.basicConfig(
        level=logging_settings.LOG_LEVEL,  # Set the logging level
        format=logging_settings.LOG_FORMAT,  # Log format
        datefmt=logging_settings.DATE_FORMAT,  # Date format
        handlers=[
            logging.FileHandler(log_filename),  # Log to a file
            logging.StreamHandler(),  # Log to console
        ],
    )

    return logging.getLogger(logging_settings.APP_NAME)
