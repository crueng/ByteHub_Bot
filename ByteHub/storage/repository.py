from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import aiosqlite

    from contextlib import AbstractAsyncContextManager
    from collections.abc import Iterable

    from .database import Database

class Repository:
    __slots__ = ["database"]

    def __init__(self, database: Database, /) -> None:
        self.database = database

    def transaction(self) -> AbstractAsyncContextManager[None]:
        return self.database.transaction()

    async def execute(self, sql: str, parameters: Iterable[Any] = (), /) -> None:
        await self.database.execute(sql, parameters)

    async def fetch_one(self, sql: str, parameters: Iterable[Any] = (), /) -> aiosqlite.Row | None:
        return await self.database.fetch_one(sql, parameters)

    async def fetch_all(self, sql: str, parameters: Iterable[Any] = (), /) -> list[aiosqlite.Row]:
        return await self.database.fetch_all(sql, parameters)

__all__ = ["Repository"]