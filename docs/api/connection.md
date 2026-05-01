# Connection

Connection lifecycle and credential management.

---

## Models

### LoginCredential

::: syntiq_mt5.connection.models.LoginCredential
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### ConnectionService

::: syntiq_mt5.connection.service.ConnectionService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),  # Never logged or serialized
    server="Broker-Demo",
    path=None,  # Optional: path to terminal64.exe
)

with MetaTrader5Client() as mt5:
    # Initialize connects to the terminal
    init = mt5.initialize(creds)
    if not init.success:
        print(f"Initialize failed: {init.error_message}")
        raise SystemExit(1)
    
    # Login authenticates with the broker
    login = mt5.login(creds)
    if not login.success:
        print(f"Login failed: {login.error_message}")
        raise SystemExit(1)
```
