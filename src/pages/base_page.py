"""BasePage — базовый класс для всех Page Objects.

Принципы POM, которых держимся:
- Все селекторы — как атрибуты класса (не хардкод внутри методов).
- Все действия над страницей — как методы.
- Никаких page.wait_for_timeout(...) — только явные условия ожидания.
- Методы возвращают other Page Objects при навигации
  (e.g. login() -> WorkspacePage) — для чейнинга.
"""
from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import Locator, Page, expect

from src.helpers.allure_utils import attach_page_html, attach_screenshot
from src.helpers.config import settings
from src.helpers.logger import StepLogger


class BasePage:
    """Базовый класс для всех Page Objects.

    В наследниках определяем:
    - url: относительный путь страницы (для open())
    - unique_locator: элемент, по наличию которого определяем что страница загружена
    """

    # Дочерние классы переопределяют
    url: str = "/"

    def __init__(self, page: Page, logger: StepLogger) -> None:
        self.page = page
        self.log = logger

        # Дефолтные таймауты
        page.set_default_timeout(settings.default_timeout)
        page.set_default_navigation_timeout(settings.navigation_timeout)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def open(self, **url_kwargs: Any) -> "BasePage":
        """Открыть страницу по self.url (с подстановкой параметров)."""
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
        """Дождаться domcontentloaded.

        Почему не networkidle: Plane — SPA с PostHog analytics + WebSocket,
        сетевая активность никогда не прекращается. networkidle даёт 30s timeout.
        domcontentloaded = DOM готов, элементы доступны — нам этого достаточно.
        Дальше явно ждём КОНКРЕТНЫЕ элементы через expect().to_be_visible().
        """
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_url_contains(self, fragment: str, timeout: int | None = None) -> None:
        """Дождаться пока URL будет содержать fragment."""
        self.log.step(f"Waiting for URL to contain '{fragment}'")
        self.page.wait_for_url(
            f"**{fragment}**", timeout=timeout or settings.navigation_timeout
        )

    # ------------------------------------------------------------------
    # Assertions (с логированием + auto-screenshot при падении)
    # ------------------------------------------------------------------
    def assert_visible(
            self, locator: Locator, name: str = "element", timeout: int = 15_000
    ) -> None:
        """Assert что элемент виден. Timeout 15s по умолчанию для медленных SPA."""
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
        """Ручной скриншот + в Allure."""
        self.log.step(f"Taking screenshot: {name}")
        attach_screenshot(self.page, name)

    def _attach_failure_artifacts(self, name: str) -> None:
        """При падении assertion — автоматически прикрепляем screenshot + HTML."""
        with allure.step(f"Attach failure artifacts: {name}"):
            attach_screenshot(self.page, f"FAIL_{name}")
            attach_page_html(self.page, f"FAIL_{name}_html")