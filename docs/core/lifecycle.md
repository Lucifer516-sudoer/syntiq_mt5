# Core concept: Lifecycle

Use one flow:

1. `initialize()`
2. `login()`
3. data calls (`positions`, `get_candles`)
4. `shutdown()` (automatic in `with` block)

```python
with MetaTrader5Client() as mt5:
    mt5.initialize(creds)
    mt5.login(creds)
    # use mt5...
```
