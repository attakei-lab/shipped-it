from functools import lru_cache
from typing import Any, TypedDict

import requests
from pydantic import BaseModel, HttpUrl

from . import Source as SourceBase


class Options(BaseModel):
    pass
    # author: list[str] = Field(default_factory=list)


class Context(TypedDict):
    name: str
    version: str
    github: dict[str, Any] | None


class Source(SourceBase):
    name: str
    options: Options

    def build_context(self, name: str) -> Context:
        data_url = f"https://pypi.org/pypi/{name}/json"
        data = fetch_project_data(data_url)
        return {
            "name": data.info.name,
            "version": data.info.version,
            "github": find_github_data(data.info),
        }


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
