from dataclasses import dataclass
from pathlib import Path

import MetaTrader5 as mt5  # type: ignore[import-untyped]

from metatrader5_wrapper._core.results import MT5ErrorResult, capture_last_error


@dataclass(frozen=True, slots=True)
class MT5CallResult:
    """Raw MT5 call result with the immediately captured global error state."""

    success: bool
    error: MT5ErrorResult


def initialize_terminal(
    *,
    terminal_path: Path | None = None,
    timeout_ms: int = 60_000,
    portable: bool = False,
) -> MT5CallResult:
    """Initialize the MT5 terminal and immediately bind ``last_error()``."""
    if terminal_path is None:
        success = mt5.initialize(timeout=timeout_ms, portable=portable)
    else:
        success = mt5.initialize(
            str(terminal_path),
            timeout=timeout_ms,
            portable=portable,
        )

    error = capture_last_error()
    return MT5CallResult(success=success, error=error)


def login_account(
    *,
    login: int,
    password: str,
    server: str,
    timeout_ms: int,
) -> MT5CallResult:
    """Log in to an MT5 account and immediately bind ``last_error()``."""
    success = mt5.login(
        login,
        password=password,
        server=server,
        timeout=timeout_ms,
    )
    error = capture_last_error()
    return MT5CallResult(success=success, error=error)


def shutdown_terminal() -> None:
    """Disconnect from the MT5 terminal."""
    mt5.shutdown()
