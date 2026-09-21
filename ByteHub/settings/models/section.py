from __future__ import annotations

from typing import Any, Self, cast

from ...errors.settings import InvalidSetting

class Section:
    __slots__ = ["data", "path"]

    def __init__(self, data: dict[str, Any], path: str, /) -> None:
        self.data = data
        self.path = path

    def child(self, key: str, /) -> Self:
        value: Any = self.data.get(key)

        if value is None:
            return type(self)({}, self._full(key))

        if not isinstance(value, dict):
            raise InvalidSetting(self._full(key), "a mapping")

        return type(self)(cast(dict[str, Any], value), self._full(key))

    def text(self, key: str, default: str, /) -> str:
        value: Any = self.data.get(key, default)

        if not isinstance(value, str):
            raise InvalidSetting(self._full(key), "a string")

        return value

    def choice(self, key: str, default: str, allowed: list[str], /) -> str:
        value = self.text(key, default).strip()

        for option in allowed:
            if option.casefold() == value.casefold():
                return option

        raise InvalidSetting(self._full(key), f"one of {', '.join(allowed)}")

    def flag(self, key: str, default: bool, /) -> bool:
        value: Any = self.data.get(key, default)

        if not isinstance(value, bool):
            raise InvalidSetting(self._full(key), "true or false")

        return value

    def number(self, key: str, default: int, /) -> int:
        value: Any = self.data.get(key, default)

        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidSetting(self._full(key), "a whole number")

        return value

    def names(self, key: str, /) -> list[str]:
        entries = self._sequence(key, "a list of names")
        names: list[str] = []

        for entry in entries:
            if not isinstance(entry, str):
                raise InvalidSetting(self._full(key), "a list of names")

            names.append(entry)

        return names

    def identifiers(self, key: str, /) -> list[int]:
        entries = self._sequence(key, "a list of ids")
        identifiers: list[int] = []

        for entry in entries:
            if not isinstance(entry, int) or isinstance(entry, bool):
                raise InvalidSetting(self._full(key), "a list of ids")

            identifiers.append(entry)

        return identifiers

    def _sequence(self, key: str, expected: str, /) -> list[Any]:
        value: Any = self.data.get(key)

        if value is None:
            return []

        if not isinstance(value, list):
            raise InvalidSetting(self._full(key), expected)

        return cast(list[Any], value)

    def _full(self, key: str, /) -> str:
        if not self.path:
            return key

        return f"{self.path}.{key}"

__all__ = ["Section"]