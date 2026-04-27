"""
Pages (wiki) test suite (TC-024..TC-025).

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


    @allure.story("Pages section has create-page UI or list")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pages
    def test_tc025_pages_section_has_content(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace pages"):
            pages_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/pages"
            )
            authenticated_page.goto(pages_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify pages section is interactive (has buttons)"):
            visible_buttons = authenticated_page.locator("button:visible").count()
            step_logger.info(f"Visible buttons on /pages: {visible_buttons}")
            assert visible_buttons >= 3, (
                f"Pages section seems empty/broken — only {visible_buttons} buttons"
            )
            step_logger.assertion(
                f"Pages section has interactive UI ({visible_buttons} buttons)",
                passed=True,
            )

        with allure.step("Try finding any 'create page' or 'new page' control"):
            candidates = [
                authenticated_page.get_by_role("button", name="Add page"),
                authenticated_page.get_by_role("button", name="New page"),
                authenticated_page.get_by_role("button", name="Create page"),
                authenticated_page.locator("button[aria-label*='page' i]"),
                authenticated_page.locator("button").filter(has_text="page"),
            ]
            for c in candidates:
                try:
                    if c.first.is_visible(timeout=1000):
                        step_logger.info(
                            f"Found create-page control: {c.first}"
                        )
                        break
                except Exception:  # noqa: BLE001
                    continue