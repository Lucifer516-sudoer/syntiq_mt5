from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.market_book.models import BookEntry


class MarketBookService:
    """Manages market depth (DOM) subscriptions and snapshots for the MT5 terminal.

    Wraps ``mt5.market_book_add()``, ``mt5.market_book_get()``, and
    ``mt5.market_book_release()`` via ``call_mt5``, parses raw
    ``BookInfo`` structs into ``BookEntry`` models, and returns
    ``Result[T]``.
    """
    def market_book_add(self, symbol: str) -> Result[bool]:
        raw = call_mt5(mt5.market_book_add, symbol)
        if raw.data is None:
            return Result.fail(raw.error, context="market_book_add", operation="market_book_add")
        try:
            success = bool(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 market_book_add payload: {exc}",
                    }
                ),
                context="market_book_add",
                operation="market_book_add",
            )
        return Result.ok(success, context="market_book_add", operation="market_book_add")

    def market_book_get(self, symbol: str) -> Result[list[BookEntry]]:
        raw = call_mt5(mt5.market_book_get, symbol)
        if raw.data is None:
            return Result.fail(raw.error, context="market_book_get", operation="market_book_get")
        try:
            entries = [
                BookEntry(
                    type=int(entry.type),
                    price=float(entry.price),
                    volume=int(entry.volume),
                    volume_real=float(entry.volume_real),
                )
                for entry in raw.data
            ]
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 market_book_get payload: {exc}",
                    }
                ),
                context="market_book_get",
                operation="market_book_get",
            )
        return Result.ok(entries, context="market_book_get", operation="market_book_get")

    def market_book_release(self, symbol: str) -> Result[bool]:
        raw = call_mt5(mt5.market_book_release, symbol)
        if raw.data is None:
            return Result.fail(raw.error, context="market_book_release", operation="market_book_release")
        try:
            success = bool(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 market_book_release payload: {exc}",
                    }
                ),
                context="market_book_release",
                operation="market_book_release",
            )
        return Result.ok(success, context="market_book_release", operation="market_book_release")
