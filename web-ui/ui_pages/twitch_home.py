from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ui_pages.base_page import BasePage


class TwitchHomePage(BasePage):
    SEARCH_ICON = (By.CSS_SELECTOR, "a[href='/directory']")

    def open_home(self, base_url):
        self.open(base_url)

    def open_search(self, base_url=None):
        """Clicks the search/browse icon to navigate to the search page."""
        wait = WebDriverWait(self.driver, 10)
        search_button = wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
        try:
            search_button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", search_button)
