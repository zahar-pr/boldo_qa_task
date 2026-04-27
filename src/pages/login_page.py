"""
Page Object for the Plane login screen.

Encapsulates the email field, OTP input and Continue button along with
submit and assertion helpers used by authentication tests.
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    url = "/"

    # --- Locators ---
    @property
    def email_input(self) -> Locator:
        return self.page.locator("#email")

    @property
    def continue_button(self) -> Locator:
        return self.page.get_by_role("button", name="Continue")

    @property
    def otp_input(self) -> Locator:
        return self.page.locator("#unique-code")

    @property
    def error_toast(self) -> Locator:
        return self.page.locator('[role="alert"], [class*="error"]').first

    # --- Actions ---
    def fill_email(self, email: str) -> "LoginPage":
        with self.log.allure_step(f"Fill email field with '{email}'"):
            self.email_input.fill(email)
        return self

    def click_continue(self) -> "LoginPage":
        with self.log.allure_step("Click Continue button"):
            self.continue_button.click()
        return self

    def submit_email(self, email: str) -> "LoginPage":
        self.fill_email(email)
        self.click_continue()
        return self

    def fill_otp(self, code: str) -> "LoginPage":
        with self.log.allure_step("Fill OTP code"):
            self.otp_input.fill(code)
        return self

    # --- Assertions ---
    def assert_otp_screen_visible(self) -> None:
        self.assert_visible(self.otp_input, name="OTP input")

    def assert_email_input_visible(self) -> None:
        self.assert_visible(self.email_input, name="Email input")

    def assert_continue_button_disabled(self) -> None:
        is_disabled = self.continue_button.is_disabled()
        self.log.assertion("Continue button is disabled", passed=is_disabled)
        if not is_disabled:
            self._attach_failure_artifacts("continue_not_disabled")
            raise AssertionError("Expected Continue button to be disabled")