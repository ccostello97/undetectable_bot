"""Custom exceptions for the undetectable_bot package."""


class StealthBrowserError(Exception):
    """Base exception for StealthBrowser errors."""


class BrowserNotInitializedError(StealthBrowserError):
    """Raised when trying to use StealthBrowser before init."""

    def __init__(self) -> None:
        super().__init__(
            "Browser not initialized. Use StealthBrowser as a context manager."
        )
