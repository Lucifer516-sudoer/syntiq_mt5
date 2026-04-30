# Task: Handle errors

Handle failures with clear operation context.

```python
res = mt5.login(creds)
if not res.success:
    print(f"{res.operation} failed: {res.error_code} {res.error_message}")
```

Output example:

```text
login failed: 10013 Invalid account
```
