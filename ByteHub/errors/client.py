from __future__ import annotations

from .base import StartupError

class ClientError(StartupError):
    pass

class LoginRefused(ClientError):
    def __init__(self) -> None:
        super().__init__("Discord refused the token, check DISCORD_TOKEN")

class IntentsRefused(ClientError):
    def __init__(self) -> None:
        super().__init__("Discord refused the privileged intents, enable Server Members, Message Content and Presence in the developer portal")

class FeatureFailed(ClientError):
    def __init__(self, name: str, reason: str, /) -> None:
        self.name = name
        self.reason = reason

        super().__init__(f"the feature {name} could not be loaded, {reason}")

class MissingSetup(ClientError):
    def __init__(self, name: str, /) -> None:
        self.name = name

        super().__init__(f"the feature {name} has no setup function, so nothing registers it")

__all__ = ["ClientError", "LoginRefused", "IntentsRefused", "FeatureFailed", "MissingSetup"]