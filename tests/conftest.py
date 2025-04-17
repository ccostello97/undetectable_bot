from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


@pytest.fixture(scope="function")
def browser() -> Generator[Browser]:
    """Create a stealth browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-dev-shm-usage",
                "--ignore-gpu-blocklist",
                "--enable-gpu",
                "--use-gl=egl",
                "--enable-webgl",
                "--enable-webgl2",
                "--enable-accelerated-2d-canvas",
                "--enable-accelerated-video-decode",
                "--enable-accelerated-video-encode",
                "--enable-native-gpu-memory-buffers",
                "--enable-gpu-rasterization",
                "--enable-zero-copy",
                "--disable-software-rasterizer",
                "--force-gpu-rasterization",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            chromium_sandbox=False,
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext]:
    """Create a stealth browser context."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        color_scheme="dark",
        locale="en-US",
        timezone_id="America/New_York",
        permissions=["notifications"],
        java_script_enabled=True,
        bypass_csp=True,
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        },
    )
    # Add stealth script
    context.add_init_script(path="undetectable_bot/js/stealth.js")
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page]:
    """Create a new page in the stealth browser context."""
    page = context.new_page()
    yield page
    page.close()
