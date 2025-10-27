import abc
import importlib
from typing import Any

from pydantic import BaseModel

from ..settings import NotifierSettings


class Notifier(BaseModel):
    name: str
    template: str

    @abc.abstractmethod
    def push(self, context: dict[str, Any]): ...


def load_notifier(name: str, settings: NotifierSettings) -> Notifier:
    def _resolve_module(name: str):
        if "." not in name:
            return f"{__name__}.{name}"
        return name

    module = importlib.import_module(_resolve_module(name))
    return module.Notifier(name=name, template=settings.template)  # type: ignore[unresolved-attribute]
