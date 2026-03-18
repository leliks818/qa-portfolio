from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass(frozen=True)
class BasePage:
    driver: WebDriver
    base_url: str
    timeout_s: int = 10

    def open(self, path: str = "/") -> None:
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    def find(self, locator):
        return WebDriverWait(self.driver, self.timeout_s).until(EC.presence_of_element_located(locator))

    def click(self, locator) -> None:
        WebDriverWait(self.driver, self.timeout_s).until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str) -> None:
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

