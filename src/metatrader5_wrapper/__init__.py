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
from metatrader5_wrapper.history import (
    history_deals_get,
    history_deals_total,
    history_orders_get,
    history_orders_total,
)
from metatrader5_wrapper.market_book import (
    market_book_add,
    market_book_get,
    market_book_release,
)
from metatrader5_wrapper.models import OperationResult
from metatrader5_wrapper.orders import (
    TradeCheckResult,
    TradeOrder,
    TradeSendResult,
    order_calc_margin,
    order_calc_profit,
    order_check,
    order_send,
    orders_get,
    orders_total,
)
from metatrader5_wrapper.positions import Position, positions_get, positions_total
from metatrader5_wrapper.rates import (
    copy_rates_from,
    copy_rates_from_pos,
    copy_rates_range,
    copy_ticks_from,
    copy_ticks_range,
)
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
    "TradeCheckResult",
    "TradeOrder",
    "TradeSendResult",
    "account_info",
    "copy_rates_from",
    "copy_rates_from_pos",
    "copy_rates_range",
    "copy_ticks_from",
    "copy_ticks_range",
    "history_deals_get",
    "history_deals_total",
    "history_orders_get",
    "history_orders_total",
    "initialize",
    "login",
    "market_book_add",
    "market_book_get",
    "market_book_release",
    "order_calc_margin",
    "order_calc_profit",
    "order_check",
    "order_send",
    "orders_get",
    "orders_total",
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
