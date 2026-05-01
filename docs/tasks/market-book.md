# Market Book

Subscribe to and read Level 2 (Depth of Market) order book data.

---

## Subscribe, read, release

```python
# 1. Subscribe
add = mt5.market_book_add("EURUSD")
if not add.success or not add.data:
    print("Market book not available for this symbol")
else:
    # 2. Read the current snapshot
    res = mt5.market_book_get("EURUSD")
    if res.success:
        print(f"Book entries: {len(res.data)}")
        for entry in res.data:
            side = "BUY " if entry.is_buy else "SELL"
            kind = "market" if entry.is_market else "limit "
            print(f"  {side} {kind}  {entry.price:.5f}  {entry.volume_real} lots")

    # 3. Release when done
    mt5.market_book_release("EURUSD")
```

```text
Book entries: 10
  SELL limit   1.08480  2.50 lots
  SELL limit   1.08475  1.00 lots
  SELL limit   1.08470  3.00 lots
  BUY  limit   1.08455  1.50 lots
  BUY  limit   1.08450  2.00 lots
```

---

## BookEntry fields

| Field | Type | Description |
|---|---|---|
| `type` | `BookType` | `SELL`, `BUY`, `SELL_MARKET`, `BUY_MARKET` |
| `price` | `float` | Price level |
| `volume` | `int` | Volume at this level (integer lots) |
| `volume_real` | `float` | Volume at this level (fractional lots) |
| `is_buy` | `bool` | `True` for buy-side entries |
| `is_sell` | `bool` | `True` for sell-side entries |
| `is_market` | `bool` | `True` for market orders (vs limit orders) |

---

## Separate bids and asks

```python
res = mt5.market_book_get("EURUSD")

if res.success:
    bids = [e for e in res.data if e.is_buy]
    asks = [e for e in res.data if e.is_sell]

    best_bid = max(bids, key=lambda e: e.price, default=None)
    best_ask = min(asks, key=lambda e: e.price, default=None)

    if best_bid and best_ask:
        print(f"Best bid: {best_bid.price}  Best ask: {best_ask.price}")
```

---

!!! note
    Market book data is not available for all symbols or brokers. `market_book_add()` returns `data=False` when the symbol does not support DOM. Always check `add.data` before calling `market_book_get()`.

---

## Failure examples

### Example 1: Market book not supported

```python
add = mt5.market_book_add("EURUSD")

if not add.success:
    print(f"Error: {add.error_message}")
elif not add.data:
    print("Market book not available for this symbol")
```

**Output:**
```text
Market book not available for this symbol
```

**Why:** Most Forex brokers don't provide Level 2 data. Market book is typically available only for exchange-traded instruments (stocks, futures).

---

### Example 2: Symbol not in Market Watch

```python
add = mt5.market_book_add("BTCUSD")

if not add.success:
    print(f"Failed: {add.error_message}")
    
    # Enable symbol first
    mt5.symbol_select("BTCUSD", True)
    
    # Retry
    add = mt5.market_book_add("BTCUSD")
```

---

### Example 3: Empty book

```python
add = mt5.market_book_add("EURUSD")

if add.success and add.data:
    res = mt5.market_book_get("EURUSD")
    
    if res.success:
        if not res.data:
            print("Book is empty (no orders at this moment)")
        else:
            print(f"Book has {len(res.data)} entries")
```

**Note:** Even when market book is supported, it can be temporarily empty.

---

## Practical notes

!!! warning "Always release subscriptions"
    ```python
    try:
        add = mt5.market_book_add("EURUSD")
        if add.success and add.data:
            # Use the book
            res = mt5.market_book_get("EURUSD")
    finally:
        # Always release, even on error
        mt5.market_book_release("EURUSD")
    ```

!!! tip "Check broker support first"
    Most retail Forex brokers don't provide DOM data. Check with your broker's documentation before relying on market book functionality.

!!! info "Real-time updates"
    `market_book_get()` returns a snapshot. For real-time updates, you need to poll it repeatedly or use MT5's event system (not exposed in this SDK).

!!! note "Volume interpretation"
    - `volume`: Integer lots (legacy field)
    - `volume_real`: Fractional lots (use this for accurate volume)
    
    Always use `volume_real` for calculations.
