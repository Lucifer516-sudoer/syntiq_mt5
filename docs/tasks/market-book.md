# Task: Work with market book

Subscribe to and retrieve Level 2 order book data.

## Subscribe to market book

```python
res = mt5.market_book_add("EURUSD")
if res.success and res.data:
    print("Subscribed to market book")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Subscribed to market book
```

## Get market book entries

```python
res = mt5.market_book_get("EURUSD")
if res.success:
    print(f"Book entries: {len(res.data)}")
    for entry in res.data[:5]:
        side = "BUY" if entry.is_buy else "SELL"
        print(f"{side}: {entry.price} @ {entry.volume_real}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Book entries: 10
SELL: 1.08465 @ 1.5
SELL: 1.08470 @ 2.0
BUY: 1.08450 @ 1.0
BUY: 1.08445 @ 1.5
BUY: 1.08440 @ 2.5
```

## Unsubscribe from market book

```python
res = mt5.market_book_release("EURUSD")
if res.success and res.data:
    print("Unsubscribed from market book")
```

Note: Market book data is not available for all symbols and brokers.
