"""
Allure helpers for screenshots, HTML snapshots and test metadata.

Used by the failure-capture hook in conftest.py and by individual tests
that need to attach extra context to the Allure report.
"""
from __future__ import annotations

import allure
from playwright.sync_api import Page


def attach_screenshot(page: Page, name: str = "screenshot") -> None:
    try:
        png = page.screenshot(full_page=True)
        allure.attach(
            body=png, name=name, attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:  # noqa: BLE001
        print(f"[allure_utils] screenshot failed: {e}")


def attach_page_html(page: Page, name: str = "page_html") -> None:
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
    allure.dynamic.epic(epic)
    if feature:
        allure.dynamic.feature(feature)
    if story:
        allure.dynamic.story(story)
    allure.dynamic.severity(severity)  # type: ignore[arg-type]
    for tag in tags or []:
        allure.dynamic.tag(tag)