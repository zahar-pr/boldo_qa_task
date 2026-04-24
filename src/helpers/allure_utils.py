"""Обёртки над allure API для единообразия в тестах."""
from __future__ import annotations

import allure
from playwright.sync_api import Page


def attach_screenshot(page: Page, name: str = "screenshot") -> None:
    """Сделать скриншот и прикрепить к Allure отчёту."""
    try:
        png = page.screenshot(full_page=True)
        allure.attach(
            body=png, name=name, attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:  # noqa: BLE001
        print(f"[allure_utils] screenshot failed: {e}")


def attach_page_html(page: Page, name: str = "page_html") -> None:
    """Прикрепить HTML страницы — полезно при падении для дебага селекторов."""
    try:
        allure.attach(
            body=page.content(),
            name=name,
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as e:  # noqa: BLE001
        print(f"[allure_utils] html attach failed: {e}")


def set_allure_metadata(
    *,
    epic: str = "Plane SaaS",
    feature: str | None = None,
    story: str | None = None,
    severity: str = "normal",
    tags: list[str] | None = None,
) -> None:
    """Динамически проставить allure-метаданные из теста.

    Вызывается в начале теста — удобно когда параметризуем и хотим разные
    story/severity для разных кейсов.
    """
    allure.dynamic.epic(epic)
    if feature:
        allure.dynamic.feature(feature)
    if story:
        allure.dynamic.story(story)
    allure.dynamic.severity(severity)  # type: ignore[arg-type]
    for tag in tags or []:
        allure.dynamic.tag(tag)