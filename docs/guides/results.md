# Results Model

The package avoids exposing raw MT5 return values directly. Instead, public
operations return typed result objects with explicit success and error state.

## `OperationResult[T]`

Most read operations return `OperationResult[T]`.

Typical fields:

- `success`
- `data`
- `error_code`
- `error_message`
- `message`
- `failed`
- `describe_error()`
- `unwrap()`
- `expect(message)`

Example:

```python
from metatrader5_wrapper import account_info

result = account_info()

if result.success and result.data is not None:
    print(result.data.balance)
else:
    print(result.error_code, result.error_message)
```

Fail-fast helpers:

```python
from metatrader5_wrapper import account_info

account = account_info().expect("Account is required before placing orders")
print(account.balance)
```

Use these helpers when failure should immediately stop the current flow. Keep
checking `success` manually when you want to recover or branch.

## `ConnectionResult`

Connection operations return `ConnectionResult`, which includes an additional
`stage` field to show whether the failure happened during initialize or login.

```python
from metatrader5_wrapper import initialize

result = initialize()

if result.failed:
    print(result.describe_error())
```

## Why this matters

The official MT5 API exposes failures through `last_error()`, which can be
overwritten by the next call. This wrapper captures that error state
immediately and binds it to the returned result object.