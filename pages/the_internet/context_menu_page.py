from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class ContextMenuPage(TheInternetPage):
    PATH = "/context_menu"

    _hotspot = (By.ID, "hot-spot")

    def hotspot(self):
        return self.wait_visible(self._hotspot)
