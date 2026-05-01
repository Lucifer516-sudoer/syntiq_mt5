# Get History

Retrieve historical orders and deals from the trade history.

---

## Historical orders by date range

```python
from datetime import datetime, timezone

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
date_to   = datetime(2024, 1, 31, tzinfo=timezone.utc)

res = mt5.history_orders_get(date_from, date_to)

if res.success:
    print(f"Orders: {len(res.data)}")
    for order in res.data[:3]:
        print(f"  #{order.ticket}  {order.symbol}  {order.volume_initial} lots  state={order.state.name}")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
Orders: 15
  #123456  EURUSD  0.10 lots  state=FILLED
  #123457  GBPUSD  0.05 lots  state=CANCELED
  #123458  EURUSD  0.10 lots  state=FILLED
```

---

## Historical deals by date range

```python
res = mt5.history_deals_get(date_from, date_to)

if res.success:
    print(f"Deals: {len(res.data)}")
    for deal in res.data[:3]:
        print(
            f"  #{deal.ticket}  {deal.symbol}  "
            f"profit={deal.profit:.2f}  net={deal.net_profit:.2f}"
        )
```

```text
Deals: 30
  #789012  EURUSD  profit=50.00  net=49.50
  #789013  EURUSD  profit=-20.00  net=-20.50
  #789014  GBPUSD  profit=30.00  net=29.50
```

---

## Filter by position ticket

```python
# All orders that touched position #123456
res = mt5.history_orders_get(position=123456)

# All deals that touched position #123456
res = mt5.history_deals_get(position=123456)
```

---

## Filter by symbol group

```python
res = mt5.history_deals_get(
    date_from=date_from,
    date_to=date_to,
    group="*USD*",
)
```

---

## Count only

```python
res = mt5.history_orders_total(date_from, date_to)
if res.success:
    print(f"Total orders: {res.data}")

res = mt5.history_deals_total(date_from, date_to)
if res.success:
    print(f"Total deals: {res.data}")
```

---

## Deal fields

| Field | Description |
|---|---|
| `ticket` | Unique deal identifier |
| `symbol` | Trading instrument |
| `type` | `DealType` — BUY, SELL, BALANCE, COMMISSION, etc. |
| `entry` | `DealEntry` — IN (opened), OUT (closed), INOUT (reversed) |
| `volume` | Executed volume in lots |
| `price` | Execution price |
| `profit` | Gross profit/loss |
| `commission` | Commission charged |
| `swap` | Swap charged |
| `net_profit` | `profit + commission + swap - fee` (computed) |
| `is_entry` | `True` if this deal opened a position |
| `is_exit` | `True` if this deal closed a position |

---

## Summarise P&L for a period

```python
res = mt5.history_deals_get(date_from, date_to)

if res.success:
    trade_deals = [d for d in res.data if d.is_buy or d.is_sell]
    total_net = sum(d.net_profit for d in trade_deals)
    print(f"Net P&L: {total_net:.2f}")
```

---

## Failure examples

### Example 1: No history available

```python
from datetime import datetime, timezone

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
date_to = datetime(2024, 1, 31, tzinfo=timezone.utc)

res = mt5.history_deals_get(date_from, date_to)

if res.success:
    if not res.data:
        print("No deals in this period")
    else:
        print(f"Found {len(res.data)} deals")
```

**Output:**
```text
No deals in this period
```

**Note:** `success=True` with empty `data` means the operation worked, but no deals exist for that date range.

---

### Example 2: Invalid position ticket

```python
res = mt5.history_deals_get(position=999999999)

if res.success:
    if not res.data:
        print("No deals found for this position (invalid ticket or no history)")
```

**Why:** The position ticket doesn't exist, or the position has no associated deals in the history.

---

### Example 3: Date range too large

```python
# Trying to fetch 5 years of history
date_from = datetime(2019, 1, 1, tzinfo=timezone.utc)
date_to = datetime(2024, 1, 1, tzinfo=timezone.utc)

res = mt5.history_deals_get(date_from, date_to)

if res.success:
    print(f"Deals: {len(res.data)}")
    # This might be slow or hit broker limits
```

**Fix:** Fetch history in smaller chunks (e.g., monthly) to avoid timeouts and memory issues.

---

## Practical notes

!!! tip "Filter trade deals only"
    History includes non-trade deals (balance adjustments, commissions, etc.). Filter for actual trades:
    ```python
    res = mt5.history_deals_get(date_from, date_to)
    
    if res.success:
        trade_deals = [d for d in res.data if d.is_buy or d.is_sell]
        print(f"Trade deals: {len(trade_deals)}")
    ```

!!! warning "Commission and swap"
    `profit` is gross P&L. Use `net_profit` for actual profit after fees:
    ```python
    deal = res.data[0]
    print(f"Gross: {deal.profit:.2f}")
    print(f"Commission: {deal.commission:.2f}")
    print(f"Swap: {deal.swap:.2f}")
    print(f"Net: {deal.net_profit:.2f}")
    ```

!!! info "Entry vs exit deals"
    - `is_entry` — Deal opened a position
    - `is_exit` — Deal closed a position
    
    Use these to separate opening and closing trades:
    ```python
    entries = [d for d in res.data if d.is_entry]
    exits = [d for d in res.data if d.is_exit]
    ```

!!! note "Historical orders vs deals"
    - **Orders** — Trade requests (can be pending, filled, canceled)
    - **Deals** — Actual executions (always filled)
    
    Use `history_deals_get()` for P&L analysis, `history_orders_get()` for order flow analysis.

!!! tip "Calculate win rate"
    ```python
    res = mt5.history_deals_get(date_from, date_to)
    
    if res.success:
        trade_deals = [d for d in res.data if d.is_exit]
        wins = [d for d in trade_deals if d.net_profit > 0]
        losses = [d for d in trade_deals if d.net_profit < 0]
        
        win_rate = len(wins) / len(trade_deals) * 100 if trade_deals else 0
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Wins: {len(wins)}  Losses: {len(losses)}")
    ```
```
