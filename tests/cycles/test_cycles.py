"""
Cycles test suite (TC-022..TC-023).

Covers the workspace cycles section reachability and the presence
of interactive UI on the cycles page.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, expect

from src.helpers.config import settings
from src.helpers.logger import StepLogger


@allure.epic("Plane SaaS")
@allure.feature("Cycles")
class TestCycles:
    @allure.story("Workspace cycles section accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cycles
    def test_tc022_cycles_section_loads(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Navigate to workspace cycles"):
            cycles_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/cycles"
            )
            authenticated_page.goto(cycles_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify cycles URL loaded"):
            assert "/cycles" in authenticated_page.url, (
                f"Expected /cycles URL, got {authenticated_page.url}"
            )
            step_logger.assertion(
                f"On cycles page: {authenticated_page.url}", passed=True
            )

    @allure.story("Cycles page has interactive UI")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cycles
    def test_tc023_cycles_page_has_content(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace cycles"):
            cycles_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/cycles"
            )
            authenticated_page.goto(cycles_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify page has interactive elements"):
            visible_buttons = authenticated_page.locator("button:visible").count()
            step_logger.info(f"Visible buttons on /cycles: {visible_buttons}")
            assert visible_buttons >= 1, (
                f"Cycles page seems broken — no buttons at all"
            )
            step_logger.assertion(
                f"Cycles page has interactive UI ({visible_buttons} buttons)",
                passed=True,
            )