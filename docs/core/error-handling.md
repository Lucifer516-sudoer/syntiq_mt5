# Core concept: Error handling

MetaTrader5 stores errors in global state (`last_error()`).

`syntiq-mt5` captures that error immediately after each operation and attaches it to `Result`.

```python
res = mt5.positions()
if not res.success:
    print(res.error_code, res.error_message, res.operation)
```
