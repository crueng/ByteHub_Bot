from __future__ import annotations

from typing import TYPE_CHECKING

from .base import StartupError

if TYPE_CHECKING:
    from pathlib import Path

class StorageError(StartupError):
    pass

class DatabaseUnavailable(StorageError):
    def __init__(self, path: Path, reason: str, /) -> None:
        self.path = path
        self.reason = reason

        super().__init__(f"the database at {path} could not be opened, {reason}")

class InvalidMigration(StorageError):
    def __init__(self, name: str, /) -> None:
        self.name = name

        super().__init__(f"the migration {name} is not named like 001_initial.sql")

class MigrationFailed(StorageError):
    def __init__(self, name: str, reason: str, /) -> None:
        self.name = name
        self.reason = reason

        super().__init__(f"the migration {name} failed, {reason}")

class SchemaTooNew(StorageError):
    def __init__(self, found: int, known: int, /) -> None:
        self.found = found
        self.known = known

        super().__init__(f"the database is at schema version {found}, but this build only knows {known}")

__all__ = ["StorageError", "DatabaseUnavailable", "InvalidMigration", "MigrationFailed", "SchemaTooNew"]