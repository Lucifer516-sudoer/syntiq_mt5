---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# syntiq-mt5

### Production-grade MetaTrader 5 SDK for Python

Typed. Reliable. Developer-first.

[Get Started](getting-started.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/lucifer516-sudoer/syntiq-mt5){ .md-button .md-button--secondary }

</div>

---

## Why syntiq-mt5?

The raw `MetaTrader5` Python package returns untyped structs, stores errors in global state, and requires you to know integer constants by heart. **syntiq-mt5 fixes all of that.**

<div class="grid cards" markdown>

-   :material-check-circle: __Typed Models__

    Pydantic v2 models with full IDE completion. No more guessing field names or types.

-   :material-shield-check: __No Exceptions__

    Every operation returns `Result[T]`. Handle success and failure explicitly — no surprises.

-   :material-code-tags: __Named Constants__

    Use `ORDER_TYPE_BUY` instead of `0`. Use `TIMEFRAME_H1` instead of `16385`. Self-documenting code.

-   :material-connection: __Automatic Cleanup__

    Context manager support. `shutdown()` is called automatically — even on exceptions.

</div>

---

## Raw MT5 vs syntiq-mt5

| Raw MT5 | syntiq-mt5 |
|---------|------------|
| Untyped namedtuples | Pydantic models with IDE completion |
| `mt5.last_error()` after every call | `result.error_code` / `result.error_message` |
| Magic integers (`0`, `1`, `16385`) | Named constants (`ORDER_TYPE_BUY`, `TIMEFRAME_H1`) |
| Raises on connection failure | Returns `Result.fail(...)` |
| Manual `mt5.shutdown()` | Automatic via context manager |

---

## Quick example

=== "syntiq-mt5"

    ```python
    from pydantic import SecretStr
    from syntiq_mt5 import LoginCredential, MetaTrader5Client, constants

    creds = LoginCredential(
        login=12345678,
        password=SecretStr("your-password"),
        server="Broker-Demo",
    )

    with MetaTrader5Client() as mt5:
        mt5.initialize(creds)
        mt5.login(creds)

        res = mt5.positions()
        if res.success:
            for p in res.data:
                print(f"{p.symbol}  {p.volume} lots  {p.pips_profit:+.1f} pips")
    ```

    ```text title="Output"
    EURUSD  0.10 lots  +12.3 pips
    GBPUSD  0.05 lots  -4.7 pips
    ```

=== "Raw MT5"

    ```python
    import MetaTrader5 as mt5

    if not mt5.initialize():
        print("initialize() failed")
        quit()

    if not mt5.login(12345678, password="your-password", server="Broker-Demo"):
        print("login() failed, error code =", mt5.last_error())
        mt5.shutdown()
        quit()

    positions = mt5.positions_get()
    if positions is None:
        print("No positions, error code =", mt5.last_error())
    elif len(positions) > 0:
        for p in positions:
            # p is a namedtuple — no IDE completion, no type hints
            print(p.symbol, p.volume, p.profit)

    mt5.shutdown()
    ```

---

## Install

```bash
pip install syntiq-mt5
```

!!! info "Requirements"
    - **Windows** — the MT5 Python API is Windows-only
    - **MetaTrader 5 terminal** installed ([download](https://www.metatrader5.com/en/download))
    - **Python 3.12+**

---

## What's next?

<div class="grid cards" markdown>

-   :material-rocket-launch: __[Quickstart](getting-started.md)__

    Full working example in under 60 seconds

-   :material-chart-timeline: __[Core Concepts](core/lifecycle.md)__

    Understand `initialize → login → use → shutdown`

-   :material-code-braces: __[Tasks](tasks/get-positions.md)__

    Copy-paste recipes for every operation

-   :material-book-open-variant: __[API Reference](api/index.md)__

    Complete auto-generated API documentation

</div>