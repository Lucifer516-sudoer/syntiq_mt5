# syntiq-mt5

A typed, testable Python interface for MetaTrader 5.

[Documentation](https://lucifer516-sudoer.github.io/syntiq_mt5/) | [Changelog](CHANGELOG.md) | [Contributing](CONTRIBUTING.md)

> Project status: alpha. Validate every trading workflow against a demo account before using it with live funds.

## Why it exists

The native `MetaTrader5` package exposes a process-global terminal connection,
global error state, loosely typed records, and operation-specific failure
sentinels. `syntiq-mt5` puts those details behind one managed session:

- direct typed return values, not `Result.data | None`;
- typed exceptions with the operation, MT5 code, and message;
- a lazy, serialized adapter around the global native extension;
- immutable tuple snapshots where an empty tuple is a valid result;
- UTC-aware date validation;
- separate `TradeCheckResult` and `TradeResult` models;
- deterministic market-book and terminal cleanup;
- an injectable adapter seam for tests on Linux, macOS, and CI.

## Requirements

- Python 3.12+
- Windows for native terminal access
- MetaTrader 5 terminal and the official `MetaTrader5` Python package

Models and fake-adapter tests work on any platform. Only native terminal access
is Windows-specific.

## Install

```bash
pip install syntiq-mt5
```

## Quickstart

```python
import os

from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MT5

credentials = LoginCredential(
    login=int(os.environ["MT5_LOGIN"]),
    password=SecretStr(os.environ["MT5_PASSWORD"]),
    server=os.environ["MT5_SERVER"],
)

with MT5(credentials) as mt5:
    account = mt5.account_info()
    positions = mt5.positions()
    print(account.login, account.balance, len(positions))
```

The context manager initializes and authenticates in one native call and always
shuts down. A second active session in the same process is rejected because the
underlying extension is process-global.

## Errors

```python
from syntiq_mt5 import MT5, MT5Error

try:
    with MT5() as mt5:
        quote = mt5.symbol_info_tick("UNKNOWN")
except MT5Error as error:
    print(error.operation, error.code, error.message)
```

Transport and payload failures raise. A valid broker rejection does not:
`order_check()` and `order_send()` return their response models so you can
inspect `retcode`, `comment`, and acceptance status.

## Safe candles

```python
from syntiq_mt5 import MT5, constants

with MT5() as mt5:
    # Position 0 is the still-forming bar, so it is excluded by default.
    candles = mt5.candles("EURUSD", constants.TIMEFRAME_H1, count=100)
```

## Development

```bash
uv sync --locked --all-groups
uv run ruff format src tests examples
uv run ruff check src tests examples
uv run mypy src
uv run pytest
uv run mkdocs build --strict
uv build
```

CI runs these checks on Linux and Windows with Python 3.12 and 3.13. Tagged
releases are built, verified, and published through PyPI trusted publishing.

## License

MIT. See [LICENSE](LICENSE).
