# Task: Get positions

Fetch open positions and read pip profit.

```python
res = mt5.positions()
if res.success and res.data:
    p = res.data[0]
    print(p.symbol, p.volume, round(p.pips_profit, 1))
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
EURUSD 0.1 10.0
```

Note: `pips_profit` is computed from symbol precision.
