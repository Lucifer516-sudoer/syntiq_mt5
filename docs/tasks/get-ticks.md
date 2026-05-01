# Get Ticks

Retrieve raw tick data for analysis and backtesting.

---

## Ticks from a start date

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 6, 1, 9, 0, tzinfo=timezone.utc)

res = mt5.copy_ticks_from(
    "EURUSD",
    date_from,
    count=500,
    flags=constants.COPY_TICKS_ALL,
)

if res.success:
    print(f"Ticks: {len(res.data)}")
    t = res.data[0]
    print(f"  time={t.time}  bid={t.bid}  ask={t.ask}  spread={t.spread:.5f}")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
Ticks: 500
  time=1717232400  bid=1.08450  ask=1.08465  spread=0.00015
```

---

## Ticks in a date range

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 6, 1, tzinfo=timezone.utc)
date_to   = datetime(2024, 6, 1, 1, 0, tzinfo=timezone.utc)  # 1 hour

res = mt5.copy_ticks_range(
    "EURUSD",
    date_from,
    date_to,
    flags=constants.COPY_TICKS_ALL,
)

if res.success:
    print(f"Ticks in range: {len(res.data)}")
```

---

## Tick flags

Choose which ticks to retrieve:

| Constant | Description |
|---|---|
| `COPY_TICKS_ALL` | All ticks (bid/ask changes + trade ticks) |
| `COPY_TICKS_INFO` | Only bid/ask price changes |
| `COPY_TICKS_TRADE` | Only last price and volume changes (exchange instruments) |

For Forex, use `COPY_TICKS_INFO` or `COPY_TICKS_ALL`. `COPY_TICKS_TRADE` is for exchange instruments with real volume.

---

## Tick fields

| Field | Description |
|---|---|
| `time` | Tick time (Unix seconds) |
| `time_msc` | Tick time (milliseconds) |
| `bid` | Bid price |
| `ask` | Ask price |
| `last` | Last trade price (exchange only; 0.0 for Forex) |
| `volume` | Last trade volume (exchange only) |
| `flags` | Bitmask of `TICK_FLAG_*` constants |
| `spread` | `ask - bid` (computed) |
| `mid_price` | `(bid + ask) / 2` (computed) |
| `has_bid` | `True` if bid changed in this tick |
| `has_ask` | `True` if ask changed in this tick |

---

## Inspect what changed in a tick

```python
from syntiq_mt5 import constants

for tick in res.data[:10]:
    changed = []
    if tick.has_bid:
        changed.append(f"bid={tick.bid}")
    if tick.has_ask:
        changed.append(f"ask={tick.ask}")
    print(f"  t={tick.time_msc}ms  {', '.join(changed)}")
```

---

## Failure examples

### Example 1: No ticks available

```python
from datetime import datetime, timezone

# Weekend or holiday
date_from = datetime(2024, 12, 25, tzinfo=timezone.utc)

res = mt5.copy_ticks_from("EURUSD", date_from, count=100, flags=constants.COPY_TICKS_ALL)

if res.success:
    if not res.data:
        print("No ticks available for this period (market was closed)")
    else:
        print(f"Found {len(res.data)} ticks")
```

**Output:**
```text
No ticks available for this period (market was closed)
```

**Note:** `success=True` with empty `data` means the operation worked, but no ticks exist for that time range.

---

### Example 2: Symbol not found

```python
res = mt5.copy_ticks_from("INVALID", date_from, count=100, flags=constants.COPY_TICKS_ALL)

if not res.success:
    print(f"Error: {res.error_message}")
    print(f"Code: {res.error_code}")
```

**Output:**
```text
Error: Symbol not found or not available
Code: 4301
```

**Fix:** Ensure the symbol exists and is enabled in Market Watch.

---

### Example 3: Date too far in the past

```python
# Trying to fetch ticks from 10 years ago
date_from = datetime(2014, 1, 1, tzinfo=timezone.utc)

res = mt5.copy_ticks_from("EURUSD", date_from, count=1000, flags=constants.COPY_TICKS_ALL)

if res.success:
    if not res.data:
        print("No tick data available for this date (beyond broker's history)")
```

**Why:** Brokers typically store tick data for a limited period (e.g., 1-2 years). Older data is not available.

---

## Practical notes

!!! tip "Use timezone-aware datetimes"
    Always use `timezone.utc` for datetime objects:
    ```python
    from datetime import datetime, timezone
    
    # ✅ Correct
    date_from = datetime(2024, 6, 1, 9, 0, tzinfo=timezone.utc)
    
    # ❌ Wrong (naive datetime)
    date_from = datetime(2024, 6, 1, 9, 0)
    ```

!!! warning "Large tick requests"
    Requesting millions of ticks can be slow and memory-intensive. Fetch ticks in chunks:
    ```python
    from datetime import timedelta
    
    start = datetime(2024, 6, 1, tzinfo=timezone.utc)
    end = datetime(2024, 6, 2, tzinfo=timezone.utc)
    
    current = start
    all_ticks = []
    
    while current < end:
        res = mt5.copy_ticks_from("EURUSD", current, count=10000, flags=constants.COPY_TICKS_ALL)
        if res.success and res.data:
            all_ticks.extend(res.data)
            current = datetime.fromtimestamp(res.data[-1].time, tz=timezone.utc)
        else:
            break
    ```

!!! info "Tick flags for Forex"
    For Forex symbols, use:
    - `COPY_TICKS_INFO` — Only bid/ask changes (most common)
    - `COPY_TICKS_ALL` — All ticks including time updates
    
    `COPY_TICKS_TRADE` is for exchange instruments with real volume (stocks, futures).

!!! note "Millisecond precision"
    Use `time_msc` for millisecond-level timestamps. `time` is in Unix seconds and loses sub-second precision.
```
