from metatrader5_wrapper._core import market_book as mt5_market_book
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.models import OperationResult


def market_book_add(symbol: str) -> OperationResult[None]:
    """Subscribe to market depth change events for ``symbol``."""
    logger.debug("Subscribing to market depth for %r.", symbol)
    result = mt5_market_book.market_book_add(symbol)
    if not result.success:
        logger.warning(
            "Unable to subscribe to market depth for %r: [%s] %s",
            symbol,
            result.error.code,
            result.error.message,
        )
        return OperationResult[None](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to subscribe to market depth for {symbol!r}.",
        )

    logger.info("Subscribed to market depth for %r.", symbol)
    return OperationResult[None](
        success=True,
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Subscribed to market depth for {symbol!r}.",
    )


def market_book_get(symbol: str) -> OperationResult[list[object]]:
    """Return market depth entries for ``symbol``."""
    logger.debug("Fetching market depth for %r.", symbol)
    result = mt5_market_book.market_book_get(symbol)
    if not result.success:
        logger.warning(
            "Unable to fetch market depth for %r: [%s] %s",
            symbol,
            result.error.code,
            result.error.message,
        )
        return OperationResult[list[object]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to fetch market depth for {symbol!r}.",
        )

    logger.info("Market depth for %r fetched successfully.", symbol)
    return OperationResult[list[object]](
        success=True,
        data=list(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Market depth for {symbol!r} fetched successfully.",
    )


def market_book_release(symbol: str) -> OperationResult[None]:
    """Cancel market depth subscription for ``symbol``."""
    logger.debug("Releasing market depth subscription for %r.", symbol)
    result = mt5_market_book.market_book_release(symbol)
    if not result.success:
        logger.warning(
            "Unable to release market depth for %r: [%s] %s",
            symbol,
            result.error.code,
            result.error.message,
        )
        return OperationResult[None](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to release market depth for {symbol!r}.",
        )

    logger.info("Released market depth subscription for %r.", symbol)
    return OperationResult[None](
        success=True,
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Released market depth subscription for {symbol!r}.",
    )
