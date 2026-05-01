# Result[T]

Every client method returns `Result[T]`. No exceptions are raised for operational failures.

---

## Structure

```python
class Result(Generic[T]):
    success: bool           # True = operation succeeded
    data: T | None          # set on success, always None on failure
    error_code: int | None  # MT5 error code on failure
    error_message: str | None  # human-readable description on failure
    context: str | None     # MT5 API function name (e.g. "positions_get")
    operation: str | None   # logical operation name
```

!!! success "Strict invariant"
    - `success=True` → `data` is set, error fields are `None`
    - `success=False` → `data` is `None`, `error_code` and `error_message` are set

---

## Basic usage

```python
from syntiq_mt5 import constants

res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=10)

if res.success:
    for candle in res.data:
        print(f"O={candle.open}  H={candle.high}  L={candle.low}  C={candle.close}")
else:
    print(f"[{res.context}] error {res.error_code}: {res.error_message}")
```

---

## Success path

```python
res = mt5.positions()

if res.success:
    print(f"{len(res.data)} open positions")
    for p in res.data:
        print(f"  {p.symbol}  {p.pips_profit:+.1f} pips")
```

`res.data` is always the correct type — `list[Position]` here. No casting needed.

---

## Failure path

```python
res = mt5.positions()

if not res.success:
    print(f"operation:  {res.operation}")
    print(f"error code: {res.error_code}")
    print(f"message:    {res.error_message}")
```

```text
operation:  positions_get
error code: -10
message:    Client not initialized. Call initialize() first.
```

---

## Empty vs failure

A successful call with no data is **not** a failure:

```python
res = mt5.positions()

if res.success:
    if not res.data:
        print("No open positions")   # success, but empty list
    else:
        print(f"{len(res.data)} positions")
```

!!! tip
    `res.success` tells you whether the call worked. `res.data` tells you what came back.

---

## Chaining calls

```python
def get_position_symbols(mt5: MetaTrader5Client) -> list[str]:
    res = mt5.positions()
    if not res.success:
        return []
    return [p.symbol for p in res.data]
```

Keep the pattern consistent: check `success`, then use `data`.

---

## Real failure scenarios

### Scenario 1: Lifecycle violation

```python
from syntiq_mt5 import MetaTrader5Client

mt5 = MetaTrader5Client()
res = mt5.positions()  # ❌ Called before initialize()

print(f"Success: {res.success}")
print(f"Error code: {res.error_code}")
print(f"Message: {res.error_message}")
print(f"Operation: {res.operation}")
```

**Output:**
```text
Success: False
Error code: -10
Message: Client not initialized. Call initialize() first.
Operation: positions_get
```

**Why this fails:** The client enforces strict lifecycle ordering. You must call `initialize()` → `login()` before any trading operations.

**Fix:**
```python
with MetaTrader5Client() as mt5:
    mt5.initialize(creds)
    mt5.login(creds)
    res = mt5.positions()  # ✅ Now it works
```

---

### Scenario 2: Invalid symbol

```python
res = mt5.symbol_info("INVALID_SYMBOL")

if not res.success:
    print(f"Error: {res.error_message}")
    print(f"Code: {res.error_code}")
```

**Output:**
```text
Error: Symbol not found or not available
Code: 4301
```

**Why this fails:** The symbol doesn't exist in your broker's symbol list, or it's not enabled in Market Watch.

**Fix:**
```python
# First, check available symbols
symbols = mt5.symbols_get(group="*USD*")
if symbols.success:
    print([s.name for s in symbols.data])

# Or enable the symbol first
mt5.symbol_select("EURUSD", True)
```

---

### Scenario 3: Insufficient margin

```python
from syntiq_mt5 import TradeRequest, constants

request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=100.0,  # ❌ Way too large
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
)

check = mt5.order_check(request)
if not check.success:
    print(f"Validation failed: {check.error_message}")
elif not check.data.is_successful:
    print(f"Order rejected: {check.data.comment}")
    print(f"Retcode: {check.data.retcode}")
```

**Output:**
```text
Order rejected: Not enough money
Retcode: 10019
```

**Why this fails:** The account doesn't have enough margin to open a 100-lot position.

**Fix:**
```python
# Calculate required margin first
margin_res = mt5.order_calc_margin(
    constants.ORDER_TYPE_BUY,
    "EURUSD",
    100.0,
    1.08500,
)

if margin_res.success:
    print(f"Required margin: {margin_res.data}")
    
    # Check account balance
    acc = mt5.account_info()
    if acc.success:
        print(f"Available margin: {acc.data.margin_free}")
```

---

### Scenario 4: Market closed

```python
from datetime import datetime, timezone

# Trying to fetch ticks when market is closed
date_from = datetime(2024, 12, 25, tzinfo=timezone.utc)  # Christmas

res = mt5.copy_ticks_from(
    "EURUSD",
    date_from,
    count=100,
    flags=constants.COPY_TICKS_ALL,
)

if not res.success:
    print(f"Failed: {res.error_message}")
elif not res.data:
    print("No ticks available (market was closed)")
```

**Output:**
```text
No ticks available (market was closed)
```

**Why this happens:** The operation succeeded (`success=True`), but no data exists for that time period.

**Key distinction:** `success=True` with empty `data` means "the call worked, but there's nothing to return."

---

## Debugging with Result[T]

### Pattern 1: Log all failures

```python
def log_failure(res: Result) -> None:
    if not res.success:
        print(f"❌ {res.operation} failed")
        print(f"   Code: {res.error_code}")
        print(f"   Message: {res.error_message}")
        if res.context:
            print(f"   Context: {res.context}")

res = mt5.positions()
log_failure(res)
```

---

### Pattern 2: Retry with backoff

```python
import time
from syntiq_mt5 import Result

def retry_operation(func, max_attempts: int = 3) -> Result:
    for attempt in range(max_attempts):
        res = func()
        if res.success:
            return res
        
        print(f"Attempt {attempt + 1} failed: {res.error_message}")
        if attempt < max_attempts - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return res  # Return last failure

res = retry_operation(lambda: mt5.symbol_info("EURUSD"))
```

---

### Pattern 3: Collect all errors

```python
def fetch_multiple_symbols(mt5, symbols: list[str]) -> dict[str, Result]:
    results = {}
    for symbol in symbols:
        results[symbol] = mt5.symbol_info(symbol)
    return results

results = fetch_multiple_symbols(mt5, ["EURUSD", "GBPUSD", "INVALID"])

# Check which ones failed
for symbol, res in results.items():
    if not res.success:
        print(f"{symbol}: {res.error_message}")
```

**Output:**
```text
INVALID: Symbol not found or not available
```

---

### Pattern 4: Assert in tests

```python
def test_positions():
    mt5 = MetaTrader5Client()
    mt5.initialize(creds)
    mt5.login(creds)
    
    res = mt5.positions()
    
    assert res.success, f"positions() failed: {res.error_message}"
    assert isinstance(res.data, list)
```

---

## Error code reference

Common error codes you'll encounter:

| Code | Meaning | Typical cause |
|------|---------|---------------|
| `-10` | Client not initialized | Called method before `initialize()` |
| `-11` | Client not logged in | Called method before `login()` |
| `1` | Generic error | Check `error_message` for details |
| `4301` | Symbol not found | Invalid symbol or not in Market Watch |
| `10004` | Requote | Price changed, retry with new price |
| `10006` | Request rejected | Broker rejected the request |
| `10013` | Invalid request | Check request parameters |
| `10014` | Invalid volume | Volume outside min/max limits |
| `10015` | Invalid price | Price outside allowed range |
| `10016` | Invalid stops | SL/TP too close to market price |
| `10019` | Not enough money | Insufficient margin |

!!! tip "When to check error codes"
    Most of the time, `error_message` is enough. Check `error_code` when you need to handle specific failures differently (e.g., retry on requote, abort on insufficient margin).
