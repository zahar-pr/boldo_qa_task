"""
Page Object for the Cycles (sprints) section.

Covers cycle list rendering, Add Cycle button and basic cycle
detail navigation used by the cycles test suite.
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.helpers.test_data import CycleData
from src.pages.base_page import BasePage


class CyclePage(BasePage):
    url = ""

    @property
    def cycles_nav_link(self) -> Locator:
        return self.page.get_by_text("Cycles", exact=True).first

    @property
    def add_cycle_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add Cycle").first

    @property
    def cycle_name_input(self) -> Locator:
        return self.page.locator("#name")

    @property
    def cycle_description_input(self) -> Locator:
        return self.page.locator("#description")

    @property
    def cycle_create_submit(self) -> Locator:
        return self.page.get_by_role("button", name="Create Cycle").first

    def open_project_cycles(self) -> "CyclePage":
        with self.log.allure_step("Open project 'Cycles' tab"):
            self.cycles_nav_link.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def create_cycle(self, data: CycleData) -> "CyclePage":
        with self.log.allure_step("Click 'Add Cycle'"):
            self.add_cycle_button.click()

        with self.log.allure_step(f"Fill cycle name: {data.name}"):
            self.cycle_name_input.fill(data.name)

        if data.description:
            with self.log.allure_step("Fill cycle description"):
                self.cycle_description_input.fill(data.description)

        with self.log.allure_step("Submit cycle"):
            self.cycle_create_submit.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def assert_cycle_visible(self, name: str) -> None:
        self.assert_text_visible(name)