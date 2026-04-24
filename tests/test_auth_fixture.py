"""Верификация auth fixture — убеждаемся что storage_state работает.

Этот тест:
1. Использует authenticated_page (с подгруженным storage_state).
2. Идёт на главную workspace'а.
3. Проверяет что НЕ редиректит на /auth (= мы реально залогинены).
4. Проверяет что в URL есть workspace slug.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from src.helpers.config import settings
from src.helpers.logger import StepLogger
from src.pages.workspace_page import WorkspacePage


@allure.epic("Plane SaaS")
@allure.feature("Infrastructure")
@allure.story("Storage state auth fixture")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
class TestAuthFixture:
    def test_storage_state_logs_user_in(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        with allure.step("Open workspace home page"):
            workspace = WorkspacePage(authenticated_page, step_logger)
            workspace.open_for_current_workspace()

        with allure.step("Assert we are in workspace (not redirected to login)"):
            current_url = authenticated_page.url
            step_logger.info(f"Current URL after load: {current_url}")

            # Если storage_state не сработал — Plane редиректит на /, где email форма
            # Проверяем что URL содержит workspace slug
            assert settings.plane_workspace_slug in current_url, (
                f"Expected workspace slug '{settings.plane_workspace_slug}' "
                f"in URL, got '{current_url}'. "
                f"Скорее всего storage_state истёк или невалиден — "
                f"перезапусти scripts/save_auth_state.py."
            )
            step_logger.assertion(
                f"URL contains workspace slug '{settings.plane_workspace_slug}'",
                passed=True,
            )

        with allure.step("Assert sidebar is visible"):
            workspace.assert_sidebar_visible()