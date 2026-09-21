from __future__ import annotations

import aiosqlite

from collections.abc import AsyncGenerator, Iterable
from typing import TYPE_CHECKING, Any, Final
from contextlib import asynccontextmanager

from ..errors.storage import DatabaseUnavailable

if TYPE_CHECKING:
    from pathlib import Path

_PRAGMAS: Final = [
    "PRAGMA journal_mode = WAL",
    "PRAGMA foreign_keys = ON",
    "PRAGMA synchronous = NORMAL"
]

class Database:
    __slots__ = ["path", "_connection"]

    def __init__(self, path: Path, /) -> None:
        self.path = path
        self._connection: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        if self._connection is not None:
            return

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)

            connection = await aiosqlite.connect(self.path, isolation_level=None)

            for pragma in _PRAGMAS:
                await connection.execute(pragma)
        except (OSError, aiosqlite.Error) as error:
            raise DatabaseUnavailable(self.path, str(error)) from error

        connection.row_factory = aiosqlite.Row
        self._connection = connection

    async def close(self) -> None:
        connection = self._connection

        if connection is None:
            return

        self._connection = None

        await connection.close()

    def is_connected(self) -> bool:
        return self._connection is not None

    async def execute(self, sql: str, parameters: Iterable[Any] = (), /) -> None:
        await self._require().execute(sql, parameters)

    async def execute_script(self, sql: str, /) -> None:
        await self._require().executescript(sql)

    async def fetch_one(self, sql: str, parameters: Iterable[Any] = (), /) -> aiosqlite.Row | None:
        async with self._require().execute(sql, parameters) as cursor:
            return await cursor.fetchone()

    async def fetch_all(self, sql: str, parameters: Iterable[Any] = (), /) -> list[aiosqlite.Row]:
        async with self._require().execute(sql, parameters) as cursor:
            return list(await cursor.fetchall())

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None]:
        connection = self._require()

        await connection.execute("BEGIN")

        try:
            yield
        except BaseException:
            await connection.rollback()

            raise

        await connection.commit()

    def _require(self) -> aiosqlite.Connection:
        connection = self._connection

        if connection is None:
            raise DatabaseUnavailable(self.path, "it is not connected")

        return connection

__all__ = ["Database"]