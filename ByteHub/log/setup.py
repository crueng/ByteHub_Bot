from __future__ import annotations

from logging import WARNING, captureWarnings, getLogger
from typing import TYPE_CHECKING

from .handlers import Handlers

if TYPE_CHECKING:
    from ..settings.models.logging import LoggingSettings

class Logging:
    __slots__ = []

    @classmethod
    def configure(cls, settings: LoggingSettings, override: str | None, /) -> None:
        root = getLogger()

        for handler in list(root.handlers):
            root.removeHandler(handler)
            handler.close()

        root.addHandler(Handlers.console())
        root.addHandler(Handlers.file(settings.file))
        root.setLevel(WARNING)

        getLogger("ByteHub").setLevel(override or settings.level)
        getLogger("discord").setLevel(settings.discord_level)

        captureWarnings(True)

__all__ = ["Logging"]