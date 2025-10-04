from pages.base_page import BasePage
from playwright.sync_api import Page
import time


class TwitchHomePage(BasePage):
    """Twitch home page object"""

    URL = "https://www.twitch.tv"

    # Locators
    SEARCH_ICON = "a[aria-label='Search'],a[href='/directory']:has-text('Просмотр'), button[aria-label='Search'], [data-a-target='search-button']"
    SEARCH_INPUT = "input[type='search'], input[aria-label='Search Input']"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        """Open Twitch homepage"""
        self.navigate_to(self.URL)
        self.handle_modal_if_present()

    def click_search_icon(self):
        """Click on search icon"""
        self.click_element(self.SEARCH_ICON)

    def search_for_game(self, game_name: str):
        """Search for a specific game"""
        self.fill_input(self.SEARCH_INPUT, game_name)
        self.page.keyboard.press("Enter")
        time.sleep(2)


class TwitchSearchResultsPage(BasePage):
    """Twitch search results page object"""

    # Locators
    LIVE_CHANNELS_TAB = "a:has-text('Live Channels'), button:has-text('Live Channels')"
    STREAMER_CARD = "[data-a-target='preview-card-image-link'], a.tw-link[href*='/videos/']"

    def __init__(self, page: Page):
        super().__init__(page)

    def scroll_and_select_streamer(self, scroll_times: int = 2, streamer_index: int = 0):
        """Scroll down and select a streamer"""
        self.scroll_down(scroll_times)

        # Wait for streamers to load
        self.page.wait_for_selector(self.STREAMER_CARD, timeout=10000)

        # Get all visible streamer cards
        streamers = self.page.locator(self.STREAMER_CARD).all()

        if len(streamers) > streamer_index:
            streamers[streamer_index].click()
            time.sleep(2)
        else:
            # Fallback: click first available streamer
            self.page.locator(self.STREAMER_CARD).first.click()
            time.sleep(2)


class TwitchStreamerPage(BasePage):
    """Twitch streamer page object"""

    # Locators
    VIDEO_PLAYER = "video, [data-a-target='player-overlay-click-handler']"
    MATURE_CONTENT_BUTTON = "button[data-test-selector='muted-segments-alert-overlay-presentation__dismiss-button']"

    def __init__(self, page: Page):
        super().__init__(page)

    def wait_for_stream_load(self):
        """Wait for stream to fully load"""
        # Handle mature content warning if present
        try:
            if self.page.locator(self.MATURE_CONTENT_BUTTON).count() > 0:
                self.click_element(self.MATURE_CONTENT_BUTTON, timeout=3000)
        except:
            pass

        # Handle any other modals
        self.handle_modal_if_present()

        # Wait for video player to be visible
        self.page.wait_for_selector(self.VIDEO_PLAYER, timeout=15000)

        # Additional wait for stream to stabilize
        time.sleep(3)

        # Wait for network idle
        try:
            self.wait_for_page_load(timeout=10000)
        except:
            pass  # Some streams may continuously load

    def capture_screenshot(self, path: str):
        """Take screenshot of streamer page"""
        return self.take_screenshot(path)
