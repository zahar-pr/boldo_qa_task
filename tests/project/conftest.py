"""Conftest для project-тестов.

Фикстура `project_data` — генерирует уникальные данные для проекта
с префиксом autotest_, чтобы тесты были изолированными.

Cleanup делается best-effort: после теста пытаемся удалить созданный
проект через UI. Если упало — оставляем мусор (потом руками почистим).
"""
from __future__ import annotations

from typing import Generator

import pytest

from src.helpers.test_data import ProjectData


@pytest.fixture
def project_data() -> ProjectData:
    """Уникальные данные для нового проекта."""
    return ProjectData()