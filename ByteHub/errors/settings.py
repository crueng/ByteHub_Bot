from __future__ import annotations

from typing import TYPE_CHECKING

from .base import StartupError

if TYPE_CHECKING:
    from pathlib import Path

class SettingsError(StartupError):
    pass

class MissingEnvironment(SettingsError):
    def __init__(self, name: str, /) -> None:
        self.name = name

        super().__init__(f"{name} is set neither in the environment nor in .env")

class InvalidEnvironment(SettingsError):
    def __init__(self, name: str, value: str, expected: str, /) -> None:
        self.name = name
        self.value = value
        self.expected = expected

        super().__init__(f"{name} is set to {value!r}, expected {expected}")

class MissingSettings(SettingsError):
    def __init__(self, path: Path, /) -> None:
        self.path = path

        super().__init__(f"no settings file at {path}")

class UnreadableSettings(SettingsError):
    def __init__(self, path: Path, reason: str, /) -> None:
        self.path = path
        self.reason = reason

        super().__init__(f"the settings file at {path} could not be read, {reason}")

class InvalidSetting(SettingsError):
    def __init__(self, key: str, expected: str, /) -> None:
        self.key = key
        self.expected = expected

        super().__init__(f"the setting {key} must be {expected}")

__all__ = ["SettingsError", "MissingEnvironment", "InvalidEnvironment", "MissingSettings", "UnreadableSettings", "InvalidSetting"]