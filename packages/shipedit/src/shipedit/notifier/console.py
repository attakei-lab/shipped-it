from typing import TypedDict

import jinja2

from . import Notifier as NotifierBase


class Context(TypedDict):
    name: str
    version: str


class Notifier(NotifierBase):
    def push(self, context: Context):
        tmpl = jinja2.Template(self.template)
        print(tmpl.render(context))
