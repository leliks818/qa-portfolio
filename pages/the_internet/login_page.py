from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class LoginPage(TheInternetPage):
    PATH = "/login"

    _username = (By.ID, "username")
    _password = (By.ID, "password")
    _submit = (By.CSS_SELECTOR, "button[type='submit']")
    _flash = (By.ID, "flash")

    def login(self, username: str, password: str) -> None:
        self.type(self._username, username)
        self.type(self._password, password)
        self.click(self._submit)

    def flash_text(self) -> str:
        return self.wait_visible(self._flash).text
