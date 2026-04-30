# syntiq-mt5

**MT5 trading API, fixed for Python developers.**

> No global-state guesswork. No ambiguous returns.

`syntiq-mt5` gives you a typed client, operation-scoped errors, and predictable results—so every call tells you exactly what happened.

## Install

```bash
pip install syntiq-mt5
```

## 10-second quickstart

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as mt5:
    mt5.initialize(creds)
    mt5.login(creds)
    res = mt5.positions()

if res.success and res.data:
    p = res.data[0]
    print(f"{p.symbol} | volume={p.volume} | profit={p.pips_profit:.1f} pips")
else:
    print(f"{res.operation} failed: {res.error_code} {res.error_message}")
```

You get one dependable pattern: data when it works, precise context when it doesn’t.

## Why this SDK exists

MT5’s default Python interface is painful in production:
- `last_error()` is global mutable state
- return types change across calls
- lifecycle mistakes are easy to ship

`syntiq-mt5` makes the safe path the obvious path:
- one client flow (`initialize -> login -> call -> shutdown`)
- one result contract (`Result[T]`) everywhere
- typed models with practical metrics (like pip-based profit)

## Result[T] pattern

```python
res = mt5.get_candles("EURUSD", timeframe=1, count=50)
if res.success:
    print(f"candles={len(res.data)}")
else:
    print(res.operation, res.error_code, res.error_message)
```

Example output:

```text
EURUSD | volume=0.10 | profit=+10.0 pips
candles=50
```

## Public API

- `MetaTrader5Client`
- `LoginCredential`
- `Result`
- `Position`
- `Candle`
