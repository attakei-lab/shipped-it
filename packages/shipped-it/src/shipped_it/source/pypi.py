from functools import lru_cache
from typing import Any, TypedDict, override

import requests
from pydantic import BaseModel, HttpUrl

from .. import models


class Options(BaseModel):
    pass
    # author: list[str] = Field(default_factory=list)


class Context(TypedDict):
    github: dict[str, Any] | None


class Source(models.Source[Options]):
    @override
    def make_release(self, release_name: str) -> models.Release:
        data_url = f"https://pypi.org/pypi/{release_name}/json"
        data = fetch_project_data(data_url)

        release = models.Release(
            source=self,  # type: ignore[invalid-argument-type]
            name=data.info.name,
            revision=data.info.version,
            extra={
                "github": find_github_data(data.info),
            },
        )
        return release


class ProjectInfo(BaseModel):
    classifiers: list[str]
    description: str
    name: str
    project_url: HttpUrl
    project_urls: dict[str, HttpUrl]
    version: str


class ProjectFileinfo(BaseModel):
    filename: str


class ProjectData(BaseModel):
    info: ProjectInfo
    last_serial: int
    releases: dict[str, list[ProjectFileinfo]]
    urls: list[ProjectFileinfo]


@lru_cache
def fetch_project_data(url: str) -> ProjectData:
    resp = requests.get(url)
    resp.raise_for_status()
    return ProjectData.model_validate(resp.json())


def find_github_data(info: ProjectInfo) -> dict[str, Any] | None:
    github_url = None
    for url in info.project_urls.values():
        if url.host == "github.com":
            github_url = url
            break
    if not github_url:
        return None
    return {
        "url": github_url,
    }
