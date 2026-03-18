from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class StatusCodesPage(TheInternetPage):
    PATH = "/status_codes"

    _content = (By.ID, "content")

    def open_code(self, code: int) -> None:
        self.click((By.LINK_TEXT, str(code)))

    def content_text(self) -> str:
        return self.wait_visible(self._content).text
