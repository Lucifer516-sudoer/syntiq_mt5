# Orders

Order placement, validation, and management.

---

## Models

### Order

::: syntiq_mt5.orders.models.Order
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### HistoricalOrder

::: syntiq_mt5.orders.models.HistoricalOrder
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### TradeRequest

::: syntiq_mt5.orders.models.TradeRequest
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### TradeResult

::: syntiq_mt5.orders.models.TradeResult
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### OrderService

::: syntiq_mt5.orders.service.OrderService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
from syntiq_mt5 import TradeRequest, constants

# Create a trade request
request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.10,
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
    sl=1.08000,
    tp=1.09000,
    deviation=10,
)

# Validate first
check = mt5.order_check(request)
if check.success and check.data.is_successful:
    # Send the order
    res = mt5.order_send(request)
    if res.success and res.data.is_successful:
        print(f"Order filled: {res.data.order}")
```
