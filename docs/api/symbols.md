# Symbols

Symbol information and specifications.

---

## Models

### SymbolInfo

::: syntiq_mt5.symbols.models.SymbolInfo
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### SymbolTick

::: syntiq_mt5.symbols.models.SymbolTick
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### SymbolService

::: syntiq_mt5.symbols.service.SymbolService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
# List all symbols
res = mt5.symbols_get()

# Filter by group
res = mt5.symbols_get(group="*USD*")

# Get symbol info
res = mt5.symbol_info("EURUSD")
if res.success:
    info = res.data
    print(f"Spread: {info.spread_pips:.1f} pips")
    print(f"Contract size: {info.contract_size}")

# Get current tick
res = mt5.symbol_info_tick("EURUSD")
```
