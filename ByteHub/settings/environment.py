from __future__ import annotations

from typing import Final, Self, override
from os import environ

from dotenv import load_dotenv

from ..errors.settings import InvalidEnvironment, MissingEnvironment
from .paths import Paths

_PRODUCTION: Final = "production"

_ENVIRONMENTS: Final = ["development", _PRODUCTION]

_LEVELS: Final = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

class Environment:
    __slots__ = ["token", "name", "log_level", "guild_id"]

    def __init__(self, token: str, name: str, log_level: str | None, guild_id: int | None, /) -> None:
        self.token = token
        self.name = name
        self.log_level = log_level
        self.guild_id = guild_id

    @classmethod
    def load(cls) -> Self:
        load_dotenv(dotenv_path=Paths.root / ".env")

        return cls(cls._token(), cls._name(), cls._log_level(), cls._guild_id())

    def is_production(self) -> bool:
        return self.name == _PRODUCTION

    @staticmethod
    def _token() -> str:
        token = environ.get("DISCORD_TOKEN", "").strip()

        if not token:
            raise MissingEnvironment("DISCORD_TOKEN")

        return token

    @staticmethod
    def _name() -> str:
        name = environ.get("BYTEHUB_ENVIRONMENT", "").strip().lower() or "development"

        if name not in _ENVIRONMENTS:
            raise InvalidEnvironment("BYTEHUB_ENVIRONMENT", name, "development or production")

        return name

    @staticmethod
    def _log_level() -> str | None:
        level = environ.get("BYTEHUB_LOG_LEVEL", "").strip().upper()

        if not level:
            return None

        if level not in _LEVELS:
            raise InvalidEnvironment("BYTEHUB_LOG_LEVEL", level, f"one of {', '.join(_LEVELS)}")

        return level

    @staticmethod
    def _guild_id() -> int | None:
        raw = environ.get("BYTEHUB_GUILD_ID", "").strip()

        if not raw:
            return None

        if not raw.isdigit():
            raise InvalidEnvironment("BYTEHUB_GUILD_ID", raw, "a guild id")

        return int(raw)

    @override
    def __repr__(self) -> str:
        return f"<Environment name={self.name!r} guild_id={self.guild_id}>"

__all__ = ["Environment"]