from datetime import datetime

from metatrader5_wrapper._convert import models_from_namedtuples
from metatrader5_wrapper._core import history as mt5_history
from metatrader5_wrapper.models import MT5NamedTupleModel, OperationResult


class HistoryOrder(MT5NamedTupleModel):
    """Typed historical order payload returned by ``MetaTrader5.history_orders_get()``."""


class HistoryDeal(MT5NamedTupleModel):
    """Typed historical deal payload returned by ``MetaTrader5.history_deals_get()``."""


def history_orders_total(
    date_from: datetime,
    date_to: datetime,
) -> OperationResult[int]:
    """Return the number of historical orders in a date range."""
    result = mt5_history.history_orders_total(date_from, date_to)
    if not result.success:
        return OperationResult[int](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 history orders total.",
        )
    return OperationResult[int](
        success=True,
        data=int(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 history orders total fetched successfully.",
    )


def history_orders_get(
    date_from: datetime,
    date_to: datetime,
    *,
    group: str | None = None,
    ticket: int | None = None,
    position: int | None = None,
) -> OperationResult[list[HistoryOrder]]:
    """Return historical orders in the given range or by ticket/position."""
    result = mt5_history.history_orders_get(
        date_from,
        date_to,
        group=group,
        ticket=ticket,
        position=position,
    )
    if not result.success:
        return OperationResult[list[HistoryOrder]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 history orders.",
        )
    return OperationResult[list[HistoryOrder]](
        success=True,
        data=models_from_namedtuples(HistoryOrder, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 history orders fetched successfully.",
    )


def history_deals_total(
    date_from: datetime,
    date_to: datetime,
) -> OperationResult[int]:
    """Return the number of historical deals in a date range."""
    result = mt5_history.history_deals_total(date_from, date_to)
    if not result.success:
        return OperationResult[int](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 history deals total.",
        )
    return OperationResult[int](
        success=True,
        data=int(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 history deals total fetched successfully.",
    )


def history_deals_get(
    date_from: datetime,
    date_to: datetime,
    *,
    group: str | None = None,
    ticket: int | None = None,
    position: int | None = None,
) -> OperationResult[list[HistoryDeal]]:
    """Return historical deals in the given range or by ticket/position."""
    result = mt5_history.history_deals_get(
        date_from,
        date_to,
        group=group,
        ticket=ticket,
        position=position,
    )
    if not result.success:
        return OperationResult[list[HistoryDeal]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 history deals.",
        )
    return OperationResult[list[HistoryDeal]](
        success=True,
        data=models_from_namedtuples(HistoryDeal, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 history deals fetched successfully.",
    )
