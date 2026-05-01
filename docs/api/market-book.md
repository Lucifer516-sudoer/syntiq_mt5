# Market Book

Level 2 order book (Depth of Market) data.

---

## Models

### BookEntry

::: syntiq_mt5.market_book.models.BookEntry
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### MarketBookService

::: syntiq_mt5.market_book.service.MarketBookService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
# Subscribe to market book
add = mt5.market_book_add("EURUSD")
if add.success and add.data:
    # Read the book
    res = mt5.market_book_get("EURUSD")
    if res.success:
        for entry in res.data:
            side = "BUY" if entry.is_buy else "SELL"
            print(f"{side}: {entry.price} @ {entry.volume_real}")
    
    # Release when done
    mt5.market_book_release("EURUSD")
```
