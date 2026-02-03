from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class TwitchStreamerPage(BasePage):
    def wait_for_loaded(self, timeout=15):
        """
        Waits for the main content of the streamer page to be visible.
        A shorter timeout is used because we are waiting for a single, reliable element.
        """
        # First, handle any pop-ups that might block the main content
        self.accept_consent_if_present(timeout=10)

        # Wait for the <main> element
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "main"))
            )
            return True
        except Exception:
            print("Warning: Streamer page main content did not load within the timeout.", flush=True)
            return False
