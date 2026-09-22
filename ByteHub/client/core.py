from __future__ import annotations

import discord

from typing import TYPE_CHECKING, Final, override
from discord.ext import commands
from logging import getLogger
from pathlib import Path

from ..errors.client import IntentsRefused, LoginRefused
from ..storage.migrations import Migrations
from listeners.lifecycle import Lifecycle
from ..storage.database import Database
from ..settings.paths import Paths
from .presence import Presence
from .loader import Loader

if TYPE_CHECKING:
    from ..settings.models.settings import Settings
    from ..settings.environment import Environment

_SCHEMA: Final = Path(__file__).resolve().parents[1] / "storage" / "schema"

_MENTIONS: Final = discord.AllowedMentions(everyone=False, roles=False)

_log: Final = getLogger(__name__)

class Client(commands.AutoShardedBot):
    def __init__(self, settings: Settings, environment: Environment, /) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.client.prefix),
            intents=discord.Intents.all(),
            owner_ids=set(settings.client.owners),
            status=Presence.status(settings.client),
            activity=Presence.activity(settings.client.activity),
            allowed_mentions=_MENTIONS,
            case_insensitive=True,
            help_command=None
        )

        self.settings = settings
        self.environment = environment
        self.database = Database(Paths.data / settings.storage.name)
        self.migrations = Migrations(self.database, _SCHEMA)
        self.loader = Loader(self, settings.features)

    @override
    async def setup_hook(self) -> None:
        await self.add_cog(Lifecycle(self))

        await self.database.connect()

        version = await self.migrations.apply()

        _log.info("The database is at schema version %s", version)

        loaded = await self.loader.load()

        _log.info("Loaded %s of %s features", len(loaded), len(self.loader.discover()))

        await self._synchronise()

    @override
    async def start(self, token: str, *, reconnect: bool = True) -> None:
        try:
            await super().start(token, reconnect=reconnect)
        except discord.LoginFailure as error:
            raise LoginRefused() from error
        except discord.PrivilegedIntentsRequired as error:
            raise IntentsRefused() from error

    @override
    async def close(self) -> None:
        try:
            await super().close()
        except AttributeError:
            _log.debug("The gateway was never opened, so there is nothing to close")
        finally:
            await self.database.close()

    async def _synchronise(self) -> None:
        if self.environment.guild_id is None:
            return

        guild = discord.Object(self.environment.guild_id)

        self.tree.copy_global_to(guild=guild)

        synchronised = await self.tree.sync(guild=guild)

        _log.info("Synchronised %s commands to guild %s", len(synchronised), self.environment.guild_id)

__all__ = ["Client"]