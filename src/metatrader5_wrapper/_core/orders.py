from typing import Any

import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5DataCallResult, capture_last_error


def orders_total() -> MT5DataCallResult:
    """Return the number of active orders."""
    data = mt5.orders_total()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def orders_get(
    *,
    symbol: str | None = None,
    group: str | None = None,
    ticket: int | None = None,
) -> MT5DataCallResult:
    """Return active orders using MT5's supported filters."""
    if symbol is not None:
        data = mt5.orders_get(symbol=symbol)
    elif group is not None:
        data = mt5.orders_get(group=group)
    elif ticket is not None:
        data = mt5.orders_get(ticket=ticket)
    else:
        data = mt5.orders_get()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def order_calc_margin(
    action: int,
    symbol: str,
    volume: float,
    price: float,
) -> MT5DataCallResult:
    """Return margin required for a trading operation."""
    data = mt5.order_calc_margin(action, symbol, volume, price)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def order_calc_profit(
    action: int,
    symbol: str,
    volume: float,
    price_open: float,
    price_close: float,
) -> MT5DataCallResult:
    """Return profit for a trading operation."""
    data = mt5.order_calc_profit(action, symbol, volume, price_open, price_close)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def order_check(request: dict[str, Any]) -> MT5DataCallResult:
    """Validate a trade request without sending it."""
    data = mt5.order_check(request)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def order_send(request: dict[str, Any]) -> MT5DataCallResult:
    """Send a trade request."""
    data = mt5.order_send(request)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)
