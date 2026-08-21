# Trading

!!! danger "Use a demo account first"
    This library cannot make an incorrect strategy safe. Verify symbol settings,
    volume, prices, filling policy, and broker behavior before live execution.

## Build a request

```python
from syntiq_mt5 import OrderFilling, OrderType, TradeAction, TradeRequest

request = TradeRequest(
    action=TradeAction.DEAL,
    symbol="EURUSD",
    volume=0.01,
    type=OrderType.BUY,
    type_filling=OrderFilling.FOK,
    deviation=20,  # points, not pips
    comment="syntiq demo",
)
```

The required fields vary by action and symbol execution mode. Do not hard-code a
filling policy without checking the symbol's capabilities.

## Check, then send

```python
check = mt5.order_check(request)
if not check.accepted:
    raise RuntimeError(f"Check rejected: {check.retcode} {check.comment}")

result = mt5.order_send(request)
if not result.is_successful:
    raise RuntimeError(f"Broker response: {result.retcode} {result.comment}")
```

`order_check()` does not submit and does not guarantee later execution.
`TradeResult.is_successful` recognizes placed, done, and partial-fill responses.
Unknown broker return codes remain available as integers.

## Calculations

```python
margin = mt5.order_calc_margin(OrderType.BUY, "EURUSD", 0.1, 1.1000)
profit = mt5.order_calc_profit(OrderType.BUY, "EURUSD", 0.1, 1.1000, 1.1050)
```

These methods accept `OrderType`, not `TradeAction`.
