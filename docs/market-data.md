# Market Data

## Recent completed candles

```python
with MT5() as mt5:
    bars = mt5.candles("EURUSD", constants.TIMEFRAME_M15, 200)
```

`candles()` starts at position `1`; position `0` is MT5's current open bar.

## Historical rates

```python
from datetime import UTC, datetime

with MT5() as mt5:
    bars = mt5.copy_rates_range(
        "EURUSD",
        constants.TIMEFRAME_H1,
        datetime(2026, 1, 1, tzinfo=UTC),
        datetime(2026, 2, 1, tzinfo=UTC),
    )
```

Available history is bounded by the terminal's **Max. bars in chart** setting.

## Ticks

Use `COPY_TICKS_ALL`, `COPY_TICKS_INFO`, or `COPY_TICKS_TRADE`:

```python
ticks = mt5.copy_ticks_from("EURUSD", start, 10_000, constants.COPY_TICKS_ALL)
```

## Market depth

Subscriptions are resources. Use the managed context so release happens even
when strategy code raises:

```python
with mt5.market_book("EURUSD"):
    snapshot = mt5.market_book_get("EURUSD")
```

Not every broker or symbol supports market depth.
