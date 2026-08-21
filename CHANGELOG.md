# Changelog

All notable changes to this project are documented in this file.

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-22

### Changed

- Replaced the public `Result[T]` contract with direct typed return values and
  typed `MT5Error` exceptions.
- Introduced the managed `MT5` session as the primary public interface.
- Moved native access behind an injectable, lazy, process-serialized adapter.
- Changed collection results to immutable tuples and kept empty results distinct
  from native failure sentinels.
- Made recent candle retrieval exclude the still-forming current bar by default.
- Required timezone-aware datetimes and normalized them to UTC.

### Fixed

- Modeled `order_check()` with its real projected-account response shape instead
  of reusing the `order_send()` result.
- Treated `False` from symbol selection and market-book operations as failure.
- Corrected margin and profit calculation parameters to use order types.
- Corrected history group filtering so it accompanies a date range.
- Corrected signed deal-fee handling in `Deal.net_profit`.
- Preserved MT5 trade placement and partial-fill responses as accepted outcomes.

### Project

- Added a committed uv lockfile and Ruff formatting workflow.
- Added Linux and Windows CI on Python 3.12 and 3.13.
- Added strict documentation and wheel installation checks.
- Added GitHub Pages deployment and tag-gated PyPI trusted publishing.
- Rebuilt the README, examples, MkDocs journey, and contributor documentation.

## [0.1.0] - 2026-04-30

- Initial release of syntiq-mt5.
- Clean MetaTrader5 client abstraction.
- Result[T] based error handling.
- Typed models for positions and candles.
- Consistent service-based architecture.
- Documentation and examples included.
