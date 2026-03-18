from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class AddRemoveElementsPage(TheInternetPage):
    PATH = "/add_remove_elements/"

    _add = (By.XPATH, "//button[normalize-space()='Add Element']")
    _delete_buttons = (By.CSS_SELECTOR, "button.added-manually")

    def add_element(self) -> None:
        self.click(self._add)

    def delete_buttons_count(self) -> int:
        return len(self.find_all(self._delete_buttons))

    def delete_one(self) -> None:
        buttons = self.find_all(self._delete_buttons)
        if not buttons:
            raise AssertionError("No Delete buttons found.")
        buttons[0].click()
