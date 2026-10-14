import os
from datetime import datetime
from src.logger import logger

def save_error_screenshot(driver, error_name: str):
    """Takes a screenshot when an error occurs and saves it cleanly."""
    # Ensure output folders exist
    os.makedirs(os.path.join("output", "screenshots"), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"output/screenshots/{error_name}_{timestamp}.png"
    
    try:
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved at: {filepath}")
    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")

def save_to_markdown(part_number: int, summary: str, scripts: list):
    """Saves extracted data into isolated markdown files (e.g., part1.md)."""
    os.makedirs("output", exist_ok=True)
    filename = f"output/part{part_number}.md"
    
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"## Part {part_number}: Django Notes\n\n")
            file.write(f"**Summary:** {summary}\n\n")
            file.write("---\n\n")
            
            for script in scripts:
                file.write("```python\n")
                file.write(f"{script}\n")
                file.write("```\n\n")
                
        logger.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to write to file {filename}: {e}")
        raise