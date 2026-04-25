"""WorkspacePage — главная страница workspace после логина.

URL: /<workspace-slug>/projects (или просто /<workspace-slug>/)
Содержит:
- Sidebar с навигацией (Projects, Cycles, Views, Pages, ...)
- User menu (аватарка справа/снизу с опцией Sign out)
"""
from __future__ import annotations

from playwright.sync_api import Locator, expect

from src.helpers.config import settings
from src.pages.base_page import BasePage


class WorkspacePage(BasePage):
    # URL пропишем динамически через open(slug=...)
    url = "/{slug}/projects"

    @property
    def projects_nav_link(self) -> Locator:
        """Ссылка 'Projects' в sidebar.

        В Plane текст "Projects" встречается дважды: в sidebar (навигация)
        и в заголовке страницы /projects. Берём .first видимый <p>, потому
        что оба валидные варианта для клика — ведут на список проектов.

        has_text (нестрогий match) вместо get_by_text(exact=True) —
        устраняет баг со strict violation на вложенных элементах.
        """
        return self.page.locator("p", has_text="Projects").first

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
    def user_avatar_trigger(self) -> Locator:
        """Триггер user menu.

        Plane не даёт data-testid на аватарке, но у неё есть tabindex=-1
        (признак кликабельного non-input элемента). Ищем контейнер с этим
        атрибутом, содержащий <img>. Это устойчивее чем селектор по
        самому <img>, который может ещё не догрузиться.
        """
        return self.page.locator(
            'div[tabindex="-1"]:has(img[src*="/assets/v2/static/"])'
        ).first

    @property
    def user_avatar(self) -> Locator:
        return self.user_avatar_trigger


    @property
    def user_avatar(self) -> Locator:
        """Алиас для обратной совместимости."""
        return self.user_avatar_trigger

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
            # Явно ждём что аватарка догрузилась с CDN — устраняет flakiness
            expect(self.user_avatar_trigger).to_be_visible(timeout=15_000)
            self.user_avatar_trigger.click()
            # Ждём что меню открылось = Sign out появился
            expect(self.sign_out_button).to_be_visible(timeout=5_000)
        return self

    def logout(self) -> "LoginPage":
        """Логаут через user menu → Sign out. Возвращает LoginPage."""
        from src.pages.login_page import LoginPage  # локальный импорт от цикла

        self.open_user_menu()
        with self.log.allure_step("Click 'Sign out'"):
            self.sign_out_button.click()

        # Ждём что сессия сброшена — появилась email-форма логина
        self.page.wait_for_url("**/", timeout=10_000)
        from playwright.sync_api import expect
        expect(self.page.locator("#email")).to_be_visible(timeout=10_000)

        return LoginPage(self.page, self.log)

    # --- Assertions ---
    def assert_loaded(self) -> None:
        """Страница загружена = URL содержит slug."""
        self.assert_url_contains(settings.plane_workspace_slug)

    def assert_sidebar_visible(self) -> None:
        self.assert_visible(self.projects_nav_link, name="Projects sidebar link")

# ----- Workspace identification -----
    @property
    def workspace_name_in_sidebar(self) -> Locator:
        """Имя текущего workspace в sidebar (обычно сверху).

        Plane показывает workspace name в дроп-дауне переключения.
        Ищем его как видимый текст внутри sidebar, по slug
        (slug чаще всего и является именем — kebab-case).
        """
        # Plane обычно отображает workspace name human-friendly,
        # но в нашем случае slug 'qa-automation-main' = name 'qa-automation-main'.
        # Если у тебя name отличается от slug — поправим.
        from src.helpers.config import settings
        return self.page.locator(
            "span, div, h4, h3, a"
        ).filter(has_text=settings.plane_workspace_slug).first

    @property
    def workspace_switcher_button(self) -> Locator:
        """Кнопка переключения workspace в sidebar (обычно сверху)."""
        # Plane делает workspace switcher как div с button-like role.
        # Селектор по тексту workspace-name + tabindex.
        from src.helpers.config import settings
        return self.page.locator(
            f'[role="button"]:has-text("{settings.plane_workspace_slug}"), '
            f'button:has-text("{settings.plane_workspace_slug}")'
        ).first

    # ----- User menu items -----
    @property
    def create_workspace_menu_item(self) -> Locator:
        """Пункт 'Create Workspace' в user menu."""
        return self.page.get_by_role("button", name="Create workspace").or_(
            self.page.get_by_text("Create workspace", exact=False)
        ).first

    @property
    def settings_menu_item(self) -> Locator:
        """Пункт 'Settings' в user menu или sidebar."""
        return self.page.get_by_role("link", name="Settings").or_(
            self.page.get_by_role("button", name="Settings")
        ).or_(
            self.page.get_by_text("Settings", exact=True)
        ).first