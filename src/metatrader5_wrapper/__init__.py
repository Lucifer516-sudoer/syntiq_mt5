from typing import Any

import MetaTrader5 as _mt5  # type: ignore[import-untyped]

from metatrader5_wrapper.account import AccountInfo, account_info
from metatrader5_wrapper.client import MetaTrader5Client
from metatrader5_wrapper.connection import (
    ConnectionResult,
    ConnectionStage,
    LoginCredential,
    initialize,
    login,
)
from metatrader5_wrapper.models import OperationResult
from metatrader5_wrapper.positions import Position, positions_get, positions_total
from metatrader5_wrapper.symbols import (
    SymbolInfo,
    Tick,
    symbol_info,
    symbol_info_tick,
    symbol_select,
    symbols_get,
    symbols_total,
)
from metatrader5_wrapper.terminal import (
    TerminalInfo,
    TerminalVersion,
    shutdown,
    terminal_info,
    version,
)

__all__ = [
    "AccountInfo",
    "ConnectionResult",
    "ConnectionStage",
    "LoginCredential",
    "MetaTrader5Client",
    "OperationResult",
    "Position",
    "SymbolInfo",
    "TerminalInfo",
    "TerminalVersion",
    "Tick",
    "account_info",
    "initialize",
    "login",
    "positions_get",
    "positions_total",
    "shutdown",
    "symbol_info",
    "symbol_info_tick",
    "symbol_select",
    "symbols_get",
    "symbols_total",
    "terminal_info",
    "version",
]


def __getattr__(name: str) -> Any:
    """Expose official MT5 constants while typed wrappers are built out."""
    if name.isupper():
        return getattr(_mt5, name)

    raise AttributeError(f"module 'metatrader5_wrapper' has no attribute {name!r}")
