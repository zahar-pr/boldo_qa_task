"""
Auth-suite fixtures.

Provides isolated_authenticated_page used by destructive tests
(such as logout) so they do not poison the shared session for other tests.
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
    if not settings.storage_state_full_path.exists():
        pytest.fail(
            "storage_state not found. Start scripts/save_auth_state.py."
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