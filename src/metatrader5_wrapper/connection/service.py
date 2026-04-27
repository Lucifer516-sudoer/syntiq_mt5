from metatrader5_wrapper._core import connection as mt5_connection
from metatrader5_wrapper._core.connection import MT5CallResult
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.connection.models import (
    ConnectionResult,
    ConnectionStage,
    LoginCredential,
)


def initialize(credentials: LoginCredential | None = None) -> ConnectionResult:
    """Initialize the MetaTrader 5 terminal and optionally log in.

    When called without credentials, initializes the terminal for use with an
    existing MT5 session or manual login later. When called with credentials,
    performs both initialization and account login as a single operation.

    The official MT5 module stores errors globally in ``last_error()``. This
    wrapper captures that error state immediately after each call and returns it
    as part of the typed ``ConnectionResult``, eliminating the need to check
    mutable global state.

    Args:
        credentials: Optional ``LoginCredential`` containing account number, password,
            server name, and connection timeout. If ``None``, the terminal initializes
            without automatic login.

    Returns:
        ConnectionResult with success status, stage (initialize or login), raw MT5
        error code and message, and a human-readable status message.

    Example:
        Initialize without credentials::

            result = initialize()
            if result.success:
                print("Terminal ready")

        Initialize with credentials::

            creds = LoginCredential(
                login=12345678,
                password=SecretStr("mypassword"),
                server="Broker-Demo"
            )
            result = initialize(creds)
            if result.failed:
                print(result.stage, result.error_code)
    """
    logger.debug("Initializing MetaTrader 5 terminal.")
    init_result = mt5_connection.initialize_terminal(
        terminal_path=credentials.terminal_path if credentials else None,
        timeout_ms=credentials.timeout_ms if credentials else 60_000,
        portable=credentials.portable if credentials else False,
    )
    if not init_result.success:
        logger.warning(
            "MetaTrader 5 terminal initialization failed: [%s] %s",
            init_result.error.code,
            init_result.error.message,
        )
        return _to_connection_result(
            init_result,
            stage=ConnectionStage.INITIALIZE,
            message="Unable to initialize the MetaTrader 5 terminal.",
        )

    if credentials is None:
        logger.info("MetaTrader 5 terminal initialized successfully.")
        return _to_connection_result(
            init_result,
            stage=ConnectionStage.INITIALIZE,
            message="MetaTrader 5 terminal initialized successfully.",
        )

    logger.debug("Logging in to MetaTrader 5 account %s.", credentials.login)
    login_result = mt5_connection.login_account(
        login=credentials.login,
        password=credentials.password.get_secret_value(),
        server=credentials.server,
        timeout_ms=credentials.timeout_ms,
    )
    if not login_result.success:
        logger.warning(
            "MetaTrader 5 account login failed for %s: [%s] %s",
            credentials.login,
            login_result.error.code,
            login_result.error.message,
        )
        return _to_connection_result(
            login_result,
            stage=ConnectionStage.LOGIN,
            message="Unable to log in to the MetaTrader 5 account.",
        )

    logger.info("MetaTrader 5 account %s connected successfully.", credentials.login)
    return _to_connection_result(
        login_result,
        stage=ConnectionStage.LOGIN,
        message="MetaTrader 5 account connected successfully.",
    )


def login(credentials: LoginCredential) -> ConnectionResult:
    """Log in to an MT5 account after the terminal has been initialized.

    Use this function when you want to defer login until after the terminal
    is already running, or when you need to switch between accounts in the
    same session.

    Args:
        credentials: LoginCredential containing account number, password, server,
            and connection timeout.

    Returns:
        ConnectionResult with success status, stage set to LOGIN, raw MT5 error
        code and message, and a descriptive status message.
    """
    logger.debug("Logging in to MetaTrader 5 account %s.", credentials.login)
    login_result = mt5_connection.login_account(
        login=credentials.login,
        password=credentials.password.get_secret_value(),
        server=credentials.server,
        timeout_ms=credentials.timeout_ms,
    )
    if not login_result.success:
        logger.warning(
            "MetaTrader 5 account login failed for %s: [%s] %s",
            credentials.login,
            login_result.error.code,
            login_result.error.message,
        )
        return _to_connection_result(
            login_result,
            stage=ConnectionStage.LOGIN,
            message="Unable to log in to the MetaTrader 5 account.",
        )

    logger.info("MetaTrader 5 account %s connected successfully.", credentials.login)
    return _to_connection_result(
        login_result,
        stage=ConnectionStage.LOGIN,
        message="MetaTrader 5 account connected successfully.",
    )


def _to_connection_result(
    result: MT5CallResult,
    *,
    stage: ConnectionStage,
    message: str,
) -> ConnectionResult:
    return ConnectionResult(
        success=result.success,
        error_code=result.error.code,
        error_message=result.error.message,
        stage=stage,
        message=message,
    )
