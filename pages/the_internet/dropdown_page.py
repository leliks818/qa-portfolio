from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.the_internet.the_internet_page import TheInternetPage


class DropdownPage(TheInternetPage):
    PATH = "/dropdown"

    _select = (By.ID, "dropdown")

    def select_by_visible_text(self, text: str) -> None:
        sel = Select(self.wait_visible(self._select))
        sel.select_by_visible_text(text)

    def selected_text(self) -> str:
        sel = Select(self.wait_visible(self._select))
        return sel.first_selected_option.text
