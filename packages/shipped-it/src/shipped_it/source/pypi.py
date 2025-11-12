from datetime import datetime
from functools import lru_cache
from typing import Any, TypedDict, override

import requests
from dateutil.parser import isoparse
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal
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

        release_date = find_release_date(data.releases, data.info.version)
        release = models.Release(
            source=self,  # type: ignore[invalid-argument-type]
            name=data.info.name,
            revision=data.info.version,
            extra={
                "github": find_github_data(data.info),
                "release_date": release_date,
                "release_date_text": make_release_date_text(release_date),
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
    upload_time_iso_8601: str


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


def find_release_date(
    releases: dict[str, list[ProjectFileinfo]], version: str
) -> datetime | None:
    if version not in releases:
        return None
    latest_uploaded = max([f.upload_time_iso_8601 for f in releases[version]])
    return isoparse(latest_uploaded)


def make_release_date_text(release_date: datetime | None) -> str | None:
    if not release_date:
        return None
    delta = relativedelta(datetime.now(tz=tzlocal()), release_date)
    match delta.days:
        case 0:
            if delta.hours <= 1:
                return "Now"
            elif delta.hours <= 6:
                return f"{delta.hours} hours ago"
            else:
                return "Today"
        case 1:
            return "Yesterday"
        case _:
            if delta.years + delta.months == 0 and delta.days <= 20:
                return f"{delta.days} days ago"
            else:
                return "Previously"
