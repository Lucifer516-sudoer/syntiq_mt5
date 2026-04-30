from __future__ import annotations

from syntiq_mt5._core.mt5_import import mt5

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.market.candles import Candle


class MarketService:
    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        raw = call_mt5(mt5.copy_rates_from_pos, symbol, timeframe, 0, count)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_rates_from_pos", operation="copy_rates_from_pos")
        try:
            candles = [
                Candle(
                    time=int(row["time"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                )
                for row in raw.data
            ]
        except (KeyError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -4,
                        "message": f"Invalid MT5 candle payload: {exc}",
                    }
                ),
                context="copy_rates_from_pos",
                operation="copy_rates_from_pos",
            )
        return Result.ok(candles, context="copy_rates_from_pos", operation="copy_rates_from_pos")
