# Your first Syntiq session

Go from an installed package to a typed account snapshot and completed candles.
The example is read-only and safe to try with a demo account.

<div class="syntiq-page-note">
<strong>Before you begin</strong>
<span>Python 3.12+, Windows, MetaTrader 5, and a broker demo account.</span>
</div>

## 1. Install

=== "pip"

    ```bash
    pip install syntiq-mt5
    ```

=== "uv"

    ```bash
    uv add syntiq-mt5
    ```

The models and fake-adapter tests work on every platform. Native terminal access
is Windows-only because that is a constraint of the official MetaTrader5 package.

## 2. Keep credentials outside your code

Set credentials in your shell or secret manager:

=== "PowerShell"

    ```powershell
    $env:MT5_LOGIN = "12345678"
    $env:MT5_PASSWORD = "demo-password"
    $env:MT5_SERVER = "Broker-Demo"
    ```

=== "Command Prompt"

    ```batch
    set MT5_LOGIN=12345678
    set MT5_PASSWORD=demo-password
    set MT5_SERVER=Broker-Demo
    ```

`LoginCredential` stores the password as Pydantic `SecretStr`, so normal
representation and logging do not reveal it.

## 3. Open one managed session

```python title="account_snapshot.py" linenums="1"
import os

from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, SyntiqMT5

credentials = LoginCredential(
    login=int(os.environ["MT5_LOGIN"]),
    password=SecretStr(os.environ["MT5_PASSWORD"]),
    server=os.environ["MT5_SERVER"],
    # path=r"C:\Program Files\MetaTrader 5\terminal64.exe",
)

with SyntiqMT5(credentials) as mt5:
    account = mt5.account_info()
    print(account.login, account.balance, account.currency)
```

The context manager acquires exclusive process ownership, initializes and
authenticates in one native call, then guarantees `shutdown()` on exit.

!!! info "Why only one session?"
    The official extension stores connection and error state globally. Syntiq
    makes this explicit instead of allowing two client objects to silently
    replace each other's terminal state.

## 4. Read typed market data

```python title="read_market.py"
from syntiq_mt5 import SyntiqMT5, constants

with SyntiqMT5(credentials) as mt5:
    positions = mt5.positions()
    candles = mt5.candles(
        "EURUSD",
        constants.TIMEFRAME_H1,
        count=100,
    )

    for position in positions:
        print(position.symbol, position.volume, position.pips_profit)

    if candles:
        print("Latest completed close:", candles[-1].close)
```

Collections are immutable tuples. `()` means the call succeeded and matched no
records. Recent candles exclude the still-forming bar by default.

## 5. Handle technical failure once

```python title="errors.py"
from syntiq_mt5 import MT5Error, SyntiqMT5

try:
    with SyntiqMT5(credentials) as mt5:
        mt5.symbol_info("NOT-A-SYMBOL")
except MT5Error as error:
    print(f"{error.operation} [{error.code}]: {error.message}")
```

Connection errors come from the native `last_error()` state. Broker decisions
come from `TradeCheckResult.retcode` or `TradeResult.retcode`; they are separate
concepts and should lead to different recovery behavior.

## 6. Use UTC deliberately

```python title="ticks.py"
from datetime import UTC, datetime, timedelta

from syntiq_mt5 import SyntiqMT5, constants

end = datetime.now(UTC)

with SyntiqMT5(credentials) as mt5:
    ticks = mt5.copy_ticks_range(
        "EURUSD",
        end - timedelta(minutes=5),
        end,
        constants.COPY_TICKS_ALL,
    )
```

Naive datetimes are rejected before the adapter call, removing local-time and
daylight-saving ambiguity from market-data queries.

<div class="syntiq-next" markdown>

**You now have the core mental model.**

[Understand the architecture](concepts.md){ .md-button }
[Read market data](market-data.md){ .md-button .md-button--primary }

</div>
