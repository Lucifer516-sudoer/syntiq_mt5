"""High-level client for the MetaTrader 5 SDK.

This module exposes ``MetaTrader5Client``, the primary entry point for all
SDK operations.  It composes the individual service classes and adds:

- Lifecycle guards (operations fail fast if ``initialize()`` was not called)
- Optional debug logging with per-call timing
- Context manager support for automatic shutdown

Typical usage::

    from syntiq_mt5 import MetaTrader5Client, LoginCredential

    creds = LoginCredential(login=12345, password="secret", server="Demo")

    with MetaTrader5Client() as client:
        client.initialize(creds)
        client.login(creds)

        result = client.positions()
        if result.success:
            for pos in result.data:
                print(pos.symbol, pos.pips_profit)
"""

from __future__ import annotations

import logging
from datetime import datetime
from time import perf_counter

from syntiq_mt5._core.errors import MT5ErrorInfo
from syntiq_mt5._core.execution import Result
from syntiq_mt5.account.models import AccountInfo
from syntiq_mt5.account.service import AccountService
from syntiq_mt5.connection.models import LoginCredential
from syntiq_mt5.connection.service import ConnectionService
from syntiq_mt5.history.models import Deal
from syntiq_mt5.history.service import HistoryService
from syntiq_mt5.market.candles import Candle
from syntiq_mt5.market.symbols import MarketService
from syntiq_mt5.market_book.models import BookEntry
from syntiq_mt5.market_book.service import MarketBookService
from syntiq_mt5.orders.models import HistoricalOrder, Order, TradeRequest, TradeResult
from syntiq_mt5.orders.service import OrderService
from syntiq_mt5.positions.models import Position
from syntiq_mt5.positions.service import PositionService
from syntiq_mt5.symbols.models import SymbolInfo, SymbolTick
from syntiq_mt5.symbols.service import SymbolService
from syntiq_mt5.terminal.models import TerminalInfo
from syntiq_mt5.terminal.service import TerminalService
from syntiq_mt5.ticks.models import Tick
from syntiq_mt5.ticks.service import TickService


class MetaTrader5Client:
    """Unified client for all MetaTrader 5 operations.

    Composes the individual service classes (connection, positions, orders,
    history, market data, etc.) behind a single interface.  All methods
    return ``Result[T]`` — never raise — so callers always handle both the
    success and failure paths explicitly.

    Lifecycle
    ---------
    1. ``initialize()`` — connect to the terminal (required before anything else)
    2. ``login()`` — authenticate with the broker (required for trading operations)
    3. (use the client)
    4. ``shutdown()`` — disconnect cleanly

    The client can also be used as a context manager; ``shutdown()`` is
    called automatically on exit regardless of whether an exception occurred.

    Args:
        debug: When ``True``, each operation logs its name, outcome, and
            elapsed time at ``DEBUG`` level via the ``syntiq_mt5`` logger.
    """
    def __init__(self, *, debug: bool = False) -> None:
        """Initialise the client and instantiate all service objects.

        Args:
            debug: Enable per-call DEBUG logging with timing information.
        """
        self.connection = ConnectionService()
        self._positions = PositionService()
        self.market = MarketService()
        self._account = AccountService()
        self._terminal = TerminalService()
        self._symbols = SymbolService()
        self._market_book = MarketBookService()
        self._ticks = TickService()
        self._orders = OrderService()
        self._history = HistoryService()
        self._initialized = False
        self._logged_in = False
        self._debug = debug
        self._logger = logging.getLogger("syntiq_mt5")

    def __enter__(self) -> MetaTrader5Client:
        """Support ``with MetaTrader5Client() as client:`` usage."""
        return self

    def __exit__(self, *_: object) -> None:
        """Call ``shutdown()`` automatically when leaving the context block."""
        shutdown_result = self.shutdown()
        if self._debug and not shutdown_result.success:
            self._logger.error("[MT5] shutdown | failure | code=%s", shutdown_result.error_code)

    def _log_result(self, name: str, result: Result[object] | Result[None], started: float) -> None:
        """Emit a DEBUG log entry for a completed operation.

        Only active when ``debug=True``.  Logs the operation name, success
        or failure status, error code, and elapsed time in milliseconds.
        """
        if not self._debug:
            return
        elapsed_ms = int((perf_counter() - started) * 1000)
        status = "success" if result.success else "failure"
        code = 0 if result.success else result.error_code
        self._logger.debug("[MT5] %s | %s | code=%s | %sms", name, status, code, elapsed_ms)

    def _guard_initialized(self, operation: str) -> Result[None] | None:
        """Return a failure result if the client has not been initialised.

        Returns ``None`` when the guard passes (client is ready), or a
        ``Result`` with error code ``-10`` when it fails.  Callers check
        the return value and short-circuit if it is not ``None``.
        """
        if self._initialized:
            return None
        return Result.fail(
            MT5ErrorInfo(code=-10, message="Client not initialized. Call initialize() first."),
            context=operation,
            operation=operation,
        )

    def _guard_result(self, operation: str) -> Result[object] | None:
        """Variant of ``_guard_initialized`` that returns ``Result[object]``.

        Used by methods that need to propagate the guard failure through a
        ``Result[T]`` with a generic type parameter.
        """
        guard = self._guard_initialized(operation)
        if guard is None:
            return None
        return Result.fail(
            MT5ErrorInfo(
                code=guard.error_code or -10,
                message=guard.error_message or "Client not initialized. Call initialize() first.",
            ),
            context=operation,
            operation=operation,
        )

    def initialize(self, credentials: LoginCredential | None = None) -> Result[None]:
        """Connect to the MetaTrader 5 terminal.

        Must be called before any other operation.  Sets the internal
        ``_initialized`` flag on success so subsequent calls to other
        methods are permitted.

        Args:
            credentials: Optional credentials; only ``path`` is used here
                to locate the terminal executable.

        Returns:
            ``Result[None]``: Success if the terminal connected.
        """
        started = perf_counter()
        result = self.connection.initialize(credentials)
        self._initialized = result.success
        self._log_result("initialize", result, started)
        return result

    def login(self, credentials: LoginCredential) -> Result[None]:
        """Authenticate with the broker.

        Requires a prior successful ``initialize()`` call.

        Args:
            credentials: Account number, password, and server name.

        Returns:
            ``Result[None]``: Success if authentication succeeded.
        """
        guard = self._guard_initialized("login")
        if guard is not None:
            self._log_result("login", guard, perf_counter())
            return guard
        started = perf_counter()
        result = self.connection.login(credentials)
        self._logged_in = result.success
        self._log_result("login", result, started)
        return result

    def shutdown(self) -> Result[None]:
        """Disconnect from the MetaTrader 5 terminal.

        Resets ``_initialized`` and ``_logged_in`` regardless of outcome.
        Safe to call multiple times.

        Returns:
            ``Result[None]``: Success in almost all cases.
        """
        started = perf_counter()
        result = self.connection.shutdown()
        self._initialized = False
        self._logged_in = False
        self._log_result("shutdown", result, started)
        return result

    def version(self) -> Result[tuple[int, int, str]]:
        """Return the connected terminal's version information.

        Returns:
            ``Result[tuple[int, int, str]]``: ``(build, date, version_string)`` on success.
        """
        guard = self._guard_result("version")
        if guard is not None:
            return Result[tuple[int, int, str]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.connection.version()
        self._log_result("version", Result[object].model_validate(result.model_dump()), started)
        return result

    def positions(self, symbol: str | None = None) -> Result[list[Position]]:
        """Retrieve all open positions, optionally filtered by symbol.

        Args:
            symbol: If provided, only positions for this symbol are returned.

        Returns:
            ``Result[list[Position]]``: Open positions on success (may be empty).
        """
        guard = self._guard_result("positions_get")
        if guard is not None:
            return Result[list[Position]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._positions.positions(symbol=symbol)
        self._log_result("positions_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def positions_total(self) -> Result[int]:
        """Return the total number of open positions.

        Returns:
            ``Result[int]``: Count of open positions on success.
        """
        guard = self._guard_result("positions_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._positions.positions_total()
        self._log_result("positions_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        """Retrieve the most recent OHLCV candles for a symbol.

        Args:
            symbol: Trading instrument name (e.g. ``"EURUSD"``).
            timeframe: MT5 timeframe constant (e.g. ``constants.TIMEFRAME_H1``).
            count: Number of bars to retrieve.

        Returns:
            ``Result[list[Candle]]``: Candles in chronological order on success.
        """
        guard = self._guard_result("copy_rates_from_pos")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.get_candles(symbol=symbol, timeframe=timeframe, count=count)
        self._log_result(
            "copy_rates_from_pos", Result[object].model_validate(result.model_dump()), started
        )
        return result

    # ── Account ───────────────────────────────────────────────────────────────

    def account_info(self) -> Result[AccountInfo]:
        """Retrieve the current trading account details.

        Returns:
            ``Result[AccountInfo]``: Account state including balance, equity,
            and margin on success.
        """
        guard = self._guard_result("account_info")
        if guard is not None:
            return Result[AccountInfo].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._account.account_info()
        self._log_result("account_info", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── Terminal ──────────────────────────────────────────────────────────────

    def terminal_info(self) -> Result[TerminalInfo]:
        """Retrieve the connected terminal's configuration and state.

        Returns:
            ``Result[TerminalInfo]``: Terminal details including connection
            status and trading permissions on success.
        """
        guard = self._guard_result("terminal_info")
        if guard is not None:
            return Result[TerminalInfo].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._terminal.terminal_info()
        self._log_result("terminal_info", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── Symbols ───────────────────────────────────────────────────────────────

    def symbols_total(self) -> Result[int]:
        """Return the total number of symbols available in the terminal.

        Returns:
            ``Result[int]``: Symbol count on success.
        """
        guard = self._guard_result("symbols_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbols_total()
        self._log_result("symbols_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbols_get(self, group: str | None = None) -> Result[list[str]]:
        """Retrieve symbol names, optionally filtered by group pattern.

        Args:
            group: Wildcard filter pattern (e.g. ``"*USD*"``).  When
                ``None``, all available symbols are returned.

        Returns:
            ``Result[list[str]]``: List of symbol names on success.
        """
        guard = self._guard_result("symbols_get")
        if guard is not None:
            return Result[list[str]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbols_get(group=group)
        self._log_result("symbols_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbol_select(self, symbol: str, enable: bool) -> Result[bool]:
        """Add or remove a symbol from the Market Watch window.

        Args:
            symbol: Trading instrument name.
            enable: ``True`` to add the symbol; ``False`` to remove it.

        Returns:
            ``Result[bool]``: ``True`` on success.
        """
        guard = self._guard_result("symbol_select")
        if guard is not None:
            return Result[bool].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbol_select(symbol=symbol, enable=enable)
        self._log_result("symbol_select", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbol_info(self, symbol: str) -> Result[SymbolInfo]:
        """Retrieve full specification data for a symbol.

        Args:
            symbol: Trading instrument name.

        Returns:
            ``Result[SymbolInfo]``: Symbol specification on success.
        """
        guard = self._guard_result("symbol_info")
        if guard is not None:
            return Result[SymbolInfo].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbol_info(symbol=symbol)
        self._log_result("symbol_info", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbol_info_tick(self, symbol: str) -> Result[SymbolTick]:
        """Retrieve the latest tick for a symbol.

        Args:
            symbol: Trading instrument name.

        Returns:
            ``Result[SymbolTick]``: The most recent bid/ask/last prices on success.
        """
        guard = self._guard_result("symbol_info_tick")
        if guard is not None:
            return Result[SymbolTick].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbol_info_tick(symbol=symbol)
        self._log_result("symbol_info_tick", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── Market Book ───────────────────────────────────────────────────────────

    def market_book_add(self, symbol: str) -> Result[bool]:
        """Subscribe to market depth (DOM) updates for a symbol.

        Must be called before ``market_book_get()`` for the same symbol.

        Args:
            symbol: Trading instrument name.

        Returns:
            ``Result[bool]``: ``True`` if the subscription was accepted.
        """
        guard = self._guard_result("market_book_add")
        if guard is not None:
            return Result[bool].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._market_book.market_book_add(symbol=symbol)
        self._log_result("market_book_add", Result[object].model_validate(result.model_dump()), started)
        return result

    def market_book_get(self, symbol: str) -> Result[list[BookEntry]]:
        """Retrieve the current market depth snapshot for a symbol.

        Requires a prior ``market_book_add()`` call for the same symbol.

        Args:
            symbol: Trading instrument name.

        Returns:
            ``Result[list[BookEntry]]``: All DOM entries on success.
        """
        guard = self._guard_result("market_book_get")
        if guard is not None:
            return Result[list[BookEntry]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._market_book.market_book_get(symbol=symbol)
        self._log_result("market_book_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def market_book_release(self, symbol: str) -> Result[bool]:
        """Unsubscribe from market depth updates for a symbol.

        Args:
            symbol: Trading instrument name.

        Returns:
            ``Result[bool]``: ``True`` if the subscription was released.
        """
        guard = self._guard_result("market_book_release")
        if guard is not None:
            return Result[bool].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._market_book.market_book_release(symbol=symbol)
        self._log_result("market_book_release", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── Historical Rates ──────────────────────────────────────────────────────

    def copy_rates_from(
        self, symbol: str, timeframe: int, date_from: datetime, count: int
    ) -> Result[list[Candle]]:
        """Retrieve candles starting from a specific datetime.

        Args:
            symbol: Trading instrument name.
            timeframe: MT5 timeframe constant.
            date_from: Start datetime (inclusive).
            count: Number of bars to retrieve going forward.

        Returns:
            ``Result[list[Candle]]``: Candles in chronological order on success.
        """
        guard = self._guard_result("copy_rates_from")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.copy_rates_from(
            symbol=symbol, timeframe=timeframe, date_from=date_from, count=count
        )
        self._log_result("copy_rates_from", Result[object].model_validate(result.model_dump()), started)
        return result

    def copy_rates_range(
        self, symbol: str, timeframe: int, date_from: datetime, date_to: datetime
    ) -> Result[list[Candle]]:
        """Retrieve all candles within a datetime range.

        Args:
            symbol: Trading instrument name.
            timeframe: MT5 timeframe constant.
            date_from: Range start datetime (inclusive).
            date_to: Range end datetime (inclusive).

        Returns:
            ``Result[list[Candle]]``: Candles in chronological order on success.
        """
        guard = self._guard_result("copy_rates_range")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.copy_rates_range(
            symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to
        )
        self._log_result("copy_rates_range", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── Tick Data ─────────────────────────────────────────────────────────────

    def copy_ticks_from(
        self, symbol: str, date_from: datetime, count: int, flags: int
    ) -> Result[list[Tick]]:
        """Retrieve ticks starting from a specific datetime.

        Args:
            symbol: Trading instrument name.
            date_from: Start datetime (inclusive).
            count: Maximum number of ticks to retrieve.
            flags: ``COPY_TICKS_*`` constant controlling which ticks to include.

        Returns:
            ``Result[list[Tick]]``: Ticks in chronological order on success.
        """
        guard = self._guard_result("copy_ticks_from")
        if guard is not None:
            return Result[list[Tick]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._ticks.copy_ticks_from(
            symbol=symbol, date_from=date_from, count=count, flags=flags
        )
        self._log_result("copy_ticks_from", Result[object].model_validate(result.model_dump()), started)
        return result

    def copy_ticks_range(
        self, symbol: str, date_from: datetime, date_to: datetime, flags: int
    ) -> Result[list[Tick]]:
        """Retrieve all ticks within a datetime range.

        Args:
            symbol: Trading instrument name.
            date_from: Range start datetime (inclusive).
            date_to: Range end datetime (inclusive).
            flags: ``COPY_TICKS_*`` constant controlling which ticks to include.

        Returns:
            ``Result[list[Tick]]``: Ticks in chronological order on success.
        """
        guard = self._guard_result("copy_ticks_range")
        if guard is not None:
            return Result[list[Tick]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._ticks.copy_ticks_range(
            symbol=symbol, date_from=date_from, date_to=date_to, flags=flags
        )
        self._log_result("copy_ticks_range", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── Orders ────────────────────────────────────────────────────────────────

    def orders_total(self) -> Result[int]:
        """Return the total number of active pending orders.

        Returns:
            ``Result[int]``: Count of pending orders on success.
        """
        guard = self._guard_result("orders_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.orders_total()
        self._log_result("orders_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def orders_get(
        self, symbol: str | None = None, group: str | None = None, ticket: int | None = None
    ) -> Result[list[Order]]:
        """Retrieve active pending orders with optional filtering.

        At most one filter argument should be provided.  When none are
        given, all active orders are returned.

        Args:
            symbol: Filter by trading instrument name.
            group: Filter by symbol group wildcard pattern.
            ticket: Filter by order ticket number.

        Returns:
            ``Result[list[Order]]``: Active orders on success (may be empty).
        """
        guard = self._guard_result("orders_get")
        if guard is not None:
            return Result[list[Order]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.orders_get(symbol=symbol, group=group, ticket=ticket)
        self._log_result("orders_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_calc_margin(self, action: int, symbol: str, volume: float, price: float) -> Result[float]:
        """Calculate the margin required for a hypothetical order.

        Args:
            action: Trade action type (``TRADE_ACTION_DEAL`` or ``TRADE_ACTION_PENDING``).
            symbol: Trading instrument name.
            volume: Order volume in lots.
            price: Intended execution price.

        Returns:
            ``Result[float]``: Required margin in account currency on success.
        """
        guard = self._guard_result("order_calc_margin")
        if guard is not None:
            return Result[float].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_calc_margin(action=action, symbol=symbol, volume=volume, price=price)
        self._log_result("order_calc_margin", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_calc_profit(
        self, action: int, symbol: str, volume: float, price_open: float, price_close: float
    ) -> Result[float]:
        """Calculate the profit for a hypothetical trade.

        Args:
            action: Trade action type (``TRADE_ACTION_DEAL``).
            symbol: Trading instrument name.
            volume: Trade volume in lots.
            price_open: Hypothetical entry price.
            price_close: Hypothetical exit price.

        Returns:
            ``Result[float]``: Estimated profit in account currency on success.
        """
        guard = self._guard_result("order_calc_profit")
        if guard is not None:
            return Result[float].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_calc_profit(
            action=action, symbol=symbol, volume=volume, price_open=price_open, price_close=price_close
        )
        self._log_result("order_calc_profit", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_check(self, request: TradeRequest) -> Result[TradeResult]:
        """Validate a trade request without submitting it.

        Useful for pre-flight checks before calling ``order_send()``.

        Args:
            request: The trade request to validate.

        Returns:
            ``Result[TradeResult]``: Validation outcome including margin
            requirements and any rejection reason on success.
        """
        guard = self._guard_result("order_check")
        if guard is not None:
            return Result[TradeResult].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_check(request=request)
        self._log_result("order_check", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_send(self, request: TradeRequest) -> Result[TradeResult]:
        """Submit a trade request to the broker.

        Args:
            request: The trade request to execute.  Use ``TradeRequest``
                with typed enum fields for ``action``, ``type``,
                ``type_filling``, and ``type_time``.

        Returns:
            ``Result[TradeResult]``: Execution outcome including the deal
            and order tickets on success.  Check ``result.data.is_successful``
            for the broker's acceptance status.
        """
        guard = self._guard_result("order_send")
        if guard is not None:
            return Result[TradeResult].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_send(request=request)
        self._log_result("order_send", Result[object].model_validate(result.model_dump()), started)
        return result

    # ── History ───────────────────────────────────────────────────────────────

    def history_orders_total(self, date_from: datetime, date_to: datetime) -> Result[int]:
        """Return the number of historical orders in a date range.

        Args:
            date_from: Range start (inclusive).
            date_to: Range end (inclusive).

        Returns:
            ``Result[int]``: Count of historical orders on success.
        """
        guard = self._guard_result("history_orders_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_orders_total(date_from=date_from, date_to=date_to)
        self._log_result("history_orders_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def history_orders_get(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Result[list[HistoricalOrder]]:
        """Retrieve historical orders with flexible filtering.

        Exactly one filter strategy must be provided: either a date range
        (``date_from`` + ``date_to``), a group pattern, a ticket, or a
        position ticket.

        Args:
            date_from: Range start (used with ``date_to``).
            date_to: Range end (used with ``date_from``).
            group: Symbol group wildcard pattern.
            ticket: Order ticket number.
            position: Position ticket to retrieve orders for.

        Returns:
            ``Result[list[HistoricalOrder]]``: Matching orders on success.
        """
        guard = self._guard_result("history_orders_get")
        if guard is not None:
            return Result[list[HistoricalOrder]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_orders_get(
            date_from=date_from, date_to=date_to, group=group, ticket=ticket, position=position
        )
        self._log_result("history_orders_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def history_deals_total(self, date_from: datetime, date_to: datetime) -> Result[int]:
        """Return the number of deals in a date range.

        Args:
            date_from: Range start (inclusive).
            date_to: Range end (inclusive).

        Returns:
            ``Result[int]``: Count of deals on success.
        """
        guard = self._guard_result("history_deals_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_deals_total(date_from=date_from, date_to=date_to)
        self._log_result("history_deals_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def history_deals_get(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Result[list[Deal]]:
        """Retrieve deals from the trade history with flexible filtering.

        Exactly one filter strategy must be provided: either a date range,
        a group pattern, a deal ticket, or a position ticket.

        Args:
            date_from: Range start (used with ``date_to``).
            date_to: Range end (used with ``date_from``).
            group: Symbol group wildcard pattern.
            ticket: Deal ticket number.
            position: Position ticket to retrieve deals for.

        Returns:
            ``Result[list[Deal]]``: Matching deals on success.
        """
        guard = self._guard_result("history_deals_get")
        if guard is not None:
            return Result[list[Deal]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_deals_get(
            date_from=date_from, date_to=date_to, group=group, ticket=ticket, position=position
        )
        self._log_result("history_deals_get", Result[object].model_validate(result.model_dump()), started)
        return result
