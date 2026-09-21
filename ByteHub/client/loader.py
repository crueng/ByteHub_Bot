from __future__ import annotations

from typing import TYPE_CHECKING, Final
from logging import getLogger
from pathlib import Path

from discord.ext import commands

from ..errors.client import FeatureFailed, MissingSetup

if TYPE_CHECKING:
    from ..settings.models.features import FeatureSettings

_PACKAGE: Final = "ByteHub.features"

_DIRECTORY: Final = Path(__file__).resolve().parents[1] / "features"

_log: Final = getLogger(__name__)

class Loader:
    __slots__ = ["client", "settings"]

    def __init__(self, client: commands.AutoShardedBot, settings: FeatureSettings, /) -> None:
        self.client = client
        self.settings = settings

    async def load(self) -> list[str]:
        loaded: list[str] = []

        for name in self.discover():
            if not self.settings.allows(name):
                _log.info("Skipping the disabled feature %s", name)

                continue

            await self._load(name)

            loaded.append(name)

        return loaded

    def discover(self) -> list[str]:
        if not _DIRECTORY.is_dir():
            return []

        found = [path.name for path in _DIRECTORY.iterdir() if (path / "__init__.py").is_file()]
        found.sort()

        return found

    async def _load(self, name: str, /) -> None:
        try:
            await self.client.load_extension(f"{_PACKAGE}.{name}")
        except commands.NoEntryPointError as error:
            raise MissingSetup(name) from error
        except commands.ExtensionError as error:
            raise FeatureFailed(name, str(error)) from error

__all__ = ["Loader"]