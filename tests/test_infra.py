"""
Infrastructure smoke tests for the framework itself.

Verifies that config loads, the logger writes and closes, test data
factories produce unique values and Allure utility helpers are callable.
"""
from __future__ import annotations

from src.helpers.allure_utils import set_allure_metadata
from src.helpers.config import settings
from src.helpers.logger import StepLogger
from src.helpers.test_data import IssueData, ProjectData


class TestInfrastructure:
    def test_config_loads(self) -> None:
        assert settings.base_url.startswith("http")
        assert settings.plane_email  # .env is filled
        assert settings.plane_workspace_slug

    def test_logger_writes_and_closes(self, tmp_path) -> None:
        log = StepLogger(test_name="infra_check")
        log.info("info message")
        log.step("step message")
        log.assertion("some check", passed=True)
        log.warning("warn message")
        log.error("error message")

        assert log.log_file.exists()
        content = log.log_file.read_text(encoding="utf-8")
        assert "[STEP]" in content
        assert "[ASSERT]" in content
        assert "PASSED" in content

        log.close()

    def test_test_data_generates_unique(self) -> None:
        p1 = ProjectData()
        p2 = ProjectData()
        assert p1.name != p2.name
        assert p1.name.startswith("autotest_project_")
        assert len(p1.identifier) >= 4

        i1 = IssueData()
        assert i1.title.startswith("autotest_issue_")

    def test_allure_metadata_callable(self) -> None:
        set_allure_metadata(
            feature="Infra",
            story="smoke",
            severity="minor",
            tags=["smoke"],
        )