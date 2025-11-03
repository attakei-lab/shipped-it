import abc
import importlib
from typing import Any

from pydantic import BaseModel

from ..settings import PublisherSettings


class Publisher(BaseModel):
    name: str
    template: str
    options: BaseModel

    @abc.abstractmethod
    def publish(self, context: dict[str, Any]): ...


def load_publisher(name: str, settings: PublisherSettings) -> Publisher:
    def _resolve_module(name: str):
        if "." not in name:
            return f"{__name__}.{name}"
        return name

    module = importlib.import_module(_resolve_module(name))
    return module.Publisher(  # type: ignore[unresolved-attribute]
        name=name,
        template=settings.template,
        options=settings.options,
    )
