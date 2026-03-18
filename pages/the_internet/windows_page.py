from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class WindowsPage(TheInternetPage):
    PATH = "/windows"

    _link = (By.LINK_TEXT, "Click Here")
    _header = (By.TAG_NAME, "h3")

    def click_open_new_window(self) -> None:
        self.click(self._link)

    def header_text(self) -> str:
        return self.wait_visible(self._header).text
