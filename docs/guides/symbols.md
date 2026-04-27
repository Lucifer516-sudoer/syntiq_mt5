# Symbols and Ticks

The symbols API exposes typed access to instrument metadata and live tick data.

## Browse symbols

```python
from metatrader5_wrapper import symbols_get

result = symbols_get(group="*USD*")

if result.success and result.data is not None:
    print(len(result.data))
```

## Inspect one symbol

```python
from metatrader5_wrapper import symbol_info

result = symbol_info("EURUSD")

if result.success and result.data is not None:
    print(result.data.name, result.data.digits, result.data.spread)
```

## Read the latest tick

```python
from metatrader5_wrapper import symbol_info_tick

tick = symbol_info_tick("EURUSD")

if tick.success and tick.data is not None:
    print(tick.data.bid, tick.data.ask)
```

## Add a symbol to MarketWatch

```python
from metatrader5_wrapper import symbol_select

result = symbol_select("EURUSD", enable=True)
```
---
## Next Steps
[Positions](positions.md)