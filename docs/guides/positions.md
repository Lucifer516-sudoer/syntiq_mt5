# Positions

---
## Next Steps
[Results Model](results.md)

The positions API exposes the current open positions in the connected MT5
session.

## Total open positions

```python
from metatrader5_wrapper import positions_total

result = positions_total()
```

## Read positions

```python
from metatrader5_wrapper import positions_get

result = positions_get(symbol="EURUSD")

if result.success and result.data is not None:
    for position in result.data:
        print(position.ticket, position.symbol, position.volume)
```

## Filtering behavior

The current implementation uses one filter at a time in this order:

- `symbol`
- `group`
- `ticket`
- no filter

If you need exact behavior details, see the generated API reference.