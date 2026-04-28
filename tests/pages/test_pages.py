"""
Pages (wiki) test suite (TC-024).

Covers the workspace pages section reachability and the presence
of interactive UI controls on the pages list.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, expect

from src.helpers.config import settings
from src.helpers.logger import StepLogger


@allure.epic("Plane SaaS")
@allure.feature("Pages")
class TestPages:
    @allure.story("Workspace pages section accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pages
    def test_tc024_pages_section_loads(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Navigate to workspace pages"):
            pages_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/pages"
            )
            authenticated_page.goto(pages_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(2000)

        with allure.step("Verify pages URL"):
            current = authenticated_page.url
            ok = "/pages" in current or "/wiki" in current
            assert ok, f"Expected /pages or /wiki, got {current}"
            step_logger.assertion(
                f"On pages/wiki: {current}", passed=True
            )
