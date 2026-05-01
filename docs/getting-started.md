# Quickstart

## Prerequisites

- **MetaTrader 5 terminal** must be installed on your system
- **Windows only** (MT5 Python API is Windows-specific)
- Valid MT5 account credentials (demo or live)

## Install

```bash
pip install syntiq-mt5
```

## Connect and fetch data

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as mt5:
    init_res = mt5.initialize(creds)
    if not init_res.success:
        print(f"Initialize failed: {init_res.error_message}")
        exit(1)
    
    login_res = mt5.login(creds)
    if not login_res.success:
        print(f"Login failed: {login_res.error_message}")
        exit(1)
    
    positions = mt5.positions()

if positions.success:
    print("positions:", len(positions.data))
else:
    print(positions.error_code, positions.error_message)
```

Output example:

```text
positions: 3
```
