from __future__ import annotations

from typing import Self, override

from .section import Section

class FeatureSettings:
    __slots__ = ["disabled"]

    def __init__(self, disabled: list[str], /) -> None:
        self.disabled = disabled

    @classmethod
    def read(cls, section: Section, /) -> Self:
        return cls([name.strip().casefold() for name in section.names("disabled")])

    def allows(self, name: str, /) -> bool:
        return name.casefold() not in self.disabled

    @override
    def __repr__(self) -> str:
        return f"<FeatureSettings disabled={self.disabled}>"

__all__ = ["FeatureSettings"]