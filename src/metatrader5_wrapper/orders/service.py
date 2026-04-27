from typing import Any

from metatrader5_wrapper._convert import models_from_namedtuples
from metatrader5_wrapper._core import orders as mt5_orders
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.models import MT5NamedTupleModel, OperationResult


class TradeCheckResult(MT5NamedTupleModel):
    """Typed result returned by ``MetaTrader5.order_check()``."""


class TradeSendResult(MT5NamedTupleModel):
    """Typed result returned by ``MetaTrader5.order_send()``."""


class TradeOrder(MT5NamedTupleModel):
    """Typed active order payload returned by ``MetaTrader5.orders_get()``."""


def orders_total() -> OperationResult[int]:
    """Return the number of active orders."""
    result = mt5_orders.orders_total()
    if not result.success:
        return OperationResult[int](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 orders total.",
        )
    return OperationResult[int](
        success=True,
        data=int(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 orders total fetched successfully.",
    )


def orders_get(
    *,
    symbol: str | None = None,
    group: str | None = None,
    ticket: int | None = None,
) -> OperationResult[list[TradeOrder]]:
    """Return active orders using the supported MT5 filters."""
    logger.debug(
        "Fetching MetaTrader 5 orders with symbol=%r group=%r ticket=%r.",
        symbol,
        group,
        ticket,
    )
    result = mt5_orders.orders_get(symbol=symbol, group=group, ticket=ticket)
    if not result.success:
        return OperationResult[list[TradeOrder]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 orders.",
        )
    return OperationResult[list[TradeOrder]](
        success=True,
        data=models_from_namedtuples(TradeOrder, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 orders fetched successfully.",
    )


def order_calc_margin(
    action: int,
    symbol: str,
    volume: float,
    price: float,
) -> OperationResult[float]:
    """Return margin required for a trading operation."""
    result = mt5_orders.order_calc_margin(action, symbol, volume, price)
    if not result.success:
        return OperationResult[float](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to calculate MetaTrader 5 margin.",
        )
    return OperationResult[float](
        success=True,
        data=float(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 margin calculated successfully.",
    )


def order_calc_profit(
    action: int,
    symbol: str,
    volume: float,
    price_open: float,
    price_close: float,
) -> OperationResult[float]:
    """Return profit for a trading operation."""
    result = mt5_orders.order_calc_profit(
        action,
        symbol,
        volume,
        price_open,
        price_close,
    )
    if not result.success:
        return OperationResult[float](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to calculate MetaTrader 5 profit.",
        )
    return OperationResult[float](
        success=True,
        data=float(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 profit calculated successfully.",
    )


def order_check(request: dict[str, Any]) -> OperationResult[TradeCheckResult]:
    """Validate a trade request without sending it."""
    result = mt5_orders.order_check(request)
    if not result.success:
        return OperationResult[TradeCheckResult](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to validate MetaTrader 5 order request.",
        )
    return OperationResult[TradeCheckResult](
        success=True,
        data=TradeCheckResult.model_validate(result.data._asdict()),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 order request validated successfully.",
    )


def order_send(request: dict[str, Any]) -> OperationResult[TradeSendResult]:
    """Send a trade request."""
    result = mt5_orders.order_send(request)
    if not result.success:
        return OperationResult[TradeSendResult](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to send MetaTrader 5 order request.",
        )
    return OperationResult[TradeSendResult](
        success=True,
        data=TradeSendResult.model_validate(result.data._asdict()),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 order request sent successfully.",
    )
