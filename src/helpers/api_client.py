"""API-клиент для setup/teardown тестовых данных.

Почему через API, а не UI:
- В 10-20 раз быстрее (нет ожиданий анимаций/сетевых запросов фронта).
- Детерминированно (UI может измениться, API — стабильнее).
- Не создаёт лишних записей в истории действий Plane.

Используется в фикстурах типа `@pytest.fixture def existing_project(api_client)`.

Важно: Plane имеет несколько API. Публичное (с PAT токеном) и внутреннее
(cookie-based, которое использует SPA). В тестах проще второе — берём куки
из storage_state и шлём запросы с теми же куками.
"""
from __future__ import annotations

from typing import Any

import httpx

from src.helpers.config import settings


class PlaneApiClient:
    """Минимальный клиент Plane API на сессионных куках.

    Создаётся из storage_state (см. auth_fixture). Методы добавляем по мере
    необходимости — начинаем с минимума, расширяем когда тест требует.
    """

    def __init__(self, cookies: dict[str, str], workspace_slug: str | None = None):
        self.base_url = settings.base_url.rstrip("/")
        self.workspace_slug = workspace_slug or settings.plane_workspace_slug
        self._client = httpx.Client(
            base_url=self.base_url,
            cookies=cookies,
            timeout=10.0,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Referer": self.base_url,
            },
        )

    # --- Context manager для использования в with ---
    def __enter__(self) -> "PlaneApiClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    # --- Projects ---
    def list_projects(self) -> list[dict[str, Any]]:
        r = self._client.get(
            f"/api/v1/workspaces/{self.workspace_slug}/projects/"
        )
        r.raise_for_status()
        return r.json()

    def delete_project(self, project_id: str) -> None:
        """Удалить проект по id. Используем в teardown."""
        r = self._client.delete(
            f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/"
        )
        # 204 No Content или 404 если уже удалён — оба ок
        if r.status_code not in (204, 404):
            r.raise_for_status()

    def cleanup_autotest_projects(self) -> int:
        """Удалить все проекты с префиксом autotest_.

        Защита от помойки в workspace после прогонов. Запускается в session teardown.
        Возвращает количество удалённых.
        """
        deleted = 0
        try:
            projects = self.list_projects()
        except httpx.HTTPError:
            return 0

        for p in projects:
            name = p.get("name", "")
            if name.startswith("autotest_"):
                try:
                    self.delete_project(p["id"])
                    deleted += 1
                except httpx.HTTPError:
                    continue
        return deleted