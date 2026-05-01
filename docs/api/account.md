# Account

Account information models and services.

---

## Models

### AccountInfo

::: syntiq_mt5.account.models.AccountInfo
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### AccountService

::: syntiq_mt5.account.service.AccountService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
res = mt5.account_info()

if res.success:
    acc = res.data
    print(f"Balance: {acc.balance} {acc.currency}")
    print(f"Equity: {acc.equity}")
    print(f"Margin used: {acc.margin_used_percent:.1f}%")
```
