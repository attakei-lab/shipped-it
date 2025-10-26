import logging

from pydantic import ValidationError
from pydantic_settings import BaseSettings, CliApp, CliPositionalArg, SettingsConfigDict


class CliSettings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    package: CliPositionalArg[str]
    """Package type of that shiped."""
    name: CliPositionalArg[str]
    """Name of target package."""


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    try:
        args = CliApp.run(CliSettings)
        logging.debug("Arguments: %s %s", args.package, args.name)
    except ValidationError as e:
        print(f"Error: {e}")
        return 1

    return 0
