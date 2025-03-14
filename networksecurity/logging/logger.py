# Security_Network/networksecurity/logging/logger.py
import logging
import os
from datetime import datetime


def setup_logger():
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    log_file_path = os.path.join(logs_dir, log_file)

    logging.basicConfig(
        filename=log_file_path,
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    return logging.getLogger(__name__)


# Explicitly assign the logger instance
log = setup_logger()  # Changed from 'logger' to 'log' to avoid conflict with module name

