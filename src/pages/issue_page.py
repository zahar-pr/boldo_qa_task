"""
Page Object for the work item (issue) creation modal.

Wraps the title input, ProseMirror description editor and Save button
selectors used by the issues test suite.
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.helpers.test_data import IssueData
from src.pages.base_page import BasePage


class IssuePage(BasePage):
    url = ""

    # --- Create issue triggers (fallback-logic) ---
    @property
    def create_first_work_item_button(self) -> Locator:
        return self.page.get_by_role("button", name="Create your first work item")

    @property
    def new_work_item_button(self) -> Locator:
        return self.page.get_by_role("button", name="New work item").first

    # --- Create issue modal ---
    @property
    def issue_title_input(self) -> Locator:
        return self.page.locator('input[name="name"][placeholder="Title"]')

    @property
    def issue_description_editor(self) -> Locator:
        return self.page.locator(
            '#issue-modal-editor div[contenteditable="true"]'
        )

    @property
    def issue_save_button(self) -> Locator:
        return self.page.get_by_role("button", name="Save")

    @property
    def issue_cancel_button(self) -> Locator:
        return self.page.get_by_role("button", name="Cancel")

    # --- Issue in list ---
    def issue_row_by_title(self, title: str) -> Locator:
        return self.page.get_by_text(title, exact=False).first

    # --- Actions ---
    def click_create_issue(self) -> "IssuePage":
        with self.log.allure_step("Click create-issue trigger"):
            first_btn = self.create_first_work_item_button
            if first_btn.is_visible():
                first_btn.click()
            else:
                self.new_work_item_button.click()

        self.assert_visible(self.issue_title_input, name="Issue modal (title input)")
        return self

    def fill_issue_form(self, data: IssueData) -> "IssuePage":
        with self.log.allure_step(f"Fill issue title: {data.title}"):
            self.issue_title_input.fill(data.title)

        if data.description:
            with self.log.allure_step("Fill issue description"):
                self.issue_description_editor.click()
                self.issue_description_editor.type(data.description)
        return self

    def submit_issue(self) -> "IssuePage":
        with self.log.allure_step("Click 'Save' issue"):
            self.issue_save_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def create_issue(self, data: IssueData) -> "IssuePage":
        self.click_create_issue()
        self.fill_issue_form(data)
        self.submit_issue()
        return self

    # --- Assertions ---
    def assert_issue_visible(self, title: str) -> None:
        self.assert_text_visible(title)

    def assert_save_button_disabled(self) -> None:
        disabled = self.issue_save_button.is_disabled()
        self.log.assertion("Save button disabled", passed=disabled)
        if not disabled:
            self._attach_failure_artifacts("save_not_disabled")
            raise AssertionError("Expected Save to be disabled")