# MetaTrader5 Wrapper
[![Deploy Documentation](https://github.com/Lucifer516-sudoer/metatrader5_wrapper/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/Lucifer516-sudoer/metatrader5_wrapper/actions/workflows/deploy-docs.yml)

**Typed, Pythonic access to the MetaTrader 5 API.** Keep MT5's power, drop the awkward parts.

## Why

The official `MetaTrader5` package is powerful but fragile:

- errors hide in `last_error()` and vanish on the next call
- results are untyped, hard to autocomplete
- no Pydantic validation

This wrapper captures errors immediately, returns typed Pydantic models, and gives you both explicit result objects and fail-fast helpers for application code.

## Install

```bash
pip install metatrader5-wrapper
```

## 30-second example

```python
from pydantic import SecretStr
from metatrader5_wrapper import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("password"),
    server="Broker-Demo",
)

with MetaTrader5Client(creds) as mt5:
    account = mt5.account()
    eurusd = mt5.symbol("EURUSD")
    tick = mt5.tick("EURUSD")

    print(account.balance)
    print(eurusd.description)
    print(tick.bid, tick.ask)
```

Prefer explicit results when you want to branch on failures:

```python
from metatrader5_wrapper import initialize

**Typed, Pythonic access to the MetaTrader 5 API.** Keep MT5's power, drop the awkward parts.



result = initialize()
if result.failed:
    print(result.describe_error())
```


## Key features



- **Typed everywhere**: Pydantic models for every input and output
- **Explicit errors**: No `last_error()` surprises; errors are captured and carried with each result
- **Fast path or explicit path**: Use `.expect()` and `.unwrap()` when you want fail-fast code, or inspect `.success` when you want branchy workflows
- **Two styles**: Use functions or `MetaTrader5Client` depending on your code
- **Full MT5 coverage**: Connection, account, symbols, ticks, positions, terminal info
- **Production ready**: Used in live trading

## Design philosophy

- Keep the MT5 mental model visible instead of hiding it behind a large abstraction.
- Make the happy path short enough for scripts and notebooks.
- Keep failure information structured enough for services and trading systems.
- Prefer one obvious way to start: `MetaTrader5Client` for most application code.

## Current API

- **Connection**: `initialize`, `login`, `shutdown`
- **Account**: `account_info`
- **Terminal**: `terminal_info`, `version`
- **Symbols**: `symbols_get`, `symbol_info`, `symbol_info_tick`, `symbol_select`
- **Positions**: `positions_get`, `positions_total`

Common client shortcuts:

- `connect()` to initialize and fail fast
- `account()`, `terminal()`, `symbol()`, `tick()`, `positions()`, `symbols()` to return typed payloads directly

## Documentation

Full docs, tutorials, and API reference: [https://haris.github.io/metatrader5_wrapper](https://haris.github.io/metatrader5_wrapper)

## Development

```bash
uv sync --all-groups
uv run pytest
uv run ruff check src tests
uv run mypy src
```

## License

MIT
