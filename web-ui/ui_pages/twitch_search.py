from selenium.webdriver.common.by import By

from ui_pages.base_page import BasePage


class TwitchSearchPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-a-target='tw-input']")
    SUGGESTION_CATEGORY_ANY = (By.CSS_SELECTOR, "a[href*='/directory/category/']")
    SUGGESTION_SEARCH_SELECTOR = "a[href^='/search?term=']"

    def __init__(self, driver):
        super().__init__(driver)
        self._last_query = None

    def search(self, query):
        """Enters a search query into the main search input."""
        self._last_query = query
        input_el = self.wait_visible(*self.SEARCH_INPUT, timeout=10)
        input_el.clear()
        input_el.send_keys(query)
        try:
            self.wait_visible(*self.SUGGESTION_CATEGORY_ANY, timeout=5)
        except Exception:
            self.wait_visible(By.CSS_SELECTOR, self.SUGGESTION_SEARCH_SELECTOR, timeout=5)

    def click_search_suggestion(self, query=None):
        """Clicks the suggestion that matches the provided query."""
        suggestions = self.driver.find_elements(*self.SUGGESTION_CATEGORY_ANY)
        if not suggestions:
            suggestions = self.driver.find_elements(By.CSS_SELECTOR, self.SUGGESTION_SEARCH_SELECTOR)
        if not suggestions:
            raise Exception("No search suggestions were found to click.")
        suggestions[0].click()
