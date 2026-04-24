"""ProjectPage — страница списка проектов + модалка создания проекта.

Flow создания:
1. open() -> /<slug>/projects
2. click_add_project() -> открывается модалка
3. fill_project_form() -> заполняем поля
4. submit_create() -> создаётся проект, редирект в него
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
        """Кнопка 'Add Project' — верхний правый угол списка проектов.
        На большом экране текст "Add Project", на мобилке — только иконка."""
        return self.page.get_by_role("button", name="Add Project").first

    def project_card_by_name(self, name: str) -> Locator:
        """Карточка проекта в списке. Находим по видимому названию."""
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
        """Заполняет форму проекта."""
        with self.log.allure_step(f"Fill project name: {data.name}"):
            self.project_name_input.fill(data.name)

        # Identifier Plane автогенерирует из name. Перезапишем своим.
        with self.log.allure_step(f"Fill identifier: {data.identifier}"):
            self.project_identifier_input.fill("")  # очистить
            self.project_identifier_input.fill(data.identifier)

        if data.description:
            with self.log.allure_step("Fill description"):
                self.project_description_input.fill(data.description)
        return self

    def submit_create(self) -> "ProjectPage":
        with self.log.allure_step("Click 'Create project' submit"):
            self.create_project_submit.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def create_project(self, data: ProjectData) -> "ProjectPage":
        """Полный flow: открыть модалку -> заполнить -> submit."""
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