from __future__ import annotations

from datetime import datetime

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.ticks.models import Tick


class TickService:
    """Retrieves tick data from the MT5 terminal.

    Wraps ``mt5.copy_ticks_from()`` and ``mt5.copy_ticks_range()`` via
    ``call_mt5``, parses the raw tick structs (which may arrive as either
    attribute-bearing objects or plain dicts depending on the MT5 build)
    into ``Tick`` models, and returns ``Result[list[Tick]]``.
    """
    def copy_ticks_from(
        self, symbol: str, date_from: datetime, count: int, flags: int
    ) -> Result[list[Tick]]:
        raw = call_mt5(mt5.copy_ticks_from, symbol, date_from, count, flags)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_ticks_from", operation="copy_ticks_from")
        try:
            ticks = [
                Tick(
                    time=int(tick.time if hasattr(tick, "time") else tick["time"]),
                    bid=float(tick.bid if hasattr(tick, "bid") else tick["bid"]),
                    ask=float(tick.ask if hasattr(tick, "ask") else tick["ask"]),
                    last=float(tick.last if hasattr(tick, "last") else tick["last"]),
                    volume=int(tick.volume if hasattr(tick, "volume") else tick["volume"]),
                    time_msc=int(tick.time_msc if hasattr(tick, "time_msc") else tick["time_msc"]),
                    flags=int(tick.flags if hasattr(tick, "flags") else tick["flags"]),
                    volume_real=float(tick.volume_real if hasattr(tick, "volume_real") else tick["volume_real"]),
                )
                for tick in raw.data
            ]
        except (KeyError, AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1004,
                        "message": f"Invalid MT5 copy_ticks_from payload: {exc}",
                    }
                ),
                context="copy_ticks_from",
                operation="copy_ticks_from",
            )
        return Result.ok(ticks, context="copy_ticks_from", operation="copy_ticks_from")

    def copy_ticks_range(
        self, symbol: str, date_from: datetime, date_to: datetime, flags: int
    ) -> Result[list[Tick]]:
        raw = call_mt5(mt5.copy_ticks_range, symbol, date_from, date_to, flags)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_ticks_range", operation="copy_ticks_range")
        try:
            ticks = [
                Tick(
                    time=int(tick.time if hasattr(tick, "time") else tick["time"]),
                    bid=float(tick.bid if hasattr(tick, "bid") else tick["bid"]),
                    ask=float(tick.ask if hasattr(tick, "ask") else tick["ask"]),
                    last=float(tick.last if hasattr(tick, "last") else tick["last"]),
                    volume=int(tick.volume if hasattr(tick, "volume") else tick["volume"]),
                    time_msc=int(tick.time_msc if hasattr(tick, "time_msc") else tick["time_msc"]),
                    flags=int(tick.flags if hasattr(tick, "flags") else tick["flags"]),
                    volume_real=float(tick.volume_real if hasattr(tick, "volume_real") else tick["volume_real"]),
                )
                for tick in raw.data
            ]
        except (KeyError, AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1004,
                        "message": f"Invalid MT5 copy_ticks_range payload: {exc}",
                    }
                ),
                context="copy_ticks_range",
                operation="copy_ticks_range",
            )
        return Result.ok(ticks, context="copy_ticks_range", operation="copy_ticks_range")
