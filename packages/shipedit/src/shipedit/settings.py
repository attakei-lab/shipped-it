import os
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class PublisherSettings(BaseModel):
    template: str
    options: dict[str, Any] = Field(default_factory=dict)
    module: str | None = None


class SourceSettings(BaseModel):
    publisher: dict[str, PublisherSettings]
    options: dict[str, Any] = Field(default_factory=dict)
    module: str | None = None


class AppSettings(BaseSettings):
    credential: dict[str, dict[str, Any]] = Field(default_factory=dict)
    source: dict[str, SourceSettings]


def discover_settings_file(arg: Path | None = None) -> Path:
    candicates = [
        Path.cwd() / "settings.toml",
    ]
    if "SHIPEDIT_SETTINGS_FILE" in os.environ:
        candicates.insert(0, Path(os.environ["SHIPEDIT_SETTINGS_FILE"]))
    for c in candicates:
        if c.exists():
            return c
    raise Exception("Settings file not found.")


def load_settings(path: Path) -> AppSettings:
    return AppSettings.model_validate(tomllib.loads(path.read_text(encoding="utf-8")))


_settings: AppSettings | None = None


def get_app_settings() -> AppSettings:
    if _settings is None:
        raise ValueError("Settings not initialized.")
    return _settings


def set_app_settings(settings: AppSettings):
    global _settings
    if _settings is not None:
        raise ValueError("Settings is already initialized.")
    _settings = settings
