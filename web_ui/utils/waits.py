from selenium.webdriver.support.ui import WebDriverWait


def wait_for_any(driver, conditions, timeout=20):
    if not conditions:
        raise TimeoutError("No conditions provided to wait_for_any")

    def _any_condition(drv):
        for condition in conditions:
            try:
                value = condition(drv)
                if value:
                    return value
            except Exception:  # noqa: BLE001
                continue
        return False

    return WebDriverWait(driver, timeout).until(_any_condition)
