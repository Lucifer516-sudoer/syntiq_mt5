# Quickstart

## Install

```bash
pip install syntiq-mt5
```

You need Python 3.12+, Windows, an installed MT5 terminal, and a broker account.
A demo account is strongly recommended.

## Connect

Keep credentials outside source control:

```python
import os

from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MT5

credentials = LoginCredential(
    login=int(os.environ["MT5_LOGIN"]),
    password=SecretStr(os.environ["MT5_PASSWORD"]),
    server=os.environ["MT5_SERVER"],
    # path=r"C:\Program Files\MetaTrader 5\terminal64.exe",  # optional
)

with MT5(credentials) as mt5:
    account = mt5.account_info()
    print(account.login, account.balance, account.currency)
```

Entering the context acquires process ownership and calls the official
`initialize()` with the supplied credentials. Exiting always calls `shutdown()`.

## Read data

```python
from syntiq_mt5 import constants

with MT5(credentials) as mt5:
    positions = mt5.positions()
    candles = mt5.candles("EURUSD", constants.TIMEFRAME_H1, count=100)

    for position in positions:
        print(position.symbol, position.volume, position.pips_profit)
```

Collections are immutable tuples. `()` means the call succeeded but no records
matched. Native `None` is treated as failure and raises `MT5CallError`.

## Handle failures

```python
from syntiq_mt5 import MT5Error

try:
    with MT5(credentials) as mt5:
        mt5.symbol_info("NOT-A-SYMBOL")
except MT5Error as error:
    print(f"{error.operation} [{error.code}]: {error.message}")
```

Do not compare connection errors with `TRADE_RETCODE_*`. Connection errors come
from `last_error()`; broker decisions come from the `retcode` in a valid check or
send response.

## Use UTC

```python
from datetime import UTC, datetime, timedelta

end = datetime.now(UTC)
with MT5(credentials) as mt5:
    ticks = mt5.copy_ticks_range(
        "EURUSD",
        end - timedelta(minutes=5),
        end,
        constants.COPY_TICKS_ALL,
    )
```

Naive datetimes are rejected before the native call.
