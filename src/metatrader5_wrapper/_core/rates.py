from datetime import datetime

import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5DataCallResult, capture_last_error


def copy_rates_from(
    symbol: str,
    timeframe: int,
    date_from: datetime,
    count: int,
) -> MT5DataCallResult:
    """Return bars starting from ``date_from``."""
    data = mt5.copy_rates_from(symbol, timeframe, date_from, count)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def copy_rates_from_pos(
    symbol: str,
    timeframe: int,
    start_pos: int,
    count: int,
) -> MT5DataCallResult:
    """Return bars starting from ``start_pos``."""
    data = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def copy_rates_range(
    symbol: str,
    timeframe: int,
    date_from: datetime,
    date_to: datetime,
) -> MT5DataCallResult:
    """Return bars within the given date range."""
    data = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def copy_ticks_from(
    symbol: str,
    date_from: datetime,
    count: int,
    flags: int,
) -> MT5DataCallResult:
    """Return ticks starting from ``date_from``."""
    data = mt5.copy_ticks_from(symbol, date_from, count, flags)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def copy_ticks_range(
    symbol: str,
    date_from: datetime,
    date_to: datetime,
    flags: int,
) -> MT5DataCallResult:
    """Return ticks within the given date range."""
    data = mt5.copy_ticks_range(symbol, date_from, date_to, flags)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)
