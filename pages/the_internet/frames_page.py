from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.the_internet.the_internet_page import TheInternetPage


class IFramePage(TheInternetPage):
    PATH = "/iframe"

    _iframe = (By.ID, "mce_0_ifr")
    _editor_body = (By.ID, "tinymce")

    def type_in_editor(self, text: str) -> None:
        frame = self.wait_presence(self._iframe)
        self.driver.switch_to.frame(frame)
        try:
            body = self.wait_visible(self._editor_body)
            # tinymce uses a contenteditable body; `.clear()` is unreliable here.
            body.send_keys(Keys.CONTROL, "a")
            body.send_keys(Keys.DELETE)
            self.driver.execute_script("arguments[0].textContent = '';", body)
            body.send_keys(text)
        finally:
            self.driver.switch_to.default_content()

    def editor_text(self) -> str:
        frame = self.wait_presence(self._iframe)
        self.driver.switch_to.frame(frame)
        try:
            return self.wait_visible(self._editor_body).text
        finally:
            self.driver.switch_to.default_content()


class NestedFramesPage(TheInternetPage):
    PATH = "/nested_frames"
