"""
Authentication test suite (TC-001..TC-005).

Covers email validation, OTP screen routing for registered and
unregistered emails, and the logout flow that clears the session.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, expect

from src.helpers.config import settings
from src.helpers.logger import StepLogger
from src.pages.login_page import LoginPage
from src.pages.workspace_page import WorkspacePage


@allure.epic("Plane SaaS")
@allure.feature("Authentication")
class TestAuth:
    @allure.story("Login with valid email redirects to OTP screen")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    @pytest.mark.critical
    def test_tc001_login_redirects_to_otp_screen(
        self, unauthenticated_page: Page, step_logger: StepLogger
    ) -> None:
        login = LoginPage(unauthenticated_page, step_logger)
        login.open()

        with allure.step(f"Submit valid email: {settings.plane_email}"):
            login.submit_email(settings.plane_email)

        with allure.step("Verify OTP screen appeared"):
            login.assert_otp_screen_visible()


    @allure.story("Login with malformed email keeps Continue button disabled")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    @pytest.mark.critical
    def test_tc002_malformed_email_blocks_submit(
            self, unauthenticated_page: Page, step_logger: StepLogger
    ) -> None:
        login = LoginPage(unauthenticated_page, step_logger)
        login.open()

        with allure.step("Fill invalid email 'abc-not-an-email'"):
            login.fill_email("abc-not-an-email")
            unauthenticated_page.keyboard.press("Tab")

        with allure.step("Assert Continue button is disabled"):
            login.assert_continue_button_disabled()

        with allure.step("Assert OTP screen is NOT shown"):
            expect(login.otp_input).not_to_be_visible()
            step_logger.assertion(
                "OTP screen NOT shown for invalid email", passed=True
            )

    @allure.story("Empty email field disables Continue button")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_tc003_empty_email_disables_continue(
        self, unauthenticated_page: Page, step_logger: StepLogger
    ) -> None:
        login = LoginPage(unauthenticated_page, step_logger)
        login.open()

        with allure.step("Assert email input is visible and empty"):
            login.assert_email_input_visible()
            email_value = login.email_input.input_value()
            step_logger.assertion(
                f"Email input is empty (value='{email_value}')",
                passed=email_value == "",
            )

        with allure.step("Assert Continue button is disabled"):
            login.assert_continue_button_disabled()

    @allure.story("Unregistered email still proceeds to OTP (privacy by design)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_tc004_unregistered_email_goes_to_otp(
        self, unauthenticated_page: Page, step_logger: StepLogger
    ) -> None:
        login = LoginPage(unauthenticated_page, step_logger)
        login.open()

        fake_email = "definitely-not-registered-1234567890@mailinator.com"
        with allure.step(f"Submit unregistered email: {fake_email}"):
            login.submit_email(fake_email)

        with allure.step("Verify OTP screen shown (no user enumeration leak)"):
            login.assert_otp_screen_visible()


    @allure.story("Logout clears session and redirects to login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    @pytest.mark.critical
    @pytest.mark.serial
    def test_tc005_logout_clears_session(
        self, isolated_authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        page = isolated_authenticated_page
        workspace = WorkspacePage(page, step_logger)

        with allure.step("Open workspace (authenticated)"):
            workspace.open_for_current_workspace()
            workspace.assert_loaded()

        with allure.step("Click user avatar → Sign out"):
            login = workspace.logout()

        with allure.step("Verify redirect to login form"):
            login.assert_email_input_visible()

        with allure.step("Verify session cookie is cleared"):
            cookies = page.context.cookies()
            session_cookies = [c for c in cookies if "session" in c["name"].lower()]
            step_logger.info(f"Session-like cookies after logout: {len(session_cookies)}")
            for c in session_cookies:
                assert len(c.get("value", "")) < 50, (
                    f"Session cookie '{c['name']}' still has value "
                    f"(len={len(c['value'])}) — session not cleared"
                )
            step_logger.assertion("No valid session cookie after logout", passed=True)