"""
HTTP client for Plane REST API (setup/teardown helper).

Reuses cookies from storage_state to enable programmatic creation
and cleanup of test entities outside the UI flow.
"""
from __future__ import annotations

from typing import Any

import httpx

from src.helpers.config import settings


class PlaneApiClient:
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

    # --- Context manager use in with ---
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
        r = self._client.delete(
            f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/"
        )
        if r.status_code not in (204, 404):
            r.raise_for_status()

    def cleanup_autotest_projects(self) -> int:
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