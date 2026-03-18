import os
import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

# PyCharm runs pytest with the working directory set to `tests/` by default.
# Ensure the repo root is on sys.path so imports like `from pages...` work.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _is_headless() -> bool:
    # HEADLESS=0 disables headless mode.
    return os.getenv("HEADLESS", "1") != "0"


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://the-internet.herokuapp.com")


# pytest-playwright configuration fixtures:
@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": _is_headless()}


@pytest.fixture(scope="session")
def browser_context_args(base_url: str):
    # base_url is used by page.goto("/path") in playwright.
    return {"base_url": base_url, "viewport": {"width": 1280, "height": 720}}


@pytest.fixture()
def driver():
    options = ChromeOptions()
    if _is_headless():
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")

    # Selenium Manager downloads the right driver automatically on modern Selenium.
    drv = webdriver.Chrome(options=options)
    try:
        yield drv
    finally:
        drv.quit()
