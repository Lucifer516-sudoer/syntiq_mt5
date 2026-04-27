import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import (
    MT5BoolCallResult,
    MT5DataCallResult,
    capture_last_error,
)


def market_book_add(symbol: str) -> MT5BoolCallResult:
    """Subscribe to market depth events for ``symbol``."""
    success = mt5.market_book_add(symbol)
    error = capture_last_error()
    return MT5BoolCallResult(success=success, error=error)


def market_book_get(symbol: str) -> MT5DataCallResult:
    """Return market depth entries for ``symbol``."""
    data = mt5.market_book_get(symbol)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def market_book_release(symbol: str) -> MT5BoolCallResult:
    """Unsubscribe from market depth events for ``symbol``."""
    success = mt5.market_book_release(symbol)
    error = capture_last_error()
    return MT5BoolCallResult(success=success, error=error)
