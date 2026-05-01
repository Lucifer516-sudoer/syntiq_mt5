# Terminal

Terminal state and configuration.

---

## Models

### TerminalInfo

::: syntiq_mt5.terminal.models.TerminalInfo
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Service

### TerminalService

::: syntiq_mt5.terminal.service.TerminalService
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

---

## Usage

```python
res = mt5.terminal_info()

if res.success:
    term = res.data
    print(f"Build: {term.build}")
    print(f"Connected: {term.connected}")
    print(f"Ready for trading: {term.is_ready_for_trading}")
    print(f"Ping: {term.ping_last} ms")
```
