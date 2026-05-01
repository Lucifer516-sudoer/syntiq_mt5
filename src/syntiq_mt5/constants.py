"""MT5 constants for trading operations, timeframes, and data retrieval."""

from syntiq_mt5._core.mt5_import import mt5

# ── Position Types ────────────────────────────────────────────────────────────
# POSITION_TYPE_BUY  (0) – long position
# POSITION_TYPE_SELL (1) – short position

# ── Position Reasons ──────────────────────────────────────────────────────────
# POSITION_REASON_CLIENT (0) – opened from desktop terminal
# POSITION_REASON_MOBILE (1) – opened from mobile app
# POSITION_REASON_WEB    (2) – opened from web terminal
# POSITION_REASON_EXPERT (3) – opened by an Expert Advisor

# ── Order Types ───────────────────────────────────────────────────────────────
# ORDER_TYPE_BUY            (0) – market buy order
# ORDER_TYPE_SELL           (1) – market sell order
# ORDER_TYPE_BUY_LIMIT      (2) – buy limit pending order
# ORDER_TYPE_SELL_LIMIT     (3) – sell limit pending order
# ORDER_TYPE_BUY_STOP       (4) – buy stop pending order
# ORDER_TYPE_SELL_STOP      (5) – sell stop pending order
# ORDER_TYPE_BUY_STOP_LIMIT (6) – buy stop-limit pending order
# ORDER_TYPE_SELL_STOP_LIMIT(7) – sell stop-limit pending order
# ORDER_TYPE_CLOSE_BY       (8) – close by opposite position

# ── Order States ──────────────────────────────────────────────────────────────
# ORDER_STATE_STARTED        (0) – order checked but not placed
# ORDER_STATE_PLACED         (1) – order accepted by broker
# ORDER_STATE_CANCELED       (2) – order cancelled by client
# ORDER_STATE_PARTIAL        (3) – order partially executed
# ORDER_STATE_FILLED         (4) – order fully executed
# ORDER_STATE_REJECTED       (5) – order rejected
# ORDER_STATE_EXPIRED        (6) – order expired
# ORDER_STATE_REQUEST_ADD    (7) – order being registered
# ORDER_STATE_REQUEST_MODIFY (8) – order being modified
# ORDER_STATE_REQUEST_CANCEL (9) – order being cancelled

# ── Order Filling ─────────────────────────────────────────────────────────────
# ORDER_FILLING_FOK    (0) – fill or kill
# ORDER_FILLING_IOC    (1) – immediate or cancel
# ORDER_FILLING_RETURN (2) – return remainder
# ORDER_FILLING_BOC    (3) – book or cancel (passive)

# ── Order Time ────────────────────────────────────────────────────────────────
# ORDER_TIME_GTC          (0) – good till cancelled
# ORDER_TIME_DAY          (1) – good till end of day
# ORDER_TIME_SPECIFIED    (2) – good till specified date
# ORDER_TIME_SPECIFIED_DAY(3) – good till specified day

# ── Order Reasons ─────────────────────────────────────────────────────────────
# ORDER_REASON_CLIENT (0) – placed from desktop terminal
# ORDER_REASON_MOBILE (1) – placed from mobile app
# ORDER_REASON_WEB    (2) – placed from web terminal
# ORDER_REASON_EXPERT (3) – placed by Expert Advisor
# ORDER_REASON_SL     (4) – triggered by stop loss
# ORDER_REASON_TP     (5) – triggered by take profit
# ORDER_REASON_SO     (6) – triggered by stop out

# ── Deal Types ────────────────────────────────────────────────────────────────
# DEAL_TYPE_BUY                    (0) – buy deal
# DEAL_TYPE_SELL                   (1) – sell deal
# DEAL_TYPE_BALANCE                (2) – balance operation
# DEAL_TYPE_CREDIT                 (3) – credit operation
# DEAL_TYPE_CHARGE                 (4) – additional charge
# DEAL_TYPE_CORRECTION             (5) – correction deal
# DEAL_TYPE_BONUS                  (6) – bonus
# DEAL_TYPE_COMMISSION             (7) – commission
# DEAL_TYPE_COMMISSION_DAILY       (8) – daily commission
# DEAL_TYPE_COMMISSION_MONTHLY     (9) – monthly commission
# DEAL_TYPE_COMMISSION_AGENT_DAILY (10) – daily agent commission
# DEAL_TYPE_COMMISSION_AGENT_MONTHLY(11)– monthly agent commission
# DEAL_TYPE_INTEREST               (12) – interest rate charge
# DEAL_TYPE_BUY_CANCELED           (13) – cancelled buy deal
# DEAL_TYPE_SELL_CANCELED          (14) – cancelled sell deal
# DEAL_DIVIDEND                    (15) – dividend
# DEAL_DIVIDEND_FRANKED            (16) – franked dividend
# DEAL_TAX                         (17) – tax charge

# ── Deal Entry ────────────────────────────────────────────────────────────────
# DEAL_ENTRY_IN     (0) – entry into the market (position opened)
# DEAL_ENTRY_OUT    (1) – exit from the market (position closed)
# DEAL_ENTRY_INOUT  (2) – reversal (position direction changed)
# DEAL_ENTRY_OUT_BY (3) – closed by an opposite position

# ── Deal Reasons ──────────────────────────────────────────────────────────────
# DEAL_REASON_CLIENT   (0) – executed from desktop terminal
# DEAL_REASON_MOBILE   (1) – executed from mobile app
# DEAL_REASON_WEB      (2) – executed from web terminal
# DEAL_REASON_EXPERT   (3) – executed by Expert Advisor
# DEAL_REASON_SL       (4) – triggered by stop loss
# DEAL_REASON_TP       (5) – triggered by take profit
# DEAL_REASON_SO       (6) – triggered by stop out
# DEAL_REASON_ROLLOVER (7) – rollover
# DEAL_REASON_VMARGIN  (8) – variation margin
# DEAL_REASON_SPLIT    (9) – split

# ── Book Types ────────────────────────────────────────────────────────────────
# BOOK_TYPE_SELL        (0) – sell order at the specified price
# BOOK_TYPE_BUY         (1) – buy order at the specified price
# BOOK_TYPE_SELL_MARKET (2) – sell order at market price
# BOOK_TYPE_BUY_MARKET  (3) – buy order at market price

# Trade Actions
TRADE_ACTION_DEAL = getattr(mt5, "TRADE_ACTION_DEAL", 1)
TRADE_ACTION_PENDING = getattr(mt5, "TRADE_ACTION_PENDING", 5)
TRADE_ACTION_SLTP = getattr(mt5, "TRADE_ACTION_SLTP", 6)
TRADE_ACTION_MODIFY = getattr(mt5, "TRADE_ACTION_MODIFY", 7)
TRADE_ACTION_REMOVE = getattr(mt5, "TRADE_ACTION_REMOVE", 8)
TRADE_ACTION_CLOSE_BY = getattr(mt5, "TRADE_ACTION_CLOSE_BY", 10)

# Order Types
ORDER_TYPE_BUY = getattr(mt5, "ORDER_TYPE_BUY", 0)
ORDER_TYPE_SELL = getattr(mt5, "ORDER_TYPE_SELL", 1)
ORDER_TYPE_BUY_LIMIT = getattr(mt5, "ORDER_TYPE_BUY_LIMIT", 2)
ORDER_TYPE_SELL_LIMIT = getattr(mt5, "ORDER_TYPE_SELL_LIMIT", 3)
ORDER_TYPE_BUY_STOP = getattr(mt5, "ORDER_TYPE_BUY_STOP", 4)
ORDER_TYPE_SELL_STOP = getattr(mt5, "ORDER_TYPE_SELL_STOP", 5)
ORDER_TYPE_BUY_STOP_LIMIT = getattr(mt5, "ORDER_TYPE_BUY_STOP_LIMIT", 6)
ORDER_TYPE_SELL_STOP_LIMIT = getattr(mt5, "ORDER_TYPE_SELL_STOP_LIMIT", 7)
ORDER_TYPE_CLOSE_BY = getattr(mt5, "ORDER_TYPE_CLOSE_BY", 8)

# Order Filling
ORDER_FILLING_FOK = getattr(mt5, "ORDER_FILLING_FOK", 0)
ORDER_FILLING_IOC = getattr(mt5, "ORDER_FILLING_IOC", 1)
ORDER_FILLING_RETURN = getattr(mt5, "ORDER_FILLING_RETURN", 2)
ORDER_FILLING_BOC = getattr(mt5, "ORDER_FILLING_BOC", 3)

# Order Time
ORDER_TIME_GTC = getattr(mt5, "ORDER_TIME_GTC", 0)
ORDER_TIME_DAY = getattr(mt5, "ORDER_TIME_DAY", 1)
ORDER_TIME_SPECIFIED = getattr(mt5, "ORDER_TIME_SPECIFIED", 2)
ORDER_TIME_SPECIFIED_DAY = getattr(mt5, "ORDER_TIME_SPECIFIED_DAY", 3)

# Position Types
POSITION_TYPE_BUY = getattr(mt5, "POSITION_TYPE_BUY", 0)
POSITION_TYPE_SELL = getattr(mt5, "POSITION_TYPE_SELL", 1)

# Position Reasons
POSITION_REASON_CLIENT = getattr(mt5, "POSITION_REASON_CLIENT", 0)
POSITION_REASON_MOBILE = getattr(mt5, "POSITION_REASON_MOBILE", 1)
POSITION_REASON_WEB = getattr(mt5, "POSITION_REASON_WEB", 2)
POSITION_REASON_EXPERT = getattr(mt5, "POSITION_REASON_EXPERT", 3)

# Order States
ORDER_STATE_STARTED = getattr(mt5, "ORDER_STATE_STARTED", 0)
ORDER_STATE_PLACED = getattr(mt5, "ORDER_STATE_PLACED", 1)
ORDER_STATE_CANCELED = getattr(mt5, "ORDER_STATE_CANCELED", 2)
ORDER_STATE_PARTIAL = getattr(mt5, "ORDER_STATE_PARTIAL", 3)
ORDER_STATE_FILLED = getattr(mt5, "ORDER_STATE_FILLED", 4)
ORDER_STATE_REJECTED = getattr(mt5, "ORDER_STATE_REJECTED", 5)
ORDER_STATE_EXPIRED = getattr(mt5, "ORDER_STATE_EXPIRED", 6)
ORDER_STATE_REQUEST_ADD = getattr(mt5, "ORDER_STATE_REQUEST_ADD", 7)
ORDER_STATE_REQUEST_MODIFY = getattr(mt5, "ORDER_STATE_REQUEST_MODIFY", 8)
ORDER_STATE_REQUEST_CANCEL = getattr(mt5, "ORDER_STATE_REQUEST_CANCEL", 9)

# Order Reasons
ORDER_REASON_CLIENT = getattr(mt5, "ORDER_REASON_CLIENT", 0)
ORDER_REASON_MOBILE = getattr(mt5, "ORDER_REASON_MOBILE", 1)
ORDER_REASON_WEB = getattr(mt5, "ORDER_REASON_WEB", 2)
ORDER_REASON_EXPERT = getattr(mt5, "ORDER_REASON_EXPERT", 3)
ORDER_REASON_SL = getattr(mt5, "ORDER_REASON_SL", 4)
ORDER_REASON_TP = getattr(mt5, "ORDER_REASON_TP", 5)
ORDER_REASON_SO = getattr(mt5, "ORDER_REASON_SO", 6)

# Deal Types
DEAL_TYPE_BUY = getattr(mt5, "DEAL_TYPE_BUY", 0)
DEAL_TYPE_SELL = getattr(mt5, "DEAL_TYPE_SELL", 1)
DEAL_TYPE_BALANCE = getattr(mt5, "DEAL_TYPE_BALANCE", 2)
DEAL_TYPE_CREDIT = getattr(mt5, "DEAL_TYPE_CREDIT", 3)
DEAL_TYPE_CHARGE = getattr(mt5, "DEAL_TYPE_CHARGE", 4)
DEAL_TYPE_CORRECTION = getattr(mt5, "DEAL_TYPE_CORRECTION", 5)
DEAL_TYPE_BONUS = getattr(mt5, "DEAL_TYPE_BONUS", 6)
DEAL_TYPE_COMMISSION = getattr(mt5, "DEAL_TYPE_COMMISSION", 7)
DEAL_TYPE_COMMISSION_DAILY = getattr(mt5, "DEAL_TYPE_COMMISSION_DAILY", 8)
DEAL_TYPE_COMMISSION_MONTHLY = getattr(mt5, "DEAL_TYPE_COMMISSION_MONTHLY", 9)
DEAL_TYPE_COMMISSION_AGENT_DAILY = getattr(mt5, "DEAL_TYPE_COMMISSION_AGENT_DAILY", 10)
DEAL_TYPE_COMMISSION_AGENT_MONTHLY = getattr(mt5, "DEAL_TYPE_COMMISSION_AGENT_MONTHLY", 11)
DEAL_TYPE_INTEREST = getattr(mt5, "DEAL_TYPE_INTEREST", 12)
DEAL_TYPE_BUY_CANCELED = getattr(mt5, "DEAL_TYPE_BUY_CANCELED", 13)
DEAL_TYPE_SELL_CANCELED = getattr(mt5, "DEAL_TYPE_SELL_CANCELED", 14)
DEAL_DIVIDEND = getattr(mt5, "DEAL_DIVIDEND", 15)
DEAL_DIVIDEND_FRANKED = getattr(mt5, "DEAL_DIVIDEND_FRANKED", 16)
DEAL_TAX = getattr(mt5, "DEAL_TAX", 17)

# Deal Entry
DEAL_ENTRY_IN = getattr(mt5, "DEAL_ENTRY_IN", 0)
DEAL_ENTRY_OUT = getattr(mt5, "DEAL_ENTRY_OUT", 1)
DEAL_ENTRY_INOUT = getattr(mt5, "DEAL_ENTRY_INOUT", 2)
DEAL_ENTRY_OUT_BY = getattr(mt5, "DEAL_ENTRY_OUT_BY", 3)

# Deal Reasons
DEAL_REASON_CLIENT = getattr(mt5, "DEAL_REASON_CLIENT", 0)
DEAL_REASON_MOBILE = getattr(mt5, "DEAL_REASON_MOBILE", 1)
DEAL_REASON_WEB = getattr(mt5, "DEAL_REASON_WEB", 2)
DEAL_REASON_EXPERT = getattr(mt5, "DEAL_REASON_EXPERT", 3)
DEAL_REASON_SL = getattr(mt5, "DEAL_REASON_SL", 4)
DEAL_REASON_TP = getattr(mt5, "DEAL_REASON_TP", 5)
DEAL_REASON_SO = getattr(mt5, "DEAL_REASON_SO", 6)
DEAL_REASON_ROLLOVER = getattr(mt5, "DEAL_REASON_ROLLOVER", 7)
DEAL_REASON_VMARGIN = getattr(mt5, "DEAL_REASON_VMARGIN", 8)
DEAL_REASON_SPLIT = getattr(mt5, "DEAL_REASON_SPLIT", 9)

# Book Types
BOOK_TYPE_SELL = getattr(mt5, "BOOK_TYPE_SELL", 1)
BOOK_TYPE_BUY = getattr(mt5, "BOOK_TYPE_BUY", 2)
BOOK_TYPE_SELL_MARKET = getattr(mt5, "BOOK_TYPE_SELL_MARKET", 3)
BOOK_TYPE_BUY_MARKET = getattr(mt5, "BOOK_TYPE_BUY_MARKET", 4)

# Timeframes
TIMEFRAME_M1 = getattr(mt5, "TIMEFRAME_M1", 1)
TIMEFRAME_M2 = getattr(mt5, "TIMEFRAME_M2", 2)
TIMEFRAME_M3 = getattr(mt5, "TIMEFRAME_M3", 3)
TIMEFRAME_M4 = getattr(mt5, "TIMEFRAME_M4", 4)
TIMEFRAME_M5 = getattr(mt5, "TIMEFRAME_M5", 5)
TIMEFRAME_M6 = getattr(mt5, "TIMEFRAME_M6", 6)
TIMEFRAME_M10 = getattr(mt5, "TIMEFRAME_M10", 10)
TIMEFRAME_M12 = getattr(mt5, "TIMEFRAME_M12", 12)
TIMEFRAME_M15 = getattr(mt5, "TIMEFRAME_M15", 15)
TIMEFRAME_M20 = getattr(mt5, "TIMEFRAME_M20", 20)
TIMEFRAME_M30 = getattr(mt5, "TIMEFRAME_M30", 30)
TIMEFRAME_H1 = getattr(mt5, "TIMEFRAME_H1", 16385)
TIMEFRAME_H2 = getattr(mt5, "TIMEFRAME_H2", 16386)
TIMEFRAME_H3 = getattr(mt5, "TIMEFRAME_H3", 16387)
TIMEFRAME_H4 = getattr(mt5, "TIMEFRAME_H4", 16388)
TIMEFRAME_H6 = getattr(mt5, "TIMEFRAME_H6", 16390)
TIMEFRAME_H8 = getattr(mt5, "TIMEFRAME_H8", 16392)
TIMEFRAME_H12 = getattr(mt5, "TIMEFRAME_H12", 16396)
TIMEFRAME_D1 = getattr(mt5, "TIMEFRAME_D1", 16408)
TIMEFRAME_W1 = getattr(mt5, "TIMEFRAME_W1", 32769)
TIMEFRAME_MN1 = getattr(mt5, "TIMEFRAME_MN1", 49153)

# Copy Ticks Flags
COPY_TICKS_ALL = getattr(mt5, "COPY_TICKS_ALL", 6)
COPY_TICKS_INFO = getattr(mt5, "COPY_TICKS_INFO", 2)
COPY_TICKS_TRADE = getattr(mt5, "COPY_TICKS_TRADE", 4)

# Tick Flags
TICK_FLAG_BID = getattr(mt5, "TICK_FLAG_BID", 2)
TICK_FLAG_ASK = getattr(mt5, "TICK_FLAG_ASK", 4)
TICK_FLAG_LAST = getattr(mt5, "TICK_FLAG_LAST", 8)
TICK_FLAG_VOLUME = getattr(mt5, "TICK_FLAG_VOLUME", 16)
TICK_FLAG_BUY = getattr(mt5, "TICK_FLAG_BUY", 32)
TICK_FLAG_SELL = getattr(mt5, "TICK_FLAG_SELL", 64)

# Trade Return Codes
TRADE_RETCODE_REQUOTE = getattr(mt5, "TRADE_RETCODE_REQUOTE", 10004)
TRADE_RETCODE_REJECT = getattr(mt5, "TRADE_RETCODE_REJECT", 10006)
TRADE_RETCODE_CANCEL = getattr(mt5, "TRADE_RETCODE_CANCEL", 10007)
TRADE_RETCODE_PLACED = getattr(mt5, "TRADE_RETCODE_PLACED", 10008)
TRADE_RETCODE_DONE = getattr(mt5, "TRADE_RETCODE_DONE", 10009)
TRADE_RETCODE_DONE_PARTIAL = getattr(mt5, "TRADE_RETCODE_DONE_PARTIAL", 10010)
TRADE_RETCODE_ERROR = getattr(mt5, "TRADE_RETCODE_ERROR", 10011)
TRADE_RETCODE_TIMEOUT = getattr(mt5, "TRADE_RETCODE_TIMEOUT", 10012)
TRADE_RETCODE_INVALID = getattr(mt5, "TRADE_RETCODE_INVALID", 10013)
TRADE_RETCODE_INVALID_VOLUME = getattr(mt5, "TRADE_RETCODE_INVALID_VOLUME", 10014)
TRADE_RETCODE_INVALID_PRICE = getattr(mt5, "TRADE_RETCODE_INVALID_PRICE", 10015)
TRADE_RETCODE_INVALID_STOPS = getattr(mt5, "TRADE_RETCODE_INVALID_STOPS", 10016)
TRADE_RETCODE_TRADE_DISABLED = getattr(mt5, "TRADE_RETCODE_TRADE_DISABLED", 10017)
TRADE_RETCODE_MARKET_CLOSED = getattr(mt5, "TRADE_RETCODE_MARKET_CLOSED", 10018)
TRADE_RETCODE_NO_MONEY = getattr(mt5, "TRADE_RETCODE_NO_MONEY", 10019)
TRADE_RETCODE_PRICE_CHANGED = getattr(mt5, "TRADE_RETCODE_PRICE_CHANGED", 10020)
TRADE_RETCODE_PRICE_OFF = getattr(mt5, "TRADE_RETCODE_PRICE_OFF", 10021)
TRADE_RETCODE_INVALID_EXPIRATION = getattr(mt5, "TRADE_RETCODE_INVALID_EXPIRATION", 10022)
TRADE_RETCODE_ORDER_CHANGED = getattr(mt5, "TRADE_RETCODE_ORDER_CHANGED", 10023)
TRADE_RETCODE_TOO_MANY_REQUESTS = getattr(mt5, "TRADE_RETCODE_TOO_MANY_REQUESTS", 10024)
TRADE_RETCODE_NO_CHANGES = getattr(mt5, "TRADE_RETCODE_NO_CHANGES", 10025)
TRADE_RETCODE_SERVER_DISABLES_AT = getattr(mt5, "TRADE_RETCODE_SERVER_DISABLES_AT", 10026)
TRADE_RETCODE_CLIENT_DISABLES_AT = getattr(mt5, "TRADE_RETCODE_CLIENT_DISABLES_AT", 10027)
TRADE_RETCODE_LOCKED = getattr(mt5, "TRADE_RETCODE_LOCKED", 10028)
TRADE_RETCODE_FROZEN = getattr(mt5, "TRADE_RETCODE_FROZEN", 10029)
TRADE_RETCODE_INVALID_FILL = getattr(mt5, "TRADE_RETCODE_INVALID_FILL", 10030)
TRADE_RETCODE_CONNECTION = getattr(mt5, "TRADE_RETCODE_CONNECTION", 10031)
TRADE_RETCODE_ONLY_REAL = getattr(mt5, "TRADE_RETCODE_ONLY_REAL", 10032)
TRADE_RETCODE_LIMIT_ORDERS = getattr(mt5, "TRADE_RETCODE_LIMIT_ORDERS", 10033)
TRADE_RETCODE_LIMIT_VOLUME = getattr(mt5, "TRADE_RETCODE_LIMIT_VOLUME", 10034)
TRADE_RETCODE_INVALID_ORDER = getattr(mt5, "TRADE_RETCODE_INVALID_ORDER", 10035)
TRADE_RETCODE_POSITION_CLOSED = getattr(mt5, "TRADE_RETCODE_POSITION_CLOSED", 10036)

# ruff: noqa: RUF022
__all__ = [
    # Trade Actions
    "TRADE_ACTION_DEAL",
    "TRADE_ACTION_PENDING",
    "TRADE_ACTION_SLTP",
    "TRADE_ACTION_MODIFY",
    "TRADE_ACTION_REMOVE",
    "TRADE_ACTION_CLOSE_BY",
    # Order Types
    "ORDER_TYPE_BUY",
    "ORDER_TYPE_SELL",
    "ORDER_TYPE_BUY_LIMIT",
    "ORDER_TYPE_SELL_LIMIT",
    "ORDER_TYPE_BUY_STOP",
    "ORDER_TYPE_SELL_STOP",
    "ORDER_TYPE_BUY_STOP_LIMIT",
    "ORDER_TYPE_SELL_STOP_LIMIT",
    "ORDER_TYPE_CLOSE_BY",
    # Order States
    "ORDER_STATE_STARTED",
    "ORDER_STATE_PLACED",
    "ORDER_STATE_CANCELED",
    "ORDER_STATE_PARTIAL",
    "ORDER_STATE_FILLED",
    "ORDER_STATE_REJECTED",
    "ORDER_STATE_EXPIRED",
    "ORDER_STATE_REQUEST_ADD",
    "ORDER_STATE_REQUEST_MODIFY",
    "ORDER_STATE_REQUEST_CANCEL",
    # Order Filling
    "ORDER_FILLING_FOK",
    "ORDER_FILLING_IOC",
    "ORDER_FILLING_RETURN",
    "ORDER_FILLING_BOC",
    # Order Time
    "ORDER_TIME_GTC",
    "ORDER_TIME_DAY",
    "ORDER_TIME_SPECIFIED",
    "ORDER_TIME_SPECIFIED_DAY",
    # Order Reasons
    "ORDER_REASON_CLIENT",
    "ORDER_REASON_MOBILE",
    "ORDER_REASON_WEB",
    "ORDER_REASON_EXPERT",
    "ORDER_REASON_SL",
    "ORDER_REASON_TP",
    "ORDER_REASON_SO",
    # Position Types
    "POSITION_TYPE_BUY",
    "POSITION_TYPE_SELL",
    # Position Reasons
    "POSITION_REASON_CLIENT",
    "POSITION_REASON_MOBILE",
    "POSITION_REASON_WEB",
    "POSITION_REASON_EXPERT",
    # Deal Types
    "DEAL_TYPE_BUY",
    "DEAL_TYPE_SELL",
    "DEAL_TYPE_BALANCE",
    "DEAL_TYPE_CREDIT",
    "DEAL_TYPE_CHARGE",
    "DEAL_TYPE_CORRECTION",
    "DEAL_TYPE_BONUS",
    "DEAL_TYPE_COMMISSION",
    "DEAL_TYPE_COMMISSION_DAILY",
    "DEAL_TYPE_COMMISSION_MONTHLY",
    "DEAL_TYPE_COMMISSION_AGENT_DAILY",
    "DEAL_TYPE_COMMISSION_AGENT_MONTHLY",
    "DEAL_TYPE_INTEREST",
    "DEAL_TYPE_BUY_CANCELED",
    "DEAL_TYPE_SELL_CANCELED",
    "DEAL_DIVIDEND",
    "DEAL_DIVIDEND_FRANKED",
    "DEAL_TAX",
    # Deal Entry
    "DEAL_ENTRY_IN",
    "DEAL_ENTRY_OUT",
    "DEAL_ENTRY_INOUT",
    "DEAL_ENTRY_OUT_BY",
    # Deal Reasons
    "DEAL_REASON_CLIENT",
    "DEAL_REASON_MOBILE",
    "DEAL_REASON_WEB",
    "DEAL_REASON_EXPERT",
    "DEAL_REASON_SL",
    "DEAL_REASON_TP",
    "DEAL_REASON_SO",
    "DEAL_REASON_ROLLOVER",
    "DEAL_REASON_VMARGIN",
    "DEAL_REASON_SPLIT",
    # Book Types
    "BOOK_TYPE_SELL",
    "BOOK_TYPE_BUY",
    "BOOK_TYPE_SELL_MARKET",
    "BOOK_TYPE_BUY_MARKET",
    # Timeframes
    "TIMEFRAME_M1",
    "TIMEFRAME_M2",
    "TIMEFRAME_M3",
    "TIMEFRAME_M4",
    "TIMEFRAME_M5",
    "TIMEFRAME_M6",
    "TIMEFRAME_M10",
    "TIMEFRAME_M12",
    "TIMEFRAME_M15",
    "TIMEFRAME_M20",
    "TIMEFRAME_M30",
    "TIMEFRAME_H1",
    "TIMEFRAME_H2",
    "TIMEFRAME_H3",
    "TIMEFRAME_H4",
    "TIMEFRAME_H6",
    "TIMEFRAME_H8",
    "TIMEFRAME_H12",
    "TIMEFRAME_D1",
    "TIMEFRAME_W1",
    "TIMEFRAME_MN1",
    # Copy Ticks Flags
    "COPY_TICKS_ALL",
    "COPY_TICKS_INFO",
    "COPY_TICKS_TRADE",
    # Tick Flags
    "TICK_FLAG_BID",
    "TICK_FLAG_ASK",
    "TICK_FLAG_LAST",
    "TICK_FLAG_VOLUME",
    "TICK_FLAG_BUY",
    "TICK_FLAG_SELL",
    # Trade Return Codes
    "TRADE_RETCODE_REQUOTE",
    "TRADE_RETCODE_REJECT",
    "TRADE_RETCODE_CANCEL",
    "TRADE_RETCODE_PLACED",
    "TRADE_RETCODE_DONE",
    "TRADE_RETCODE_DONE_PARTIAL",
    "TRADE_RETCODE_ERROR",
    "TRADE_RETCODE_TIMEOUT",
    "TRADE_RETCODE_INVALID",
    "TRADE_RETCODE_INVALID_VOLUME",
    "TRADE_RETCODE_INVALID_PRICE",
    "TRADE_RETCODE_INVALID_STOPS",
    "TRADE_RETCODE_TRADE_DISABLED",
    "TRADE_RETCODE_MARKET_CLOSED",
    "TRADE_RETCODE_NO_MONEY",
    "TRADE_RETCODE_PRICE_CHANGED",
    "TRADE_RETCODE_PRICE_OFF",
    "TRADE_RETCODE_INVALID_EXPIRATION",
    "TRADE_RETCODE_ORDER_CHANGED",
    "TRADE_RETCODE_TOO_MANY_REQUESTS",
    "TRADE_RETCODE_NO_CHANGES",
    "TRADE_RETCODE_SERVER_DISABLES_AT",
    "TRADE_RETCODE_CLIENT_DISABLES_AT",
    "TRADE_RETCODE_LOCKED",
    "TRADE_RETCODE_FROZEN",
    "TRADE_RETCODE_INVALID_FILL",
    "TRADE_RETCODE_CONNECTION",
    "TRADE_RETCODE_ONLY_REAL",
    "TRADE_RETCODE_LIMIT_ORDERS",
    "TRADE_RETCODE_LIMIT_VOLUME",
    "TRADE_RETCODE_INVALID_ORDER",
    "TRADE_RETCODE_POSITION_CLOSED",
]
