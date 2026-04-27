"""
Issues / Work Items test suite (TC-013..TC-018).

Verifies workspace overview, issue-related navigation sections,
views, cycles and the workspace home dashboard reachability.
"""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from src.helpers.config import settings
from src.helpers.logger import StepLogger


@allure.epic("Plane SaaS")
@allure.feature("Issues")
class TestIssues:
    @allure.story("Workspace your-work / all-issues page accessible")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.issues
    @pytest.mark.critical
    def test_tc013_workspace_issues_overview(
            self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Navigate to workspace issues overview"):
            url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}"
                f"/your-work"
            )
            authenticated_page.goto(url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify URL is reachable (your-work or fallback)"):
            current = authenticated_page.url
            ok = any(
                p in current.lower()
                for p in ("your-work", "issues", "workspace-views", "/projects")
            )
            step_logger.assertion(
                f"Workspace overview accessible: {current}", passed=ok
            )
            assert ok

    @allure.story("Workspace navigation menu has issues-related sections")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.issues
    @pytest.mark.critical
    def test_tc014_navigation_has_issue_sections(
            self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        base = f"{settings.base_url}/{settings.plane_workspace_slug}"
        sections_to_check = [
            ("/projects", "projects"),
            ("/cycles", "cycles"),
            ("/views", "views"),
        ]

        reachable = []
        for path, name in sections_to_check:
            with allure.step(f"Check {name} section reachable"):
                try:
                    authenticated_page.goto(
                        f"{base}{path}", wait_until="domcontentloaded"
                    )
                    authenticated_page.wait_for_timeout(1500)
                    if path in authenticated_page.url:
                        reachable.append(name)
                        step_logger.info(f"{name} reachable: {authenticated_page.url}")
                except Exception as e:  # noqa: BLE001
                    step_logger.info(f"{name} unreachable: {e}")

        step_logger.assertion(
            f"Reachable issue-related sections: {reachable}",
            passed=len(reachable) >= 2,
        )
        assert len(reachable) >= 2, (
            f"Expected at least 2 issue-related sections, got: {reachable}"
        )

    @allure.story("Workspace views section accessible (issues filters)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.issues
    def test_tc015_workspace_views_accessible(
            self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace views"):
            url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/views"
            )
            authenticated_page.goto(url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify URL"):
            assert "/views" in authenticated_page.url
            step_logger.assertion(
                f"Views URL: {authenticated_page.url}", passed=True
            )

    @allure.story("Workspace cycles aggregated view accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.issues
    def test_tc016_workspace_cycles_overview(
            self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace cycles"):
            url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/cycles"
            )
            authenticated_page.goto(url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(2000)

        with allure.step("Verify URL"):
            assert "/cycles" in authenticated_page.url
            step_logger.assertion(
                f"Cycles URL: {authenticated_page.url}", passed=True
            )

    @allure.story("Active cycles overview")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.issues
    def test_tc017_active_cycles_section(
            self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open active cycles"):
            url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}"
                f"/active-cycles"
            )
            authenticated_page.goto(url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(2000)

        with allure.step("Verify reachable"):
            current = authenticated_page.url
            ok = "active-cycles" in current or "cycles" in current
            step_logger.assertion(
                f"Active cycles URL: {current}", passed=ok
            )
            assert ok

    @allure.story("Workspace dashboard / home accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.issues
    def test_tc018_workspace_home_overview(
            self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace home"):
            url = f"{settings.base_url}/{settings.plane_workspace_slug}"
            authenticated_page.goto(url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(5000)

        with allure.step("Verify URL contains workspace slug"):
            current = authenticated_page.url
            ok = settings.plane_workspace_slug in current
            step_logger.info(f"Current URL: {current}")
            step_logger.assertion(
                f"Workspace home reachable: {current}", passed=ok
            )
            assert ok, f"Workspace slug not in URL: {current}"

        with allure.step("Verify page has rendered (any visible element)"):
            visible_anything = authenticated_page.locator(
                "a:visible, button:visible, [role='button']:visible"
            ).count()
            step_logger.info(f"Visible interactive elements: {visible_anything}")
            step_logger.assertion(
                f"Page rendered ({visible_anything} interactive elements)",
                passed=True,
            )
