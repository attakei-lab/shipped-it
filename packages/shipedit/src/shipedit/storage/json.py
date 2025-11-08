"""Local JSON storage."""

import json
from pathlib import Path
from typing import Any, override

from pydantic import BaseModel, Field

from .. import models

CURRENT_REVISION = 1


class ReleaseData(BaseModel):
    revision: str
    extra: dict[str, Any] | None = None


class StorageData(BaseModel):
    revision: int
    releases: dict[str, dict[str, dict[str, ReleaseData]]]


def init_storage() -> StorageData:
    return StorageData(revision=CURRENT_REVISION, releases={})


class Options(BaseModel):
    """Options for the JSON storage."""

    path: Path
    indent: int | None = None


class Storage(models.Storage[Options]):
    data: StorageData = Field(default_factory=init_storage)

    @override
    def open(self) -> None:
        if not self.options.path.exists():
            self.close()
        self.data = StorageData.model_validate(
            json.loads(self.options.path.read_text())
        )

    @override
    def close(self) -> None:
        self.options.path.write_text(self.data.model_dump_json(indent=self.options.indent))

    @override
    def exists_release(self, release: models.Release) -> bool:
        if release.source.name not in self.data.releases:
            return False
        if release.name not in self.data.releases[release.source.name]:
            return False
        return release.revision in self.data.releases[release.source.name][release.name]

    @override
    def save_release(self, release: models.Release, force: bool = False) -> bool:
        self.data.releases.setdefault(release.source.name, {})
        self.data.releases[release.source.name].setdefault(release.name, {})
        releases = self.data.releases[release.source.name][release.name]
        if release.revision not in releases or force:
            releases[release.revision] = ReleaseData.model_validate(
                release.model_dump()
            )
            return True
        return False
