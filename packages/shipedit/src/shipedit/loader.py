from importlib import import_module

from . import models, settings


def load_source[T_O](
    name: str, settings: settings.SourceSettings
) -> models.Source[T_O]:
    fullname = settings.module or f"shipedit.source.{name}"
    module = import_module(fullname)
    klass = getattr(module, "Source")
    return klass(name=name, options=settings.options)


def load_publisher[T_O](
    name: str, settings: settings.PublisherSettings
) -> models.Publisher[T_O]:
    fullname = settings.module or f"shipedit.publisher.{name}"
    module = import_module(fullname)
    klass = getattr(module, "Publisher")
    return klass(name=name, template=settings.template, options=settings.options)
