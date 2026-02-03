import pytest

from web_ui.ui_pages.twitch_home import TwitchHomePage
from web_ui.ui_pages.twitch_results import TwitchResultsPage
from web_ui.ui_pages.twitch_search import TwitchSearchPage
from web_ui.ui_pages.twitch_streamer import TwitchStreamerPage
from web_ui.utils.scroll import scroll_down
from web_ui.utils.screenshot import save_screenshot


@pytest.mark.parametrize(
    "mobile_device_name",
    ["Pixel 7", "iPhone 14 Pro Max"],
    indirect=True,
)
def test_twitch_search_and_open_streamer(driver, base_url, screenshots_dir, mobile_device_name):
    home = TwitchHomePage(driver)
    search = TwitchSearchPage(driver)
    results = TwitchResultsPage(driver)
    streamer = TwitchStreamerPage(driver)

    print("\n[STEP 1] Open Twitch homepage")
    home.open_home(base_url)
    
    print("[STEP 2] Accept consent pop-up if present")
    home.accept_consent_if_present()
    
    print("[STEP 3] Navigate to the search page")
    home.open_search(base_url)

    print("[STEP 4] Search for 'StarCraft II'")
    search.search("StarCraft II")
    
    print("[STEP 5] Click the 'StarCraft II' category suggestion")
    search.click_search_suggestion()

    print("[STEP 6] Scroll down the results page")
    scroll_down(driver, times=2, pause=1)

    print("[STEP 7] Select the first available streamer")
    results.select_streamer()
    
    print("[STEP 8] Wait for the streamer's page to load")
    print(f"  - Streamer URL: {driver.current_url}", flush=True)
    streamer.wait_for_loaded()

    print("[STEP 9] Save a screenshot of the final page")
    save_screenshot(driver, screenshots_dir, name_prefix="streamer_page", device_name=mobile_device_name)
