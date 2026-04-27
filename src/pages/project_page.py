"""
Page Object for the project list and Create Project modal.

Covers Add Project button, modal form fields (name, identifier,
description) and submit/cancel lifecycle plus settings navigation.
"""
from __future__ import annotations

from playwright.sync_api import Locator

from src.helpers.config import settings
from src.helpers.test_data import ProjectData
from src.pages.base_page import BasePage


class ProjectPage(BasePage):
    url = "/{slug}/projects"

    # --- Project list ---
    @property
    def add_project_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add Project").first

    def project_card_by_name(self, name: str) -> Locator:
        return self.page.locator(
            f'a:has-text("{name}"), div:has-text("{name}")'
        ).first

    # --- Create project modal ---
    @property
    def project_name_input(self) -> Locator:
        return self.page.locator("#name")

    @property
    def project_identifier_input(self) -> Locator:
        return self.page.locator("#identifier")

    @property
    def project_description_input(self) -> Locator:
        return self.page.locator("#description")

    @property
    def create_project_submit(self) -> Locator:
        return self.page.get_by_role("button", name="Create project")

    @property
    def cancel_button(self) -> Locator:
        return self.page.get_by_role("button", name="Cancel")

    # --- Actions ---
    def open_for_current_workspace(self) -> "ProjectPage":
        return self.open(slug=settings.plane_workspace_slug)  # type: ignore[return-value]

    def click_add_project(self) -> "ProjectPage":
        with self.log.allure_step("Click 'Add Project'"):
            self.add_project_button.click()
        self.assert_visible(self.project_name_input, name="Create project modal")
        return self

    def fill_project_form(self, data: ProjectData) -> "ProjectPage":
        with self.log.allure_step(f"Fill project name: {data.name}"):
            self.project_name_input.fill(data.name)

        with self.log.allure_step(f"Fill identifier: {data.identifier}"):
            self.project_identifier_input.fill("")
            self.project_identifier_input.fill(data.identifier)

        if data.description:
            with self.log.allure_step("Fill description"):
                self.project_description_input.fill(data.description)
        return self

    def submit_create(self, wait_for_redirect: bool = False) -> "ProjectPage":
        with self.log.allure_step("Click 'Create project' submit"):
            self.create_project_submit.click()

        if not wait_for_redirect:
            self.page.wait_for_timeout(1500)
            try:
                self.page.goto(
                    f"{settings.base_url}/{settings.plane_workspace_slug}/projects",
                    wait_until="domcontentloaded",
                )
            except Exception:  # noqa: BLE001
                pass
            return self

        try:
            self.page.wait_for_function(
                "() => !document.querySelector('#name')",
                timeout=10_000,
            )
        except Exception:  # noqa: BLE001
            pass
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def create_project(self, data: ProjectData) -> "ProjectPage":
        self.click_add_project()
        self.fill_project_form(data)
        self.submit_create()
        return self

    def open_project_by_name(self, name: str) -> "ProjectPage":
        with self.log.allure_step(f"Open project '{name}'"):
            self.project_card_by_name(name).click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    # --- Assertions ---
    def assert_project_visible(self, name: str) -> None:
        self.assert_text_visible(name)

    def assert_create_submit_disabled(self) -> None:
        is_disabled = self.create_project_submit.is_disabled()
        self.log.assertion("Create project button disabled", passed=is_disabled)
        if not is_disabled:
            self._attach_failure_artifacts("create_btn_not_disabled")
            raise AssertionError("Expected Create button to be disabled")


# ----- Project deletion -----
    def project_settings_url(self, project_id: str) -> str:
        return (
            f"{settings.base_url}/{settings.plane_workspace_slug}"
            f"/projects/{project_id}/settings"
        )

    @property
    def delete_project_button(self) -> Locator:
        return self.page.get_by_role("button", name="Delete project").or_(
            self.page.get_by_text("Delete project", exact=False)
        ).first

    @property
    def delete_confirm_input(self) -> Locator:
        return self.page.locator(
            'input[placeholder*="confirm"], input[placeholder*="Confirm"], '
            'input[placeholder*="project"], input[placeholder*="name"]'
        ).first

    @property
    def delete_confirm_submit(self) -> Locator:
        return self.page.get_by_role("button", name="Delete").last

    # ----- Project URL navigation -----
    def open_project_settings_by_name(self, name: str) -> None:
        with self.log.allure_step(f"Open project '{name}' settings"):
            project_link = self.page.get_by_text(name, exact=False).first
            project_link.click()
            self.page.wait_for_load_state("domcontentloaded")
            current_url = self.page.url.rstrip("/")
            self.page.goto(f"{current_url}/settings")
            self.page.wait_for_load_state("domcontentloaded")

    def get_current_project_id_from_url(self, timeout_ms: int = 10_000) -> str | None:
        elapsed = 0
        poll = 500
        while elapsed < timeout_ms:
            url = self.page.url
            if "/projects/" in url:
                parts = url.split("/projects/")
                if len(parts) >= 2 and parts[1]:
                    pid = parts[1].split("/")[0].split("?")[0]
                    if pid and pid != "":
                        return pid
            self.page.wait_for_timeout(poll)
            elapsed += poll
        return None