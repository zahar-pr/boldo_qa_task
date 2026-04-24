"""WorkspacePage — главная страница workspace после логина.

URL: /<workspace-slug>/projects (или просто /<workspace-slug>/)
Содержит:
- Sidebar с навигацией (Projects, Cycles, Views, Pages, ...)
- User menu (аватарка справа/снизу с опцией Sign out)
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.helpers.config import settings
from src.pages.base_page import BasePage


class WorkspacePage(BasePage):
    # URL пропишем динамически через open(slug=...)
    url = "/{slug}/projects"

    # --- Sidebar ---
    @property
    def projects_nav_link(self) -> Locator:
        """Ссылка "Projects" в sidebar. По видимому тексту."""
        return self.page.get_by_text("Projects", exact=True).first

    @property
    def cycles_nav_link(self) -> Locator:
        return self.page.get_by_text("Your cycles", exact=True).first

    @property
    def pages_nav_link(self) -> Locator:
        return self.page.get_by_text("Your pages", exact=True).first

    # --- User menu ---
    @property
    def sign_out_button(self) -> Locator:
        return self.page.get_by_role("button", name="Sign out")

    @property
    def user_avatar(self) -> Locator:
        """Аватарка пользователя — кнопка, открывающая user menu.
        Plane не даёт data-testid/aria, поэтому ищем по изображению внутри."""
        return self.page.locator("img[src*='/assets/v2/static/']").first

    # --- Actions ---
    def open_for_current_workspace(self) -> "WorkspacePage":
        return self.open(slug=settings.plane_workspace_slug)  # type: ignore[return-value]

    def go_to_projects(self) -> "WorkspacePage":
        with self.log.allure_step("Click 'Projects' in sidebar"):
            self.projects_nav_link.click()
        self.wait_for_url_contains("/projects")
        return self

    def open_user_menu(self) -> "WorkspacePage":
        with self.log.allure_step("Open user menu (click avatar)"):
            self.user_avatar.click()
        return self

    def logout(self) -> "LoginPage":  # noqa: F821 — forward ref
        """Логаут: открыть user menu, нажать Sign out, дождаться редиректа."""
        from src.pages.login_page import LoginPage  # локальный импорт -> избежать цикл

        self.open_user_menu()
        with self.log.allure_step("Click 'Sign out'"):
            self.sign_out_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return LoginPage(self.page, self.log)

    # --- Assertions ---
    def assert_loaded(self) -> None:
        """Страница загружена = URL содержит slug."""
        self.assert_url_contains(settings.plane_workspace_slug)

    def assert_sidebar_visible(self) -> None:
        self.assert_visible(self.projects_nav_link, name="Projects sidebar link")