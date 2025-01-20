"""Logging module for the budget app"""

import logging
import pathlib
from logging.handlers import RotatingFileHandler

# global variables
LOGGER_NAME = 'budget'
LOGGER_FILE_NAME = 'logs/budget.log'
LOGGER_LEVEL = 'DEBUG'
LOGGING_MAX_LOG_SIZE = 5 * 1024 * 1024
LOGGING_FILE_BACKUP_COUNT = 5

def configure_logger(
        name=LOGGER_NAME,
        log_file=LOGGER_FILE_NAME,
        level=LOGGER_LEVEL,
        size_limit=LOGGING_MAX_LOG_SIZE,
        backup_count=LOGGING_FILE_BACKUP_COUNT
        ):
    
    """setting up the default budget app logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        #create the loggin file and direcetories as needed
        log_dir = pathlib.Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        handler = RotatingFileHandler(log_file, maxBytes=size_limit, backupCount=backup_count)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)


def budget_logger() -> logging.Logger:
    """Returns the current instance of the logger"""

    return logging.getLogger(LOGGER_NAME)