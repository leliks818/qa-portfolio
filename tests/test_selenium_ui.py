import pytest
from selenium.webdriver.common.by import By

from pages.the_internet.login_page import LoginPage


@pytest.mark.ui
def test_selenium_login_success(driver, base_url):
    page = LoginPage(driver=driver, base_url=base_url)
    page.open()
    page.login("tomsmith", "SuperSecretPassword!")

    flash = page.flash_text()
    assert "You logged into a secure area!" in flash
