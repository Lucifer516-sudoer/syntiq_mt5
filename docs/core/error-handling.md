# Error Handling

`syntiq-mt5` never raises exceptions for operational failures. All errors are returned as `Result` values.

---

## How MT5 errors work

The raw `MetaTrader5` library has a critical design flaw: it stores the last error in **global mutable state**.

### The problem with `last_error()`

```python
import MetaTrader5 as mt5

# Call 1: fails
mt5.symbol_info("INVALID")

# Call 2: succeeds
mt5.symbol_info("EURUSD")

# Now check the error
error = mt5.last_error()
print(error)  # (1, 'Success') ❌ The real error is gone!
```

**What went wrong:**
1. First call fails → MT5 stores error code `4301` ("Symbol not found")
2. Second call succeeds → MT5 **overwrites** the error with `(1, 'Success')`
3. When you check `last_error()`, you get the wrong result

### Why this is dangerous

```python
# ❌ WRONG: Error is lost
res1 = mt5.symbol_info("INVALID")  # Fails
res2 = mt5.symbol_info("EURUSD")   # Succeeds
error = mt5.last_error()           # Returns success!

# ❌ WRONG: Race condition in concurrent code
res = mt5.positions()
# Another thread calls mt5.account_info() here
error = mt5.last_error()  # Wrong error!

# ❌ WRONG: Forgot to check immediately
res = mt5.positions()
do_some_processing()
error = mt5.last_error()  # Might be overwritten
```

### How syntiq-mt5 solves this

`syntiq-mt5` captures `last_error()` **immediately** after every operation and attaches it to the returned `Result`. The error is bound to the operation that produced it.

```python
from syntiq_mt5 import MetaTrader5Client

mt5 = MetaTrader5Client()

# Each Result carries its own error
res1 = mt5.symbol_info("INVALID")   # res1.error_code = 4301
res2 = mt5.symbol_info("EURUSD")    # res2.error_code = None

# Errors are preserved
print(res1.error_code)     # 4301 ✅
print(res1.error_message)  # "Symbol not found" ✅
print(res2.success)        # True ✅
```

**Benefits:**
- ✅ No race conditions
- ✅ No lost errors
- ✅ No manual `last_error()` calls
- ✅ Errors are immutable and bound to their operation
- ✅ Safe in concurrent code (each Result is independent)

!!! success "You never need to call `last_error()` yourself"
    The SDK handles it automatically. Every `Result` contains the error that occurred during that specific operation.

---

## Reading errors

```python
res = mt5.login(creds)

if not res.success:
    print(f"operation:  {res.operation}")   # "login"
    print(f"context:    {res.context}")     # MT5 API function name
    print(f"error code: {res.error_code}")  # e.g. 10013
    print(f"message:    {res.error_message}")
```

```text
operation:  login
context:    login
error code: 10013
message:    Invalid account
```

---

## SDK-internal errors

Some errors originate inside the SDK, not from MT5. These use negative error codes:

!!! warning "SDK error codes"
    | Code | Meaning |
    |---|---|
    | `-10` | `initialize()` was not called before this operation |

```python
mt5 = MetaTrader5Client()
res = mt5.positions()

# res.success == False
# res.error_code == -10
# res.error_message == "Client not initialized. Call initialize() first."
```

---

## Handling specific errors

```python
from syntiq_mt5 import constants

res = mt5.order_send(request)

if not res.success:
    # SDK-level failure (connection, not initialized, etc.)
    print(f"SDK error {res.error_code}: {res.error_message}")
elif not res.data.is_successful:
    # Broker rejected the order
    retcode = res.data.retcode
    if retcode == constants.TRADE_RETCODE_NO_MONEY:
        print("Insufficient funds")
    elif retcode == constants.TRADE_RETCODE_MARKET_CLOSED:
        print("Market is closed")
    elif retcode == constants.TRADE_RETCODE_REQUOTE:
        print(f"Requote — new price: {res.data.ask}")
    else:
        print(f"Order rejected: {res.data.comment} (retcode {retcode})")
else:
    print(f"Order filled: deal={res.data.deal}, order={res.data.order}")
```

---

## Two-level check for trade operations

`order_send()` and `order_check()` have two layers of success:

!!! info "Two-level validation"
    1. **`res.success`** — did the SDK call succeed (connection, parsing, etc.)?
    2. **`res.data.is_successful`** — did the broker accept the trade?

```python
res = mt5.order_send(request)

if res.success and res.data.is_successful:
    print("Trade accepted")
elif res.success and not res.data.is_successful:
    print(f"Trade rejected by broker: {res.data.comment}")
else:
    print(f"SDK error: {res.error_message}")
```

---

## Exception classes

Exceptions are reserved for unrecoverable situations that cannot return a `Result` (e.g. during object construction). You will not encounter these in normal usage.

| Exception | When raised |
|---|---|
| `MT5Error` | Base class for all SDK exceptions |
| `MT5ConnectionError` | Unrecoverable connection lifecycle failure |
| `MT5ExecutionError` | Unrecoverable data retrieval or trade execution failure |
