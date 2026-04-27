import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import (
    MT5BoolCallResult,
    MT5DataCallResult,
    capture_last_error,
)


def symbols_total() -> MT5DataCallResult:
    """Return the number of symbols available in the terminal."""
    data = mt5.symbols_total()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def symbols_get(*, group: str | None = None) -> MT5DataCallResult:
    """Return symbols, optionally filtered by an MT5 group mask."""
    data = mt5.symbols_get() if group is None else mt5.symbols_get(group=group)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def symbol_info(symbol: str) -> MT5DataCallResult:
    """Return info for one financial instrument."""
    data = mt5.symbol_info(symbol)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def symbol_info_tick(symbol: str) -> MT5DataCallResult:
    """Return the latest tick for one financial instrument."""
    data = mt5.symbol_info_tick(symbol)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def symbol_select(symbol: str, enable: bool = True) -> MT5BoolCallResult:
    """Select or remove a symbol in MarketWatch."""
    success = mt5.symbol_select(symbol, enable)
    error = capture_last_error()
    return MT5BoolCallResult(success=success, error=error)
