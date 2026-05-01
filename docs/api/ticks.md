# Ticks

Raw tick data retrieval services.

---

## Models

### Tick

::: syntiq_mt5.ticks.models.Tick
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### TickService

::: syntiq_mt5.ticks.service.TickService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 1, 1, 9, 0, tzinfo=timezone.utc)

# Get ticks from a date
res = mt5.copy_ticks_from(
    "EURUSD",
    date_from,
    count=1000,
    flags=constants.COPY_TICKS_ALL,
)

# Get ticks in a range
date_to = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
res = mt5.copy_ticks_range(
    "EURUSD",
    date_from,
    date_to,
    flags=constants.COPY_TICKS_INFO,
)
```
