import asyncio
from pathlib import Path
from types import TracebackType

from playwright.async_api import (
    Browser,
    BrowserContext,
    Playwright,
    async_playwright,
)

from undetectable_bot.browser.constants import (
    ARGS,
    CONTEXT_SETTINGS,
    STEALTH_JS_PATH,
)
from undetectable_bot.exceptions import BrowserNotInitializedError


class AsyncStealthBrowser:
    """An asynchronous version of StealthBrowser."""

    def __init__(self, *, headless: bool = True) -> None:
        self.headless = headless
        self.browser: Browser | None = None
        self.playwright: Playwright | None = None

    async def new_context(self) -> BrowserContext:
        """Create a new browser context."""
        if not self.browser:
            raise BrowserNotInitializedError
        context: BrowserContext = await self.browser.new_context(
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
        await context.add_init_script(path=str(STEALTH_JS_PATH))
        return context

    async def __aenter__(self) -> "AsyncStealthBrowser":
        """Enter the asynchronous context manager."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=ARGS,
            chromium_sandbox=False,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the asynchronous context manager."""
        if self.playwright:
            await self.playwright.stop()


async def test_async_stealth_browser() -> None:
    """Test the async stealth browser."""
    async with AsyncStealthBrowser() as browser:
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://bot.sannysoft.com/")
        await page.wait_for_load_state("networkidle")

        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        screenshot_path = data_dir / "screenshot.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)

        html_path = data_dir / "index.html"
        html_path.write_text(await page.content(), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(test_async_stealth_browser())
