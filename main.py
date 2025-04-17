"""Module for launching a stealth browser using Playwright."""

import json
import logging
from pathlib import Path

from playwright.sync_api import sync_playwright

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def launch_stealth_browser() -> None:
    """Launch a browser with stealth configurations to avoid detection.

    This function sets up a Chromium browser with various anti-detection
    measures and takes a screenshot of the bot detection test page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Use False if you want to visually debug
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--window-size=1280,800",
            ],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            timezone_id="America/New_York",
            geolocation={"longitude": -74.0060, "latitude": 40.7128},
            permissions=["geolocation", "notifications"],
            viewport={"width": 1280, "height": 800},
        )

        page = context.new_page()

        # 🛠 Enhanced stealth patches
        stealth_js = """
        // Improved WebDriver removal
        delete Object.getPrototypeOf(navigator).webdriver;

        // Pass the Chrome test with complete implementation
        const makeChrome = () => {
            const chrome = {
                app: {
                    InstallState: {
                        DISABLED: 'disabled',
                        INSTALLED: 'installed',
                        NOT_INSTALLED: 'not_installed'
                    },
                    RunningState: {
                        CANNOT_RUN: 'cannot_run',
                        READY_TO_RUN: 'ready_to_run',
                        RUNNING: 'running'
                    },
                    getDetails: function() {},
                    getIsInstalled: function() { return false; },
                    installState: function() { return 'not_installed'; },
                    isInstalled: false,
                    runningState: function() { return 'cannot_run'; }
                },
                runtime: {
                    OnInstalledReason: {
                        CHROME_UPDATE: 'chrome_update',
                        INSTALL: 'install',
                        UPDATE: 'update'
                    },
                    OnRestartRequiredReason: {
                        APP_UPDATE: 'app_update',
                        OS_UPDATE: 'os_update',
                        PERIODIC: 'periodic'
                    },
                    PlatformArch: {
                        ARM: 'arm',
                        X86_32: 'x86-32',
                        X86_64: 'x86-64'
                    },
                    PlatformNaclArch: {
                        ARM: 'arm',
                        X86_32: 'x86-32',
                        X86_64: 'x86-64'
                    },
                    PlatformOs: {
                        ANDROID: 'android',
                        CROS: 'cros',
                        LINUX: 'linux',
                        MAC: 'mac',
                        WIN: 'win'
                    },
                    RequestUpdateCheckStatus: {
                        NO_UPDATE: 'no_update',
                        THROTTLED: 'throttled',
                        UPDATE_AVAILABLE: 'update_available'
                    },
                    connect: function() {},
                    id: undefined,
                    reload: function() {},
                    requestUpdateCheck: function() {},
                    restart: function() {},
                    sendMessage: function() {},
                    setUninstallURL: function() {},
                    requestFileSystem: function() {},
                    getPackageDirectoryEntry: function() {}
                },
                csi: function() { return {}; },
                loadTimes: function() { return {}; }
            };
            return chrome;
        };
        window.chrome = makeChrome();

        // Improved Plugins implementation with proper prototype chain
        const makePluginArray = () => {
            // Create a proper array-like object
            const pluginArray = Object.create(PluginArray.prototype);

            const makePlugin = (name, filename, desc, suffixes, type) => {
                const plugin = Object.create(Plugin.prototype);
                Object.defineProperties(plugin, {
                    '0': {
                        value: { type, suffixes, description: desc },
                        enumerable: true
                    },
                    'description': {
                        value: desc,
                        enumerable: true
                    },
                    'filename': {
                        value: filename,
                        enumerable: true
                    },
                    'name': {
                        value: name,
                        enumerable: true
                    },
                    'length': {
                        value: 1,
                        enumerable: true
                    }
                });

                return plugin;
            };

            // Create the plugins with line breaks for readability
            const plugins = [
                makePlugin(
                    'Chrome PDF Plugin',
                    'internal-pdf-viewer',
                    'Portable Document Format',
                    'pdf',
                    'application/pdf'
                ),
                makePlugin(
                    'Chrome PDF Viewer',
                    'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                    'Portable Document Format',
                    'pdf',
                    'application/pdf'
                ),
                makePlugin(
                    'Native Client',
                    'internal-nacl-plugin',
                    '',
                    '',
                    'application/x-nacl'
                )
            ];

            // Add plugins to the array-like object
            plugins.forEach((plugin, i) => {
                Object.defineProperty(pluginArray, i, {
                    value: plugin,
                    enumerable: true
                });
            });

            // Add required properties
            Object.defineProperties(pluginArray, {
                'length': {
                    value: plugins.length,
                    enumerable: true
                },
                'item': {
                    value: function(index) {
                        return this[index] || null;
                    },
                    enumerable: false
                },
                'namedItem': {
                    value: function(name) {
                        return Array.prototype.find.call(
                            this,
                            p => p.name === name
                        ) || null;
                    },
                    enumerable: false
                },
                'refresh': {
                    value: function() {},
                    enumerable: false
                }
            });

            return pluginArray;
        };

        // Replace the plugins property with our enhanced version
        Object.defineProperty(navigator, 'plugins', {
            get: () => makePluginArray(),
            enumerable: true,
            configurable: true
        });

        // Pass the Languages test
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
            enumerable: true,
            configurable: true
        });

        // Pass the Window/Viewport tests with randomization
        const randInt = (min, max) => (
            Math.floor(Math.random() * (max - min + 1)) + min
        );

        const originalInnerHeight = window.innerHeight;
        const originalOuterHeight = window.outerHeight + randInt(0, 10);
        const originalInnerWidth = window.innerWidth;
        const originalOuterWidth = window.outerWidth + randInt(0, 10);

        Object.defineProperties(window, {
            innerHeight: {
                get: () => originalInnerHeight,
                configurable: true
            },
            outerHeight: {
                get: () => originalOuterHeight,
                configurable: true
            },
            innerWidth: {
                get: () => originalInnerWidth,
                configurable: true
            },
            outerWidth: {
                get: () => originalOuterWidth,
                configurable: true
            },
            devicePixelRatio: {
                get: () => 1 + (Math.random() * 0.1)
            }
        });

        // Enhanced Canvas Fingerprinting protection with unique noise
        const canvasNoise = new WeakMap();

        const getNoisePattern = (canvas) => {
            if (!canvasNoise.has(canvas)) {
                const pattern = new Uint8Array(256);
                for (let i = 0; i < 256; i++) {
                    pattern[i] = Math.floor(Math.random() * 3);  // 0, 1, or 2
                }
                canvasNoise.set(canvas, pattern);
            }
            return canvasNoise.get(canvas);
        };

        const originalGetContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type) {
            const context = originalGetContext.apply(this, arguments);
            if (type === '2d') {
                const noisePattern = getNoisePattern(this);
                const originalGetImageData = context.getImageData;
                context.getImageData = function() {
                    const imageData = originalGetImageData.apply(
                        this,
                        arguments
                    );
                    // Add consistent but unique noise per canvas
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        const noiseIndex = (i/4) % 256;
                        const noise = noisePattern[noiseIndex];
                        imageData.data[i] += noise;     // Red
                        imageData.data[i + 1] += noise; // Green
                        imageData.data[i + 2] += noise; // Blue
                    }
                    return imageData;
                };

                // Add subtle variations to other canvas operations
                const originalFillRect = context.fillRect;
                context.fillRect = function() {
                    const args = Array.from(arguments);
                    const noise = (
                        noisePattern[(Math.random() * 256) | 0] * 0.1
                    );
                    args[0] += noise;
                    args[1] += noise;
                    return originalFillRect.apply(this, args);
                };

                // Add noise to other drawing operations
                const drawingOps = [
                    'fillText',
                    'strokeText',
                    'lineTo',
                    'bezierCurveTo'
                ];
                drawingOps.forEach(method => {
                    if (context[method]) {
                        const original = context[method];
                        context[method] = function() {
                            const args = Array.from(arguments);
                            const noise = (
                                noisePattern[(Math.random() * 256) | 0] * 0.1
                            );
                            if (typeof args[0] === 'number') args[0] += noise;
                            if (typeof args[1] === 'number') args[1] += noise;
                            return original.apply(this, args);
                        };
                    }
                });
            }
            return context;
        };

        // Fix for Notification permission
        if (window.Notification &&
            window.Notification.permission !== 'granted') {
            Object.defineProperty(window.Notification, 'permission', {
                get: () => 'granted'
            });
        }
        """
        page.add_init_script(stealth_js)

        # Optional: test fingerprint status
        page.goto("https://bot.sannysoft.com/")

        # Take a full page screenshot
        page.screenshot(
            path="stealth_check_full.png",
            full_page=True,  # This captures the entire scrollable page
        )

        # Save the page HTML
        html_content = page.content()
        html_path = Path("stealth_check.html")
        html_path.write_text(html_content, encoding="utf-8")

        # Extract test results
        test_results = page.evaluate("""
            () => {
                const results = {};
                // Get all test rows
                const rows = document.querySelectorAll('tr');
                rows.forEach(row => {
                    const testName = row.querySelector(
                        'td:first-child'
                    )?.textContent.trim();
                    const result = row.querySelector(
                        'td:last-child'
                    )?.textContent.trim();
                    if (testName && result) {
                        results[testName] = result;
                    }
                });
                return results;
            }
        """)

        # Save test results as JSON
        results_path = Path("stealth_check_results.json")
        results_path.write_text(
            json.dumps(test_results, indent=2), encoding="utf-8"
        )

        logger.info("Page title: %s", page.title())
        logger.info("Test results saved to stealth_check_results.json")
        browser.close()


if __name__ == "__main__":
    launch_stealth_browser()
