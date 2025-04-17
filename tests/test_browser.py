from playwright.sync_api import Page


def test_stealth_browser(page: Page) -> None:
    """Test that the stealth browser successfully evades detection."""
    # Navigate to the bot detection test page
    page.goto("https://bot.sannysoft.com")
    page.wait_for_load_state("networkidle")

    # Get all test results
    test_results: dict[str, str] = {}

    # Basic tests
    test_results["User Agent"] = (
        page.locator("#user-agent-result").text_content() or ""
    )
    test_results["WebDriver"] = (
        page.locator("#webdriver-result").text_content() or ""
    )
    test_results["WebDriver Advanced"] = (
        page.locator("#advanced-webdriver-result").text_content() or ""
    )
    test_results["Chrome"] = (
        page.locator("#chrome-result").text_content() or ""
    )
    test_results["Permissions"] = (
        page.locator("#permissions-result").text_content() or ""
    )
    test_results["Plugins Length"] = (
        page.locator("#plugins-length-result").text_content() or ""
    )
    test_results["Plugins Type"] = (
        page.locator("#plugins-type-result").text_content() or ""
    )
    test_results["Languages"] = (
        page.locator("#languages-result").text_content() or ""
    )
    test_results["WebGL Vendor"] = (
        page.locator("#webgl-vendor").text_content() or ""
    )
    test_results["WebGL Renderer"] = (
        page.locator("#webgl-renderer").text_content() or ""
    )
    test_results["Broken Image"] = (
        page.locator("#broken-image-dimensions").text_content() or ""
    )

    # Verify test results
    assert "Chrome/120.0.0.0" in test_results["User Agent"], (
        "User agent should be Chrome 120"
    )
    assert "missing (passed)" in test_results["WebDriver"], (
        "WebDriver should not be detected"
    )
    assert "passed" in test_results["WebDriver Advanced"], (
        "Advanced WebDriver check should pass"
    )
    assert "present (passed)" in test_results["Chrome"], (
        "Chrome object should be present"
    )
    assert "granted" in test_results["Permissions"], (
        "Permissions should be granted"
    )
    assert "3" in test_results["Plugins Length"], "Should have 3 plugins"
    assert "passed" in test_results["Plugins Type"], (
        "Plugins type should be correct"
    )
    assert "en-US" in test_results["Languages"], "Language should be en-US"
    assert "Intel Inc." in test_results["WebGL Vendor"], (
        "WebGL vendor should be Intel"
    )
    assert "Intel HD Graphics 4000" in test_results["WebGL Renderer"], (
        "WebGL renderer should be Intel HD Graphics"
    )
    assert "16x16" in test_results["Broken Image"], (
        "Broken image dimensions should be 16x16"
    )

    # Get Fingerprint Scanner results
    fp_rows = page.locator("#fp2 tr")
    fp_count = fp_rows.count()

    for i in range(fp_count):
        row = fp_rows.nth(i)
        test_name = row.locator("td").nth(0).text_content() or ""
        test_result = row.locator("td").nth(1).text_content() or ""
        test_results[f"FP_{test_name}"] = test_result

    # Verify Fingerprint Scanner results
    fp_tests = [
        "PHANTOM_UA",
        "PHANTOM_PROPERTIES",
        "PHANTOM_ETSL",
        "PHANTOM_LANGUAGE",
        "PHANTOM_WEBSOCKET",
        "MQ_SCREEN",
        "PHANTOM_OVERFLOW",
        "PHANTOM_WINDOW_HEIGHT",
        "HEADCHR_UA",
        "HEADCHR_CHROME_OBJ",
        "HEADCHR_PERMISSIONS",
        "HEADCHR_PLUGINS",
        "HEADCHR_IFRAME",
        "CHR_DEBUG_TOOLS",
        "SELENIUM_DRIVER",
        "CHR_BATTERY",
        "CHR_MEMORY",
        "TRANSPARENT_PIXEL",
        "SEQUENTUM",
        "VIDEO_CODECS",
    ]

    for test in fp_tests:
        assert test_results.get(f"FP_{test}") == "ok", (
            f"Fingerprint test {test} should pass"
        )
