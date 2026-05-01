# Core

Result[T], errors, and execution primitives.

---

## Result[T]

### Result

::: syntiq_mt5._core.execution.Result
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Errors

### MT5Error

::: syntiq_mt5._core.errors.MT5Error
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### MT5ConnectionError

::: syntiq_mt5._core.errors.MT5ConnectionError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### MT5ExecutionError

::: syntiq_mt5._core.errors.MT5ExecutionError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

### MT5ErrorInfo

::: syntiq_mt5._core.errors.MT5ErrorInfo
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

Every operation returns `Result[T]`:

```python
res = mt5.positions()

if res.success:
    # Success path
    for p in res.data:
        print(p.symbol)
else:
    # Failure path
    print(f"Operation: {res.operation}")
    print(f"Error code: {res.error_code}")
    print(f"Message: {res.error_message}")
```

Exceptions are reserved for unrecoverable situations (e.g., during object construction). You will not encounter them in normal usage.
