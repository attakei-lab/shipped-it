import abc
import importlib
from typing import Any

from pydantic import BaseModel


class Source(BaseModel):
    name: str
    options: BaseModel

    @abc.abstractmethod
    def build_context(self, name: str) -> dict[str, Any]: ...


def load_source(name: str, options: dict[str, Any]) -> Source:
    def _resolve_module(name: str):
        if "." not in name:
            return f"{__name__}.{name}"
        return name

    module = importlib.import_module(_resolve_module(name))
    return module.Source(name=name, options=options)  # type: ignore[unresolved-attribute]
