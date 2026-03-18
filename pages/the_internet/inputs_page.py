from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class InputsPage(TheInternetPage):
    PATH = "/inputs"

    _input = (By.TAG_NAME, "input")

    def set_value(self, value: str) -> None:
        self.type(self._input, value)

    def value(self) -> str:
        return self.wait_presence(self._input).get_attribute("value") or ""
