# Task: Get candles

Fetch recent candles for a symbol.

```python
res = mt5.get_candles("EURUSD", timeframe=1, count=50)
if res.success:
    print("candles:", len(res.data))
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
candles: 50
```
