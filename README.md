# syntiq-mt5

**MT5 trading API, fixed for Python developers.**

> No global-state guesswork. No ambiguous returns.

`syntiq-mt5` gives you a typed client, operation-scoped errors, and predictable results—so every call tells you exactly what happened.

## Prerequisites

- **MetaTrader 5 terminal** must be installed
- **Windows only** (MT5 Python API limitation)
- Valid MT5 account credentials

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
    init_res = mt5.initialize(creds)
    if not init_res.success:
        print(f"Initialize failed: {init_res.error_message}")
        exit(1)
    
    login_res = mt5.login(creds)
    if not login_res.success:
        print(f"Login failed: {login_res.error_message}")
        exit(1)
    
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

## Using Constants

All MT5 constants are available through the SDK—no need to import `MetaTrader5` directly:

```python
from syntiq_mt5 import constants

# Timeframes
res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=50)

# Order types
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.1,
    type=constants.ORDER_TYPE_BUY,
    price=1.1000
)

# Tick flags
ticks = mt5.get_ticks("EURUSD", flags=constants.COPY_TICKS_ALL, count=100)
```

See the [Constants Reference](https://syntiq-mt5.readthedocs.io/reference/constants/) for the complete list.

## Result[T] pattern

```python
from syntiq_mt5 import constants

res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=50)
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

### Core
- `MetaTrader5Client` - Main client for all MT5 operations
- `LoginCredential` - Authentication credentials
- `Result[T]` - Generic result wrapper with success/error handling

### Account & Terminal
- `AccountInfo` - Account balance, equity, margin, leverage
- `TerminalInfo` - Terminal version, build, connection status

### Market Data
- `Candle` - OHLC price data
- `Tick` - Tick-level price updates
- `SymbolInfo` - Symbol specifications and trading parameters
- `SymbolTick` - Current symbol tick data

### Trading
- `Position` - Open position with P&L calculations
- `Order` - Pending order
- `HistoricalOrder` - Historical order record
- `Deal` - Completed transaction
- `TradeRequest` - Order request parameters
- `TradeResult` - Order execution result

### Market Depth
- `BookEntry` - Level 2 order book entry
