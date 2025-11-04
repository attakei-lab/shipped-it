"""Domain models."""

import abc
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel


class Source[T_O = BaseModel](BaseModel, metaclass=abc.ABCMeta):
    """Source of releases."""

    name: str
    """Source name to manage in this application."""
    options: T_O
    """Option values for methods."""

    @abc.abstractmethod
    def make_release(self, release_name: str) -> "Release[T_O]": ...


class Release(BaseModel):
    """Release entity of sources."""

    source: Source
    """Source object that release is fetched from."""
    name: str
    """Name of this entity in source.
    
    This is made from package name, slug of blog, and source's behavior.
    """
    revision: str = "latest"
    """It is set when release has revesion."""

    extra: dict[str, Any] | None = None

    def to_context(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "revision": self.revision,
        } | (self.extra or {})


class Publisher[T_O = BaseModel](BaseModel, metaclass=abc.ABCMeta):
    """Publishing component for release entity."""

    name: str
    """Publisher name to manage in this application."""
    options: T_O
    """Option values for methods."""
    template: str | None = None
    """Message template to publish release entity."""

    @abc.abstractmethod
    def publish(self, release: Release): ...


@runtime_checkable
class SourceModule(Protocol):
    """Protocol that defines requirements as 'Source' module."""

    Options: type[BaseModel]
    Source: type[Source]


@runtime_checkable
class PublisherModule(Protocol):
    """Protocol that defines requirements as 'Publisher' module."""

    Options: type[BaseModel]
    Publisher: type[Publisher]
