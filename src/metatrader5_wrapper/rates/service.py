from datetime import datetime

from metatrader5_wrapper._core import rates as mt5_rates
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.models import OperationResult


def copy_rates_from(
    symbol: str,
    timeframe: int,
    date_from: datetime,
    count: int,
) -> OperationResult[list[object]]:
    """Return bars starting from ``date_from``."""
    logger.debug(
        "Copying rates for %r from %s with timeframe=%r count=%r.",
        symbol,
        date_from,
        timeframe,
        count,
    )
    result = mt5_rates.copy_rates_from(symbol, timeframe, date_from, count)
    if not result.success:
        return OperationResult[list[object]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to copy rates for {symbol!r} from {date_from}.",
        )
    return OperationResult[list[object]](
        success=True,
        data=list(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Rates for {symbol!r} copied successfully.",
    )


def copy_rates_from_pos(
    symbol: str,
    timeframe: int,
    start_pos: int,
    count: int,
) -> OperationResult[list[object]]:
    """Return bars starting from ``start_pos``."""
    result = mt5_rates.copy_rates_from_pos(symbol, timeframe, start_pos, count)
    if not result.success:
        return OperationResult[list[object]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to copy rates for {symbol!r} from position {start_pos}.",
        )
    return OperationResult[list[object]](
        success=True,
        data=list(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Rates for {symbol!r} copied successfully.",
    )


def copy_rates_range(
    symbol: str,
    timeframe: int,
    date_from: datetime,
    date_to: datetime,
) -> OperationResult[list[object]]:
    """Return bars within the given date range."""
    result = mt5_rates.copy_rates_range(symbol, timeframe, date_from, date_to)
    if not result.success:
        return OperationResult[list[object]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to copy rates for {symbol!r} in the given range.",
        )
    return OperationResult[list[object]](
        success=True,
        data=list(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Rates for {symbol!r} copied successfully.",
    )


def copy_ticks_from(
    symbol: str,
    date_from: datetime,
    count: int,
    flags: int,
) -> OperationResult[list[object]]:
    """Return ticks starting from ``date_from``."""
    result = mt5_rates.copy_ticks_from(symbol, date_from, count, flags)
    if not result.success:
        return OperationResult[list[object]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to copy ticks for {symbol!r} from {date_from}.",
        )
    return OperationResult[list[object]](
        success=True,
        data=list(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Ticks for {symbol!r} copied successfully.",
    )


def copy_ticks_range(
    symbol: str,
    date_from: datetime,
    date_to: datetime,
    flags: int,
) -> OperationResult[list[object]]:
    """Return ticks within the given date range."""
    result = mt5_rates.copy_ticks_range(symbol, date_from, date_to, flags)
    if not result.success:
        return OperationResult[list[object]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to copy ticks for {symbol!r} in the given range.",
        )
    return OperationResult[list[object]](
        success=True,
        data=list(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Ticks for {symbol!r} copied successfully.",
    )
