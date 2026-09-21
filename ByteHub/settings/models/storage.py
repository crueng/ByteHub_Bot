from __future__ import annotations

from typing import Self, override

from .section import Section

class StorageSettings:
    __slots__ = ["name"]

    def __init__(self, name: str, /) -> None:
        self.name = name

    @classmethod
    def read(cls, section: Section, /) -> Self:
        return cls(section.text("name", "bytehub.db"))

    @override
    def __repr__(self) -> str:
        return f"<StorageSettings name={self.name!r}>"

__all__ = ["StorageSettings"]