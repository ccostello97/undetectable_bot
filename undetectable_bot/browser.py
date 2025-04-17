from pathlib import Path

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


def create_data_dir() -> Path:
    """Create data directory if it doesn't exist."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir


def launch_stealth_browser() -> None:
    """Launch a stealth browser with anti-detection measures."""
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(
            headless=True,  # Run in headless mode
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-dev-shm-usage",
                "--ignore-gpu-blocklist",
                "--enable-gpu",
                "--use-gl=egl",  # Use EGL instead of desktop GL for better headless support
                "--enable-webgl",
                "--enable-webgl2",
                "--enable-accelerated-2d-canvas",
                "--enable-accelerated-video-decode",
                "--enable-accelerated-video-encode",
                "--enable-native-gpu-memory-buffers",
                "--enable-gpu-rasterization",
                "--enable-zero-copy",
                "--disable-software-rasterizer",  # Force hardware acceleration
                "--force-gpu-rasterization",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            chromium_sandbox=False,
        )

        # Create stealth context
        context: BrowserContext = browser.new_context(
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

        # Add stealth script from file
        context.add_init_script(path="undetectable_bot/js/stealth.js")

        # Create new page
        page: Page = context.new_page()

        try:
            # Navigate to test page
            page.goto("https://bot.sannysoft.com/")
            page.wait_for_load_state("networkidle")

            # Create data directory
            data_dir = create_data_dir()

            # Save screenshot
            screenshot_path = data_dir / "screenshot.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

            # Save HTML
            html_path = data_dir / "index.html"
            html_path.write_text(page.content(), encoding="utf-8")

        finally:
            page.close()
            context.close()
            browser.close()


if __name__ == "__main__":
    launch_stealth_browser()
