from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.the_internet.the_internet_page import TheInternetPage


class KeyPressesPage(TheInternetPage):
    PATH = "/key_presses"

    _target = (By.ID, "target")
    _result = (By.ID, "result")

    def press(self, key) -> None:
        el = self.wait_visible(self._target)
        el.click()
        ActionChains(self.driver).send_keys(key).perform()

    def result_text(self) -> str:
        return self.wait_visible(self._result).text

    def wait_result_contains(self, expected: str) -> str:
        def _has_text(_):
            el = self.wait_presence(self._result)
            return el.text if expected in (el.text or "") else False

        return WebDriverWait(self.driver, self.timeout_s).until(_has_text)
