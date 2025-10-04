import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import os
from datetime import datetime


@pytest.fixture(scope="session")
def playwright():
    """Playwright instance - create once per test session"""
    with sync_playwright() as p:
        yield p
    # Playwright automatically closes when exiting 'with' block


@pytest.fixture(scope="session")
def browser(playwright):
    """
    Browser fixture using Chromium (Google Chrome engine)
    Required for: "Mobile emulator from Google Chrome"
    """
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
        args=[
            "--start-maximized",
            "--autoplay-policy=no-user-gesture-required",
            "--disable-web-security",
        ]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, playwright):

    # Use Google Pixel device - authentic Chrome Mobile emulation
    device = playwright.devices['iPhone 13 Pro']

    # Create context with Google Chrome mobile emulation
    context = browser.new_context(**device)

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Page instance for each test"""
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 seconds timeout
    yield page
    page.close()


@pytest.fixture(scope="session", autouse=True)
def setup_screenshots_dir():
    """Create screenshots directory if it doesn’t exist"""
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    return screenshots_dir


@pytest.fixture
def screenshot_path(setup_screenshots_dir):
    """Generate unique screenshot path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(setup_screenshots_dir, f"streamer_{timestamp}.png")
