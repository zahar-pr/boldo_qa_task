"""
Page Object for the project Kanban board view.

Encapsulates column locators and card drag-and-drop interactions
(currently used as a placeholder for future expansion).
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class KanbanPage(BasePage):
    url = ""

    # --- View toggle ---
    @property
    def kanban_view_button(self) -> Locator:
        return self.page.get_by_role("button", name="Kanban").first

    @property
    def list_view_button(self) -> Locator:
        return self.page.get_by_role("button", name="List").first

    # --- Columns / cards ---
    def column_by_state_name(self, state: str) -> Locator:
        return self.page.locator(
            f'[class*="kanban"] :has-text("{state}")'
        ).first

    def card_by_title(self, title: str) -> Locator:
        return self.page.get_by_text(title, exact=False).first

    # --- Actions ---
    def switch_to_kanban(self) -> "KanbanPage":
        with self.log.allure_step("Switch to Kanban view"):
            self.kanban_view_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def drag_card_between_columns(
        self, card_title: str, from_state: str, to_state: str
    ) -> "KanbanPage":
        with self.log.allure_step(
            f"Drag '{card_title}' from '{from_state}' to '{to_state}'"
        ):
            source = self.card_by_title(card_title)
            target = self.column_by_state_name(to_state)
            source.drag_to(target)
        return self

    # --- Assertions ---
    def assert_card_in_column(self, card_title: str, state: str) -> None:
        column = self.column_by_state_name(state)
        card_inside = column.locator(f':has-text("{card_title}")').first
        self.assert_visible(card_inside, name=f"Card '{card_title}' in '{state}'")