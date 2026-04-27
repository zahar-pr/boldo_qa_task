"""
Workspace test suite (TC-006..TC-008).

Covers Create Workspace flow accessibility, workspace name visibility
in the navigation and access to the workspace settings page.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, expect

from src.helpers.config import settings
from src.helpers.logger import StepLogger
from src.pages.workspace_page import WorkspacePage


@allure.epic("Plane SaaS")
@allure.feature("Workspace")
class TestWorkspace:
    @allure.story("Create Workspace flow is accessible via direct URL")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.workspace
    @pytest.mark.critical
    def test_tc006_create_workspace_flow_accessible(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        create_url = f"{settings.base_url}/create-workspace"
        with allure.step(f"Navigate directly to {create_url}"):
            authenticated_page.goto(create_url)
            authenticated_page.wait_for_load_state("domcontentloaded")

        with allure.step("Verify Create Workspace form is loaded"):
            form_input = authenticated_page.locator("input, textarea").first
            expect(form_input).to_be_visible(timeout=10_000)
            step_logger.assertion(
                "Create workspace form input visible", passed=True
            )

        with allure.step("Verify URL is create-workspace flow"):
            current_url = authenticated_page.url
            assert (
                "create-workspace" in current_url
                or "/onboarding" in current_url
            ), f"Expected create-workspace URL, got {current_url}"
            step_logger.assertion(
                f"URL is create workspace flow: {current_url}", passed=True
            )

    @allure.story("Current workspace name is displayed in navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.workspace
    def test_tc007_workspace_name_in_navigation(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        workspace = WorkspacePage(authenticated_page, step_logger)
        workspace.open_for_current_workspace()
        workspace.assert_loaded()

        with allure.step(
            f"Verify workspace name '{settings.plane_workspace_slug}' visible"
        ):
            workspace_label = authenticated_page.get_by_text(
                settings.plane_workspace_slug, exact=False
            ).first
            expect(workspace_label).to_be_visible(timeout=10_000)
            step_logger.assertion(
                f"Workspace '{settings.plane_workspace_slug}' visible in UI",
                passed=True,
            )

    @allure.story("Workspace settings page is accessible from navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.workspace
    def test_tc008_workspace_settings_accessible(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open settings URL directly"):
            settings_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/settings"
            )
            authenticated_page.goto(settings_url)
            authenticated_page.wait_for_load_state("domcontentloaded")

        with allure.step("Verify settings page loaded"):
            current_url = authenticated_page.url
            assert "/settings" in current_url, (
                f"Expected /settings in URL, got {current_url}"
            )
            step_logger.assertion(
                f"URL contains '/settings' (got: {current_url})", passed=True
            )

        with allure.step("Verify some settings content is visible"):
            settings_indicators = authenticated_page.locator(
                "text=/General|Members|Billing|Workspace/i"
            ).first
            expect(settings_indicators).to_be_visible(timeout=10_000)
            step_logger.assertion(
                "Settings content (General/Members/Billing) visible",
                passed=True,
            )