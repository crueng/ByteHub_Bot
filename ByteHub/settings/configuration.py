from __future__ import annotations

import yaml

from typing import TYPE_CHECKING, Any, cast

from ..errors.settings import MissingSettings, UnreadableSettings
from .models.settings import Settings
from .paths import Paths

if TYPE_CHECKING:
    from pathlib import Path

class Configuration:
    __slots__ = []

    @classmethod
    def load(cls) -> Settings:
        base = cls._read(Paths.settings)

        if base is None:
            raise MissingSettings(Paths.settings)

        overrides = cls._read(Paths.overrides)

        if overrides is None:
            return Settings.read(base)

        return Settings.read(cls._merge(base, overrides))

    @classmethod
    def _read(cls, path: Path, /) -> dict[str, Any] | None:
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except OSError as error:
            raise UnreadableSettings(path, error.strerror or "it could not be opened") from error

        try:
            data: Any = yaml.safe_load(text)
        except yaml.YAMLError as error:
            raise UnreadableSettings(path, cls._reason(error)) from error

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise UnreadableSettings(path, "it must hold a mapping at the top level")

        return cast(dict[str, Any], data)

    @classmethod
    def _merge(cls, base: dict[str, Any], overrides: dict[str, Any], /) -> dict[str, Any]:
        merged = dict(base)

        for key, value in overrides.items():
            current = merged.get(key)

            if isinstance(current, dict) and isinstance(value, dict):
                merged[key] = cls._merge(cast(dict[str, Any], current), cast(dict[str, Any], value))
            else:
                merged[key] = value

        return merged

    @staticmethod
    def _reason(error: yaml.YAMLError, /) -> str:
        if not isinstance(error, yaml.MarkedYAMLError) or error.problem is None:
            return "it is not valid YAML"

        mark = error.problem_mark

        if mark is None:
            return error.problem

        return f"{error.problem} at line {mark.line + 1}"

__all__ = ["Configuration"]