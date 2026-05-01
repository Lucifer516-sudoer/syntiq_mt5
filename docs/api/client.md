# Client

The main entry point for all MetaTrader 5 operations.

---

## MetaTrader5Client

::: syntiq_mt5.MetaTrader5Client
    options:
      show_root_heading: true
      show_source: false
      members:
        - __init__
        - __enter__
        - __exit__
        - initialize
        - login
        - shutdown
        - version
        - positions
        - positions_total
        - get_candles
        - copy_rates_from
        - copy_rates_range
        - account_info
        - terminal_info
        - symbols_total
        - symbols_get
        - symbol_select
        - symbol_info
        - symbol_info_tick
        - market_book_add
        - market_book_get
        - market_book_release
        - copy_ticks_from
        - copy_ticks_range
        - orders_total
        - orders_get
        - order_calc_margin
        - order_calc_profit
        - order_check
        - order_send
        - history_orders_total
        - history_orders_get
        - history_deals_total
        - history_deals_get

---

## Usage

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),
    server="Broker-Demo",
)

with MetaTrader5Client(debug=True) as mt5:
    # Initialize and login
    mt5.initialize(creds)
    mt5.login(creds)
    
    # Use any method
    res = mt5.positions()
    if res.success:
        for p in res.data:
            print(f"{p.symbol}: {p.pips_profit:+.1f} pips")
```

The client automatically calls `shutdown()` when the context manager exits.
