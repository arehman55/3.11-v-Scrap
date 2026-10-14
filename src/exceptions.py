# Custom exceptions for clean error handling
class ScraperError(Exception):
    """Base exception for all scraper related errors."""
    pass

class ElementNotFoundError(ScraperError):
    """Raised when a specific web element is not found on the page."""
    pass

class NavigationError(ScraperError):
    """Raised when page fails to load or link clicking fails."""
    pass

class ValidationError(ScraperError):
    """Raised when the loaded page is incorrect or out of scope (e.g., loaded Part 4 instead of 1-3)."""
    pass