# History

Historical orders and deals retrieval.

---

## Models

### Deal

::: syntiq_mt5.history.models.Deal
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### HistoryService

::: syntiq_mt5.history.service.HistoryService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
from datetime import datetime, timezone

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
date_to = datetime(2024, 1, 31, tzinfo=timezone.utc)

# Get historical orders
res = mt5.history_orders_get(date_from, date_to)

# Get historical deals
res = mt5.history_deals_get(date_from, date_to)

# Filter by position
res = mt5.history_deals_get(position=123456)
```
