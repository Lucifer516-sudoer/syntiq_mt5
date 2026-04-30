# Core concept: Result[T]

Every client call returns `Result[T]`.

- On success: `success=True`, `data` is set.
- On failure: `success=False`, error code/message/context are set.

```python
res = mt5.get_candles("EURUSD", timeframe=1, count=10)
if res.success:
    print(len(res.data))
else:
    print(res.operation, res.error_code, res.error_message)
```
