"""
One-time interactive script to capture a Plane session.

Opens Chromium for manual OTP login, then persists cookies and localStorage
to auth/storage_state.json so subsequent test runs can reuse the session.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout  # noqa: E402

from src.helpers.config import settings

MANUAL_LOGIN_TIMEOUT_MS = 5 * 60 * 1000
POLL_INTERVAL_MS = 500
MIN_FREE_RAM_GB = 3.0


def check_system_resources() -> None:
    try:
        import psutil  # type: ignore[import-not-found]

        free_gb = psutil.virtual_memory().available / (1024**3)
        if free_gb < MIN_FREE_RAM_GB:
            print(
                f"\n⚠️  ВНИМАНИЕ: свободно {free_gb:.1f} GB RAM "
                f"(рекомендуется минимум {MIN_FREE_RAM_GB} GB)."
            )
            print("   Chromium может крашиться на тяжёлых страницах Plane.")
            print("   Закрой браузер/IDE/Docker перед запуском.")
            input("   Нажми Enter чтобы продолжить всё равно (или Ctrl+C)...\n")
    except ImportError:
        if shutil.which("free"):
            import subprocess

            result = subprocess.run(
                ["free", "-g"], capture_output=True, text=True
            )
            print(f"\nRAM info:\n{result.stdout}")


def main() -> None:
    storage_path = settings.storage_state_full_path
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Plane auth — Chromium version")
    print("=" * 70)
    print(f"Target:          {settings.base_url}")
    print(f"Expected email:  {settings.plane_email}")
    print(f"Workspace slug:  {settings.plane_workspace_slug}")
    print(f"Save to:         {storage_path}")
    print("=" * 70)

    check_system_resources()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=50,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
        )
        page = context.new_page()
        page.set_default_timeout(30_000)
        page.set_default_navigation_timeout(45_000)

        page.goto(settings.base_url)

        print("\n>>> Chromium открыт. Логинься руками:")
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
            try:
                current_url = page.url
            except Exception as e:  # noqa: BLE001
                print(f"\n❌ Браузер отвалился: {e}")
                print("   Скорее всего краш из-за нехватки памяти.")
                print("   Закрой Chrome и другие тяжёлые процессы, перезапусти.")
                return

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
            input("    Если залогинен — нажми Enter для сохранения. ")

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