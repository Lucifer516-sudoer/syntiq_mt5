import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5DataCallResult, capture_last_error


def account_info() -> MT5DataCallResult:
    """Return current account info and immediately bind ``last_error()``."""
    data = mt5.account_info()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)
