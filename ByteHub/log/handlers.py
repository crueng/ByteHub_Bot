from __future__ import annotations

from logging.handlers import RotatingFileHandler
from logging import Handler, StreamHandler
from typing import TYPE_CHECKING
from sys import stdout

from .formatters import ConsoleFormatter, FileFormatter
from ..errors.base import StartupError
from ..settings.paths import Paths

if TYPE_CHECKING:
    from ..settings.models.logging import LogFileSettings

class Handlers:
    __slots__ = []

    @staticmethod
    def console() -> Handler:
        handler = StreamHandler(stdout)

        if stdout.isatty():
            handler.setFormatter(ConsoleFormatter())
        else:
            handler.setFormatter(FileFormatter())

        return handler

    @staticmethod
    def file(settings: LogFileSettings, /) -> Handler:
        path = Paths.logs / settings.name

        try:
            Paths.logs.mkdir(parents=True, exist_ok=True)

            handler = RotatingFileHandler(
                filename=path,
                maxBytes=settings.max_bytes,
                backupCount=settings.backups,
                encoding="utf-8"
            )
        except OSError as error:
            raise StartupError(f"the log file at {path} could not be opened, {error.strerror or error}") from error

        handler.setFormatter(FileFormatter())

        return handler

__all__ = ["Handlers"]