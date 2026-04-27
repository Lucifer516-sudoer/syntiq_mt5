from metatrader5_wrapper._convert import models_from_namedtuples
from metatrader5_wrapper._core import positions as mt5_positions
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.models import OperationResult
from metatrader5_wrapper.positions.models import Position


def positions_total() -> OperationResult[int]:
    """Count the number of currently open positions.

    Returns:
        OperationResult[int] with the position count on success.

    Example::

        result = positions_total()
        if result.success:
            print(f"Open positions: {result.data}")
    """
    logger.debug("Fetching MetaTrader 5 positions total.")
    result = mt5_positions.positions_total()
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 positions total: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[int](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 positions total.",
        )

    logger.info("MetaTrader 5 positions total fetched successfully.")
    return OperationResult[int](
        success=True,
        data=int(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 positions total fetched successfully.",
    )


def positions_get(
    *,
    symbol: str | None = None,
    group: str | None = None,
    ticket: int | None = None,
) -> OperationResult[list[Position]]:
    """Fetch open positions, optionally filtered by symbol, group, or ticket.

    The filter is applied in priority order: symbol is checked first, then group,
    then ticket. Only one filter is used even if multiple are provided.

    Args:
        symbol: Optional symbol name to filter positions (e.g., "EURUSD").
        group: Optional group filter using MT5 wildcards (e.g., "*USD*").
        ticket: Optional position ticket number for exact lookup.

    Returns:
        OperationResult[list[Position]] with typed position objects on success,
        or error details on failure.

    Example::

        # Get all open positions
        result = positions_get()

        # Get positions for EURUSD only
        result = positions_get(symbol="EURUSD")
        if result.success and result.data:
            for pos in result.data:
                print(f"Ticket: {pos.ticket}, Volume: {pos.volume}")

        # Get a specific position by ticket
        result = positions_get(ticket=12345)
    """
    logger.debug(
        "Fetching MetaTrader 5 positions with symbol=%r group=%r ticket=%r.",
        symbol,
        group,
        ticket,
    )
    result = mt5_positions.positions_get(symbol=symbol, group=group, ticket=ticket)
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 positions: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[list[Position]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 positions.",
        )

    logger.info("MetaTrader 5 positions fetched successfully.")
    return OperationResult[list[Position]](
        success=True,
        data=models_from_namedtuples(Position, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 positions fetched successfully.",
    )
