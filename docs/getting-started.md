# Getting Started

---
## Next Steps
[API Reference](api/index.md)


## New Features

The wrapper now includes support for historical orders and deals.

## Install

```bash
pip install metatrader5-wrapper
```

## Build the docs

The documentation site currently targets the MkDocs 1.x ecosystem.
Material for MkDocs and the plugins used by this project are not compatible
with MkDocs 2.0, so keep the docs toolchain on `mkdocs<2`.

```bash
uv sync --all-groups
uv run mkdocs build
```

## Recommended path: use the client

For most scripts, services, and bots, start with `MetaTrader5Client`. It keeps
connection lifecycle scoped and makes the happy path short.

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
    terminal = mt5.terminal()

    print(account.login, account.balance)
    print(terminal.name, terminal.connected)
    history_orders = mt5.history_orders_get(datetime(2021, 1, 1), datetime(2021, 1, 10))
    history_deals = mt5.history_deals_get(datetime(2021, 1, 1), datetime(2021, 1, 10))
```

## Explicit result flow

If an existing MetaTrader 5 session is already available, you can initialize
without explicit credentials.

```python
from metatrader5_wrapper import initialize, shutdown

result = initialize()

result.expect("Could not initialize MetaTrader 5")

shutdown()
```

## Initialize with credentials

```python
from pydantic import SecretStr

from metatrader5_wrapper import LoginCredential, initialize

credentials = LoginCredential(
    login=12345678,
    password=SecretStr("password"),
    server="Broker-Demo",
    timeout=60,
)

result = initialize(credentials)

if result.failed:
    print(result.describe_error())
```

## Fail-fast convenience helpers

```python
from metatrader5_wrapper import MetaTrader5Client

with MetaTrader5Client(credentials) as mt5:
    account = mt5.account()
    eurusd = mt5.symbol("EURUSD")
    tick = mt5.tick("EURUSD")

    print(account.balance)
    print(eurusd.name, tick.bid, tick.ask)
```

## What to read next

- [Connection](guides/connection.md)
- [Client vs Functions](guides/client-vs-functions.md)
- [API Reference](api/index.md)