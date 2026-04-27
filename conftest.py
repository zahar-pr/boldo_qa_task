"""
Global pytest fixtures and Playwright launch configuration.

Defines authenticated/unauthenticated page fixtures, custom logger fixture,
and the auto-capture hook that attaches screenshots and HTML snapshots
to Allure on test failure.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserType, Page

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from src.helpers.allure_utils import attach_page_html, attach_screenshot
from src.helpers.config import settings
from src.helpers.logger import StepLogger


def _kill_zombie_browsers() -> None:
    if os.name != "posix":
        return
    patterns = [
        "ms-playwright/chromium",
        "ms-playwright/firefox",
        "ms-playwright/webkit",
        "playwright/driver",
    ]
    for pattern in patterns:
        subprocess.run(
            ["pkill", "-9", "-f", pattern],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def _check_ram_before_session() -> None:
    try:
        import psutil
    except ImportError:
        return
    free_gb = psutil.virtual_memory().available / (1024 ** 3)
    if free_gb < 5.0:
        print(
            f"\n{'=' * 70}\n"
            f"⚠️  Low RAM: free {free_gb:.1f} GB (need >5 GB)\n"
            f"    Solution: pkill -f /opt/google/chrome\n"
            f"             sudo swapoff -a && sudo swapon -a\n"
            f"{'=' * 70}\n"
        )


_kill_zombie_browsers()
_check_ram_before_session()


@pytest.fixture(scope="session")
def browser_type_launch_args(
        browser_type_launch_args: dict[str, Any], browser_name: str
) -> dict[str, Any]:
    base: dict[str, Any] = {
        **browser_type_launch_args,
        "headless": settings.headless,
        "slow_mo": 0,
    }
    if browser_name == "chromium":
        base["args"] = [
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-software-rasterizer",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-sync",
            "--disable-translate",
            "--mute-audio",
            "--no-first-run",
            "--disable-features=site-per-process,TranslateUI",
            "--js-flags=--max-old-space-size=512",
        ]
    return base


@pytest.fixture(scope="session")
def browser(
    browser_type: BrowserType,
    browser_type_launch_args: dict[str, Any],
) -> Generator[Browser, None, None]:
    """Session-scope browser for CI speed.

    Locally (weak machines) we used function-scope to prevent RAM
    accumulation crash on heavy SPAs. CI has clean Ubuntu 22.04 with
    plenty of RAM — session-scope is 5x faster.
    """
    browser = browser_type.launch(**browser_type_launch_args)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def browser_context_args(
        browser_context_args: dict[str, Any],
) -> dict[str, Any]:
    args: dict[str, Any] = {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }
    storage_path = settings.storage_state_full_path
    if storage_path.exists():
        args["storage_state"] = str(storage_path)
    return args


@pytest.fixture
def step_logger(request: pytest.FixtureRequest) -> Generator[StepLogger, None, None]:
    test_name = request.node.name
    logger = StepLogger(test_name=test_name)
    logger.info(f"Test started: {test_name}")
    try:
        yield logger
    finally:
        logger.info(f"Test finished: {test_name}")
        logger.attach_log_to_allure()
        logger.close()


@pytest.fixture
def authenticated_page(
        page: Page, step_logger: StepLogger
) -> Generator[Page, None, None]:
    if not settings.storage_state_full_path.exists():
        pytest.fail(
            f"storage_state not found: {settings.storage_state_full_path}\n"
            f"Start: python scripts/save_auth_state.py"
        )
    step_logger.info(f"Using storage_state from {settings.storage_state_full_path}")
    yield page


@pytest.fixture
def unauthenticated_page(
        browser: Browser, step_logger: StepLogger
) -> Generator[Page, None, None]:
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
    )
    page = context.new_page()
    page.set_default_timeout(settings.default_timeout)
    page.set_default_navigation_timeout(settings.navigation_timeout)
    step_logger.info("Using unauthenticated context (no storage_state)")
    try:
        yield page
    finally:
        context.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(
        item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, Any, None]:
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page: Page | None = None
        for fixture_name in ("authenticated_page", "unauthenticated_page", "page"):
            if fixture_name in item.funcargs:
                candidate = item.funcargs[fixture_name]
                if isinstance(candidate, Page):
                    page = candidate
                    break
        if page is not None:
            try:
                with allure.step("Auto-capture failure artifacts"):
                    attach_screenshot(page, name=f"failure_{item.name}")
                    attach_page_html(page, name=f"failure_html_{item.name}")
            except Exception:
                pass
