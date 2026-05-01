# Positions

Open position models and retrieval services.

---

## Models

### Position

::: syntiq_mt5.positions.models.Position
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### PositionService

::: syntiq_mt5.positions.service.PositionService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
# Get all positions
res = mt5.positions()
if res.success:
    for p in res.data:
        print(f"{p.symbol}: {p.pips_profit:+.1f} pips")

# Filter by symbol
res = mt5.positions(symbol="EURUSD")

# Count only
res = mt5.positions_total()
```
