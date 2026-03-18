from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class JSAlertsPage(TheInternetPage):
    PATH = "/javascript_alerts"

    _js_alert_btn = (By.XPATH, "//button[normalize-space()='Click for JS Alert']")
    _js_confirm_btn = (By.XPATH, "//button[normalize-space()='Click for JS Confirm']")
    _js_prompt_btn = (By.XPATH, "//button[normalize-space()='Click for JS Prompt']")
    _result = (By.ID, "result")

    def click_alert(self) -> None:
        self.click(self._js_alert_btn)

    def click_confirm(self) -> None:
        self.click(self._js_confirm_btn)

    def click_prompt(self) -> None:
        self.click(self._js_prompt_btn)

    def result_text(self) -> str:
        return self.wait_visible(self._result).text
