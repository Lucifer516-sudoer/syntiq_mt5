import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5DataCallResult, capture_last_error


def positions_total() -> MT5DataCallResult:
    """Return the number of open positions."""
    data = mt5.positions_total()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def positions_get(
    *,
    symbol: str | None = None,
    group: str | None = None,
    ticket: int | None = None,
) -> MT5DataCallResult:
    """Return open positions using MT5's supported filters."""
    if symbol is not None:
        data = mt5.positions_get(symbol=symbol)
    elif group is not None:
        data = mt5.positions_get(group=group)
    elif ticket is not None:
        data = mt5.positions_get(ticket=ticket)
    else:
        data = mt5.positions_get()

    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)
