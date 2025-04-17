from collections.abc import Sequence
from pathlib import Path
from typing import Literal, TypedDict

from playwright.sync_api import ViewportSize

USER_AGENT: str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

EXTRA_HTTP_HEADERS: dict[str, str] = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

ColorScheme = Literal["dark", "light", "no-preference", "null"]


class ContextSettings(TypedDict):
    viewport: ViewportSize
    user_agent: str
    color_scheme: ColorScheme
    locale: str
    timezone_id: str
    permissions: Sequence[str]
    java_script_enabled: bool
    bypass_csp: bool
    extra_http_headers: dict[str, str]


CONTEXT_SETTINGS: ContextSettings = {
    "viewport": {"width": 1920, "height": 1080},
    "user_agent": USER_AGENT,
    "color_scheme": "dark",
    "locale": "en-US",
    "timezone_id": "America/New_York",
    "permissions": ["notifications"],
    "java_script_enabled": True,
    "bypass_csp": True,
    "extra_http_headers": EXTRA_HTTP_HEADERS,
}

ARGS = [
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
]

STEALTH_JS_PATH: Path = Path(__file__).parent.parent / "js" / "stealth.js"
