# Task: Get candles

Fetch recent candles for a symbol.

```python
from syntiq_mt5 import constants

res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_M1, count=50)
if res.success:
    print("candles:", len(res.data))
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
candles: 50
```
