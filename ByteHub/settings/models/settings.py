from __future__ import annotations

from typing import Any, Self, override

from .features import FeatureSettings
from .logging import LoggingSettings
from .storage import StorageSettings
from .client import ClientSettings
from .section import Section

class Settings:
    __slots__ = ["client", "logging", "storage", "features"]

    def __init__(
        self,
        client: ClientSettings,
        logging: LoggingSettings,
        storage: StorageSettings,
        features: FeatureSettings,
        /
    ) -> None:
        self.client = client
        self.logging = logging
        self.storage = storage
        self.features = features

    @classmethod
    def read(cls, data: dict[str, Any], /) -> Self:
        root = Section(data, "")

        return cls(
            ClientSettings.read(root.child("client")),
            LoggingSettings.read(root.child("logging")),
            StorageSettings.read(root.child("database")),
            FeatureSettings.read(root.child("features"))
        )

    @override
    def __repr__(self) -> str:
        return f"<Settings client={self.client!r} logging={self.logging!r} storage={self.storage!r} features={self.features!r}>"

__all__ = ["Settings"]