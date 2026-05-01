# 🚀 Quickstart

Get from install to live data in under 60 seconds.

---

## Prerequisites

!!! info "What you need"
    - **Windows** — the MT5 Python API is Windows-only
    - **MetaTrader 5 terminal** installed ([download](https://www.metatrader5.com/en/download))
    - A valid MT5 account (demo accounts work fine)
    - **Python 3.12+**

---

## Install

```bash
pip install syntiq-mt5
```

---

## Minimal working example

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,                        # your MT5 account number
    password=SecretStr("your-password"),   # stored as a secret — never logged
    server="Broker-Demo",                  # broker server name from MT5 terminal
)

with MetaTrader5Client() as mt5:
    # 1. Connect to the terminal
    init = mt5.initialize(creds)
    if not init.success:
        print(f"Initialize failed: {init.error_message}")
        raise SystemExit(1)

    # 2. Authenticate with the broker
    login = mt5.login(creds)
    if not login.success:
        print(f"Login failed: {login.error_message}")
        raise SystemExit(1)

    # 3. Fetch open positions
    res = mt5.positions()
    if res.success:
        print(f"Open positions: {len(res.data)}")
        for p in res.data:
            print(f"  {p.symbol}  {p.volume} lots  {p.pips_profit:+.1f} pips")
    else:
        print(f"Error {res.error_code}: {res.error_message}")

# mt5.shutdown() is called automatically when the `with` block exits
```

```text title="Output"
Open positions: 2
  EURUSD  0.10 lots  +12.3 pips
  GBPUSD  0.05 lots  -4.7 pips
```

---

## Full lifecycle example

This example shows the complete flow: initialize → login → fetch data → shutdown.

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client, constants

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),
    server="Broker-Demo",
)

with MetaTrader5Client(debug=True) as mt5:
    # Initialize
    init = mt5.initialize(creds)
    if not init.success:
        print(f"❌ Initialize failed: {init.error_message}")
        raise SystemExit(1)
    print("✅ Connected to terminal")

    # Login
    login = mt5.login(creds)
    if not login.success:
        print(f"❌ Login failed: {login.error_message}")
        raise SystemExit(1)
    print("✅ Authenticated with broker")

    # Get account info
    acc = mt5.account_info()
    if acc.success:
        print(f"📊 Account: {acc.data.login} | Balance: {acc.data.balance} {acc.data.currency}")

    # Get positions
    pos = mt5.positions()
    if pos.success:
        print(f"📈 Open positions: {len(pos.data)}")
        for p in pos.data:
            direction = "LONG" if p.is_buy else "SHORT"
            print(f"   {p.symbol} {direction} {p.volume} lots @ {p.price_open} | P&L: {p.pips_profit:+.1f} pips")

    # Get recent candles
    candles = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=5)
    if candles.success:
        print(f"📊 Last 5 H1 candles for EURUSD:")
        for c in candles.data:
            print(f"   O={c.open} H={c.high} L={c.low} C={c.close}")

print("✅ Shutdown complete")
```

```text title="Output"
[MT5] initialize | success | code=0 | 142ms
✅ Connected to terminal
[MT5] login | success | code=0 | 87ms
✅ Authenticated with broker
[MT5] account_info | success | code=0 | 5ms
📊 Account: 12345678 | Balance: 10000.0 USD
[MT5] positions_get | success | code=0 | 12ms
📈 Open positions: 2
   EURUSD LONG 0.1 lots @ 1.08450 | P&L: +12.3 pips
   GBPUSD SHORT 0.05 lots @ 1.26800 | P&L: -4.7 pips
[MT5] copy_rates_from_pos | success | code=0 | 8ms
📊 Last 5 H1 candles for EURUSD:
   O=1.08320 H=1.08450 L=1.08290 C=1.08410
   O=1.08410 H=1.08520 L=1.08380 C=1.08490
   O=1.08490 H=1.08550 L=1.08470 C=1.08530
   O=1.08530 H=1.08600 L=1.08510 C=1.08580
   O=1.08580 H=1.08620 L=1.08560 C=1.08600
✅ Shutdown complete
```

---

## Error handling example

Every operation can fail. Always check `result.success`.

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("wrong-password"),  # Intentionally wrong
    server="Broker-Demo",
)

with MetaTrader5Client() as mt5:
    init = mt5.initialize(creds)
    if not init.success:
        print(f"❌ Initialize failed")
        print(f"   Operation: {init.operation}")
        print(f"   Error code: {init.error_code}")
        print(f"   Message: {init.error_message}")
        raise SystemExit(1)

    login = mt5.login(creds)
    if not login.success:
        print(f"❌ Login failed")
        print(f"   Operation: {login.operation}")
        print(f"   Error code: {login.error_code}")
        print(f"   Message: {login.error_message}")
        raise SystemExit(1)
```

```text title="Output (failure case)"
❌ Login failed
   Operation: login
   Error code: 10013
   Message: Invalid account
```

!!! warning "Common failure scenarios"
    - **Error -10**: `initialize()` was not called first
    - **Error 10013**: Invalid account number or password
    - **Error 10014**: Wrong server name
    - **Terminal not running**: `initialize()` fails silently — always check `result.success`

---

## What just happened?

=== "Step 1: Initialize"
    ```python
    init = mt5.initialize(creds)
    ```
    Connects to the MT5 terminal process on your machine. The terminal must already be running.

=== "Step 2: Login"
    ```python
    login = mt5.login(creds)
    ```
    Authenticates with the broker server using your account number, password, and server name.

=== "Step 3: Use"
    ```python
    res = mt5.positions()
    ```
    All data and trading operations are available after a successful login.

=== "Step 4: Shutdown"
    ```python
    # Automatic when `with` block exits
    ```
    Disconnects from the terminal. Called automatically — even if an exception occurs.

!!! tip "Result\[T\] pattern"
    Every method returns `Result[T]`. Check `result.success` before accessing `result.data`.

---

## Next steps

<div class="grid cards" markdown>

-   :material-timeline-clock: __[Lifecycle](core/lifecycle.md)__

    ---

    Common mistakes and the full connection flow

-   :material-check-decagram: __[Result\[T\]](core/results.md)__

    ---

    How to handle success and failure

-   :material-candlestick: __[Get Candles](tasks/get-candles.md)__

    ---

    Fetch OHLCV price data

-   :material-cash-multiple: __[Place Orders](tasks/place-orders.md)__

    ---

    Validate and send trade requests

</div>
