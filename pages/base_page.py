from playwright.sync_api import Page, expect
import time


class BasePage:
    """Base page class with common methods"""

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a specific URL"""
        self.page.goto(url, wait_until="domcontentloaded")
        time.sleep(1)

    def click_element(self, selector: str, timeout: int = 10000):
        """Click on an element with explicit wait"""
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.click()
        time.sleep(0.5)

    def fill_input(self, selector: str, text: str):
        """Fill input field"""
        element = self.page.locator(selector)
        element.wait_for(state="visible")
        element.fill(text)
        time.sleep(0.5)

    def scroll_down(self, times: int = 1):
        """Scroll down the page"""
        for _ in range(times):
            self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            time.sleep(1)  # Wait for content to load

    def take_screenshot(self, path: str):
        """Take a screenshot"""
        self.page.screenshot(path=path, full_page=True)
        return path

    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for page to fully load"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def handle_modal_if_present(self):
        """Handle modal/popup if it appears"""
        modal_selectors = [
            "button[data-a-target='consent-banner-accept']",
            "button[aria-label='Close']",
            "button:has-text('Accept')",
            "button:has-text('Close')",
            "[data-a-target='player-overlay-mature-accept']",
            "button.consent-banner-button"
        ]

        for selector in modal_selectors:
            try:
                if self.page.locator(selector).count() > 0:
                    self.page.locator(selector).first.click(timeout=3000)
                    time.sleep(1)
            except:
                continue
