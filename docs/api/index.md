# API Reference

Complete API documentation for all public modules, classes, and methods.

---

## Overview

The syntiq-mt5 API is organized into focused modules:

<div class="grid cards" markdown>

-   :material-application:{ .lg .middle } __[Client](client.md)__

    ---

    Main entry point — `MetaTrader5Client` with all operations

-   :material-account-cash:{ .lg .middle } __[Account](account.md)__

    ---

    Account information models and services

-   :material-chart-line:{ .lg .middle } __[Positions](positions.md)__

    ---

    Open position models and retrieval

-   :material-candlestick:{ .lg .middle } __[Market](market.md)__

    ---

    Candles, rates, and market data

-   :material-cash-multiple:{ .lg .middle } __[Orders](orders.md)__

    ---

    Order placement, validation, and management

-   :material-history:{ .lg .middle } __[History](history.md)__

    ---

    Historical orders and deals

-   :material-currency-usd:{ .lg .middle } __[Symbols](symbols.md)__

    ---

    Symbol information and specifications

-   :material-chart-scatter-plot:{ .lg .middle } __[Ticks](ticks.md)__

    ---

    Raw tick data retrieval

-   :material-monitor:{ .lg .middle } __[Terminal](terminal.md)__

    ---

    Terminal state and configuration

-   :material-book-open:{ .lg .middle } __[Market Book](market-book.md)__

    ---

    Level 2 order book data

-   :material-connection:{ .lg .middle } __[Connection](connection.md)__

    ---

    Connection lifecycle and credentials

-   :material-cog:{ .lg .middle } __[Core](core.md)__

    ---

    Result[T], errors, and execution primitives

</div>

---

## Usage Pattern

All API methods follow the same pattern:

```python
from syntiq_mt5 import MetaTrader5Client

with MetaTrader5Client() as mt5:
    result = mt5.some_operation()
    
    if result.success:
        # Use result.data
        print(result.data)
    else:
        # Handle error
        print(f"Error {result.error_code}: {result.error_message}")
```

Every method returns `Result[T]` — never raises exceptions for operational failures.
