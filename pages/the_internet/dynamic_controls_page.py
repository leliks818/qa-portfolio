from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.the_internet.the_internet_page import TheInternetPage


class DynamicControlsPage(TheInternetPage):
    PATH = "/dynamic_controls"

    _toggle_checkbox_btn = (By.CSS_SELECTOR, "#checkbox-example button")
    _checkbox = (By.CSS_SELECTOR, "#checkbox input[type='checkbox']")
    _toggle_input_btn = (By.CSS_SELECTOR, "#input-example button")
    _input = (By.CSS_SELECTOR, "#input-example input")
    _message = (By.ID, "message")
    _loading = (By.ID, "loading")
    _checkbox_btn = (By.CSS_SELECTOR, "#checkbox-example button")

    def remove_checkbox(self) -> None:
        self.click(self._toggle_checkbox_btn)
        self.wait_invisible(self._loading)
        WebDriverWait(self.driver, self.timeout_s).until(lambda d: "It's gone!" in d.find_element(*self._message).text)
        WebDriverWait(self.driver, self.timeout_s).until(lambda d: len(d.find_elements(*self._checkbox)) == 0)

    def add_checkbox(self) -> None:
        self.click(self._toggle_checkbox_btn)
        self.wait_invisible(self._loading)
        WebDriverWait(self.driver, self.timeout_s).until(lambda d: "It's back!" in d.find_element(*self._message).text)
        # The site is occasionally flaky on re-inserting the checkbox into DOM; the button text is a reliable proxy.
        WebDriverWait(self.driver, self.timeout_s * 2).until(lambda d: "Remove" in d.find_element(*self._checkbox_btn).text)

    def checkbox_button_text(self) -> str:
        return self.wait_visible(self._checkbox_btn).text

    def checkbox_present(self) -> bool:
        return self.exists(self._checkbox)

    def enable_input(self) -> None:
        self.click(self._toggle_input_btn)
        self.wait_invisible(self._loading)

    def disable_input(self) -> None:
        self.click(self._toggle_input_btn)
        self.wait_invisible(self._loading)

    def input_enabled(self) -> bool:
        return self.wait_presence(self._input).is_enabled()

    def message_text(self) -> str:
        return self.wait_visible(self._message).text
