"""
Firefox variant of the auth state saver.

Same purpose as save_auth_state.py but launches Firefox — useful when
Chromium is unstable on the local machine.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout  # noqa: E402

from src.helpers.config import settings  # noqa: E402

MANUAL_LOGIN_TIMEOUT_MS = 5 * 60 * 1000
POLL_INTERVAL_MS = 500


def main() -> None:
    storage_path = settings.storage_state_full_path
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Plane auth — Firefox version")
    print("=" * 70)
    print(f"Target:          {settings.base_url}")
    print(f"Expected email:  {settings.plane_email}")
    print(f"Workspace slug:  {settings.plane_workspace_slug}")
    print(f"Save to:         {storage_path}")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=50)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
        )
        page = context.new_page()
        page.set_default_timeout(30_000)
        page.set_default_navigation_timeout(45_000)

        page.goto(settings.base_url)

        print("\n>>> Firefox открыт. Логинься руками:")
        print(f"    1. Введи email: {settings.plane_email}")
        print("    2. Нажми Continue → получи 6-значный код в почте.")
        print("    3. Введи код → нажми Continue.")
        print("\n>>> Скрипт проверяет URL каждые 0.5 сек.")
        print(
            f">>> Как только увидит '/{settings.plane_workspace_slug}' — сохранит.\n"
        )

        slug = settings.plane_workspace_slug
        elapsed = 0
        detected = False

        while elapsed < MANUAL_LOGIN_TIMEOUT_MS:
            current_url = page.url
            if slug in current_url:
                print(f"\n✅ URL detected: {current_url}")
                detected = True
                break
            page.wait_for_timeout(POLL_INTERVAL_MS)
            elapsed += POLL_INTERVAL_MS

            if elapsed % 15_000 == 0:
                print(f"   [{elapsed // 1000}s] current URL: {current_url}")

        if not detected:
            print("\n⚠️  Не дождались URL с workspace slug за 5 минут.")
            print(f"    Текущий URL: {page.url}")
            input("    Если всё же залогинен — нажми Enter для сохранения. ")

        print("   Ждём 3 сек на запись localStorage...")
        page.wait_for_timeout(3000)

        context.storage_state(path=str(storage_path))

        storage = storage_path.read_text()
        has_cookies = '"cookies": []' not in storage
        has_origins = '"origins": []' not in storage

        print(f"\n✅ Storage state сохранён: {storage_path}")
        print(f"   Размер:   {storage_path.stat().st_size} bytes")
        print(f"   Cookies:  {'✓ есть' if has_cookies else '✗ ПУСТО'}")
        print(f"   Origins:  {'✓ есть' if has_origins else '✗ ПУСТО'}")

        browser.close()


if __name__ == "__main__":
    main()