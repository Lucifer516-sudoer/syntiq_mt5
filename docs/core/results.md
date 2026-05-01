# Core concept: Result[T]

Every client call returns `Result[T]`.

- On success: `success=True`, `data` is set.
- On failure: `success=False`, error code/message/context are set.

```python
from syntiq_mt5 import constants

res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_M1, count=10)
if res.success:
    print(len(res.data))
else:
    print(res.operation, res.error_code, res.error_message)
```
