"""
Page Object for the workspace Pages (wiki) editor.

Covers the document list, Add Page control and rich-text editor area
used by the pages test suite.
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.helpers.test_data import PageData
from src.pages.base_page import BasePage


class PageEditorPage(BasePage):
    url = ""

    @property
    def pages_nav_link(self) -> Locator:
        return self.page.get_by_text("Pages", exact=True).first

    @property
    def add_page_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add page").first

    @property
    def page_title_input(self) -> Locator:
        return self.page.locator(
            'input[placeholder*="Title"], [contenteditable="true"]'
        ).first

    @property
    def page_content_editor(self) -> Locator:
        return self.page.locator('[contenteditable="true"]').nth(1)

    def open_pages(self) -> "PageEditorPage":
        with self.log.allure_step("Open 'Pages' tab"):
            self.pages_nav_link.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def create_page(self, data: PageData) -> "PageEditorPage":
        with self.log.allure_step("Click 'Add page'"):
            self.add_page_button.click()
        self.page.wait_for_load_state("domcontentloaded")

        with self.log.allure_step(f"Fill page title: {data.title}"):
            self.page_title_input.click()
            self.page_title_input.fill(data.title)

        if data.content:
            with self.log.allure_step("Fill page content"):
                self.page_content_editor.click()
                self.page_content_editor.type(data.content)

        self.page.wait_for_load_state("domcontentloaded")
        return self

    def assert_page_visible(self, title: str) -> None:
        self.assert_text_visible(title)