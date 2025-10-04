import logging

import pytest
import os
from playwright.sync_api import Page
from pages.twitch_pages import TwitchHomePage, TwitchSearchResultsPage, TwitchStreamerPage


class TestTwitchSearch:
    """Test suite for Twitch search functionality"""

    @pytest.mark.parametrize("game_name,scroll_times,streamer_index", [
        ("StarCraft II", 2, 0),
        ("StarCraft II", 2, 1),
        ("StarCraft II", 2, 2),
    ])
    def test_search_and_capture_streamer(
        self,
        page: Page,
        screenshot_path: str,
        game_name: str,
        scroll_times: int,
        streamer_index: int
    ):
        # Initialize page objects
        home_page = TwitchHomePage(page)
        search_results = TwitchSearchResultsPage(page)
        streamer_page = TwitchStreamerPage(page)
        # Step 1: Go to Twitch
        home_page.open()
        assert "twitch.tv" in page.url, "Failed to navigate to Twitch"
        # Step 2: Click search icon
        home_page.click_search_icon()

        # Step 3: Input game name
        home_page.search_for_game(game_name)

        # Step 4-5: Scroll and select streamer
        search_results.scroll_and_select_streamer(
            scroll_times=scroll_times,
            streamer_index=streamer_index
        )

        # Step 6: Wait for stream load and take screenshot
        streamer_page.wait_for_stream_load()

        # Modify screenshot path to include test parameters
        base_name = os.path.splitext(screenshot_path)[0]
        unique_path = f"{base_name}_streamer{streamer_index}.png"

        screenshot_file = streamer_page.capture_screenshot(unique_path)

        # Validations
        assert os.path.exists(screenshot_file), "Screenshot was not created"
        assert os.path.getsize(screenshot_file) > 0, "Screenshot file is empty"
        assert "twitch.tv" in page.url, "Not on Twitch domain"

        logging.info(f" Test passed! Screenshot saved: {screenshot_file}")

    def test_search_basic_flow(self, page: Page, screenshot_path: str):
        home_page = TwitchHomePage(page)
        search_results = TwitchSearchResultsPage(page)
        streamer_page = TwitchStreamerPage(page)

        # Execute test steps
        home_page.open()
        assert "twitch.tv" in page.url, "Failed to navigate to Twitch"
        logging.info(f"Page is successfully displayed")

        home_page.click_search_icon()
        assert page.is_visible(home_page.SEARCH_INPUT), "Search input is not visible after clicking search icon"
        logging.info("Search icon clicked and input visible")

        home_page.search_for_game("StarCraft II")
        assert page.is_visible(home_page.SEARCH_INPUT), "Search input is not visible after clicking search icon"
        logging.info("Search icon clicked and input visible")

        search_results.scroll_and_select_streamer(scroll_times=2, streamer_index=0)
        streamer_page.wait_for_stream_load()
        assert page.is_visible(streamer_page.VIDEO_PLAYER), "Video player not visible"
        logging.info("Streamer selected and page navigated")

        screenshot_file = streamer_page.capture_screenshot(screenshot_path)
        # Comprehensive validations
        assert os.path.exists(screenshot_file), "Screenshot file was not created"
        file_size = os.path.getsize(screenshot_file)
        assert file_size > 10000, f"Screenshot file too small ({file_size} bytes), may be invalid"
        assert "twitch.tv" in page.url, "Not on Twitch domain"
        assert (
            page.is_visible("video")
            or page.is_visible("[data-a-target='player-overlay-click-handler']")
        ), "Video player not found on page"

        logging.info(f"Basic flow test passed! Screenshot: {screenshot_file} ({file_size} bytes)")
