# Getting Started

## Install

```bash
pip install metatrader5-wrapper
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