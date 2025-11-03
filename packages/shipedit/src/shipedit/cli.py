import logging

import dotenv
from pydantic import FilePath, ValidationError
from pydantic_settings import BaseSettings, CliApp, CliPositionalArg, SettingsConfigDict

from .publisher import load_publisher
from .source import load_source
from .settings import load_settings, discover_settings_file, set_app_settings


class CliSettings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    settings_path: FilePath | None = None
    source: CliPositionalArg[str]
    """Package type of that shiped."""
    release: CliPositionalArg[str]
    """Name of target package."""


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    try:
        args = CliApp.run(CliSettings)
        logging.debug("Arguments: %s %s", args.source, args.release)
        if args.settings_path is None:
            args.settings_path = discover_settings_file()
        settings = load_settings(args.settings_path)
        set_app_settings(settings)
    except ValidationError as e:
        print(f"Error: {e}")
        return 1

    # Loading package app
    if args.source not in settings.source:
        print(f"Error: Package '{args.source}' not found in settings.")
        return 1
    pkg_settings = settings.source[args.source]
    package = load_source(args.source, pkg_settings.options)
    context = package.build_context(args.release)
    publishers = [
        load_publisher(name, settings)
        for name, settings in pkg_settings.publisher.items()
    ]
    for p in publishers:
        p.publish(context)
    return 0
