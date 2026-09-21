from __future__ import annotations

from pathlib import Path
from typing import Final
from os import environ

class Paths:
    __slots__ = []

    root: Final = Path(__file__).resolve().parents[2]
    config: Final = root / "config"
    settings: Final = config / "settings.yaml"
    overrides: Final = config / "settings.local.yaml"
    data: Final = Path(environ.get("BYTEHUB_DATA_DIR") or root / "data")
    logs: Final = Path(environ.get("BYTEHUB_LOGS_DIR") or root / "logs")

    @classmethod
    def ensure_directories(cls) -> None:
        cls.data.mkdir(parents=True, exist_ok=True)
        cls.logs.mkdir(parents=True, exist_ok=True)

__all__ = ["Paths"]