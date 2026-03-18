from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@dataclass(frozen=True)
class BasePage:
    driver: WebDriver
    base_url: str
    timeout_s: int = 10

    def open(self, path: str = "/") -> None:
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    def find(self, locator):
        return self.wait_presence(locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def wait_presence(self, locator):
        return WebDriverWait(self.driver, self.timeout_s).until(EC.presence_of_element_located(locator))

    def wait_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout_s).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return WebDriverWait(self.driver, self.timeout_s).until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator) -> bool:
        return WebDriverWait(self.driver, self.timeout_s).until(EC.invisibility_of_element_located(locator))

    def click(self, locator) -> None:
        self.wait_clickable(locator).click()

    def type(self, locator, text: str) -> None:
        el = self.wait_visible(locator)
        el.clear()
        el.send_keys(text)

    def exists(self, locator) -> bool:
        try:
            self.wait_presence(locator)
            return True
        except TimeoutException:
            return False
