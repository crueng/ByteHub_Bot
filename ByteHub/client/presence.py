from __future__ import annotations

import discord

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from ..settings.models.client import ActivitySettings, ClientSettings

_STATUSES: Final = {
    "online": discord.Status.online,
    "idle": discord.Status.idle,
    "dnd": discord.Status.dnd,
    "invisible": discord.Status.invisible
}

_ACTIVITIES: Final = {
    "playing": discord.ActivityType.playing,
    "streaming": discord.ActivityType.streaming,
    "listening": discord.ActivityType.listening,
    "watching": discord.ActivityType.watching,
    "competing": discord.ActivityType.competing
}

class Presence:
    __slots__ = []

    @staticmethod
    def status(settings: ClientSettings, /) -> discord.Status:
        return _STATUSES.get(settings.status, discord.Status.online)

    @staticmethod
    def activity(settings: ActivitySettings, /) -> discord.BaseActivity | None:
        if not settings.is_set():
            return None

        if settings.type == "custom":
            return discord.CustomActivity(settings.text)

        activity = _ACTIVITIES.get(settings.type, discord.ActivityType.playing)

        return discord.Activity(type=activity, name=settings.text)

__all__ = ["Presence"]