from __future__ import annotations

from typing import ClassVar

class ByteHubError(Exception):
    user_facing: ClassVar[bool] = False

class StartupError(ByteHubError):
    pass

__all__ = ["ByteHubError", "StartupError"]