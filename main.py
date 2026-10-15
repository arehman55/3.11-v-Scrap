import sys
from src.scraper import DjangoNotesScraper
from src.logger import logger
from src.exceptions import ScraperError
from src.desktop_emailer import RobocorpEmailer

def main():
    logger.info("Starting Django Notes Scraper Project...")
    scraper = DjangoNotesScraper()
    
    try:
        # Run the core scraping logic
        scraper.run()
        logger.info("Extraction completed successfully. Check the 'output' folder.")
        
        # Initialize and trigger the Robocorp RPA process
        logger.info("Triggering Desktop UI Email Automation via Robocorp...")
        
        # Define the target email address for the automated report
        RECEIVER_EMAIL = "fma766688@gmail.com" 
        
        # Instantiate the RPA bot and execute the email dispatch sequence
        rpa_bot = RobocorpEmailer(RECEIVER_EMAIL)
        rpa_bot.send_automated_email()
        
    except ScraperError as e:
        # Catch custom scraper logic errors cleanly and exit
        logger.error(f"Application Stopped: {e}")
        sys.exit(1)
    except Exception as e:
        # Catch any unexpected Python system crashes cleanly
        logger.error(f"Critical System Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()