# Changelog

All notable changes to this project are documented in this file.

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-30

### Added - Full MT5 API Coverage

#### Account & Terminal
- `account_info()` - Retrieve account balance, equity, margin, and leverage
- `terminal_info()` - Get terminal version, build, and connection status
- `AccountInfo` model with computed properties for margin usage and equity ratios
- `TerminalInfo` model with trading readiness checks

#### Symbol Operations
- `symbols_total()` - Count available symbols
- `symbols_get()` - List all symbols or filter by group
- `symbol_select()` - Enable/disable symbols for trading
- `symbol_info()` - Get detailed symbol specifications
- `symbol_info_tick()` - Retrieve current tick data
- `SymbolInfo` model with 100+ fields and computed properties
- `SymbolTick` model with spread and mid-price calculations

#### Market Data Extensions
- `copy_rates_from()` - Get candles from specific date
- `copy_rates_range()` - Get candles in date range
- `copy_ticks_from()` - Retrieve tick data from specific date
- `copy_ticks_range()` - Retrieve tick data in date range
- `Tick` model with flag-based filtering and computed properties

#### Order Management
- `orders_total()` - Count pending orders
- `orders_get()` - Retrieve pending orders with filtering
- `order_calc_margin()` - Calculate required margin
- `order_calc_profit()` - Calculate expected profit
- `order_check()` - Validate order before sending
- `order_send()` - Execute trade orders
- `Order` model with state checking properties
- `TradeRequest` model for order parameters
- `TradeResult` model with success/failure checks

#### Trading History
- `history_orders_total()` - Count historical orders
- `history_orders_get()` - Retrieve historical orders
- `history_deals_total()` - Count historical deals
- `history_deals_get()` - Retrieve historical deals
- `HistoricalOrder` model with duration calculations
- `Deal` model with net profit calculations including commission and swap

#### Market Depth
- `market_book_add()` - Subscribe to Level 2 order book
- `market_book_get()` - Retrieve order book entries
- `market_book_release()` - Unsubscribe from order book
- `BookEntry` model with buy/sell identification

### Documentation
- Added 6 new task pages: account info, symbols, ticks, history, orders, market book
- Updated navigation in mkdocs.yml
- Updated README with complete public API listing
- Added full_api_demo.py example demonstrating all features

### Architecture
- Maintained strict Result[T] pattern across all new features
- Followed model → service → client layered architecture
- All MT5 calls use _core.raw.call_mt5 wrapper
- Comprehensive error handling with operation metadata
- Type-safe with mypy validation passing

## [0.1.0] - 2026-04-30

- Initial release of syntiq-mt5.
- Clean MetaTrader5 client abstraction.
- Result[T] based error handling.
- Typed models for positions and candles.
- Consistent service-based architecture.
- Documentation and examples included.
