# Market

Candles, rates, and market data services.

---

## Models

### Candle

::: syntiq_mt5.market.candles.Candle
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Services

### MarketService

::: syntiq_mt5.market.symbols.MarketService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
from syntiq_mt5 import constants

# Get recent candles
res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=100)

# Get candles from a date
from datetime import datetime, timezone
date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
res = mt5.copy_rates_from("EURUSD", constants.TIMEFRAME_D1, date_from, count=30)

# Get candles in a range
date_to = datetime(2024, 1, 31, tzinfo=timezone.utc)
res = mt5.copy_rates_range("EURUSD", constants.TIMEFRAME_H4, date_from, date_to)
```
