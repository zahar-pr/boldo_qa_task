"""Root conftest — глобальные фикстуры для всех тестов.

Ключевые фикстуры:
- step_logger (function): кастомный логгер, создаётся на каждый тест.
- browser_context_args (function, override pytest-playwright):
    добавляем storage_state + viewport к каждому контексту.
- authenticated_page (function): готовая страница с уже залогиненным юзером.
- _capture_failure_artifacts (autouse): при FAIL — скриншот + HTML + лог в Allure.

Фикстуры пересоздаются на каждый тест ради изоляции
(function scope — дефолт). Чтобы ускорить — browser стартует один раз
за сессию (делает за нас pytest-playwright).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Generator

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

# Делаем src/ импортируемым из любого теста
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from src.helpers.allure_utils import attach_page_html, attach_screenshot  # noqa: E402
from src.helpers.config import settings  # noqa: E402
from src.helpers.logger import StepLogger  # noqa: E402


# ---------------------------------------------------------------------------
# pytest-playwright overrides
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict[str, Any]) -> dict[str, Any]:
    """Переопределяем launch args браузера.

    Флаги --disable-gpu, --no-sandbox, --disable-dev-shm-usage спасают от
    крашей Chromium на Linux, особенно когда:
    - /dev/shm недостаточно большой (пишем в /tmp вместо /dev/shm)
    - GPU-рендеринг конфликтует с драйвером
    - Контейнер без SYS_ADMIN capabilities (CI)
    Эти же флаги Google рекомендует для Docker/CI сред.
    """
    return {
        **browser_type_launch_args,
        "headless": settings.headless,
        "slow_mo": 0,
        "args": [
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    }


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, Any],
) -> dict[str, Any]:
    """Дефолтные параметры контекста: viewport + storage_state если есть."""
    args: dict[str, Any] = {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }
    storage_path = settings.storage_state_full_path
    if storage_path.exists():
        args["storage_state"] = str(storage_path)
    return args


# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
@pytest.fixture
def step_logger(request: pytest.FixtureRequest) -> Generator[StepLogger, None, None]:
    """Кастомный логгер для текущего теста.

    Пишет в logs/<test_name>_<timestamp>.log + в консоль.
    В конце теста прикрепляет лог к Allure отчёту.
    """
    test_name = request.node.name
    logger = StepLogger(test_name=test_name)
    logger.info(f"Test started: {test_name}")
    try:
        yield logger
    finally:
        logger.info(f"Test finished: {test_name}")
        logger.attach_log_to_allure()
        logger.close()


# ---------------------------------------------------------------------------
# Authenticated page — главная фикстура для большинства тестов.
# ---------------------------------------------------------------------------
@pytest.fixture
def authenticated_page(
    page: Page, step_logger: StepLogger
) -> Generator[Page, None, None]:
    """Страница с подгруженным storage_state (залогиненный юзер).

    Автоматически открывает главную workspace'а. Тесты, которые хотят
    начать с конкретной страницы, делают .goto() сами.

    Если storage_state.json отсутствует — тест падает с понятной ошибкой
    ("запусти scripts/save_auth_state.py").
    """
    if not settings.storage_state_full_path.exists():
        pytest.fail(
            f"storage_state не найден: {settings.storage_state_full_path}\n"
            f"Запусти один раз: python scripts/save_auth_state.py\n"
            f"Скрипт откроет браузер, залогинься руками, сессия сохранится."
        )

    step_logger.info(f"Using storage_state from {settings.storage_state_full_path}")
    yield page


# ---------------------------------------------------------------------------
# Unauthenticated page — для тестов логина/валидации форм.
# ---------------------------------------------------------------------------
@pytest.fixture
def unauthenticated_page(
    browser: Any, step_logger: StepLogger
) -> Generator[Page, None, None]:
    """Чистая страница БЕЗ storage_state. Для auth-тестов."""
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


# ---------------------------------------------------------------------------
# Auto-capture при падении теста — screenshot + HTML в Allure.
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, Any, None]:
    """Хук pytest: срабатывает после каждой фазы теста.

    Если тест упал в фазе 'call' — достаём page из фикстур и делаем
    скриншот/HTML в Allure. Это безопасная сетка: даже если тест
    забыл сам приложить артефакты — мы их добавим.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Ищем первую доступную page в активных фикстурах теста
        page: Page | None = None
        for fixture_name in ("authenticated_page", "unauthenticated_page", "page"):
            if fixture_name in item.funcargs:
                candidate = item.funcargs[fixture_name]
                if isinstance(candidate, Page):
                    page = candidate
                    break

        if page is not None:
            with allure.step("Auto-capture failure artifacts"):
                attach_screenshot(page, name=f"failure_{item.name}")
                attach_page_html(page, name=f"failure_html_{item.name}")


# ---------------------------------------------------------------------------
# Autotest data cleanup — в конце сессии (best effort).
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def cleanup_autotest_data() -> Generator[None, None, None]:
    """После всей сессии — чистим autotest_ записи через API.

    Если API недоступен — молча пропускаем. Мусор потом можно удалить руками
    в UI (проекты с префиксом autotest_).
    """
    yield
    # TODO: подключим после первого зелёного прогона тестов,
    # когда будет понятно, как Plane API реагирует на session-куки.
    # Сейчас no-op.