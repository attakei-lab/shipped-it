import logging

from pydantic import FilePath, ValidationError
from pydantic_settings import BaseSettings, CliApp, CliPositionalArg, SettingsConfigDict

from .notifier import load_notifier
from .package import load_package
from .settings import load_settings, discover_settings_file


class CliSettings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    settings_path: FilePath | None = None
    package: CliPositionalArg[str]
    """Package type of that shiped."""
    name: CliPositionalArg[str]
    """Name of target package."""


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    try:
        args = CliApp.run(CliSettings)
        logging.debug("Arguments: %s %s", args.package, args.name)
        if args.settings_path is None:
            args.settings_path = discover_settings_file()
        settings = load_settings(args.settings_path)
    except ValidationError as e:
        print(f"Error: {e}")
        return 1

    # Loading package app
    if args.package not in settings.package:
        print(f"Error: Package '{args.package}' not found in settings.")
        return 1
    pkg_settings = settings.package[args.package]
    package = load_package(args.package, pkg_settings.options)
    context = package.build_context(args.name)
    notifiers = [
        load_notifier(name, settings)
        for name, settings in pkg_settings.notifier.items()
    ]
    for notifier in notifiers:
        notifier.push(context)
    return 0
