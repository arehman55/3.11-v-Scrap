import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Importing custom modules for logging, error handling, and file saving
from src.logger import logger
from src.exceptions import ElementNotFoundError, NavigationError, ValidationError, ScraperError
from src.utils import save_error_screenshot, save_to_markdown

class DjangoNotesScraper:
    def __init__(self):
        # The starting URL for the scraper. We only provide Part 1 here.
        # The scraper will automatically find the "next part" link and click it for subsequent parts.
        self.start_url = "https://docs.djangoproject.com/en/stable/intro/tutorial01/"
        
        # Placeholder for the browser instance (Selenium WebDriver)
        self.driver = None

    def setup_driver(self):
        """
        Initializes the Chrome browser safely with standard options.
        It ensures the browser opens in maximized mode for better element visibility.
        """
        try:
            # Set up Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized") # Maximizing helps prevent elements from being hidden
            
            # Start the Chrome browser
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver initialized successfully.")
        except WebDriverException as e:
            # If Chrome fails to start (e.g., missing driver), log it and raise a custom error
            logger.error("Could not start Chrome browser.")
            raise ScraperError(f"WebDriver Initialization Failed: {e}")

    def validate_page(self, expected_part: int):
        """
        Validates that the browser is currently on the correct tutorial part.
        It checks the main heading (H1) of the page to confirm the part number.
        """
        logger.info(f"Validating page content for Part {expected_part}...")
        try:
            # Wait up to 10 seconds for the H1 tag (main heading) to appear on the page
            wait = WebDriverWait(self.driver, 10)
            heading_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            heading_text = heading_element.text.lower() # Convert to lowercase for easy comparison
        except TimeoutException:
            # If H1 is not found within 10 seconds, take a screenshot and raise an error
            save_error_screenshot(self.driver, f"validation_timeout_part_{expected_part}")
            raise ValidationError(f"Could not find a heading (H1) on the page to validate Part {expected_part}.")

        # STRICT VALIDATION RULE:
        # 1. Ensure we didn't accidentally navigate to "Part 4"
        # 2. Ensure the expected part number (e.g., "part 1") is actually in the heading
        if "part 4" in heading_text or f"part {expected_part}" not in heading_text:
            save_error_screenshot(self.driver, f"wrong_page_loaded_part_{expected_part}")
            raise ValidationError(
                f"SECURITY STOP: We accidentally landed on '{heading_text}' instead of Part {expected_part}. "
                "Extraction has been blocked to prevent wrong data copying."
            )
        
        logger.info(f"Validation Passed: Confirmed we are exactly on Part {expected_part}.")

    def scroll_page(self):
        """
        Scrolls the page from top to bottom smoothly.
        This mimics human behavior and ensures lazy-loaded elements or styles are fully rendered.
        """
        logger.info("Scrolling page to the bottom...")
        try:
            # Get the total height of the webpage
            total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
            
            # Scroll down in small increments (600 pixels) to look natural
            for i in range(1, total_height, 600):
                self.driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(0.1) # Brief pause during scroll
            
            # Finally, jump exactly to the very bottom to be safe
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5) # Wait half a second after reaching the bottom
        except Exception as e:
            # Scrolling is not critical, so we just log a warning if it fails, without stopping the script
            logger.warning(f"Minor issue while scrolling: {e}")

    def extract_data(self, part_number: int):
        """
        Finds and extracts the main summary (first paragraph) and all Python/Console code blocks.
        """
        logger.info("Extracting summary and scripts...")
        try:
            # Wait up to 10 seconds for the main documentation container to load
            wait = WebDriverWait(self.driver, 10)
            content_section = wait.until(EC.presence_of_element_located((By.ID, "docs-content")))
            
            # Step 1: Extract the Summary
            # Find all paragraph <p> tags inside the content section
            paragraphs = content_section.find_elements(By.TAG_NAME, "p")
            if not paragraphs:
                raise ElementNotFoundError(f"Summary text not found on Part {part_number}")
            
            # Take the first paragraph as the summary, and limit it to 150 characters
            full_summary = paragraphs[0].text
            summary = full_summary[:150] + "..." if len(full_summary) > 150 else full_summary
            
            # Step 2: Extract Code Blocks
            # Use CSS selectors to find both Python code blocks and Console command blocks
            code_blocks = content_section.find_elements(By.CSS_SELECTOR, "div.highlight-python pre, div.highlight-console pre")
            
            # Extract text from each block and remove extra whitespace
            scripts = [block.text.strip() for block in code_blocks if block.text.strip()]
            
            if not scripts:
                logger.warning(f"No scripts found in Part {part_number}")
                
            # Return the extracted data back to the main loop
            return summary, scripts
        
        except ElementNotFoundError:
            # Triggered if paragraphs are missing
            save_error_screenshot(self.driver, f"missing_data_part_{part_number}")
            raise
        except Exception as e:
            # Triggered for any other unexpected error during extraction
            save_error_screenshot(self.driver, f"extraction_error_part_{part_number}")
            raise ScraperError(f"Failed to extract data on Part {part_number}: {e}")

    def click_next_part(self, current_part: int):
        """
        Finds the link pointing to the next tutorial part at the bottom of the page
        and clicks it using standard core Selenium functionality.
        """
        next_part = current_part + 1
        logger.info(f"Looking for link to click and navigate to Part {next_part}...")
        
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # XPath logic: Look for an anchor tag (<a>) where the text contains 'part 2', 'part 3', etc.
            # 'translate' is used to make the text case-insensitive (converts 'PART' to 'part')
            xpath = f"//a[contains(translate(text(), 'PART', 'part'), 'part {next_part}')]"
            
            # Wait until the link is strictly visible and clickable on the screen
            next_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Perform a standard core Python/Selenium click (No JS injection used here)
            next_link.click()
            logger.info(f"Successfully clicked link for Part {next_part}.")
            
        except TimeoutException:
            # If the link is not found or not clickable within 10 seconds
            save_error_screenshot(self.driver, f"next_link_not_found_part_{next_part}")
            raise NavigationError(f"Could not find the navigation link for Part {next_part} at the bottom of the page.")
        except Exception as e:
            # If the standard click fails (e.g., ElementClickInterceptedException)
            save_error_screenshot(self.driver, f"navigation_error_part_{next_part}")
            raise NavigationError(f"Failed to click next link for Part {next_part} using standard click: {e}")

    def run(self):
        """
        The main execution loop that combines all the steps.
        Flow: Setup Browser -> Load Part 1 -> Loop(Validate -> Extract -> Save -> Scroll -> Click Next)
        """
        try:
            # Initialize the browser
            self.setup_driver()
            
            logger.info(f"--- Launching First Page ---")
            
            # Yahan humne initial load ke liye error handling aur screenshot add kar diya hai
            try:
                self.driver.get(self.start_url)
            except Exception as e:
                save_error_screenshot(self.driver, "initial_page_load_failed")
                raise NavigationError(f"Internet connection issue or URL invalid: {e}")
            
            # Loop through Part 1, Part 2, and Part 3
            for part in range(1, 4):
                logger.info(f"--- Processing Part {part} ---")
                
                # 1. Page Validation: Check if we are on the correct part and NOT on part 4
                self.validate_page(part)
                
                # 2. Extract Data: Get the summary and python/console scripts
                summary, scripts = self.extract_data(part)
                
                # 3. Save to File: Write the extracted data into isolated Markdown files
                save_to_markdown(part, summary, scripts)
                
                # 4. Scroll Down: Simulate human scrolling
                self.scroll_page()
                
                # 5. Navigate to Next Part
                if part < 3:
                    self.click_next_part(part)
                    time.sleep(3) 
                
        finally:
            self.close()

    def close(self):
        """
        Safely quits the Chrome WebDriver and closes all associated windows.
        """
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed successfully.")