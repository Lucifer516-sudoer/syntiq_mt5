# Task: Get trading history

Retrieve historical orders and deals.

## Get historical orders

```python
from datetime import datetime, timezone

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
date_to = datetime(2024, 1, 31, tzinfo=timezone.utc)

res = mt5.history_orders_get(date_from, date_to)
if res.success:
    print(f"Orders: {len(res.data)}")
    if res.data:
        order = res.data[0]
        print(f"Ticket: {order.ticket}, Symbol: {order.symbol}, Volume: {order.volume_initial}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Orders: 15
Ticket: 123456, Symbol: EURUSD, Volume: 0.1
```

## Get historical deals

```python
res = mt5.history_deals_get(date_from, date_to)
if res.success:
    print(f"Deals: {len(res.data)}")
    if res.data:
        deal = res.data[0]
        print(f"Ticket: {deal.ticket}, Symbol: {deal.symbol}")
        print(f"Profit: {deal.profit}, Commission: {deal.commission}")
        print(f"Net profit: {deal.net_profit}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Deals: 30
Ticket: 789012, Symbol: EURUSD
Profit: 50.0, Commission: -0.5
Net profit: 49.5
```

## Get orders for a specific position

```python
res = mt5.history_orders_get(position=123456)
if res.success:
    print(f"Orders for position: {len(res.data)}")
```

Note: `net_profit` includes profit, commission, swap, and fees.
