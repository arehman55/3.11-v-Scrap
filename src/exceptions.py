# Custom exceptions for clean, enterprise-grade error handling

class ScraperError(Exception):
    """Base exception for all web scraping and automation-related errors in the project."""
    pass

class ElementNotFoundError(ScraperError):
    """Raised when a specific web DOM element or Windows UI locator is not found."""
    pass

class NavigationError(ScraperError):
    """Raised when a web page fails to load, or UI navigation/clicking fails."""
    pass

class ValidationError(ScraperError):
    """Raised when the loaded page or extracted data is incorrect or out of expected scope."""
    pass

class ScraperTimeoutError(ScraperError):
    """Raised when a network request, page load, or UI element wait exceeds the maximum allowed time."""
    pass

class FileOperationError(ScraperError):
    """Raised when there is a critical failure in creating, reading, or saving the markdown output files."""
    pass

class RPAExecutionError(ScraperError):
    """Raised when the Robocorp Desktop Automation (e.g., launching Thunderbird, attaching files) fails."""
    pass