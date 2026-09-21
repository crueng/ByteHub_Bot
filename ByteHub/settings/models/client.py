from __future__ import annotations

from typing import Final, Self, override

from .section import Section

_STATUSES: Final = ["online", "idle", "dnd", "invisible"]

_ACTIVITIES: Final = ["playing", "streaming", "listening", "watching", "competing", "custom"]

class ActivitySettings:
    __slots__ = ["type", "text"]

    def __init__(self, type: str, text: str, /) -> None:
        self.type = type
        self.text = text

    @classmethod
    def read(cls, section: Section, /) -> Self:
        return cls(section.choice("type", "playing", _ACTIVITIES), section.text("text", ""))

    def is_set(self) -> bool:
        return bool(self.text)

    @override
    def __repr__(self) -> str:
        return f"<ActivitySettings type={self.type!r} text={self.text!r}>"

class ClientSettings:
    __slots__ = ["prefix", "owners", "status", "activity"]

    def __init__(self, prefix: str, owners: list[int], status: str, activity: ActivitySettings, /) -> None:
        self.prefix = prefix
        self.owners = owners
        self.status = status
        self.activity = activity

    @classmethod
    def read(cls, section: Section, /) -> Self:
        return cls(
            section.text("prefix", "!"),
            section.identifiers("owners"),
            section.choice("status", "online", _STATUSES),
            ActivitySettings.read(section.child("activity"))
        )

    @override
    def __repr__(self) -> str:
        return f"<ClientSettings prefix={self.prefix!r} status={self.status!r} owners={len(self.owners)}>"

__all__ = ["ActivitySettings", "ClientSettings"]