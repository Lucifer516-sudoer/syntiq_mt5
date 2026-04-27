# Connection

---
## Next Steps
[Results Model](results.md)

The wrapper keeps connection logic explicit. MetaTrader 5 initialization and
account login are treated as separate stages so failures can be reported with a
clear `stage`, `error_code`, and `error_message`.

## `initialize(credentials=None)`

`initialize()` starts the MetaTrader 5 terminal. When credentials are provided,
the wrapper initializes the terminal first and then performs login.

```python
from metatrader5_wrapper import initialize

result = initialize()
```

With credentials:

```python
from metatrader5_wrapper import LoginCredential, initialize
from pydantic import SecretStr

credentials = LoginCredential(
    login=12345678,
    password=SecretStr("password"),
    server="Broker-Demo",
)

result = initialize(credentials)
```

## `login(credentials)`

Use `login()` when the terminal is already initialized and you want an explicit
login step.

## `shutdown()`

Always shut down the MT5 session when you are done, unless your application is
intentionally keeping the terminal open.

```python
from metatrader5_wrapper import shutdown

shutdown_result = shutdown()
```

## Failure handling

Connection failures return `ConnectionResult` instead of raising automatically.
That makes it straightforward to surface the raw MT5 error while keeping a
consistent application flow.

```python
result = initialize(credentials)

if result.failed:
    print(result.stage)
    print(result.error_code)
    print(result.error_message)
```