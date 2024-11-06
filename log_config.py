import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file='app.log', log_level=logging.INFO):
    """ Set up logging configuration."""

    # Create a logger and Set the logging level
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a console handler and set the format
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Implement log rotation

    # 1. Use RotatingFileHandler for size-based rotation.
    # 10 MB size limit
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)

    # 2. Use TimedRotatingFileHandler for time-based rotation.
    # Daily rotation
    # file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)

    file_handler.setFormatter(formatter)

    # Remove existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
