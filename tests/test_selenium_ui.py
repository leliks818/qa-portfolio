import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


@pytest.mark.ui
def test_selenium_login_success(driver, base_url):
    page = BasePage(driver=driver, base_url=base_url)
    page.open("/login")

    page.type((By.ID, "username"), "tomsmith")
    page.type((By.ID, "password"), "SuperSecretPassword!")
    page.click((By.CSS_SELECTOR, "button[type='submit']"))

    flash = page.find((By.ID, "flash")).text
    assert "You logged into a secure area!" in flash

