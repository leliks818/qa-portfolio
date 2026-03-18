from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class DynamicLoadingPage(TheInternetPage):
    PATH = "/dynamic_loading"

    def open_example(self, example_num: int) -> None:
        self.open(f"{self.PATH.rstrip('/')}/{example_num}")


class DynamicLoadingExamplePage(TheInternetPage):
    _start = (By.CSS_SELECTOR, "#start button")
    _finish = (By.ID, "finish")
    _loading = (By.ID, "loading")

    def start(self) -> None:
        self.click(self._start)

    def wait_finished_text(self) -> str:
        # Wait for spinner to disappear and the finish text to be visible.
        self.wait_invisible(self._loading)
        return self.wait_visible(self._finish).text
