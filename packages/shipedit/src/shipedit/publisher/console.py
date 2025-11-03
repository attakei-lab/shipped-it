from typing import TypedDict

import jinja2

from . import Publisher as PublisherBase


class Context(TypedDict):
    name: str
    version: str


class Publisher(PublisherBase):
    def publish(self, context: Context):
        tmpl = jinja2.Template(self.template)
        print(tmpl.render(context))
