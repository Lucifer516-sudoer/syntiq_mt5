# Task: Get account information

Retrieve account balance, equity, margin, and leverage.

```python
res = mt5.account_info()
if res.success:
    acc = res.data
    print(f"Balance: {acc.balance} {acc.currency}")
    print(f"Equity: {acc.equity}")
    print(f"Margin: {acc.margin}")
    print(f"Free Margin: {acc.margin_free}")
    print(f"Margin Level: {acc.margin_level}%")
    print(f"Leverage: 1:{acc.leverage}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Balance: 10000.0 USD
Equity: 10150.0
Margin: 100.0
Free Margin: 10050.0
Margin Level: 10150.0%
Leverage: 1:100
```

Note: `margin_used_percent` and `equity_to_balance_ratio` are computed properties.
