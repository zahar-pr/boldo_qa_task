"""
Page Object for the project List view.

Encapsulates the list-mode toggle and row-level selectors for tests
that verify the layout switcher and inline row interactions.
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class ListViewPage(BasePage):
    url = ""

    @property
    def list_view_button(self) -> Locator:
        return self.page.get_by_role("button", name="List").first

    def issue_row_by_title(self, title: str) -> Locator:
        return self.page.get_by_text(title, exact=False).first

    # --- Filters (placeholder) ---
    @property
    def filter_button(self) -> Locator:
        return self.page.get_by_role("button", name="Filters").first

    def switch_to_list(self) -> "ListViewPage":
        with self.log.allure_step("Switch to List view"):
            self.list_view_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def assert_issue_in_list(self, title: str) -> None:
        self.assert_text_visible(title)