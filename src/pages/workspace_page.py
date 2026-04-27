"""
Page Object for the workspace shell (sidebar, user menu, navigation).

Handles project sidebar links, the user-avatar dropdown, logout flow
and assertions about the currently-selected workspace.
"""
from __future__ import annotations

from playwright.sync_api import Locator, expect

from src.helpers.config import settings
from src.pages.base_page import BasePage


class WorkspacePage(BasePage):
    url = "/{slug}/projects"

    @property
    def projects_nav_link(self) -> Locator:
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
        return self.page.locator(
            'div[tabindex="-1"]:has(img[src*="/assets/v2/static/"])'
        ).first

    @property
    def user_avatar(self) -> Locator:
        return self.user_avatar_trigger


    @property
    def user_avatar(self) -> Locator:
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
            expect(self.user_avatar_trigger).to_be_visible(timeout=15_000)
            self.user_avatar_trigger.click()
            expect(self.sign_out_button).to_be_visible(timeout=5_000)
        return self

    def logout(self) -> "LoginPage":
        from src.pages.login_page import LoginPage

        self.open_user_menu()
        with self.log.allure_step("Click 'Sign out'"):
            self.sign_out_button.click()

        self.page.wait_for_url("**/", timeout=10_000)
        from playwright.sync_api import expect
        expect(self.page.locator("#email")).to_be_visible(timeout=10_000)

        return LoginPage(self.page, self.log)

    # --- Assertions ---
    def assert_loaded(self) -> None:
        self.assert_url_contains(settings.plane_workspace_slug)

    def assert_sidebar_visible(self) -> None:
        self.assert_visible(self.projects_nav_link, name="Projects sidebar link")

# ----- Workspace identification -----
    @property
    def workspace_name_in_sidebar(self) -> Locator:
        from src.helpers.config import settings
        return self.page.locator(
            "span, div, h4, h3, a"
        ).filter(has_text=settings.plane_workspace_slug).first

    @property
    def workspace_switcher_button(self) -> Locator:
        from src.helpers.config import settings
        return self.page.locator(
            f'[role="button"]:has-text("{settings.plane_workspace_slug}"), '
            f'button:has-text("{settings.plane_workspace_slug}")'
        ).first

    # ----- User menu items -----
    @property
    def create_workspace_menu_item(self) -> Locator:
        return self.page.get_by_role("button", name="Create workspace").or_(
            self.page.get_by_text("Create workspace", exact=False)
        ).first

    @property
    def settings_menu_item(self) -> Locator:
        return self.page.get_by_role("link", name="Settings").or_(
            self.page.get_by_role("button", name="Settings")
        ).or_(
            self.page.get_by_text("Settings", exact=True)
        ).first