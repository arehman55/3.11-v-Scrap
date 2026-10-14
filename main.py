import sys
from src.scraper import DjangoNotesScraper
from src.logger import logger
from src.exceptions import ScraperError

def main():
    logger.info("Starting Django Notes Scraper Project...")
    scraper = DjangoNotesScraper()
    
    try:
        scraper.run()
        logger.info("Extraction completed successfully. Check the 'output' folder.")
    except ScraperError as e:
        # Catches our custom logic errors cleanly
        logger.error(f"Application Stopped: {e}")
        sys.exit(1)
    except Exception as e:
        # Catches unexpected Python crashes cleanly
        logger.error(f"Critical System Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()