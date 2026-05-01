# Constants Reference

All MT5 constants are available through `syntiq_mt5.constants`—no need to import `MetaTrader5` directly.

## Import

```python
from syntiq_mt5 import constants
```

---

## Trade Actions

Used in `TradeRequest.action` to specify the type of trading operation.

| Constant | Value | Description |
|----------|-------|-------------|
| `TRADE_ACTION_DEAL` | 1 | Place a trade order for immediate execution (market order) |
| `TRADE_ACTION_PENDING` | 5 | Place a pending order |
| `TRADE_ACTION_SLTP` | 6 | Modify stop loss and take profit |
| `TRADE_ACTION_MODIFY` | 7 | Modify parameters of a previously placed order |
| `TRADE_ACTION_REMOVE` | 8 | Remove a pending order |
| `TRADE_ACTION_CLOSE_BY` | 10 | Close a position by an opposite one |

**Example:**

```python
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.1,
    type=constants.ORDER_TYPE_BUY,
    price=1.1000
)
```

---

## Order Types

Used in `TradeRequest.type` to specify the order type.

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_TYPE_BUY` | 0 | Market buy order |
| `ORDER_TYPE_SELL` | 1 | Market sell order |
| `ORDER_TYPE_BUY_LIMIT` | 2 | Buy limit pending order |
| `ORDER_TYPE_SELL_LIMIT` | 3 | Sell limit pending order |
| `ORDER_TYPE_BUY_STOP` | 4 | Buy stop pending order |
| `ORDER_TYPE_SELL_STOP` | 5 | Sell stop pending order |
| `ORDER_TYPE_BUY_STOP_LIMIT` | 6 | Buy stop limit pending order |
| `ORDER_TYPE_SELL_STOP_LIMIT` | 7 | Sell stop limit pending order |
| `ORDER_TYPE_CLOSE_BY` | 8 | Close by order |

**Example:**

```python
# Market buy
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.1,
    type=constants.ORDER_TYPE_BUY
)

# Buy limit order
request = TradeRequest(
    action=constants.TRADE_ACTION_PENDING,
    symbol="EURUSD",
    volume=0.1,
    type=constants.ORDER_TYPE_BUY_LIMIT,
    price=1.0950
)
```

---

## Order Filling Modes

Used in `TradeRequest.type_filling` to specify order execution policy.

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_FILLING_FOK` | 0 | Fill or Kill - order must be filled in full or canceled |
| `ORDER_FILLING_IOC` | 1 | Immediate or Cancel - fill available volume, cancel the rest |
| `ORDER_FILLING_RETURN` | 2 | Return - order is placed in the order book |
| `ORDER_FILLING_BOC` | 3 | Book or Cancel - order must be placed in the order book or canceled |

---

## Order Time Modes

Used in `TradeRequest.type_time` to specify order lifetime.

| Constant | Value | Description |
|----------|-------|-------------|
| `ORDER_TIME_GTC` | 0 | Good Till Cancelled - order is active until explicitly canceled |
| `ORDER_TIME_DAY` | 1 | Good Till Day - order is active until the end of the trading day |
| `ORDER_TIME_SPECIFIED` | 2 | Good Till Specified - order is active until the specified date |
| `ORDER_TIME_SPECIFIED_DAY` | 3 | Good Till Specified Day - order is active until 23:59:59 of the specified day |

---

## Position Types

Used to identify position direction.

| Constant | Value | Description |
|----------|-------|-------------|
| `POSITION_TYPE_BUY` | 0 | Long position (buy) |
| `POSITION_TYPE_SELL` | 1 | Short position (sell) |

---

## Timeframes

Used in `get_candles()` to specify the candle period.

### Minutes

| Constant | Value | Description |
|----------|-------|-------------|
| `TIMEFRAME_M1` | 1 | 1 minute |
| `TIMEFRAME_M2` | 2 | 2 minutes |
| `TIMEFRAME_M3` | 3 | 3 minutes |
| `TIMEFRAME_M4` | 4 | 4 minutes |
| `TIMEFRAME_M5` | 5 | 5 minutes |
| `TIMEFRAME_M6` | 6 | 6 minutes |
| `TIMEFRAME_M10` | 10 | 10 minutes |
| `TIMEFRAME_M12` | 12 | 12 minutes |
| `TIMEFRAME_M15` | 15 | 15 minutes |
| `TIMEFRAME_M20` | 20 | 20 minutes |
| `TIMEFRAME_M30` | 30 | 30 minutes |

### Hours

| Constant | Value | Description |
|----------|-------|-------------|
| `TIMEFRAME_H1` | 16385 | 1 hour |
| `TIMEFRAME_H2` | 16386 | 2 hours |
| `TIMEFRAME_H3` | 16387 | 3 hours |
| `TIMEFRAME_H4` | 16388 | 4 hours |
| `TIMEFRAME_H6` | 16390 | 6 hours |
| `TIMEFRAME_H8` | 16392 | 8 hours |
| `TIMEFRAME_H12` | 16396 | 12 hours |

### Days and Longer

| Constant | Value | Description |
|----------|-------|-------------|
| `TIMEFRAME_D1` | 16408 | 1 day |
| `TIMEFRAME_W1` | 32769 | 1 week |
| `TIMEFRAME_MN1` | 49153 | 1 month |

**Example:**

```python
# Get 1-hour candles
res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=100)

# Get daily candles
res = mt5.get_candles("GBPUSD", timeframe=constants.TIMEFRAME_D1, count=30)
```

---

## Tick Copy Flags

Used in `get_ticks()` to specify which ticks to retrieve.

| Constant | Value | Description |
|----------|-------|-------------|
| `COPY_TICKS_ALL` | 6 | All ticks (info + trade) |
| `COPY_TICKS_INFO` | 2 | Ticks with bid/ask changes |
| `COPY_TICKS_TRADE` | 4 | Ticks with last price and volume changes |

**Example:**

```python
# Get all ticks
ticks = mt5.get_ticks("EURUSD", flags=constants.COPY_TICKS_ALL, count=1000)

# Get only trade ticks
ticks = mt5.get_ticks("EURUSD", flags=constants.COPY_TICKS_TRADE, count=1000)
```

---

## Tick Flags

Flags present in tick data indicating what changed.

| Constant | Value | Description |
|----------|-------|-------------|
| `TICK_FLAG_BID` | 2 | Bid price changed |
| `TICK_FLAG_ASK` | 4 | Ask price changed |
| `TICK_FLAG_LAST` | 8 | Last price changed |
| `TICK_FLAG_VOLUME` | 16 | Volume changed |
| `TICK_FLAG_BUY` | 32 | Last deal was a buy |
| `TICK_FLAG_SELL` | 64 | Last deal was a sell |

---

## Trade Return Codes

Return codes from trade operations (order placement, modification, etc.).

### Success Codes

| Constant | Value | Description |
|----------|-------|-------------|
| `TRADE_RETCODE_DONE` | 10009 | Request completed successfully |
| `TRADE_RETCODE_DONE_PARTIAL` | 10010 | Request completed partially |
| `TRADE_RETCODE_PLACED` | 10008 | Order placed |

### Error Codes

| Constant | Value | Description |
|----------|-------|-------------|
| `TRADE_RETCODE_REQUOTE` | 10004 | Requote |
| `TRADE_RETCODE_REJECT` | 10006 | Request rejected |
| `TRADE_RETCODE_CANCEL` | 10007 | Request canceled by trader |
| `TRADE_RETCODE_ERROR` | 10011 | Request processing error |
| `TRADE_RETCODE_TIMEOUT` | 10012 | Request timeout |
| `TRADE_RETCODE_INVALID` | 10013 | Invalid request |
| `TRADE_RETCODE_INVALID_VOLUME` | 10014 | Invalid volume |
| `TRADE_RETCODE_INVALID_PRICE` | 10015 | Invalid price |
| `TRADE_RETCODE_INVALID_STOPS` | 10016 | Invalid stops |
| `TRADE_RETCODE_TRADE_DISABLED` | 10017 | Trade is disabled |
| `TRADE_RETCODE_MARKET_CLOSED` | 10018 | Market is closed |
| `TRADE_RETCODE_NO_MONEY` | 10019 | Not enough money |
| `TRADE_RETCODE_PRICE_CHANGED` | 10020 | Price changed |
| `TRADE_RETCODE_PRICE_OFF` | 10021 | No quotes |
| `TRADE_RETCODE_INVALID_EXPIRATION` | 10022 | Invalid expiration |
| `TRADE_RETCODE_ORDER_CHANGED` | 10023 | Order state changed |
| `TRADE_RETCODE_TOO_MANY_REQUESTS` | 10024 | Too many requests |
| `TRADE_RETCODE_NO_CHANGES` | 10025 | No changes in request |
| `TRADE_RETCODE_SERVER_DISABLES_AT` | 10026 | Autotrading disabled by server |
| `TRADE_RETCODE_CLIENT_DISABLES_AT` | 10027 | Autotrading disabled by client |
| `TRADE_RETCODE_LOCKED` | 10028 | Request locked for processing |
| `TRADE_RETCODE_FROZEN` | 10029 | Order or position frozen |
| `TRADE_RETCODE_INVALID_FILL` | 10030 | Invalid fill type |
| `TRADE_RETCODE_CONNECTION` | 10031 | No connection |
| `TRADE_RETCODE_ONLY_REAL` | 10032 | Only real accounts allowed |
| `TRADE_RETCODE_LIMIT_ORDERS` | 10033 | Orders limit reached |
| `TRADE_RETCODE_LIMIT_VOLUME` | 10034 | Volume limit reached |
| `TRADE_RETCODE_INVALID_ORDER` | 10035 | Invalid or prohibited order type |
| `TRADE_RETCODE_POSITION_CLOSED` | 10036 | Position already closed |

**Example:**

```python
result = mt5.order_send(request)
if result.success:
    if result.data.retcode == constants.TRADE_RETCODE_DONE:
        print("Order executed successfully")
    elif result.data.retcode == constants.TRADE_RETCODE_DONE_PARTIAL:
        print("Order partially executed")
else:
    print(f"Order failed: {result.error_message}")
```
