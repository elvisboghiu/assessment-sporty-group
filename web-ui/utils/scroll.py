import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def scroll_down(driver, times=1, pause=0.6):
    for _ in range(times):
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(pause)
