from __future__ import annotations

from typing import Final, Self, override

from .section import Section

_LEVELS: Final = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

class LogFileSettings:
    __slots__ = ["name", "max_megabytes", "backups"]

    def __init__(self, name: str, max_megabytes: int, backups: int, /) -> None:
        self.name = name
        self.max_megabytes = max_megabytes
        self.backups = backups

    @classmethod
    def read(cls, section: Section, /) -> Self:
        return cls(
            section.text("name", "bytehub.log"),
            section.number("max_megabytes", 5),
            section.number("backups", 5)
        )

    @property
    def max_bytes(self) -> int:
        return self.max_megabytes * 1024 * 1024

    def rotates(self) -> bool:
        return self.max_megabytes > 0

    @override
    def __repr__(self) -> str:
        return f"<LogFileSettings name={self.name!r} max_megabytes={self.max_megabytes} backups={self.backups}>"

class LoggingSettings:
    __slots__ = ["level", "discord_level", "file"]

    def __init__(self, level: str, discord_level: str, file: LogFileSettings, /) -> None:
        self.level = level
        self.discord_level = discord_level
        self.file = file

    @classmethod
    def read(cls, section: Section, /) -> Self:
        return cls(
            section.choice("level", "INFO", _LEVELS),
            section.choice("discord_level", "WARNING", _LEVELS),
            LogFileSettings.read(section.child("file"))
        )

    @override
    def __repr__(self) -> str:
        return f"<LoggingSettings level={self.level!r} discord_level={self.discord_level!r} file={self.file!r}>"

__all__ = ["LogFileSettings", "LoggingSettings"]