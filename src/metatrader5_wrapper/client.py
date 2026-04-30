from __future__ import annotations

from metatrader5_wrapper._core.execution import Result
from metatrader5_wrapper.connection.models import LoginCredentials
from metatrader5_wrapper.connection.service import ConnectionService
from metatrader5_wrapper.market.candles import Candle
from metatrader5_wrapper.market.symbols import MarketService
from metatrader5_wrapper.positions.models import Position
from metatrader5_wrapper.positions.service import PositionService


class MetaTrader5Client:
    def __init__(self) -> None:
        self.connection = ConnectionService()
        self._positions = PositionService()
        self.market = MarketService()

    def __enter__(self) -> "MetaTrader5Client":
        return self

    def __exit__(self, *_: object) -> None:
        self.shutdown()

    def initialize(self, credentials: LoginCredentials | None = None) -> Result[None]:
        return self.connection.initialize(credentials)

    def login(self, credentials: LoginCredentials) -> Result[None]:
        return self.connection.login(credentials)

    def shutdown(self) -> Result[None]:
        return self.connection.shutdown()

    def positions(self, symbol: str | None = None) -> Result[list[Position]]:
        return self._positions.positions(symbol=symbol)

    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        return self.market.get_candles(symbol=symbol, timeframe=timeframe, count=count)
