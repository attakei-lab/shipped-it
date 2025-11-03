"""Domain models."""

from pydantic import BaseModel


class Source(BaseModel):
    """Source of releases."""

    name: str
    """Source name to manage in this application."""
    provider: str | None = None
    """Type name of this source."""

    def get_provider(self) -> str:
        """Retrive provider name.

        ``provider`` may be ``None``. If ``provider`` is ``None``, it returns value of ``name``.
        """
        return self.provider or self.name


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
