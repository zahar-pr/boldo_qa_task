"""Одноразовый скрипт: открывает браузер, ты логинишься руками,
скрипт сохраняет cookies+localStorage в auth/storage_state.json.

Запуск:
    python scripts/save_auth_state.py

Что делает:
1. Открывает Chromium в видимом режиме (headed).
2. Идёт на app.plane.so.
3. Ждёт когда ты залогинишься (email → OTP из почты).
4. Ждёт пока ты нажмёшь Enter в терминале (знак что залогинился).
5. Сохраняет storage_state в файл.

Важно: этот файл НЕ коммитится (в .gitignore).
Для CI его нужно будет закодировать в base64 и положить в GitHub Secrets.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Делаем src/ импортируемым
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from playwright.sync_api import sync_playwright  # noqa: E402

from src.helpers.config import settings  # noqa: E402


def main() -> None:
    storage_path = settings.storage_state_full_path
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Plane auth — save storage_state")
    print("=" * 70)
    print(f"Target: {settings.base_url}")
    print(f"Expected email: {settings.plane_email}")
    print(f"Storage will be saved to: {storage_path}")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.goto(settings.base_url)

        print("\n>>> Браузер открыт. Залогинься руками:")
        print(f"    1. Введи email: {settings.plane_email}")
        print("    2. Нажми Continue.")
        print("    3. Зайди в почту, скопируй 6-значный код.")
        print("    4. Введи код на странице, нажми Continue.")
        print("    5. Дождись редиректа в workspace.")
        print("\n>>> Когда увидишь главную страницу Plane — вернись сюда")
        print(">>> и нажми Enter, чтобы сохранить сессию.")
        input("\nPress Enter when logged in... ")

        # Верификация что мы в workspace: URL должен содержать slug
        current_url = page.url
        if settings.plane_workspace_slug not in current_url:
            print(
                f"\n⚠️  WARNING: URL не содержит workspace slug "
                f"'{settings.plane_workspace_slug}'.\n"
                f"    Current URL: {current_url}\n"
                f"    Возможно ты не залогинен или slug в .env неверный.\n"
                f"    Сохраняю storage всё равно, но тесты могут падать."
            )

        context.storage_state(path=str(storage_path))
        print(f"\n✅ Storage state сохранён: {storage_path}")
        print(f"   Размер: {storage_path.stat().st_size} bytes")

        browser.close()


if __name__ == "__main__":
    main()