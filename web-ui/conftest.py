import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def screenshots_dir():
    base = Path(__file__).parent / "screenshots"
    base.mkdir(parents=True, exist_ok=True)
    return base


@pytest.fixture(scope="session")
def base_url():
    return "https://www.twitch.tv"


@pytest.fixture(scope="session")
def chrome_driver_path():
    return os.getenv("CHROMEDRIVER_PATH")


@pytest.fixture(scope="session")
def headless():
    return os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}


@pytest.fixture(scope="function")
def mobile_device_name(request):
    return getattr(request, "param", os.getenv("MOBILE_DEVICE_NAME"))


@pytest.fixture(scope="function")
def mobile_emulation_config(mobile_device_name):
    if mobile_device_name:
        return {"deviceName": mobile_device_name}

    width = int(os.getenv("MOBILE_WIDTH", "393"))
    height = int(os.getenv("MOBILE_HEIGHT", "851"))
    pixel_ratio = float(os.getenv("MOBILE_PIXEL_RATIO", "3"))
    user_agent = os.getenv(
        "MOBILE_USER_AGENT",
        "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    )
    return {
        "deviceMetrics": {"width": width, "height": height, "pixelRatio": pixel_ratio},
        "userAgent": user_agent,
    }


@pytest.fixture(scope="function")
def driver(headless, mobile_emulation_config, chrome_driver_path):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--remote-debugging-port=0")
    options.add_experimental_option("mobileEmulation", mobile_emulation_config)

    print("Starting Chrome driver", flush=True)
    if chrome_driver_path:
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    print("Chrome driver started", flush=True)

    driver.set_page_load_timeout(45)
    yield driver
    driver.quit()
