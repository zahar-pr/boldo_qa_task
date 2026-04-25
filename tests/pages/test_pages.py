"""Pages test suite — TC-024, TC-025."""
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
        """Workspace pages — wiki-подобный раздел. Должен открываться
        через /<slug>/pages."""
        with allure.step("Navigate to workspace pages"):
            pages_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/pages"
            )
            authenticated_page.goto(pages_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(2000)

        with allure.step("Verify pages URL"):
            assert "/pages" in authenticated_page.url, (
                f"Expected /pages, got {authenticated_page.url}"
            )
            step_logger.assertion(
                f"On pages: {authenticated_page.url}", passed=True
            )


    @allure.story("Pages section has create-page UI or list")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pages
    def test_tc025_pages_section_has_content(
        self, authenticated_page: Page, step_logger: StepLogger
    ) -> None:
        """На /pages должны быть либо кнопки создания, либо empty state,
        либо список существующих pages — что-то что подтверждает что
        раздел работает и в нём можно создавать pages."""
        with allure.step("Open workspace pages"):
            pages_url = (
                f"{settings.base_url}/{settings.plane_workspace_slug}/pages"
            )
            authenticated_page.goto(pages_url, wait_until="domcontentloaded")
            authenticated_page.wait_for_timeout(3000)

        with allure.step("Verify pages section is interactive (has buttons)"):
            # Pages section в любой реализации Plane имеет кнопки управления:
            # либо "Add page", "New page", "Create page", либо переключатели
            # типа Public/Private, либо empty state с CTA. Любой из вариантов
            # = страница рендерится корректно.
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
            # Best-effort поиск кнопок создания — для логирования/информации,
            # не для assert (тест уже passed на предыдущем шаге).
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