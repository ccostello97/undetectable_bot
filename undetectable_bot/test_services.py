import asyncio
import logging
from pathlib import Path
from typing import Final

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Page

from undetectable_bot.async_api import AsyncStealthBrowser

logger = logging.getLogger(__name__)

TEST_SERVICES: Final[dict[str, str]] = {
    "bot_sannysoft": "https://bot.sannysoft.com/",
}


async def save_page_content(
    page: Page, service_name: str, data_dir: Path
) -> None:
    """Save page content and screenshot for a test service."""
    service_dir = data_dir / service_name
    service_dir.mkdir(exist_ok=True)

    # Save screenshot
    screenshot_path = service_dir / "screenshot.png"
    await page.screenshot(path=str(screenshot_path), full_page=True)

    # Save HTML content
    html_path = service_dir / "index.html"
    html_path.write_text(await page.content(), encoding="utf-8")


async def test_service(
    page: Page, service_name: str, url: str, data_dir: Path
) -> None:
    """Test a single service and save results."""
    logger.info("Testing %s...", service_name)
    await page.goto(url)
    await page.wait_for_load_state("networkidle")
    await save_page_content(page, service_name, data_dir)
    logger.info("Completed %s", service_name)


async def test_all_services() -> None:
    """Test all browser detection services."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    async with AsyncStealthBrowser() as browser:
        context = await browser.new_context()
        page = await context.new_page()

        for service_name, url in TEST_SERVICES.items():
            try:
                await test_service(page, service_name, url, data_dir)
            except PlaywrightError:
                logger.exception("Error testing %s", service_name)

        await page.close()


if __name__ == "__main__":
    asyncio.run(test_all_services())
