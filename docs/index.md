---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# syntiq-mt5

### MetaTrader 5, shaped for Python developers

Direct values. Typed failures. Managed global state.

[Start in five minutes](quickstart.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/Lucifer516-sudoer/syntiq_mt5){ .md-button }

</div>

## One session, one honest interface

The official MT5 extension is process-global and reports failures differently
for different functions. This library does not pretend otherwise. One `MT5`
session owns the terminal, serializes native calls with immediate error capture,
and turns raw records into typed models.

<div class="grid cards" markdown>

- **Direct return values**

    `positions()` returns `tuple[Position, ...]`. No wrapper and no optional data.

- **Typed failures**

    Every `MT5Error` includes `operation`, `code`, and `message`.

- **Correct trade responses**

    Checks expose projected margin. Sends expose execution details. They are not
    forced into one inaccurate model.

- **Testable without Windows**

    Inject a fake adapter at the native seam and exercise the same public session.

</div>

```python
from syntiq_mt5 import SyntiqMT5, constants

with SyntiqMT5() as mt5:
    quote = mt5.symbol_info_tick("EURUSD")
    candles = mt5.candles("EURUSD", constants.TIMEFRAME_H1, 100)
    positions = mt5.positions(symbol="EURUSD")

print(quote.bid, quote.ask, len(candles), len(positions))
```

!!! warning "Alpha and trading risk"
    The package is under active development. Test all order logic against a demo
    account. `order_check()` is a pre-flight check, not a guarantee of execution.

## Supported areas

| Area | Interface |
| --- | --- |
| Lifecycle | `initialize`, `login`, `shutdown`, context manager |
| Terminal | `version`, `account_info`, `terminal_info` |
| Market data | symbols, quotes, completed candles, rates, ticks |
| Portfolio | positions and pending orders |
| Trading | margin/profit calculation, check, send |
| History | order and deal queries by UTC range, ticket, or position |
| Market depth | managed subscription context and snapshots |

The native dependency is Windows-only. Documentation, models, and fake-adapter
tests work on every development platform.
