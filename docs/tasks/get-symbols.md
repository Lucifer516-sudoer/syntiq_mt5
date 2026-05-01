# Task: Work with symbols

Enumerate symbols, get symbol information, and retrieve current tick.

## List all symbols

```python
res = mt5.symbols_get()
if res.success:
    print(f"Total symbols: {len(res.data)}")
    print("First 5:", res.data[:5])
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Total symbols: 120
First 5: ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
```

## Get symbol information

```python
res = mt5.symbol_info("EURUSD")
if res.success:
    info = res.data
    print(f"Symbol: {info.name}")
    print(f"Digits: {info.digits}")
    print(f"Point: {info.point}")
    print(f"Spread: {info.spread_pips} pips")
    print(f"Contract size: {info.contract_size}")
    print(f"Min volume: {info.volume_min}")
    print(f"Max volume: {info.volume_max}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Symbol: EURUSD
Digits: 5
Point: 1e-05
Spread: 1.5 pips
Contract size: 100000.0
Min volume: 0.01
Max volume: 100.0
```

## Get current tick

```python
res = mt5.symbol_info_tick("EURUSD")
if res.success:
    tick = res.data
    print(f"Bid: {tick.bid}")
    print(f"Ask: {tick.ask}")
    print(f"Spread: {tick.spread}")
else:
    print(res.error_code, res.error_message)
```

Output example:

```text
Bid: 1.08450
Ask: 1.08465
Spread: 0.00015
```
