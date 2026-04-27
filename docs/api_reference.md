# API Reference

---
## Next Steps
[Getting Started](getting-started.md)

`metatrader5_wrapper` is a typed facade over the official `MetaTrader5` Python
package. Public functions call MetaTrader 5, immediately capture
`MetaTrader5.last_error()`, and return Pydantic result models instead of relying
on global MT5 error state.

## Design

The package is split into three layers:

- `metatrader5_wrapper._core`: thin raw MT5 calls that capture `last_error()`
- domain services such as `connection.service` and `symbols.service`: convert
  raw MT5 payloads into typed result objects
- public exports in `metatrader5_wrapper.__init__`: replacement-style functions,
  models, constants, and `MetaTrader5Client`

The `_core` modules are internal. Prefer importing from `metatrader5_wrapper` or
from the domain packages.

## Logging

The package uses Python's standard `logging` module with the logger name
`metatrader5_wrapper`.

The wrapper does not configure logging, add handlers, or change global logging
settings. Applications can opt in with normal logging configuration:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

Service functions log:

- `DEBUG` before calling MT5
- `INFO` when an operation succeeds
- `WARNING` when MT5 reports a failed operation

Credentials are not logged. Account login numbers, symbol names, filters, MT5
error codes, and MT5 error messages may be logged.

## Results

### OperationResult[T]

Generic result returned by account, terminal, symbol, and position operations.

Fields:

- `success`: `True` when the operation succeeded
- `data`: typed payload, or `None` on failure
- `error_code`: raw MT5 error code captured after the call
- `error_message`: raw MT5 error message captured after the call
- `message`: wrapper-level human-readable message
- `failed`: property returning `not success`

### ConnectionResult

Result returned by `initialize()` and `login()`.

Fields:

- `success`
- `error_code`
- `error_message`
- `stage`: `ConnectionStage.INITIALIZE` or `ConnectionStage.LOGIN`
- `message`
- `failed`: property returning `not success`

## Connection

### LoginCredential

Typed connection input.

Fields:

- `terminal_path`: optional path to a terminal executable
- `login`: MT5 account number
- `password`: `pydantic.SecretStr`
- `server`: MT5 trade server name
- `timeout`: connection timeout in seconds, default `60`
- `portable`: whether MT5 should run in portable mode
- `timeout_ms`: property used internally by the MT5 API

### initialize(credentials=None)

Initializes the MT5 terminal. When credentials are provided, it initializes the
terminal first and then logs in to the account.

Returns `ConnectionResult`.

### login(credentials)

Logs in to an account after the terminal has already been initialized.

Returns `ConnectionResult`.

### shutdown()

Disconnects from the MT5 terminal.

Returns `OperationResult[None]`.

## Terminal

### terminal_info()

Returns terminal details as `OperationResult[TerminalInfo]`.

`TerminalInfo` contains fields such as connection status, trading permissions,
build number, path values, company, language, and terminal name.

### version()

Returns terminal version details as `OperationResult[TerminalVersion]`.

`TerminalVersion` fields:

- `version`
- `build`
- `release_date`

## Account

### account_info()

Returns active account details as `OperationResult[AccountInfo]`.

`AccountInfo` contains account identity, leverage, trade permissions, margin
mode, balances, margin values, currency, server, and broker company.

## Symbols

### symbols_total()

Returns the number of symbols available in the terminal as
`OperationResult[int]`.

### symbols_get(group=None)

Returns available symbols as `OperationResult[list[SymbolInfo]]`.

`group` is passed through to the official MT5 `symbols_get(group=...)` filter.

### symbol_info(symbol)

Returns one symbol as `OperationResult[SymbolInfo]`.

`SymbolInfo` includes common instrument metadata such as `name`, `description`,
`path`, currencies, digits, spread, visibility, trading modes, volume limits,
point size, and latest quoted prices when MT5 provides them.

### symbol_info_tick(symbol)

Returns the latest tick as `OperationResult[Tick]`.

`Tick` fields:

- `time`
- `bid`
- `ask`
- `last`
- `volume`
- `time_msc`
- `flags`
- `volume_real`

### symbol_select(symbol, enable=True)

Adds or removes a symbol from MarketWatch.

Returns `OperationResult[None]`.

## Positions

### positions_total()

Returns the number of open positions as `OperationResult[int]`.

### positions_get(symbol=None, group=None, ticket=None)

Returns open positions as `OperationResult[list[Position]]`.

Only one MT5 filter is used at a time, matching the current implementation
order:

- `symbol`
- `group`
- `ticket`
- no filter

`Position` includes ticket, open/update times, order type, magic number,
identifier, reason, volume, prices, swap, profit, symbol, comment, and optional
external ID.

## Client Facade

`MetaTrader5Client` groups the same public operations behind an object-oriented
interface.

```python
from metatrader5_wrapper import MetaTrader5Client

with MetaTrader5Client(credentials) as mt5:
    account = mt5.account_info()
    symbols = mt5.symbols_get(group="*USD*")
```

The context manager calls `initialize()` on entry and `shutdown()` on exit. If
initialization fails, it raises `RuntimeError` with the connection result
message and MT5 error details.

## MT5 Constants

Uppercase attributes not defined by the wrapper are forwarded to the official
`MetaTrader5` module. This allows existing code to access constants such as
order, position, and timeframe values while typed wrappers are added over time.

```python
import metatrader5_wrapper as mt5

timeframe = mt5.TIMEFRAME_M1
```

## Development Commands

```bash
uv sync --all-groups
uv run pytest
uv run ruff check src tests
uv run ruff format src tests
uv run mypy src
```
