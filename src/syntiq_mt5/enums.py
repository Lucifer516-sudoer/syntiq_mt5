"""Typed IntEnum classes for all MT5 enum-valued fields.

These enums are the single source of truth for valid MT5 enum values within
the SDK.  They are backed by the integer constants in ``syntiq_mt5.constants``
so the numeric values are always in sync with the live MT5 library.

Why enums instead of raw integers
----------------------------------
MT5 returns plain integers for all enum-typed fields.  Without typed enums,
a field like ``position.type == 0`` is opaque — the reader must know that
``0`` means BUY.  With ``IntEnum``, the same check becomes
``position.type == PositionType.BUY``, which is self-documenting and
statically verifiable.

Backward compatibility
-----------------------
All enums inherit from ``int`` (via ``IntEnum``), so existing code that
passes raw integers to model constructors continues to work — Pydantic v2
coerces the integer to the matching enum member automatically.  An
unrecognised integer raises ``pydantic.ValidationError`` at parse time,
not silently at runtime.

Usage::

    from syntiq_mt5.enums import PositionType, OrderType, DealType

    # Explicit enum usage (preferred)
    if position.type == PositionType.BUY:
        ...

    # Raw int still accepted by Pydantic (backward compatible)
    Position(type=0, ...)  # coerced to PositionType.BUY
"""

from enum import IntEnum

from syntiq_mt5 import constants

__all__ = [
    "PositionType",
    "PositionReason",
    "OrderType",
    "OrderState",
    "OrderFilling",
    "OrderTime",
    "OrderReason",
    "DealType",
    "DealEntry",
    "DealReason",
    "BookType",
    "TradeAction",
]


# ── Positions ─────────────────────────────────────────────────────────────────

class PositionType(IntEnum):
    """Direction of an open position."""

    BUY = constants.POSITION_TYPE_BUY    # 0 – long position
    SELL = constants.POSITION_TYPE_SELL  # 1 – short position


class PositionReason(IntEnum):
    """Origin of an open position — how it was opened."""

    CLIENT = constants.POSITION_REASON_CLIENT  # 0 – desktop terminal
    MOBILE = constants.POSITION_REASON_MOBILE  # 1 – mobile app
    WEB = constants.POSITION_REASON_WEB        # 2 – web terminal
    EXPERT = constants.POSITION_REASON_EXPERT  # 3 – Expert Advisor


# ── Orders ────────────────────────────────────────────────────────────────────

class OrderType(IntEnum):
    """Type of a pending or market order."""

    BUY = constants.ORDER_TYPE_BUY                          # 0 – market buy
    SELL = constants.ORDER_TYPE_SELL                        # 1 – market sell
    BUY_LIMIT = constants.ORDER_TYPE_BUY_LIMIT              # 2 – buy limit
    SELL_LIMIT = constants.ORDER_TYPE_SELL_LIMIT            # 3 – sell limit
    BUY_STOP = constants.ORDER_TYPE_BUY_STOP                # 4 – buy stop
    SELL_STOP = constants.ORDER_TYPE_SELL_STOP              # 5 – sell stop
    BUY_STOP_LIMIT = constants.ORDER_TYPE_BUY_STOP_LIMIT    # 6 – buy stop-limit
    SELL_STOP_LIMIT = constants.ORDER_TYPE_SELL_STOP_LIMIT  # 7 – sell stop-limit
    CLOSE_BY = constants.ORDER_TYPE_CLOSE_BY                # 8 – close by opposite


class OrderState(IntEnum):
    """Lifecycle state of an order from placement to completion."""

    STARTED = constants.ORDER_STATE_STARTED                  # 0 – checked, not yet placed
    PLACED = constants.ORDER_STATE_PLACED                    # 1 – accepted by broker
    CANCELED = constants.ORDER_STATE_CANCELED                # 2 – cancelled by client
    PARTIAL = constants.ORDER_STATE_PARTIAL                  # 3 – partially executed
    FILLED = constants.ORDER_STATE_FILLED                    # 4 – fully executed
    REJECTED = constants.ORDER_STATE_REJECTED                # 5 – rejected by broker
    EXPIRED = constants.ORDER_STATE_EXPIRED                  # 6 – expired
    REQUEST_ADD = constants.ORDER_STATE_REQUEST_ADD          # 7 – being registered
    REQUEST_MODIFY = constants.ORDER_STATE_REQUEST_MODIFY    # 8 – being modified
    REQUEST_CANCEL = constants.ORDER_STATE_REQUEST_CANCEL    # 9 – being cancelled


class OrderFilling(IntEnum):
    """Fill policy controlling how an order is executed against available liquidity."""

    FOK = constants.ORDER_FILLING_FOK        # 0 – fill or kill: execute fully or cancel
    IOC = constants.ORDER_FILLING_IOC        # 1 – immediate or cancel: fill what's available
    RETURN = constants.ORDER_FILLING_RETURN  # 2 – return remainder as a new order
    BOC = constants.ORDER_FILLING_BOC        # 3 – book or cancel: passive fill only


class OrderTime(IntEnum):
    """Expiry policy controlling how long an order remains active."""

    GTC = constants.ORDER_TIME_GTC                      # 0 – good till cancelled
    DAY = constants.ORDER_TIME_DAY                      # 1 – good till end of trading day
    SPECIFIED = constants.ORDER_TIME_SPECIFIED          # 2 – good till specified datetime
    SPECIFIED_DAY = constants.ORDER_TIME_SPECIFIED_DAY  # 3 – good till specified day


class OrderReason(IntEnum):
    """Origin of an order — what triggered its placement."""

    CLIENT = constants.ORDER_REASON_CLIENT  # 0 – placed from desktop terminal
    MOBILE = constants.ORDER_REASON_MOBILE  # 1 – placed from mobile app
    WEB = constants.ORDER_REASON_WEB        # 2 – placed from web terminal
    EXPERT = constants.ORDER_REASON_EXPERT  # 3 – placed by Expert Advisor
    SL = constants.ORDER_REASON_SL          # 4 – triggered by stop loss
    TP = constants.ORDER_REASON_TP          # 5 – triggered by take profit
    SO = constants.ORDER_REASON_SO          # 6 – triggered by stop out


# ── Deals ─────────────────────────────────────────────────────────────────────

class DealType(IntEnum):
    """Type of a deal (completed transaction).

    Most deals are BUY or SELL.  The remaining types represent non-trade
    account operations such as balance adjustments, commissions, and swaps.
    """

    BUY = constants.DEAL_TYPE_BUY                                        # 0
    SELL = constants.DEAL_TYPE_SELL                                      # 1
    BALANCE = constants.DEAL_TYPE_BALANCE                                # 2
    CREDIT = constants.DEAL_TYPE_CREDIT                                  # 3
    CHARGE = constants.DEAL_TYPE_CHARGE                                  # 4
    CORRECTION = constants.DEAL_TYPE_CORRECTION                          # 5
    BONUS = constants.DEAL_TYPE_BONUS                                    # 6
    COMMISSION = constants.DEAL_TYPE_COMMISSION                          # 7
    COMMISSION_DAILY = constants.DEAL_TYPE_COMMISSION_DAILY              # 8
    COMMISSION_MONTHLY = constants.DEAL_TYPE_COMMISSION_MONTHLY          # 9
    COMMISSION_AGENT_DAILY = constants.DEAL_TYPE_COMMISSION_AGENT_DAILY  # 10
    COMMISSION_AGENT_MONTHLY = constants.DEAL_TYPE_COMMISSION_AGENT_MONTHLY  # 11
    INTEREST = constants.DEAL_TYPE_INTEREST                              # 12
    BUY_CANCELED = constants.DEAL_TYPE_BUY_CANCELED                     # 13
    SELL_CANCELED = constants.DEAL_TYPE_SELL_CANCELED                    # 14
    DIVIDEND = constants.DEAL_DIVIDEND                                   # 15
    DIVIDEND_FRANKED = constants.DEAL_DIVIDEND_FRANKED                   # 16
    TAX = constants.DEAL_TAX                                             # 17


class DealEntry(IntEnum):
    """How a deal relates to the position it affects."""

    IN = constants.DEAL_ENTRY_IN          # 0 – opens a new position
    OUT = constants.DEAL_ENTRY_OUT        # 1 – closes an existing position
    INOUT = constants.DEAL_ENTRY_INOUT    # 2 – reverses position direction
    OUT_BY = constants.DEAL_ENTRY_OUT_BY  # 3 – closed by an opposite position


class DealReason(IntEnum):
    """Origin of a deal — what caused the transaction."""

    CLIENT = constants.DEAL_REASON_CLIENT      # 0 – desktop terminal
    MOBILE = constants.DEAL_REASON_MOBILE      # 1 – mobile app
    WEB = constants.DEAL_REASON_WEB            # 2 – web terminal
    EXPERT = constants.DEAL_REASON_EXPERT      # 3 – Expert Advisor
    SL = constants.DEAL_REASON_SL              # 4 – stop loss
    TP = constants.DEAL_REASON_TP              # 5 – take profit
    SO = constants.DEAL_REASON_SO              # 6 – stop out
    ROLLOVER = constants.DEAL_REASON_ROLLOVER  # 7 – overnight rollover
    VMARGIN = constants.DEAL_REASON_VMARGIN    # 8 – variation margin
    SPLIT = constants.DEAL_REASON_SPLIT        # 9 – corporate action split


# ── Market Book ───────────────────────────────────────────────────────────────

class BookType(IntEnum):
    """Type of a market depth (DOM) entry."""

    SELL = constants.BOOK_TYPE_SELL                # 1 – sell limit order
    BUY = constants.BOOK_TYPE_BUY                  # 2 – buy limit order
    SELL_MARKET = constants.BOOK_TYPE_SELL_MARKET  # 3 – sell market order
    BUY_MARKET = constants.BOOK_TYPE_BUY_MARKET    # 4 – buy market order


# ── Trade Actions ─────────────────────────────────────────────────────────────

class TradeAction(IntEnum):
    """Action type for a trade request sent via ``order_send``."""

    DEAL = constants.TRADE_ACTION_DEAL          # 1 – execute a market order immediately
    PENDING = constants.TRADE_ACTION_PENDING    # 5 – place a pending order
    SLTP = constants.TRADE_ACTION_SLTP          # 6 – modify SL/TP of an open position
    MODIFY = constants.TRADE_ACTION_MODIFY      # 7 – modify a pending order's parameters
    REMOVE = constants.TRADE_ACTION_REMOVE      # 8 – delete a pending order
    CLOSE_BY = constants.TRADE_ACTION_CLOSE_BY  # 10 – close a position by an opposite one
