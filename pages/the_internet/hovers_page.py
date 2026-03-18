from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.the_internet.the_internet_page import TheInternetPage


class HoversPage(TheInternetPage):
    PATH = "/hovers"

    _figures = (By.CSS_SELECTOR, "div.figure")

    def hover_figure(self, index_1_based: int) -> None:
        self.wait_presence(self._figures)
        figures = self.find_all(self._figures)
        fig = figures[index_1_based - 1]
        ActionChains(self.driver).move_to_element(fig).perform()

    def caption_text(self, index_1_based: int) -> str:
        self.wait_presence(self._figures)
        figures = self.find_all(self._figures)
        fig = figures[index_1_based - 1]
        caption = fig.find_element(By.CSS_SELECTOR, "div.figcaption h5")
        return caption.text
