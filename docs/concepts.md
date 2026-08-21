# Design And Semantics

## Process-global ownership

The official extension has one terminal connection and one `last_error()` state
per process. `MT5` therefore allows one active session at a time. Multiple
accounts require separate processes, not multiple client objects.

## Return values

Successful operations return their value directly:

```python
positions: tuple[Position, ...] = mt5.positions()
account: AccountInfo = mt5.account_info()
```

An empty tuple is successful absence. It is not conflated with the `None` failure
sentinel used by the native query functions.

## Failures

| Exception | Meaning |
| --- | --- |
| `MT5StateError` | The session is inactive or another session owns MT5 |
| `MT5PlatformError` | The official native package is unavailable |
| `MT5CallError` | MT5 returned the documented failure sentinel |
| `MT5PayloadError` | MT5 returned data that cannot satisfy its model |

All inherit from `MT5Error` and carry `operation`, `code`, and `message`.

The adapter invokes a native operation and reads `last_error()` while holding the
same lock. No wrapper call can overwrite the error between those steps.

## Broker decisions

Transport success is not broker acceptance. A valid `order_send()` response can
contain a rejection, requote, placement, completion, or partial fill. The
response is returned as a `TradeResult`; inspect `retcode` and `is_successful`.

`order_check()` has a different native response shape and returns
`TradeCheckResult`, including projected balance, equity, margin, and free margin.

## Time

- Input datetimes must be timezone-aware.
- Inputs are normalized to UTC.
- Rate ranges use the official inclusive endpoints.
- `copy_rates_from()` selects bars at or before its timestamp, moving into history.
- Recent `candles()` exclude native bar position `0` by default because it is
  still forming. Pass `include_current=True` only when that is intentional.

## Threading

Native calls are serialized for error integrity. This does not make the terminal
an independently scalable concurrent backend. Run separate terminals in separate
processes when isolation is required.
