"""Локальный conftest для auth-тестов.

Зачем:
- Для TC-005 logout нужна ОТДЕЛЬНАЯ копия storage_state.
  Если использовать общий — logout выйдет из глобальной сессии и
  все остальные тесты в прогоне начнут падать.
- Решение: создаём изолированный контекст с СВОЕЙ копией storage.
"""
from __future__ import annotations

from typing import Any, Generator

import pytest
from playwright.sync_api import Browser, Page

from src.helpers.config import settings


@pytest.fixture
def isolated_authenticated_page(
    browser: Browser,
) -> Generator[Page, None, None]:
    """Страница с подгруженным storage_state в ИЗОЛИРОВАННОМ контексте.

    Используется в logout-тесте: logout убьёт сессию этого контекста,
    но storage_state.json на диске не тронем → остальные тесты работают.
    """
    if not settings.storage_state_full_path.exists():
        pytest.fail(
            "storage_state не найден. Запусти scripts/save_auth_state.py."
        )

    context = browser.new_context(
        storage_state=str(settings.storage_state_full_path),
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
    )
    page = context.new_page()
    page.set_default_timeout(settings.default_timeout)
    page.set_default_navigation_timeout(settings.navigation_timeout)

    try:
        yield page
    finally:
        context.close()