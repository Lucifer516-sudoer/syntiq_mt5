from metatrader5_wrapper._convert import (
    model_from_namedtuple,
    models_from_namedtuples,
)
from metatrader5_wrapper._core import symbols as mt5_symbols
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.models import OperationResult
from metatrader5_wrapper.symbols.models import SymbolInfo, Tick


def symbols_total() -> OperationResult[int]:
    """Count the total number of tradeable symbols in the terminal.

    Returns:
        OperationResult[int] with the symbol count on success, or error details
        on failure.

    Example::

        result = symbols_total()
        if result.success:
            print(f"Terminal has {result.data} symbols")
    """
    logger.debug("Fetching MetaTrader 5 symbols total.")
    result = mt5_symbols.symbols_total()
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 symbols total: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[int](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 symbols total.",
        )

    logger.info("MetaTrader 5 symbols total fetched successfully.")
    return OperationResult[int](
        success=True,
        data=int(result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 symbols total fetched successfully.",
    )


def symbols_get(group: str | None = None) -> OperationResult[list[SymbolInfo]]:
    """Fetch available trading symbols, optionally filtered by group.

    Args:
        group: Optional MT5 group filter string (e.g., "*USD*", "CRYPTO*").
            If ``None``, returns all symbols.

    Returns:
        OperationResult[list[SymbolInfo]] with a list of typed symbol objects on
        success, or error details on failure.

    Example::

        # Get all symbols
        result = symbols_get()

        # Get only USD pairs
        result = symbols_get(group="*USD*")
        if result.success and result.data:
            for sym in result.data:
                print(sym.name, sym.spread)
    """
    logger.debug("Fetching MetaTrader 5 symbols with group=%r.", group)
    result = mt5_symbols.symbols_get(group=group)
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 symbols: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[list[SymbolInfo]](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 symbols.",
        )

    logger.info("MetaTrader 5 symbols fetched successfully.")
    return OperationResult[list[SymbolInfo]](
        success=True,
        data=models_from_namedtuples(SymbolInfo, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 symbols fetched successfully.",
    )


def symbol_info(symbol: str) -> OperationResult[SymbolInfo]:
    """Fetch detailed information for a single trading symbol.

    Args:
        symbol: Symbol name (e.g., "EURUSD", "AAPL").

    Returns:
        OperationResult[SymbolInfo] with typed symbol metadata on success,
        including name, spread, point value, volume limits, and other
        instrument details.

    Example::

        result = symbol_info("EURUSD")
        if result.success and result.data:
            sym = result.data
            print(f"Spread: {sym.spread}")
            print(f"Digits: {sym.digits}")
            print(f"Point: {sym.point}")
    """
    logger.debug("Fetching MetaTrader 5 symbol info for %r.", symbol)
    result = mt5_symbols.symbol_info(symbol)
    if not result.success:
        logger.warning(
            "Unable to fetch symbol info for %r: [%s] %s",
            symbol,
            result.error.code,
            result.error.message,
        )
        return OperationResult[SymbolInfo](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to fetch symbol info for {symbol!r}.",
        )

    logger.info("Symbol info for %r fetched successfully.", symbol)
    return OperationResult[SymbolInfo](
        success=True,
        data=model_from_namedtuple(SymbolInfo, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Symbol info for {symbol!r} fetched successfully.",
    )


def symbol_info_tick(symbol: str) -> OperationResult[Tick]:
    """Fetch the latest tick data for a symbol.

    Args:
        symbol: Symbol name (e.g., "EURUSD").

    Returns:
        OperationResult[Tick] with bid, ask, time, and volume data on success.

    Example::

        result = symbol_info_tick("EURUSD")
        if result.success and result.data:
            tick = result.data
            print(f"Bid: {tick.bid}")
            print(f"Ask: {tick.ask}")
            print(f"Spread: {tick.ask - tick.bid}")
    """
    logger.debug("Fetching latest MetaTrader 5 tick for %r.", symbol)
    result = mt5_symbols.symbol_info_tick(symbol)
    if not result.success:
        logger.warning(
            "Unable to fetch latest tick for %r: [%s] %s",
            symbol,
            result.error.code,
            result.error.message,
        )
        return OperationResult[Tick](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to fetch latest tick for {symbol!r}.",
        )

    logger.info("Latest tick for %r fetched successfully.", symbol)
    return OperationResult[Tick](
        success=True,
        data=model_from_namedtuple(Tick, result.data),
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"Latest tick for {symbol!r} fetched successfully.",
    )


def symbol_select(symbol: str, enable: bool = True) -> OperationResult[None]:
    """Add or remove a symbol from the terminal's MarketWatch.

    Args:
        symbol: Symbol name to select or deselect.
        enable: If ``True`` (default), adds the symbol to MarketWatch.
            If ``False``, removes it.

    Returns:
        OperationResult[None] indicating success or failure of the operation.

    Example::

        # Add EURUSD to MarketWatch
        result = symbol_select("EURUSD", enable=True)

        # Remove from MarketWatch
        result = symbol_select("EURUSD", enable=False)
    """
    logger.debug("Updating MarketWatch visibility for %r to %s.", symbol, enable)
    result = mt5_symbols.symbol_select(symbol, enable)
    if not result.success:
        logger.warning(
            "Unable to update MarketWatch visibility for %r: [%s] %s",
            symbol,
            result.error.code,
            result.error.message,
        )
        return OperationResult[None](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message=f"Unable to update MarketWatch visibility for {symbol!r}.",
        )

    logger.info("MarketWatch visibility updated for %r.", symbol)
    return OperationResult[None](
        success=True,
        error_code=result.error.code,
        error_message=result.error.message,
        message=f"MarketWatch visibility updated for {symbol!r}.",
    )
