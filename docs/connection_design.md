MT5 Python API has untyped, unclear connection/login behavior.
We provide a deterministic, typed connection interface.

---

## Next Decisions

### 1. Error Structure
We need to define what information is exposed when MT5 fails.

Fields to decide:
- error_code (from mt5.last_error)
- error_message
- stage ("init" | "login")

---

### 2. initialize() Contract
Current ambiguity:
- Accepts None → unclear meaning

Options:
- Require credentials (simpler)
- Allow None → reuse existing session (needs clear logic)

Decision pending.

---

### 3. MT5 Error Integration
Currently:
- Errors are generic strings

Problem:
- Losing mt5.last_error() info

Need:
- Capture and expose MT5 error code + message

---
## Next Steps
[Getting Started](getting-started.md)