"""LoginPage — страница входа в Plane.

Особенность Plane: passwordless auth.
1. Вводим email -> нажимаем Continue -> попадаем на экран OTP.
2. Вводим 6-значный код из email -> Continue -> попадаем в workspace.

Для автотестов логин через OTP пропускается (см. auth fixture со storage_state).
Эта страница используется для:
- Тестов валидации формы (empty email, invalid email).
- Единичного теста логина с ручным вводом OTP (если понадобится).
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
        """Тост с ошибкой валидации/авторизации. Plane обычно показывает
        сообщения под инпутом или через toast. Точный селектор уточним
        при прогоне тестов."""
        # Общий паттерн: элемент с role="alert" или текст с красным цветом.
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
        """Заполнить email и нажать Continue (без ввода OTP)."""
        self.fill_email(email)
        self.click_continue()
        return self

    def fill_otp(self, code: str) -> "LoginPage":
        with self.log.allure_step("Fill OTP code"):
            self.otp_input.fill(code)
        return self

    # --- Assertions ---
    def assert_otp_screen_visible(self) -> None:
        """После ввода email мы должны оказаться на экране ввода OTP."""
        self.assert_visible(self.otp_input, name="OTP input")

    def assert_email_input_visible(self) -> None:
        self.assert_visible(self.email_input, name="Email input")

    def assert_continue_button_disabled(self) -> None:
        """При пустом email кнопка Continue должна быть disabled."""
        is_disabled = self.continue_button.is_disabled()
        self.log.assertion("Continue button is disabled", passed=is_disabled)
        if not is_disabled:
            self._attach_failure_artifacts("continue_not_disabled")
            raise AssertionError("Expected Continue button to be disabled")