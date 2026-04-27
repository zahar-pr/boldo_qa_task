"""
Typed application settings loaded from .env via pydantic-settings.

Provides fail-fast validation on startup and resolved paths for
storage_state and other runtime artifacts.
"""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Target ---
    base_url: str = Field(default="https://app.plane.so", alias="BASE_URL")

    # --- Plane account ---
    plane_email: str = Field(alias="PLANE_EMAIL")
    plane_workspace_slug: str = Field(alias="PLANE_WORKSPACE_SLUG")

    # --- Browser ---
    headless: bool = Field(default=True, alias="HEADLESS")
    default_timeout: int = Field(default=15_000, alias="DEFAULT_TIMEOUT")
    navigation_timeout: int = Field(default=30_000, alias="NAVIGATION_TIMEOUT")

    # --- Paths ---
    storage_state_path: str = Field(
        default="auth/storage_state.json", alias="STORAGE_STATE_PATH"
    )

    @property
    def storage_state_full_path(self) -> Path:
        return ROOT_DIR / self.storage_state_path

    @property
    def logs_dir(self) -> Path:
        path = ROOT_DIR / "logs"
        path.mkdir(exist_ok=True)
        return path

    @property
    def auth_dir(self) -> Path:
        path = ROOT_DIR / "auth"
        path.mkdir(exist_ok=True)
        return path


settings = Settings()  # type: ignore[call-arg]