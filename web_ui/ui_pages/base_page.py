from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from web_ui.utils.waits import wait_for_any


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def wait_visible(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    def wait_clickable(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))

    def click(self, by, value, timeout=10):
        el = self.wait_clickable(by, value, timeout)
        el.click()
        return el

    def type(self, by, value, text, timeout=10):
        el = self.wait_visible(by, value, timeout)
        el.clear()
        el.send_keys(text)
        return el

    def accept_consent_if_present(self, timeout=5):
        selectors = [
            (By.CSS_SELECTOR, "button[data-a-target='consent-banner-accept']"),
            (By.CSS_SELECTOR, "button[data-a-target='consent-banner-confirm']"),
        ]

        def _try_click_in_context():
            conditions = [EC.element_to_be_clickable((by, value)) for by, value in selectors]
            try:
                el = wait_for_any(self.driver, conditions, timeout=timeout)
                el.click()
                return True
            except TimeoutException:
                return False

        if _try_click_in_context():
            return True

        iframe_selectors = [
            "iframe[id*='consent']",
            "iframe[id*='privacy']",
            "iframe[name*='sp_message']",
            "iframe[src*='consent']",
            "iframe[src*='privacy']",
        ]
        for selector in iframe_selectors:
            frames = self.driver.find_elements(By.CSS_SELECTOR, selector)
            for frame in frames:
                try:
                    self.driver.switch_to.frame(frame)
                    if _try_click_in_context():
                        self.driver.switch_to.default_content()
                        return True
                finally:
                    self.driver.switch_to.default_content()
        return False
