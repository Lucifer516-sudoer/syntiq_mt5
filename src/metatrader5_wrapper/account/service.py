from metatrader5_wrapper._convert import model_from_namedtuple
from metatrader5_wrapper._core import account as mt5_account
from metatrader5_wrapper._logging import logger
from metatrader5_wrapper.account.models import AccountInfo
from metatrader5_wrapper.models import OperationResult


def account_info() -> OperationResult[AccountInfo]:
    """Fetch current account details as a typed model.

    Requires an active, logged-in MT5 session. Reads account balance, equity,
    margin, leverage, trading permissions, and account metadata from the
    terminal.

    Returns:
        OperationResult[AccountInfo] with success status, typed AccountInfo data
        on success, raw MT5 error code and message on failure, and a status message.

    Example::

        result = account_info()
        if result.success and result.data:
            print(f"Balance: {result.data.balance}")
            print(f"Equity: {result.data.equity}")
            print(f"Margin: {result.data.margin}")
        else:
            print(result.error_code, result.error_message)
    """
    logger.debug("Fetching MetaTrader 5 account info.")
    result = mt5_account.account_info()
    if not result.success:
        logger.warning(
            "Unable to fetch MetaTrader 5 account info: [%s] %s",
            result.error.code,
            result.error.message,
        )
        return OperationResult[AccountInfo](
            success=False,
            error_code=result.error.code,
            error_message=result.error.message,
            message="Unable to fetch MetaTrader 5 account info.",
        )

    account = model_from_namedtuple(AccountInfo, result.data)
    logger.info("MetaTrader 5 account info fetched successfully.")
    return OperationResult[AccountInfo](
        success=True,
        data=account,
        error_code=result.error.code,
        error_message=result.error.message,
        message="MetaTrader 5 account info fetched successfully.",
    )
