from __future__ import annotations

from typing import TYPE_CHECKING, Final
from logging import getLogger

from discord.ext import commands

if TYPE_CHECKING:
    from ..core import Client

_log: Final = getLogger(__name__)

class Lifecycle(commands.Cog):
    def __init__(self, client: Client, /) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        user = self.client.user

        if user is None:
            return

        _log.info("Signed in as %s with the id %s", user, user.id)
        _log.info("Serving %s guilds across %s shards", len(self.client.guilds), self.client.shard_count)

    @commands.Cog.listener()
    async def on_shard_ready(self, shard: int, /) -> None:
        _log.info("Shard %s is ready", shard)

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard: int, /) -> None:
        _log.info("Shard %s resumed its session", shard)

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard: int, /) -> None:
        _log.warning("Shard %s lost the gateway", shard)

__all__ = ["Lifecycle"]