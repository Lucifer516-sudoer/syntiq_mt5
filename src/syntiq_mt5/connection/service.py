from __future__ import annotations

from syntiq_mt5._core.mt5_import import mt5

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.connection.models import LoginCredential


class ConnectionService:
    def __init__(self) -> None:
        self._initialized = False

    def initialize(self, credentials: LoginCredential | None = None) -> Result[None]:
        if self._initialized:
            return Result.ok(None, context="initialize", operation="initialize")
        kwargs = {"path": credentials.path} if credentials and credentials.path else {}
        raw = call_mt5(mt5.initialize, **kwargs)
        if not raw.data:
            return Result.fail(raw.error, context="initialize", operation="initialize")
        self._initialized = True
        return Result.ok(None, context="initialize", operation="initialize")

    def login(self, credentials: LoginCredential) -> Result[None]:
        raw = call_mt5(
            mt5.login,
            login=credentials.login,
            password=credentials.password.get_secret_value(),
            server=credentials.server,
        )
        if not raw.data:
            return Result.fail(raw.error, context="login", operation="login")
        return Result.ok(None, context="login", operation="login")

    def shutdown(self) -> Result[None]:
        raw = call_mt5(mt5.shutdown)
        self._initialized = False
        if raw.data is False:
            return Result.fail(raw.error, context="shutdown", operation="shutdown")
        return Result.ok(None, context="shutdown", operation="shutdown")
