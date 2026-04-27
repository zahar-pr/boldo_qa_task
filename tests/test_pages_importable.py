"""
Import-time check that every Page Object class instantiates cleanly.

Catches regressions where a page module is broken syntactically or has
missing imports — runs before functional suites.
"""
from __future__ import annotations

import pytest

from src.helpers.logger import StepLogger
from src.pages.base_page import BasePage
from src.pages.cycle_page import CyclePage
from src.pages.issue_page import IssuePage
from src.pages.kanban_page import KanbanPage
from src.pages.list_view_page import ListViewPage
from src.pages.login_page import LoginPage
from src.pages.page_editor_page import PageEditorPage
from src.pages.project_page import ProjectPage
from src.pages.workspace_page import WorkspacePage


@pytest.fixture
def fake_logger() -> StepLogger:
    return StepLogger(test_name="pom_import_check")


class TestPageObjectsImportable:
    def test_all_pages_import(self, fake_logger: StepLogger, page) -> None:
        pages = [
            BasePage(page, fake_logger),
            LoginPage(page, fake_logger),
            WorkspacePage(page, fake_logger),
            ProjectPage(page, fake_logger),
            IssuePage(page, fake_logger),
            KanbanPage(page, fake_logger),
            ListViewPage(page, fake_logger),
            CyclePage(page, fake_logger),
            PageEditorPage(page, fake_logger),
        ]
        assert len(pages) == 9
        fake_logger.close()