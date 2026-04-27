"""
BasePage — shared methods for all Page Object classes.

Provides URL navigation, visibility/text/url assertions, screenshot helpers
and Allure step integration. Every page-specific class inherits from it.
"""
from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import Locator, Page, expect

from src.helpers.allure_utils import attach_page_html, attach_screenshot
from src.helpers.config import settings
from src.helpers.logger import StepLogger


class BasePage:
    url: str = "/"

    def __init__(self, page: Page, logger: StepLogger) -> None:
        self.page = page
        self.log = logger

        page.set_default_timeout(settings.default_timeout)
        page.set_default_navigation_timeout(settings.navigation_timeout)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def open(self, **url_kwargs: Any) -> "BasePage":
        path = self.url.format(**url_kwargs) if url_kwargs else self.url
        full_url = f"{settings.base_url.rstrip('/')}{path}"
        self.log.step(f"Navigating to {full_url}")
        self.page.goto(full_url)
        self.wait_for_page_load()
        return self

    def reload(self) -> None:
        self.log.step("Reloading page")
        self.page.reload()
        self.wait_for_page_load()

    def get_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    # ------------------------------------------------------------------
    # Waits
    # ------------------------------------------------------------------
    def wait_for_page_load(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_url_contains(self, fragment: str, timeout: int | None = None) -> None:
        self.log.step(f"Waiting for URL to contain '{fragment}'")
        self.page.wait_for_url(
            f"**{fragment}**", timeout=timeout or settings.navigation_timeout
        )

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------
    def assert_visible(
            self, locator: Locator, name: str = "element", timeout: int = 15_000
    ) -> None:
        try:
            expect(locator).to_be_visible(timeout=timeout)
            self.log.assertion(f"{name} is visible", passed=True)
        except AssertionError:
            self.log.assertion(f"{name} is visible", passed=False)
            self._attach_failure_artifacts(f"assert_visible_{name}")
            raise

    def assert_url_contains(self, fragment: str) -> None:
        current = self.page.url
        passed = fragment in current
        self.log.assertion(
            f"URL contains '{fragment}' (actual: {current})", passed=passed
        )
        if not passed:
            self._attach_failure_artifacts(f"assert_url_contains_{fragment}")
            raise AssertionError(
                f"Expected URL to contain '{fragment}', got '{current}'"
            )

    def assert_text_visible(self, text: str) -> None:
        locator = self.page.get_by_text(text, exact=False).first
        try:
            expect(locator).to_be_visible()
            self.log.assertion(f"Text '{text}' visible", passed=True)
        except AssertionError:
            self.log.assertion(f"Text '{text}' visible", passed=False)
            self._attach_failure_artifacts(f"assert_text_{text[:30]}")
            raise

    # ------------------------------------------------------------------
    # Artifacts
    # ------------------------------------------------------------------
    def take_screenshot(self, name: str = "screenshot") -> None:
        self.log.step(f"Taking screenshot: {name}")
        attach_screenshot(self.page, name)

    def _attach_failure_artifacts(self, name: str) -> None:
        with allure.step(f"Attach failure artifacts: {name}"):
            attach_screenshot(self.page, f"FAIL_{name}")
            attach_page_html(self.page, f"FAIL_{name}_html")
