import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class NotifierSettings(BaseModel):
    template: str


class PackageSettings(BaseModel):
    notifier: dict[str, NotifierSettings]
    options: dict[str, Any] = Field(default_factory=dict)
    module: str | None = None


class AppSettings(BaseSettings):
    package: dict[str, PackageSettings]


def discover_settings_file() -> Path:
    candicates = [
        Path.cwd() / "settings.toml",
    ]
    for c in candicates:
        if c.exists():
            return c
    raise Exception("Settings file not found.")


def load_settings(path: Path) -> AppSettings:
    return AppSettings.model_validate(tomllib.loads(path.read_text(encoding="utf-8")))
