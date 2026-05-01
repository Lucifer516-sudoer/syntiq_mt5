# Lifecycle

Every session follows the same four steps.

```mermaid
graph LR
    A[initialize] --> B[login]
    B --> C[use]
    C --> D[shutdown]
    style A fill:#7c4dff
    style B fill:#7c4dff
    style C fill:#00bcd4
    style D fill:#7c4dff
```

---

## Why order matters

The lifecycle is **strictly ordered** for a reason:

1. **`initialize()`** establishes the connection to the MT5 terminal process
2. **`login()`** authenticates with the broker server **through** that connection
3. **Use** operations require both connection **and** authentication
4. **`shutdown()`** cleanly releases resources

**You cannot skip steps.** Calling `login()` before `initialize()` will fail because there's no connection to send the authentication request through. Calling `positions()` before `login()` will fail because the broker hasn't authenticated your session.

---

## The pattern

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),
    server="Broker-Demo",
)

with MetaTrader5Client() as mt5:
    init = mt5.initialize(creds)
    if not init.success:
        raise SystemExit(f"initialize failed: {init.error_message}")

    login = mt5.login(creds)
    if not login.success:
        raise SystemExit(f"login failed: {login.error_message}")

    # all operations go here
    res = mt5.account_info()
    ...

# shutdown() is called automatically here
```

---

## Step by step

### :material-numeric-1-circle: `initialize(creds)`

Connects to the MT5 terminal process on your machine. The terminal must already be running.

- Accepts optional `path` in `LoginCredential` to locate `terminal64.exe`
- Must succeed before any other call
- Sets an internal `_initialized` flag — all other methods check this flag and fail fast if it is not set

**What happens internally:**

1. SDK calls `mt5.initialize()` from the MetaTrader5 library
2. MT5 library searches for a running terminal process
3. If found, establishes IPC connection
4. Returns success/failure

### :material-numeric-2-circle: `login(creds)`

Authenticates with the broker server using your account number, password, and server name.

- Requires a successful `initialize()` first
- `server` must match exactly what appears in the MT5 terminal (e.g. `"ICMarkets-Demo"`)

**What happens internally:**

1. SDK calls `mt5.login()` with your credentials
2. MT5 terminal sends authentication request to broker server
3. Broker validates credentials and returns session token
4. Returns success/failure

### :material-numeric-3-circle: Use the client

All data and trading operations are available after a successful login. See the [Tasks](../tasks/get-positions.md) section for copy-paste examples.

### :material-numeric-4-circle: `shutdown()`

Disconnects from the terminal. Called automatically when the `with` block exits — even if an exception occurs.

**What happens internally:**

1. SDK calls `mt5.shutdown()`
2. MT5 library closes IPC connection to terminal
3. Resources are released

---

## Common mistakes

!!! failure "Calling methods before `initialize()`"
    ```python
    mt5 = MetaTrader5Client()
    res = mt5.positions()  # fails immediately
    # res.success == False
    # res.error_code == -10
    # res.error_message == "Client not initialized. Call initialize() first."
    ```
    
    **Why this fails:** The SDK checks the `_initialized` flag before every operation. If it's not set, the operation is rejected immediately with error code `-10`.

!!! failure "Not checking `initialize()` result"
    ```python
    mt5.initialize(creds)   # silently fails if terminal is not running
    mt5.login(creds)        # also fails — but with a confusing error
    ```
    
    **Why this fails:** If the terminal isn't running, `initialize()` returns `success=False`. But if you don't check it, you'll call `login()` next, which will fail with a cryptic error because there's no connection.
    
    **Always check `result.success` after `initialize()` and `login()`.**

!!! failure "Wrong server name"
    ```python
    creds = LoginCredential(
        login=12345678,
        password=SecretStr("correct-password"),
        server="Wrong-Server",  # Typo or wrong server
    )
    
    login = mt5.login(creds)
    # login.success == False
    # login.error_code == 10014
    # login.error_message == "Invalid server"
    ```
    
    **Why this fails:** The `server` field must match the broker server name **exactly** as shown in the MT5 terminal's login screen. Even a small typo will cause authentication to fail.

!!! failure "Skipping `login()` and calling operations directly"
    ```python
    mt5.initialize(creds)
    res = mt5.positions()  # fails — not authenticated
    # res.success == False
    # res.error_code varies by operation
    ```
    
    **Why this fails:** Most operations require authentication. The broker won't return data for an unauthenticated session.

---

## Misuse example with failure result

This example shows what happens when you violate the lifecycle order:

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),
    server="Broker-Demo",
)

mt5 = MetaTrader5Client()

# ❌ WRONG: Calling positions() before initialize()
res = mt5.positions()
print(f"Success: {res.success}")
print(f"Error code: {res.error_code}")
print(f"Error message: {res.error_message}")
print(f"Operation: {res.operation}")
```

```text title="Output"
Success: False
Error code: -10
Error message: Client not initialized. Call initialize() first.
Operation: positions_get
```

**The SDK protects you** by failing fast with a clear error message. You don't get a cryptic crash — you get a `Result` that tells you exactly what went wrong.

---

## Debug mode

Enable per-call timing and status logging:

```python
with MetaTrader5Client(debug=True) as mt5:
    mt5.initialize(creds)
    mt5.login(creds)
    mt5.positions()
```

```text title="Output"
[MT5] initialize | success | code=0 | 142ms
[MT5] login | success | code=0 | 87ms
[MT5] positions_get | success | code=0 | 12ms
```

!!! info
    Logs are emitted at `DEBUG` level via the `syntiq_mt5` logger.
