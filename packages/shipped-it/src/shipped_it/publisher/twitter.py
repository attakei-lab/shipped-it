"""(X)Twitter task definitions."""

from __future__ import annotations

from typing import TypedDict, override

import jinja2
import tweepy
from pydantic import BaseModel

from .. import models
from ..settings import get_app_settings


class Options(BaseModel):
    credential: str


class Context(TypedDict):
    name: str
    version: str


class AppCredentials(BaseModel):
    """Credentials set of Twitter Application."""

    bearer_token: str
    consumer_key: str
    consumer_key_secret: str
    access_token: str
    access_token_secret: str

    def create_client(self) -> tweepy.Client:
        """Initialize Tweepy client."""
        return tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_key_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )


class Publisher(models.Publisher[Options]):
    @override
    def publish(self, release: models.Release, extra_values: dict[str, str]):
        tool_settings = get_app_settings().credential[self.options.credential]
        cred = AppCredentials(**tool_settings)
        tmpl = jinja2.Template(self.template or "")
        cred.create_client().create_tweet(
            text=tmpl.render(release.to_context(), extra=extra_values)
        )
