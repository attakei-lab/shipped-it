"""Domain models."""

from pydantic import BaseModel


class Source(BaseModel):
    """Source of releases."""

    name: str
    """Source name to manage in this application."""
    module: str | None = None
    """Module name that includes som behaviors source."""


class Release(BaseModel):
    """Release entity of sources."""

    source: Source
    """Source object that release is fetched from."""
    name: str
    """Name of this entity in source.
    
    This is made from package name, slug of blog, and source's behavior.
    """
    version: str | None = None
    """It is set when release has revesion."""


class Publisher(BaseModel):
    name: str
    """Publisher name to manage in this application."""
    module: str | None = None
    """Module name that includes som behaviors publisher."""
