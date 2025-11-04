from importlib import import_module

from . import models, settings


def load_source(name: str, settings: settings.SourceSettings) -> models.Source:
    """Load source module and create source object.

    If ``settings.module`` is valid string, load module from value.
    If ``settings.module`` is ``None``, load bundled module from ``name``.
    """
    fullname = settings.module or f"shipedit.source.{name}"
    module = import_module(fullname)
    if not isinstance(module, models.SourceModule):
        raise ValueError("Loaded module is not source.")
    return module.Source(
        name=name,
        options=settings.options,  # type: ignore[invalid-argument-type] - It converts automately by Pydantic.
    )


def load_publisher(name: str, settings: settings.PublisherSettings) -> models.Publisher:
    """Load pubisher module and create publisher object.

    If ``settings.module`` is valid string, load module from value.
    If ``settings.module`` is ``None``, load bundled module from ``name``.
    """
    fullname = settings.module or f"shipedit.publisher.{name}"
    module = import_module(fullname)
    if not isinstance(module, models.PublisherModule):
        raise ValueError("Loaded module is not publisher.")
    return module.Publisher(
        name=name,
        template=settings.template,
        options=settings.options,  # type: ignore[invalid-argument-type] - It converts automately by Pydantic.
    )
