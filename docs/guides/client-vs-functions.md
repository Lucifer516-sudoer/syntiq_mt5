# Client vs Functions

The package supports two public styles.

## Start with the client

Use `MetaTrader5Client` first unless you have a reason not to. It gives you a
clean lifecycle boundary and the shortest happy-path code.

```python
from metatrader5_wrapper import MetaTrader5Client

with MetaTrader5Client(credentials) as mt5:
    account = mt5.account()
    positions = mt5.positions(symbol="EURUSD")
```

This style is usually best for application code, services, bots, notebooks,
and scripts that should read cleanly from top to bottom.

## Function-style API

Use module-level functions if you want a minimal wrapper over the MT5 API shape.

```python
from metatrader5_wrapper import account_info, initialize, shutdown

initialize()
account = account_info()
shutdown()
```

This style is useful when migrating existing procedural MT5 code.

## Which one should you document first

Lead with `MetaTrader5Client` in tutorials and examples because it gives users
the cleanest mental model. Keep function-style examples in the API reference
and migration-oriented sections.