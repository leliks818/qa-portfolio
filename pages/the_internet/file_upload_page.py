from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.the_internet.the_internet_page import TheInternetPage


class FileUploadPage(TheInternetPage):
    PATH = "/upload"

    _file_input = (By.ID, "file-upload")
    _upload_btn = (By.ID, "file-submit")
    _uploaded_files = (By.ID, "uploaded-files")

    def upload(self, file_path: str) -> None:
        self.wait_presence(self._file_input).send_keys(file_path)
        self.click(self._upload_btn)

    def uploaded_filename(self) -> str:
        return self.wait_visible(self._uploaded_files).text
