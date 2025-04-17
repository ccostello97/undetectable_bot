from pathlib import Path

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


def launch_stealth_browser(*, headless: bool = True) -> None:
    """Launch a stealth browser with anti-detection measures."""
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-infobars",
                "--disable-blink-features=AutomationControlled",
                "--ignore-certificate-errors",
                "--ignore-certificate-errors-spki-list",
                "--disable-web-security",
                "--allow-running-insecure-content",
                "--disable-domain-reliability",
                "--disable-features=WebRtcHideLocalIpsWithMdns",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-extensions",
                "--window-position=0,0",
                "--disable-features=VizDisplayCompositor",
                "--mute-audio",
                "--disable-features=IsolateOrigins,site-per-process",
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
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)

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
