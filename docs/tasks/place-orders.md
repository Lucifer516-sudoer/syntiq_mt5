# Task: Place and manage orders

Validate and send trade orders.

## Check order before sending

```python
from syntiq_mt5 import TradeRequest, constants

request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.1,
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
    sl=1.08000,
    tp=1.09000,
    deviation=10,
    comment="Test order",
)

res = mt5.order_check(request)
if res.success:
    result = res.data
    if result.is_successful:
        print("Order check passed")
        print(f"Required margin: {result.price}")
    else:
        print(f"Order check failed: {result.comment}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Order check passed
Required margin: 108.5
```

## Send order

```python
res = mt5.order_send(request)
if res.success:
    result = res.data
    if result.is_successful:
        print(f"Order placed: {result.order}")
        print(f"Deal: {result.deal}")
    else:
        print(f"Order failed: {result.comment}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Order placed: 123456
Deal: 789012
```

## Calculate margin and profit

```python
from syntiq_mt5 import constants

# Calculate required margin
res = mt5.order_calc_margin(
    constants.ORDER_TYPE_BUY, "EURUSD", 0.1, 1.08500
)
if res.success:
    print(f"Required margin: {res.data}")

# Calculate expected profit
res = mt5.order_calc_profit(
    constants.ORDER_TYPE_BUY, "EURUSD", 0.1, 1.08500, 1.09000
)
if res.success:
    print(f"Expected profit: {res.data}")
```

Output example:

```text
Required margin: 108.5
Expected profit: 50.0
```

Note: Use `constants.TRADE_ACTION_*` and `constants.ORDER_TYPE_*` instead of magic numbers.
