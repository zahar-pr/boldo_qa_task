"""
Views test suite (TC-019..TC-021).

Covers workspace views section reachability, projects-as-view loading
and the presence of interactive UI controls on the views page.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, expect

from src.helpers.config import settings
from src.helpers.logger import StepLogger


@allure.epic("Plane SaaS")
@allure.feature("Views")
class TestViews:
    @allure.story("Workspace views section is accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.views
    def test_tc019_views_section_loads(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Navigate to workspace views"):
            views_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/views"
            )
            authenticated_page.goto(views_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify views URL"):
            assert "/views" in authenticated_page.url, (
                f"Expected /views URL, got {authenticated_page.url}"
            )
            step_logger.assertion(
                f"On views page: {authenticated_page.url}", passed=True
            )

    @allure.story("Workspace projects list view is accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.views
    def test_tc020_projects_view_loads(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Navigate to projects list"):
            projects_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/projects"
            )
            authenticated_page.goto(projects_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify projects URL loaded"):
            assert "/projects" in authenticated_page.url
            step_logger.assertion(
                f"On projects view: {authenticated_page.url}", passed=True
            )

    @allure.story("Views page has interactive layout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.views
    @pytest.mark.critical
    def test_tc021_views_page_has_content(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace views"):
            views_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/views"
            )
            authenticated_page.goto(views_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Find interactive elements"):
            visible_buttons = authenticated_page.locator("button:visible").count()
            step_logger.info(f"Visible buttons on /views: {visible_buttons}")
            assert visible_buttons >= 1, (
                f"Views page broken — no buttons"
            )
            step_logger.assertion(
                f"Views page has interactive UI ({visible_buttons} buttons)",
                passed=True,
            )