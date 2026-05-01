# Task: Get tick data

Retrieve historical tick data for backtesting and analysis.

## Get ticks from a specific date

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
res = mt5.copy_ticks_from("EURUSD", date_from, count=100, flags=constants.COPY_TICKS_ALL)
if res.success:
    print(f"Ticks: {len(res.data)}")
    tick = res.data[0]
    print(f"Time: {tick.time}, Bid: {tick.bid}, Ask: {tick.ask}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Ticks: 100
Time: 1704067200, Bid: 1.08450, Ask: 1.08465
```

## Get ticks in a date range

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
date_to = datetime(2024, 1, 2, tzinfo=timezone.utc)
res = mt5.copy_ticks_range("EURUSD", date_from, date_to, flags=constants.COPY_TICKS_ALL)
if res.success:
    print(f"Ticks: {len(res.data)}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Ticks: 5432
```

Note: Use `constants.COPY_TICKS_INFO` for bid/ask ticks, `constants.COPY_TICKS_TRADE` for trade ticks, or `constants.COPY_TICKS_ALL` for all ticks.
