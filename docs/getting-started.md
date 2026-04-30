# Quickstart

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
    mt5.initialize(creds)
    mt5.login(creds)
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
