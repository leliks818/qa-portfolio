from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.the_internet.the_internet_page import TheInternetPage


class HorizontalSliderPage(TheInternetPage):
    PATH = "/horizontal_slider"

    _slider = (By.CSS_SELECTOR, "input[type='range']")
    _value = (By.ID, "range")

    def move_right(self, steps: int = 1) -> None:
        slider = self.wait_visible(self._slider)
        slider.click()
        slider.send_keys(Keys.ARROW_RIGHT * steps)

    def move_left(self, steps: int = 1) -> None:
        slider = self.wait_visible(self._slider)
        slider.click()
        slider.send_keys(Keys.ARROW_LEFT * steps)

    def value_text(self) -> str:
        return self.wait_visible(self._value).text
