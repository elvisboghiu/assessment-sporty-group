from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_pages.base_page import BasePage


class TwitchResultsPage(BasePage):
    def select_streamer(self):
        """
        Selects a streamer from the visible results using a
        specific selector based on the page's HTML structure.
        """
        selectors = [
            (
                By.CSS_SELECTOR,
                "a[data-a-target='preview-card-image-link'],"
                "a[data-a-target='preview-card-title-link']",
            ),
            (By.CSS_SELECTOR, "article button[aria-label*='Live']"),
            (By.CSS_SELECTOR, "article a[href^='/']"),
        ]

        all_streamers = []
        for by, value in selectors:
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: len(d.find_elements(by, value)) > 0
                )
                all_streamers = self.driver.find_elements(by, value)
                if all_streamers:
                    break
            except Exception:
                continue

        if not all_streamers:
            raise Exception("No streamer links were found on the results page.")

        visible_streamers = [s for s in all_streamers if s.is_displayed()]

        if not visible_streamers:
            raise Exception("No visible streamer links were found on the page using the new selector.")

        # Filter out non-streamer navigation links.
        filtered_streamers = []
        for el in visible_streamers:
            href = (el.get_attribute("href") or "").lower()
            if href and "/directory" not in href and "/search" not in href:
                filtered_streamers.append(el)
        if filtered_streamers:
            visible_streamers = filtered_streamers

        # Select the streamer from the bottom of the visible list to avoid
        # repeatedly picking the same top entries after scrolling.
        target_streamer = visible_streamers[-1]

        # Scroll the element into view to ensure it's properly aligned and clickable.
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_streamer)

        # Wait for the element to be clickable and then click it.
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(target_streamer)).click()
        except Exception:
            # Use a JavaScript click as a fallback if the standard click fails.
            self.driver.execute_script("arguments[0].click();", target_streamer)
