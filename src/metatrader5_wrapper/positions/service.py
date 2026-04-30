from __future__ import annotations

from metatrader5_wrapper._core.mt5_import import mt5

from metatrader5_wrapper._core.execution import Result
from metatrader5_wrapper._core.raw import call_mt5
from metatrader5_wrapper.positions.models import Position


class PositionService:
    def __init__(self) -> None:
        self._symbol_cache: dict[str, tuple[int, float]] = {}

    def positions(self, symbol: str | None = None) -> Result[list[Position]]:
        raw = call_mt5(mt5.positions_get, symbol=symbol) if symbol else call_mt5(mt5.positions_get)
        if raw.data is None:
            return Result.fail(raw.error, context="positions_get")
        rows = list(raw.data)
        symbols = {row.symbol for row in rows if row.symbol not in self._symbol_cache}
        for sym in symbols:
            info_raw = call_mt5(mt5.symbol_info, sym)
            if info_raw.data is None:
                return Result.fail(info_raw.error, context=f"symbol_info:{sym}")
            self._symbol_cache[sym] = (int(info_raw.data.digits), float(info_raw.data.point))

        try:
            parsed = [
                Position(
                    ticket=int(row.ticket),
                    symbol=row.symbol,
                    price_open=float(row.price_open),
                    price_current=float(row.price_current),
                    tp=float(row.tp),
                    sl=float(row.sl),
                    volume=float(row.volume),
                    type=int(row.type),
                    digits=self._symbol_cache[row.symbol][0],
                    point=self._symbol_cache[row.symbol][1],
                )
                for row in rows
            ]
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 position payload: {exc}",
                    }
                ),
                context="positions_get",
            )
        return Result.ok(parsed, context="positions_get")
