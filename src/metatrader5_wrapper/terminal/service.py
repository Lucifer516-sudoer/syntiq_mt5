from typing import cast

from metatrader5_wrapper._convert import model_from_namedtuple
from metatrader5_wrapper._core import connection as mt5_connection
from metatrader5_wrapper._core import terminal as mt5_terminal
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.models import OperationResult
from metatrader5_wrapper.terminal.models import TerminalInfo, TerminalVersion


def terminal_info() -> OperationResult[TerminalInfo]:
    """Fetch MetaTrader 5 terminal information and status.

    Returns:
        OperationResult[TerminalInfo] with terminal metadata including connection
        status, trading permissions, paths, language, and company name.

    Example::

        result = terminal_info()
        if result.success and result.data:
            print(f"Terminal: {result.data.name}")
            print(f"Build: {result.data.build}")
            print(f"Connected: {result.data.connected}")
    """
    logger.debug("Fetching MetaTrader 5 terminal info.")
    result = mt5_terminal.terminal_info()
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 terminal info: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[TerminalInfo](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 terminal info.",
        )

    terminal = model_from_namedtuple(TerminalInfo, result.data)
    logger.info("MetaTrader 5 terminal info fetched successfully.")
    return OperationResult[TerminalInfo](
        success=True,
        data=terminal,
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 terminal info fetched successfully.",
    )


def version() -> OperationResult[TerminalVersion]:
    """Fetch MetaTrader 5 terminal version and build information.

    Returns:
        OperationResult[TerminalVersion] with version number, build number, and
        release date.

    Example::

        result = version()
        if result.success and result.data:
            print(f"Version: {result.data.version}.{result.data.build}")
            print(f"Released: {result.data.release_date}")
    """
    logger.debug("Fetching MetaTrader 5 terminal version.")
    result = mt5_terminal.version()
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 terminal version: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[TerminalVersion](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 terminal version.",
        )

    version_number, build, release_date = cast(tuple[int, int, str], result.data)
    logger.info("MetaTrader 5 terminal version fetched successfully.")
    return OperationResult[TerminalVersion](
        success=True,
        data=TerminalVersion(
            version=version_number,
            build=build,
            release_date=release_date,
        ),
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 terminal version fetched successfully.",
    )


def shutdown() -> OperationResult[None]:
    """Cleanly disconnect from the MetaTrader 5 terminal.

    Closes the active MT5 session and releases resources. Should be called when
    your application is finished trading or connecting to the terminal.

    Returns:
        OperationResult[None] indicating the shutdown completed successfully.

    Example::

        result = shutdown()
        if result.success:
            print("Terminal closed")
    """
    logger.debug("Shutting down MetaTrader 5 terminal.")
    mt5_connection.shutdown_terminal()
    logger.info("MetaTrader 5 terminal shutdown completed.")
    return OperationResult[None](
        success=True,
        message="MetaTrader 5 terminal shutdown completed.",
    )
