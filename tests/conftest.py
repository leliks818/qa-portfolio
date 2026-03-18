import os
import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait

try:
    import allure
    from allure_commons.types import AttachmentType

    _HAVE_ALLURE = True
except Exception:  # pragma: no cover
    allure = None
    AttachmentType = None
    _HAVE_ALLURE = False

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


@pytest.fixture(scope="session")
def driver():
    options = ChromeOptions()
    if _is_headless():
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # Selenium Manager downloads the right driver automatically on modern Selenium.
    drv = webdriver.Chrome(options=options)
    drv.set_page_load_timeout(30)
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture(autouse=True)
def _selenium_test_cleanup(request):
    """Keep Selenium tests isolated even when using a session-scoped driver.

    If a test uses the `driver` fixture:
    - close stray alerts
    - close extra windows/tabs
    - clear cookies/storage
    """

    yield

    drv = request.node.funcargs.get("driver")
    if not drv:
        return

    # Dismiss unexpected alerts to avoid blocking the next test.
    try:
        WebDriverWait(drv, 0.5).until(lambda d: d.switch_to.alert)
        try:
            drv.switch_to.alert.accept()
        except Exception:
            try:
                drv.switch_to.alert.dismiss()
            except Exception:
                pass
    except Exception:
        pass

    # Close extra tabs/windows and return to the first handle.
    try:
        handles = list(drv.window_handles)
        if handles:
            keep = handles[0]
            for h in handles[1:]:
                try:
                    drv.switch_to.window(h)
                    drv.close()
                except Exception:
                    pass
            try:
                drv.switch_to.window(keep)
            except Exception:
                pass
    except Exception:
        pass

    try:
        drv.delete_all_cookies()
    except Exception:
        pass

    # Best-effort local/session storage cleanup on the current origin.
    try:
        drv.execute_script("window.localStorage && window.localStorage.clear();")
        drv.execute_script("window.sessionStorage && window.sessionStorage.clear();")
    except Exception:
        pass


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or rep.passed:
        return

    if not _HAVE_ALLURE:
        return

    drv = item.funcargs.get("driver")
    if not drv:
        return

    try:
        allure.attach(
            drv.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=AttachmentType.PNG,
        )
    except WebDriverException:
        pass

    try:
        allure.attach(
            drv.page_source,
            name="page_source",
            attachment_type=AttachmentType.HTML,
        )
    except WebDriverException:
        pass

    try:
        allure.attach(
            drv.current_url,
            name="current_url",
            attachment_type=AttachmentType.TEXT,
        )
    except WebDriverException:
        pass

    try:
        logs = drv.get_log("browser")
        if logs:
            text = "\n".join(f"{e.get('level')}: {e.get('message')}" for e in logs)
            allure.attach(text, name="browser_console", attachment_type=AttachmentType.TEXT)
    except Exception:
        # Some driver builds do not support log retrieval.
        pass
