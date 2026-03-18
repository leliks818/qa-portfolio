from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class CheckboxesPage(TheInternetPage):
    PATH = "/checkboxes"

    _checkboxes = (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    def _box(self, index: int):
        self.wait_presence(self._checkboxes)
        boxes = self.find_all(self._checkboxes)
        return boxes[index]

    def is_checked(self, index: int) -> bool:
        return self._box(index).is_selected()

    def set_checked(self, index: int, value: bool) -> None:
        box = self._box(index)
        if box.is_selected() != value:
            box.click()
