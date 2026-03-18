from __future__ import annotations

from pages.base_page import BasePage


class TheInternetPage(BasePage):
    PATH: str = "/"

    def open(self, path: str | None = None) -> None:
        super().open(self.PATH if path is None else path)

