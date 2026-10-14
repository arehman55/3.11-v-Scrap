import logging
import sys

def setup_logger():
    logger = logging.getLogger("DjangoScraper")
    logger.setLevel(logging.DEBUG)

    # Console handler: Clean simple messages for the terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    # File handler: Detailed logs for debugging (saves to file instead of terminal)
    file_handler = logging.FileHandler("scraper.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()