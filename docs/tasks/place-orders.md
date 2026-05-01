# Place Orders

Validate and execute trade requests using `TradeRequest`.

---

## Market order (buy)

```python
from syntiq_mt5 import TradeRequest, constants

request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.10,
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
    sl=1.08000,
    tp=1.09000,
    deviation=10,
    comment="my order",
)

# 1. Validate first (no order is placed)
check = mt5.order_check(request)
if check.success and check.data.is_successful:
    print("Validation passed — sending order")

    # 2. Send the order
    res = mt5.order_send(request)
    if res.success and res.data.is_successful:
        print(f"Filled: order={res.data.order}  deal={res.data.deal}  price={res.data.price}")
    else:
        print(f"Rejected: {res.data.comment if res.success else res.error_message}")
else:
    reason = check.data.comment if check.success else check.error_message
    print(f"Validation failed: {reason}")
```

```text
Validation passed — sending order
Filled: order=123456  deal=789012  price=1.08503
```

---

## Pending order (buy limit)

```python
request = TradeRequest(
    action=constants.TRADE_ACTION_PENDING,
    symbol="EURUSD",
    volume=0.10,
    type=constants.ORDER_TYPE_BUY_LIMIT,
    price=1.08000,
    sl=1.07500,
    tp=1.09000,
    type_time=constants.ORDER_TIME_GTC,
    comment="buy limit",
)

res = mt5.order_send(request)
if res.success and res.data.is_successful:
    print(f"Pending order placed: {res.data.order}")
```

---

## Modify SL/TP on an open position

```python
request = TradeRequest(
    action=constants.TRADE_ACTION_SLTP,
    symbol="EURUSD",
    position=123456,   # position ticket
    sl=1.07800,
    tp=1.09500,
)

res = mt5.order_send(request)
if res.success and res.data.is_successful:
    print("SL/TP updated")
```

---

## Pre-flight calculations

```python
# Required margin for 0.1 lot EURUSD buy at 1.08500
margin = mt5.order_calc_margin(constants.ORDER_TYPE_BUY, "EURUSD", 0.10, 1.08500)
if margin.success:
    print(f"Required margin: {margin.data:.2f}")

# Expected profit for 50-pip move
profit = mt5.order_calc_profit(constants.ORDER_TYPE_BUY, "EURUSD", 0.10, 1.08500, 1.09000)
if profit.success:
    print(f"Expected profit: {profit.data:.2f}")
```

```text
Required margin: 108.50
Expected profit: 50.00
```

---

## TradeRequest fields

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | `TradeAction` | required | `TRADE_ACTION_DEAL`, `PENDING`, `SLTP`, `MODIFY`, `REMOVE`, `CLOSE_BY` |
| `symbol` | `str` | `""` | Trading instrument |
| `volume` | `float` | `0.0` | Lots |
| `type` | `OrderType` | `BUY` | Order type |
| `price` | `float` | `0.0` | Execution price |
| `sl` | `float` | `0.0` | Stop loss (`0.0` = not set) |
| `tp` | `float` | `0.0` | Take profit (`0.0` = not set) |
| `deviation` | `int` | `0` | Max price deviation in points |
| `type_filling` | `OrderFilling` | `FOK` | Fill policy |
| `type_time` | `OrderTime` | `GTC` | Expiry policy |
| `comment` | `str` | `""` | Order comment |
| `position` | `int` | `0` | Position ticket (for `SLTP` action) |
| `order` | `int` | `0` | Order ticket (for `MODIFY`/`REMOVE`) |

---

## Checking the result

`order_send()` has two layers of success:

```python
res = mt5.order_send(request)

if not res.success:
    # SDK-level failure (not connected, parse error, etc.)
    print(f"SDK error: {res.error_message}")
elif not res.data.is_successful:
    # Broker rejected the trade
    print(f"Broker rejected: {res.data.comment} (retcode {res.data.retcode})")
else:
    # Trade accepted
    print(f"Deal: {res.data.deal}  Order: {res.data.order}")
```

See [Error Handling](../core/error-handling.md) and [Constants → Trade Return Codes](../reference/constants.md#trade-return-codes) for retcode details.

---

## Failure examples

### Example 1: Insufficient margin

```python
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=10.0,  # ❌ Too large for account
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
)

check = mt5.order_check(request)
if check.success and not check.data.is_successful:
    print(f"Validation failed: {check.data.comment}")
    print(f"Retcode: {check.data.retcode}")
```

**Output:**
```text
Validation failed: Not enough money
Retcode: 10019
```

**Fix:** Calculate required margin first using `order_calc_margin()` and check against `account_info().margin_free`.

---

### Example 2: Invalid volume

```python
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.001,  # ❌ Below minimum
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
)

res = mt5.order_send(request)
if res.success and not res.data.is_successful:
    print(f"Rejected: {res.data.comment}")
```

**Output:**
```text
Rejected: Invalid volume
```

**Fix:** Check `symbol_info("EURUSD").volume_min` and `volume_step` before placing orders.

---

### Example 3: Invalid stops (too close)

```python
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.10,
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
    sl=1.08490,  # ❌ Only 1 pip away
    tp=1.09000,
)

res = mt5.order_send(request)
if res.success and not res.data.is_successful:
    print(f"Rejected: {res.data.comment}")
```

**Output:**
```text
Rejected: Invalid stops
```

**Fix:** Check `symbol_info("EURUSD").trade_stops_level` for minimum distance in points.

---

### Example 4: Market closed

```python
from datetime import datetime, timezone

# Trying to trade on Sunday
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.10,
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
)

res = mt5.order_send(request)
if res.success and not res.data.is_successful:
    print(f"Rejected: {res.data.comment}")
    print(f"Retcode: {res.data.retcode}")
```

**Output:**
```text
Rejected: Market is closed
Retcode: 10018
```

**Fix:** Check `terminal_info().trade_allowed` and symbol trading sessions before placing orders.

---

## Practical notes

!!! tip "Always validate before sending"
    Use `order_check()` before `order_send()` to catch validation errors without consuming a trade request. This is especially important for automated systems.

!!! warning "Handle requotes"
    When `retcode == TRADE_RETCODE_REQUOTE`, the price has moved. The new price is in `res.data.ask` or `res.data.bid`. Update your request and retry.

!!! info "Deviation parameter"
    `deviation` allows the broker to execute at a slightly different price (in points). Set it to `0` for strict price execution, or `10-20` for more flexibility in fast markets.

!!! note "Fill policies"
    - `ORDER_FILLING_FOK` (Fill or Kill): Execute the entire volume immediately or reject
    - `ORDER_FILLING_IOC` (Immediate or Cancel): Execute partial volume, cancel the rest
    - `ORDER_FILLING_RETURN`: Used for exchange instruments
    
    Most Forex brokers require `FOK`. Check `symbol_info().filling_mode` to see what's supported.
