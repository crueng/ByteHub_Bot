from __future__ import annotations

import aiosqlite
import re

from typing import TYPE_CHECKING, Final, override

from ..errors.storage import InvalidMigration, MigrationFailed, SchemaTooNew

if TYPE_CHECKING:
    from pathlib import Path

    from .database import Database

_PATTERN: Final = re.compile(r"^(?P<version>\d{3,})_[a-z0-9_]+\.sql$")

_TABLE: Final = "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"

class Migration:
    __slots__ = ["version", "path"]

    def __init__(self, version: int, path: Path, /) -> None:
        self.version = version
        self.path = path

    @property
    def name(self) -> str:
        return self.path.name

    @override
    def __repr__(self) -> str:
        return f"<Migration version={self.version} name={self.name!r}>"

class Migrations:
    __slots__ = ["database", "directory"]

    def __init__(self, database: Database, directory: Path, /) -> None:
        self.database = database
        self.directory = directory

    async def apply(self) -> int:
        await self.database.execute(_TABLE)

        current = await self._current()
        found = self._discover()
        known = found[-1].version if found else 0

        if current > known:
            raise SchemaTooNew(current, known)

        for migration in found:
            if migration.version > current:
                await self._run(migration)

        return known

    async def _current(self) -> int:
        row = await self.database.fetch_one("SELECT MAX(version) FROM schema_version")

        if row is None or row[0] is None:
            return 0

        return int(row[0])

    def _discover(self) -> list[Migration]:
        if not self.directory.is_dir():
            return []

        found: list[Migration] = []

        for path in self.directory.iterdir():
            if path.suffix != ".sql":
                continue

            match = _PATTERN.match(path.name)

            if match is None:
                raise InvalidMigration(path.name)

            found.append(Migration(int(match["version"]), path))

        found.sort(key=lambda migration: migration.version)

        return found

    async def _run(self, migration: Migration, /) -> None:
        try:
            statements = migration.path.read_text(encoding="utf-8")
        except OSError as error:
            raise MigrationFailed(migration.name, error.strerror or str(error)) from error

        script = f"BEGIN;\n{statements}\nINSERT INTO schema_version (version) VALUES ({migration.version});\nCOMMIT;"

        try:
            await self.database.execute_script(script)
        except aiosqlite.Error as error:
            await self.database.execute("ROLLBACK")

            raise MigrationFailed(migration.name, str(error)) from error

__all__ = ["Migration", "Migrations"]