from typing import TypedDict, override

import jinja2
from pydantic import BaseModel

from .. import models


class Options(BaseModel):
    pass


class Context(TypedDict):
    name: str
    revision: str


class Publisher(models.Publisher[Options]):
    @override
    def publish(self, release: models.Release):
        tmpl = jinja2.Template(self.template or "")
        print(tmpl.render(release.to_context()))
