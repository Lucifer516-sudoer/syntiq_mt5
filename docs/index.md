# MetaTrader5 Wrapper

Typed, Pythonic access to the official `MetaTrader5` Python package.

`metatrader5_wrapper` keeps the underlying MT5 behavior visible while making
results safer and easier to use in application code. Raw terminal calls are
wrapped in typed result models so you can handle success and failure without
depending on mutable global error state, and the client adds a fail-fast path
for the common happy flow.

## Why use it

- typed public API for editors and static type checkers
- Pydantic models for validated inputs and structured outputs
- MT5 error details captured immediately after each operation
- both explicit result-style and fail-fast helper-style workflows
- both function-style and client-style interfaces

## Installation

```bash
pip install metatrader5-wrapper
```

## Quick example

```python
from pydantic import SecretStr

from metatrader5_wrapper import LoginCredential, MetaTrader5Client

credentials = LoginCredential(
    login=12345678,
    password=SecretStr("password"),
    server="Broker-Demo",
    timeout=60,
)

with MetaTrader5Client(credentials) as mt5:
    account = mt5.account()
    positions = mt5.positions(symbol="EURUSD")

    print(account.balance)
    print(len(positions))
```

If you want to keep branching explicit, the result models stay available:

```python
from metatrader5_wrapper import initialize

result = initialize()

if result.failed:
    print(result.describe_error())
```

## Documentation map

- Start with [Getting Started](getting-started.md)
- Read [Connection](guides/connection.md) for terminal lifecycle behavior
- Read [Results Model](guides/results.md) for `ConnectionResult` and `OperationResult`
- Read [Client vs Functions](guides/client-vs-functions.md) to choose your style
- Use [API Reference](api/index.md) for generated signatures and docstrings

## Current API surface

- connection: `initialize`, `login`, `shutdown`
- terminal: `terminal_info`, `version`
- account: `account_info`
- symbols: `symbols_total`, `symbols_get`, `symbol_info`, `symbol_info_tick`, `symbol_select`
- positions: `positions_total`, `positions_get`
- client facade: `MetaTrader5Client`