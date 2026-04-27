from datetime import datetime

import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5DataCallResult, capture_last_error


def history_orders_total(date_from: datetime, date_to: datetime) -> MT5DataCallResult:
    """Return the number of historical orders in a date range."""
    data = mt5.history_orders_total(date_from, date_to)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def history_orders_get(
    date_from: datetime,
    date_to: datetime,
    *,
    group: str | None = None,
    ticket: int | None = None,
    position: int | None = None,
) -> MT5DataCallResult:
    """Return historical orders filtered by group, ticket, or position."""
    if group is not None:
        data = mt5.history_orders_get(date_from, date_to, group=group)
    elif ticket is not None:
        data = mt5.history_orders_get(ticket=ticket)
    elif position is not None:
        data = mt5.history_orders_get(position=position)
    else:
        data = mt5.history_orders_get(date_from, date_to)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def history_deals_total(date_from: datetime, date_to: datetime) -> MT5DataCallResult:
    """Return the number of historical deals in a date range."""
    data = mt5.history_deals_total(date_from, date_to)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def history_deals_get(
    date_from: datetime,
    date_to: datetime,
    *,
    group: str | None = None,
    ticket: int | None = None,
    position: int | None = None,
) -> MT5DataCallResult:
    """Return historical deals filtered by group, ticket, or position."""
    if group is not None:
        data = mt5.history_deals_get(date_from, date_to, group=group)
    elif ticket is not None:
        data = mt5.history_deals_get(ticket=ticket)
    elif position is not None:
        data = mt5.history_deals_get(position=position)
    else:
        data = mt5.history_deals_get(date_from, date_to)
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)
