import logging

import dotenv
from pydantic import AliasChoices, Field, FilePath, ValidationError, field_validator
from pydantic_settings import BaseSettings, CliApp, CliPositionalArg, SettingsConfigDict
from shipped_it import loader
from shipped_it.settings import discover_settings_file, load_settings, set_app_settings


class CliSettings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    settings_path: FilePath | None = None
    source: CliPositionalArg[str]
    """Package type of that shipped."""
    release: CliPositionalArg[str]
    """Name of target package."""
    extra_values: dict[str, str] = Field(
        default_factory=dict,
        validation_alias=AliasChoices("e", "extra-values"),
        json_schema_extra={"cli": {"nargs": "+"}},
    )
    """Values passed template context, this must be list of ``KEY=VALUE`` style string."""

    @field_validator("extra_values", mode="before")
    @classmethod
    def _parse_key_pairs(cls, items: list[str] | dict):
        if isinstance(items, dict):
            return items

        if not isinstance(items, list):
            raise ValueError("Invalid format")

        result = {}
        for item in items:
            if isinstance(item, str) and "=" in item:
                key, value = item.split("=", 1)
                result[key] = value
            else:
                raise ValueError("Invalid value")

        return result


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

    # Initialize storage
    if settings.storage:
        storage = loader.load_storage(settings.storage)
        storage.open()

    # Loading package app
    if args.source not in settings.source:
        print(f"Error: Package '{args.source}' not found in settings.")
        return 1
    src_settings = settings.source[args.source]
    source = loader.load_source(args.source, src_settings)
    release = source.make_release(args.release)
    if settings.storage:
        if storage.exists_release(release):
            print(f"Release '{args.release}' already exists in storage.")
            storage.close()
            return 0
        storage.save_release(release)
    publishers = [
        loader.load_publisher(name, settings)
        for name, settings in src_settings.publisher.items()
    ]
    for p in publishers:
        p.publish(release)

    if settings.storage:
        storage.close()
    return 0
