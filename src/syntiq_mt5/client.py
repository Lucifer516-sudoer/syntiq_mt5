from __future__ import annotations

import logging
from time import perf_counter

from syntiq_mt5._core.errors import MT5ErrorInfo
from syntiq_mt5._core.execution import Result
from syntiq_mt5.connection.models import LoginCredential
from syntiq_mt5.connection.service import ConnectionService
from syntiq_mt5.market.candles import Candle
from syntiq_mt5.market.symbols import MarketService
from syntiq_mt5.positions.models import Position
from syntiq_mt5.positions.service import PositionService


class MetaTrader5Client:
    def __init__(self, *, debug: bool = False) -> None:
        self.connection = ConnectionService()
        self._positions = PositionService()
        self.market = MarketService()
        self._initialized = False
        self._logged_in = False
        self._debug = debug
        self._logger = logging.getLogger("syntiq_mt5")

    def __enter__(self) -> "MetaTrader5Client":
        return self

    def __exit__(self, *_: object) -> None:
        shutdown_result = self.shutdown()
        if self._debug and not shutdown_result.success:
            self._logger.error("[MT5] shutdown | failure | code=%s", shutdown_result.error_code)

    def _log_result(self, name: str, result: Result[object], started: float) -> None:
        if not self._debug:
            return
        elapsed_ms = int((perf_counter() - started) * 1000)
        status = "success" if result.success else "failure"
        code = 0 if result.success else result.error_code
        self._logger.debug("[MT5] %s | %s | code=%s | %sms", name, status, code, elapsed_ms)

    def _guard_initialized(self, operation: str) -> Result[None] | None:
        if self._initialized:
            return None
        return Result.fail(
            MT5ErrorInfo(code=-10, message="Client not initialized. Call initialize() first."),
            context=operation,
            operation=operation,
        )

    def _guard_result(self, operation: str) -> Result[object] | None:
        guard = self._guard_initialized(operation)
        if guard is None:
            return None
        return Result.fail(
            MT5ErrorInfo(
                code=guard.error_code or -10,
                message=guard.error_message or "Client not initialized. Call initialize() first.",
            ),
            context=operation,
            operation=operation,
        )

    def initialize(self, credentials: LoginCredential | None = None) -> Result[None]:
        started = perf_counter()
        result = self.connection.initialize(credentials)
        self._initialized = result.success
        self._log_result("initialize", result, started)
        return result

    def login(self, credentials: LoginCredential) -> Result[None]:
        guard = self._guard_initialized("login")
        if guard is not None:
            self._log_result("login", guard, perf_counter())
            return guard
        started = perf_counter()
        result = self.connection.login(credentials)
        self._logged_in = result.success
        self._log_result("login", result, started)
        return result

    def shutdown(self) -> Result[None]:
        started = perf_counter()
        result = self.connection.shutdown()
        self._initialized = False
        self._logged_in = False
        self._log_result("shutdown", result, started)
        return result

    def positions(self, symbol: str | None = None) -> Result[list[Position]]:
        guard = self._guard_result("positions_get")
        if guard is not None:
            return Result[list[Position]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._positions.positions(symbol=symbol)
        self._log_result("positions_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        guard = self._guard_result("copy_rates_from_pos")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.get_candles(symbol=symbol, timeframe=timeframe, count=count)
        self._log_result(
            "copy_rates_from_pos", Result[object].model_validate(result.model_dump()), started
        )
        return result
