import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5DataCallResult, capture_last_error


def terminal_info() -> MT5DataCallResult:
    """Return terminal info and immediately bind ``last_error()``."""
    data = mt5.terminal_info()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)


def version() -> MT5DataCallResult:
    """Return terminal version and immediately bind ``last_error()``."""
    data = mt5.version()
    error = capture_last_error()
    return MT5DataCallResult(data=data, error=error)
