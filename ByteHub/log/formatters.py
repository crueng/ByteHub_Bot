from __future__ import annotations

from logging import CRITICAL, DEBUG, ERROR, Formatter, INFO, LogRecord, WARNING
from typing import Final, override

_RESET: Final = "\x1b[0m"

_DIM: Final = "\x1b[38;5;245m"

_CLOCK: Final = "%H:%M:%S"

_COLOURS: Final = {
    DEBUG: "\x1b[38;5;244m",
    INFO: "\x1b[38;5;39m",
    WARNING: "\x1b[38;5;220m",
    ERROR: "\x1b[38;5;196m",
    CRITICAL: "\x1b[1;38;5;196m"
}

class FileFormatter(Formatter):
    def __init__(self) -> None:
        super().__init__(fmt="%(asctime)s %(levelname)-8s %(name)s %(message)s")

class ConsoleFormatter(Formatter):
    def __init__(self) -> None:
        super().__init__(fmt=self._layout(""), datefmt=_CLOCK)

        self.styles = {level: Formatter(fmt=self._layout(colour), datefmt=_CLOCK) for level, colour in _COLOURS.items()}

    @override
    def format(self, record: LogRecord) -> str:
        style = self.styles.get(record.levelno)

        if style is None:
            return super().format(record)

        return style.format(record)

    @staticmethod
    def _layout(colour: str, /) -> str:
        return f"{_DIM}%(asctime)s{_RESET} {colour}%(levelname)-8s{_RESET} {_DIM}%(name)s{_RESET} %(message)s"

__all__ = ["FileFormatter", "ConsoleFormatter"]