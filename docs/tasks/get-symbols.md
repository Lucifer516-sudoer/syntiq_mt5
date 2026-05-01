# Get Symbols

List available symbols, query their specifications, and get the current tick.

---

## List all symbols

```python
res = mt5.symbols_get()

if res.success:
    print(f"Total: {len(res.data)}")
    print("First 5:", res.data[:5])
```

```text
Total: 120
First 5: ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
```

---

## Filter by group pattern

```python
res = mt5.symbols_get(group="*USD*")

if res.success:
    print(res.data)
```

```text
['EURUSD', 'GBPUSD', 'AUDUSD', 'USDCAD', 'USDCHF', ...]
```

---

## Symbol specification

```python
res = mt5.symbol_info("EURUSD")

if res.success:
    info = res.data
    print(f"Digits:        {info.digits}")
    print(f"Spread:        {info.spread_pips:.1f} pips")
    print(f"Contract size: {info.contract_size}")
    print(f"Min volume:    {info.volume_min}")
    print(f"Max volume:    {info.volume_max}")
    print(f"Volume step:   {info.volume_step}")
    print(f"Pip size:      {info.pip_size}")
```

```text
Digits:        5
Spread:        1.5 pips
Contract size: 100000.0
Min volume:    0.01
Max volume:    100.0
Volume step:   0.01
Pip size:      0.0001
```

---

## Current tick

```python
res = mt5.symbol_info_tick("EURUSD")

if res.success:
    tick = res.data
    print(f"Bid:    {tick.bid}")
    print(f"Ask:    {tick.ask}")
    print(f"Spread: {tick.spread:.5f}")
    print(f"Mid:    {tick.mid_price:.5f}")
```

```text
Bid:    1.08450
Ask:    1.08465
Spread: 0.00015
Mid:    1.08458
```

---

## Add/remove from Market Watch

```python
# Add BTCUSD to Market Watch
res = mt5.symbol_select("BTCUSD", enable=True)

# Remove it
res = mt5.symbol_select("BTCUSD", enable=False)
```

A symbol must be in Market Watch before you can trade it or fetch its data.

---

## Key SymbolInfo fields

| Field | Description |
|---|---|
| `name` | Symbol name |
| `digits` | Decimal places in price |
| `point` | Smallest price increment |
| `pip_size` | Pip size (accounts for 3/5-digit symbols) |
| `spread` | Current spread in points |
| `spread_pips` | Current spread in pips (computed) |
| `bid` / `ask` | Current bid/ask prices |
| `volume_min` | Minimum trade volume |
| `volume_max` | Maximum trade volume |
| `volume_step` | Volume increment |
| `trade_contract_size` | Contract size (e.g. 100000 for standard Forex lot) |
| `currency_base` | Base currency |
| `currency_profit` | Profit currency |

---

## Failure examples

### Example 1: Symbol not found

```python
res = mt5.symbol_info("INVALID_SYMBOL")

if not res.success:
    print(f"Error: {res.error_message}")
    print(f"Code: {res.error_code}")
```

**Output:**
```text
Error: Symbol not found or not available
Code: 4301
```

**Fix:** Use `symbols_get()` to list available symbols, or enable the symbol in Market Watch first.

---

### Example 2: Symbol not in Market Watch

```python
# Symbol exists but not visible
res = mt5.symbol_info("BTCUSD")

if not res.success:
    print("Symbol not available")
    
    # Enable it
    enable = mt5.symbol_select("BTCUSD", True)
    if enable.success and enable.data:
        # Now it works
        res = mt5.symbol_info("BTCUSD")
        print(f"Symbol enabled: {res.data.name}")
```

---

### Example 3: Empty symbol list

```python
res = mt5.symbols_get(group="*XYZ*")

if res.success:
    if not res.data:
        print("No symbols match this pattern")
    else:
        print(f"Found: {res.data}")
```

**Output:**
```text
No symbols match this pattern
```

**Note:** `success=True` with empty `data` means the operation worked, but no symbols matched the filter.

---

## Practical notes

!!! tip "Check spread before trading"
    ```python
    info = mt5.symbol_info("EURUSD")
    if info.success and info.data.spread_pips > 3.0:
        print("⚠️ High spread — consider waiting")
    ```

!!! warning "Volume constraints"
    Always check `volume_min`, `volume_max`, and `volume_step` before placing orders:
    ```python
    info = mt5.symbol_info("EURUSD")
    if info.success:
        # Round volume to valid step
        volume = 0.15
        step = info.data.volume_step
        valid_volume = round(volume / step) * step
        print(f"Adjusted volume: {valid_volume}")
    ```

!!! info "Pip size calculation"
    The SDK automatically calculates `pip_size` for both 3-digit (JPY) and 5-digit (EUR, GBP) symbols:
    - EURUSD (5 digits): `pip_size = 0.0001`
    - USDJPY (3 digits): `pip_size = 0.01`
    
    Use `spread_pips` instead of `spread` for consistent pip-based calculations.

!!! note "Symbol groups"
    Common patterns:
    - `"*USD*"` — All symbols with USD
    - `"EUR*"` — All symbols starting with EUR
    - `"*JPY"` — All symbols ending with JPY
    - `"Crypto*"` — All crypto symbols (if broker supports)
