from pathlib import Path
from types import TracebackType

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Playwright,
    sync_playwright,
)

from undetectable_bot.browser.constants import (
    ARGS,
    CONTEXT_SETTINGS,
    STEALTH_JS_PATH,
)
from undetectable_bot.exceptions import BrowserNotInitializedError


class StealthBrowser:
    """A stealthy browser that evades detection."""

    def __init__(self, *, headless: bool = True) -> None:
        self.headless = headless
        self.browser: Browser | None = None
        self.playwright: Playwright | None = None

    def new_context(self) -> BrowserContext:
        """Create a new browser context."""
        if not self.browser:
            raise BrowserNotInitializedError
        context: BrowserContext = self.browser.new_context(
            viewport=CONTEXT_SETTINGS["viewport"],
            user_agent=CONTEXT_SETTINGS["user_agent"],
            color_scheme=CONTEXT_SETTINGS["color_scheme"],
            locale=CONTEXT_SETTINGS["locale"],
            timezone_id=CONTEXT_SETTINGS["timezone_id"],
            permissions=CONTEXT_SETTINGS["permissions"],
            java_script_enabled=CONTEXT_SETTINGS["java_script_enabled"],
            bypass_csp=CONTEXT_SETTINGS["bypass_csp"],
            extra_http_headers=CONTEXT_SETTINGS["extra_http_headers"],
        )
        context.add_init_script(path=str(STEALTH_JS_PATH))
        return context

    def __enter__(self) -> "StealthBrowser":
        """Enter the synchronous context manager."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=ARGS,
            chromium_sandbox=False,
        )
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the synchronous context manager."""
        if self.playwright:
            self.playwright.stop()


def test_sync_stealth_browser() -> None:
    """Test the sync stealth browser."""
    with StealthBrowser() as browser:
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://bot.sannysoft.com/")
        page.wait_for_load_state("networkidle")

        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        screenshot_path = data_dir / "screenshot.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        html_path = data_dir / "index.html"
        html_path.write_text(page.content(), encoding="utf-8")


if __name__ == "__main__":
    test_sync_stealth_browser()
