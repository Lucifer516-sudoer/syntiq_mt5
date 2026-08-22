"""Developer-facing MetaTrader 5 session.

The session is the package's deep module: it owns lifecycle, operation-specific
failure rules, UTC validation, raw payload conversion, and market-book cleanup.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from datetime import UTC, datetime
from threading import Lock
from typing import Any, TypeVar, cast

from pydantic import ValidationError

from syntiq_mt5._internal.model import MT5Model
from syntiq_mt5._internal.native import DEFAULT_ADAPTER
from syntiq_mt5.account.models import AccountInfo
from syntiq_mt5.adapter import MT5Adapter
from syntiq_mt5.connection.models import LoginCredential
from syntiq_mt5.enums import OrderType
from syntiq_mt5.errors import (
    ErrorInfo,
    MT5CallError,
    MT5PayloadError,
    MT5PlatformError,
    MT5StateError,
)
from syntiq_mt5.history.models import Deal
from syntiq_mt5.market.candles import Candle
from syntiq_mt5.market_book.models import BookEntry
from syntiq_mt5.orders.models import (
    HistoricalOrder,
    Order,
    TradeCheckResult,
    TradeRequest,
    TradeResult,
)
from syntiq_mt5.positions.models import Position
from syntiq_mt5.symbols.models import SymbolInfo, SymbolTick
from syntiq_mt5.terminal.models import TerminalInfo
from syntiq_mt5.ticks.models import Tick

ModelT = TypeVar("ModelT", bound=MT5Model)


class SyntiqMT5:
    """A managed, typed session over the process-global MT5 terminal.

    Pass credentials to the constructor for the common one-step context-manager
    flow, or call :meth:`initialize` and :meth:`login` explicitly. Only one
    native session may be active in a process at a time.

    All terminal operations share one error contract. Inactive sessions raise
    :class:`MT5StateError`; unavailable native integration raises
    :class:`MT5PlatformError`; native failures raise :class:`MT5CallError`; and
    invalid native response shapes raise :class:`MT5PayloadError`. Invalid
    caller values such as naive datetimes or non-positive counts raise
    :class:`ValueError` before crossing the adapter seam.
    """

    _lease = Lock()

    def __init__(
        self,
        credentials: LoginCredential | None = None,
        *,
        adapter: MT5Adapter | None = None,
    ) -> None:
        """Create a session without connecting until ``initialize`` or entry.

        Args:
            credentials: Optional credentials used when entering the context.
            adapter: Alternate transport, typically a deterministic test fake.

        """
        self._credentials = credentials
        self._adapter = adapter or DEFAULT_ADAPTER
        self._active = False
        self._owns_lease = False
        self._symbol_cache: dict[str, tuple[int, float]] = {}
        self._last_error = ErrorInfo(code=1, message="Success")

    def __enter__(self) -> SyntiqMT5:
        """Initialize the configured terminal and return this active session."""
        if self._active:
            raise MT5StateError(
                "context_enter",
                -10,
                "this MT5 session is already active and cannot be re-entered",
            )
        self.initialize(self._credentials)
        return self

    def __exit__(self, *_: object) -> None:
        """Shut down the terminal when leaving the managed context."""
        self.shutdown()

    @property
    def connected(self) -> bool:
        """Whether this object currently owns an initialized MT5 session."""
        return self._active

    def initialize(self, credentials: LoginCredential | None = None) -> None:
        """Initialize MT5, optionally authenticating in the same native call.

        Args:
            credentials: Optional terminal path and account credentials passed
                to the official ``initialize`` operation.

        Raises:
            MT5StateError: If another session owns the process-global terminal.
            MT5CallError: If native initialization fails.
            MT5PlatformError: If the official package is unavailable.

        The process lease is released automatically when initialization fails.
        Calling this method on an already active session is a no-op.
        """
        if self._active:
            return
        if not self._lease.acquire(blocking=False):
            raise MT5StateError(
                "initialize",
                -10,
                "another MT5 session already owns the process-global terminal",
            )
        self._owns_lease = True
        try:
            kwargs: dict[str, object] = {}
            args: tuple[object, ...] = ()
            if credentials is not None:
                kwargs = {
                    "login": credentials.login,
                    "password": credentials.password.get_secret_value(),
                    "server": credentials.server,
                    "timeout": credentials.timeout,
                    "portable": credentials.portable,
                }
                if credentials.path:
                    args = (credentials.path,)
            self._call_bool("initialize", *args, **kwargs)
            self._active = True
            self._credentials = credentials
        except Exception:
            self._release_lease()
            raise

    def login(self, credentials: LoginCredential) -> None:
        """Authenticate the initialized terminal with a trading account.

        Args:
            credentials: Account number, secret password, server, and timeout.

        Raises:
            MT5StateError: If this session has not been initialized.
            MT5CallError: If the terminal cannot authenticate the account.
        """
        self._require_active("login")
        self._call_bool(
            "login",
            login=credentials.login,
            password=credentials.password.get_secret_value(),
            server=credentials.server,
            timeout=credentials.timeout,
        )
        self._credentials = credentials
        self._symbol_cache.clear()

    def shutdown(self) -> None:
        """Close the terminal connection and release process ownership.

        Calling shutdown without an owned lease is a no-op. Local state and the
        process lease are released even when native shutdown raises an error.
        """
        if not self._owns_lease:
            return
        try:
            if self._active:
                self._call("shutdown")
        finally:
            self._active = False
            self._symbol_cache.clear()
            self._release_lease()

    def version(self) -> tuple[int, int, str]:
        """Return ``(terminal_version, build, release_date)``."""
        value = self._call_required("version")
        try:
            version, build, release_date = value
            return int(version), int(build), str(release_date)
        except (TypeError, ValueError) as exc:
            raise self._payload_error("version", exc) from exc

    def account_info(self) -> AccountInfo:
        """Return a snapshot of the currently authenticated trading account."""
        return self._model("account_info", AccountInfo)

    def terminal_info(self) -> TerminalInfo:
        """Return terminal configuration, connectivity, and permission state."""
        return self._model("terminal_info", TerminalInfo)

    def positions(self, symbol: str | None = None) -> tuple[Position, ...]:
        """Return open positions, optionally restricted to one symbol.

        An empty tuple is a successful result. Symbol precision is attached to
        every position so its pip-related convenience properties remain valid.
        """
        kwargs = {"symbol": symbol} if symbol is not None else {}
        rows = self._rows("positions_get", **kwargs)
        try:
            mappings = tuple(self._mapping(row) for row in rows)
            names = tuple(str(row["symbol"]) for row in mappings)
        except (KeyError, TypeError, ValueError) as exc:
            raise self._payload_error("positions_get", exc) from exc
        missing = {name for name in names if name not in self._symbol_cache}
        for name in missing:
            info = self.symbol_info(name)
            self._symbol_cache[name] = (info.digits, info.point)
        return tuple(
            self._parse_model(
                "positions_get",
                Position,
                {
                    **row,
                    "digits": self._symbol_cache[name][0],
                    "point": self._symbol_cache[name][1],
                },
            )
            for row, name in zip(mappings, names, strict=True)
        )

    def positions_total(self) -> int:
        """Return the number of currently open positions."""
        return self._integer("positions_total")

    def symbols_total(self) -> int:
        """Return the number of symbols known to the connected terminal."""
        return self._integer("symbols_total")

    def symbols_get(self, group: str | None = None) -> tuple[SymbolInfo, ...]:
        """Return symbol specifications, optionally filtered by an MT5 group mask.

        Args:
            group: Comma-separated masks applied from left to right. ``*`` is a
                wildcard and ``!`` excludes matches, for example
                ``"*USD*,!USDJPY"``.

        Returns:
            Matching specifications, or an empty tuple when nothing matches.
        """
        kwargs = {"group": group} if group is not None else {}
        return tuple(
            self._parse_model("symbols_get", SymbolInfo, row)
            for row in self._rows("symbols_get", **kwargs)
        )

    def symbol_select(self, symbol: str, enable: bool = True) -> None:
        """Add a symbol to Market Watch or remove it when ``enable`` is false."""
        self._call_bool("symbol_select", symbol, enable)

    def symbol_info(self, symbol: str) -> SymbolInfo:
        """Return the complete terminal specification for ``symbol``."""
        return self._model("symbol_info", SymbolInfo, symbol)

    def symbol_info_tick(self, symbol: str) -> SymbolTick:
        """Return the latest quote tick for ``symbol``."""
        return self._model("symbol_info_tick", SymbolTick, symbol)

    def candles(
        self,
        symbol: str,
        timeframe: int,
        count: int,
        *,
        include_current: bool = False,
    ) -> tuple[Candle, ...]:
        """Return recent candles chronologically.

        Args:
            symbol: Broker-defined instrument name.
            timeframe: One of the exported ``TIMEFRAME_*`` integer constants.
            count: Positive maximum number of candles.
            include_current: Include native position zero, which is still forming.

        Returns:
            Completed candles by default, or an empty tuple when none are loaded.

        Raises:
            ValueError: If ``count`` is not positive.
        """
        if count <= 0:
            raise ValueError("count must be greater than zero")
        start_pos = 0 if include_current else 1
        rows = self._rows("copy_rates_from_pos", symbol, timeframe, start_pos, count)
        return tuple(
            self._parse_model("copy_rates_from_pos", Candle, row) for row in rows
        )

    def copy_rates_from(
        self,
        symbol: str,
        timeframe: int,
        date_from: datetime,
        count: int,
    ) -> tuple[Candle, ...]:
        """Return up to ``count`` bars at or before an aware UTC instant.

        Args:
            symbol: Broker-defined instrument name.
            timeframe: One of the exported ``TIMEFRAME_*`` constants.
            date_from: Timezone-aware upper boundary, normalized to UTC.
            count: Positive maximum number of candles moving into history.

        Raises:
            ValueError: If the datetime is naive or ``count`` is not positive.
        """
        if count <= 0:
            raise ValueError("count must be greater than zero")
        rows = self._rows(
            "copy_rates_from", symbol, timeframe, self._utc(date_from), count
        )
        return tuple(self._parse_model("copy_rates_from", Candle, row) for row in rows)

    def copy_rates_range(
        self,
        symbol: str,
        timeframe: int,
        date_from: datetime,
        date_to: datetime,
    ) -> tuple[Candle, ...]:
        """Return candles whose open times fall in the inclusive UTC range.

        Both boundaries must be timezone-aware and ``date_from`` must not follow
        ``date_to``. An empty tuple is a successful no-data response.
        """
        start, end = self._range(date_from, date_to)
        rows = self._rows("copy_rates_range", symbol, timeframe, start, end)
        return tuple(self._parse_model("copy_rates_range", Candle, row) for row in rows)

    def copy_ticks_from(
        self,
        symbol: str,
        date_from: datetime,
        count: int,
        flags: int,
    ) -> tuple[Tick, ...]:
        """Return up to ``count`` ticks beginning at an aware UTC instant.

        Args:
            symbol: Broker-defined instrument name.
            date_from: Timezone-aware lower boundary, normalized to UTC.
            count: Positive maximum number of ticks.
            flags: One of ``COPY_TICKS_ALL``, ``COPY_TICKS_INFO``, or
                ``COPY_TICKS_TRADE``.

        Raises:
            ValueError: If the datetime is naive or ``count`` is not positive.
        """
        if count <= 0:
            raise ValueError("count must be greater than zero")
        rows = self._rows("copy_ticks_from", symbol, self._utc(date_from), count, flags)
        return tuple(self._parse_model("copy_ticks_from", Tick, row) for row in rows)

    def copy_ticks_range(
        self,
        symbol: str,
        date_from: datetime,
        date_to: datetime,
        flags: int,
    ) -> tuple[Tick, ...]:
        """Return ticks within the supplied timezone-aware date range.

        ``flags`` must be an exported ``COPY_TICKS_*`` value. Both boundaries
        are normalized to UTC and an empty tuple is a valid response.
        """
        start, end = self._range(date_from, date_to)
        rows = self._rows("copy_ticks_range", symbol, start, end, flags)
        return tuple(self._parse_model("copy_ticks_range", Tick, row) for row in rows)

    def market_book_add(self, symbol: str) -> None:
        """Subscribe the terminal to market-depth updates for ``symbol``."""
        self._call_bool("market_book_add", symbol)

    def market_book_get(self, symbol: str) -> tuple[BookEntry, ...]:
        """Return the current market-depth snapshot for a subscribed symbol."""
        return tuple(
            self._parse_model("market_book_get", BookEntry, row)
            for row in self._rows("market_book_get", symbol)
        )

    def market_book_release(self, symbol: str) -> None:
        """Release a previously acquired market-depth subscription."""
        self._call_bool("market_book_release", symbol)

    @contextmanager
    def market_book(self, symbol: str) -> Iterator[SyntiqMT5]:
        """Subscribe to market depth and always release it on context exit."""
        self.market_book_add(symbol)
        try:
            yield self
        finally:
            self.market_book_release(symbol)

    def orders_total(self) -> int:
        """Return the number of active pending orders."""
        return self._integer("orders_total")

    def orders_get(
        self,
        *,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> tuple[Order, ...]:
        """Return active orders selected by at most one supported filter.

        Args:
            symbol: Exact symbol filter.
            group: MT5 wildcard group mask.
            ticket: Exact order ticket.

        Raises:
            ValueError: If more than one filter is supplied.

        """
        selected = [("symbol", symbol), ("group", group), ("ticket", ticket)]
        supplied = [(name, value) for name, value in selected if value is not None]
        if len(supplied) > 1:
            raise ValueError("provide at most one of symbol, group, or ticket")
        kwargs = dict(supplied)
        return tuple(
            self._parse_model("orders_get", Order, row)
            for row in self._rows("orders_get", **kwargs)
        )

    def order_calc_margin(
        self,
        order_type: OrderType | int,
        symbol: str,
        volume: float,
        price: float,
    ) -> float:
        """Calculate required margin for a hypothetical BUY or SELL order.

        ``volume`` is expressed in trading lots, ``price`` in symbol price
        units, and the returned amount in account currency.
        """
        return self._number("order_calc_margin", int(order_type), symbol, volume, price)

    def order_calc_profit(
        self,
        order_type: OrderType | int,
        symbol: str,
        volume: float,
        price_open: float,
        price_close: float,
    ) -> float:
        """Calculate hypothetical profit in account currency between two prices.

        ``volume`` is expressed in trading lots. ``order_type`` describes BUY or
        SELL direction rather than a ``TradeAction``.
        """
        return self._number(
            "order_calc_profit",
            int(order_type),
            symbol,
            volume,
            price_open,
            price_close,
        )

    def order_check(self, request: TradeRequest) -> TradeCheckResult:
        """Validate a request and return projected account impact without sending."""
        return self._model("order_check", TradeCheckResult, request.to_native())

    def order_send(self, request: TradeRequest) -> TradeResult:
        """Submit a trade request and return the broker's complete response.

        A returned response can represent rejection or partial execution. Inspect
        ``retcode`` and ``is_successful``; transport failures raise ``MT5Error``.
        """
        return self._model("order_send", TradeResult, request.to_native())

    def history_orders_get(
        self,
        *,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> tuple[HistoricalOrder, ...]:
        """Return historical orders by date range, order ticket, or position.

        ``group`` is valid only with a complete date range. Exactly one query
        strategy must be supplied.
        """
        args, kwargs = self._history_query(date_from, date_to, group, ticket, position)
        rows = self._rows("history_orders_get", *args, **kwargs)
        return tuple(
            self._parse_model("history_orders_get", HistoricalOrder, row)
            for row in rows
        )

    def history_deals_get(
        self,
        *,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> tuple[Deal, ...]:
        """Return historical deals by date range, order ticket, or position.

        Exactly one complete date range, ticket, or position strategy is
        required. ``group`` is accepted only with a date range.
        """
        args, kwargs = self._history_query(date_from, date_to, group, ticket, position)
        rows = self._rows("history_deals_get", *args, **kwargs)
        return tuple(self._parse_model("history_deals_get", Deal, row) for row in rows)

    def history_orders_total(self, date_from: datetime, date_to: datetime) -> int:
        """Return historical-order count for an inclusive UTC date range."""
        start, end = self._range(date_from, date_to)
        return self._integer("history_orders_total", start, end)

    def history_deals_total(self, date_from: datetime, date_to: datetime) -> int:
        """Return historical-deal count for an inclusive UTC date range."""
        start, end = self._range(date_from, date_to)
        return self._integer("history_deals_total", start, end)

    def _call(
        self,
        operation: str,
        *args: object,
        **kwargs: object,
    ) -> Any:
        if operation not in {"initialize", "shutdown"}:
            self._require_active(operation)
        raw = self._adapter.call(operation, *args, **kwargs)
        self._last_error = raw.error
        if raw.failed:
            error_type = MT5PlatformError if raw.platform_unavailable else MT5CallError
            raise error_type(operation, raw.error.code, raw.error.message)
        return raw.data

    def _call_required(self, operation: str, *args: object, **kwargs: object) -> Any:
        value = self._call(operation, *args, **kwargs)
        if value is None:
            self._raise_call_error(operation)
        return value

    def _call_bool(self, operation: str, *args: object, **kwargs: object) -> None:
        if self._call(operation, *args, **kwargs) is not True:
            self._raise_call_error(operation)

    def _raise_call_error(self, operation: str) -> None:
        raise MT5CallError(operation, self._last_error.code, self._last_error.message)

    def _rows(self, operation: str, *args: object, **kwargs: object) -> tuple[Any, ...]:
        value = self._call_required(operation, *args, **kwargs)
        try:
            return tuple(value)
        except TypeError as exc:
            raise self._payload_error(operation, exc) from exc

    def _model(
        self,
        operation: str,
        model: type[ModelT],
        *args: object,
        **kwargs: object,
    ) -> ModelT:
        value = self._call_required(operation, *args, **kwargs)
        return self._parse_model(operation, model, value)

    def _parse_model(
        self, operation: str, model: type[ModelT], value: object
    ) -> ModelT:
        try:
            return model.model_validate(self._mapping(value))
        except (TypeError, ValueError, ValidationError) as exc:
            raise self._payload_error(operation, exc) from exc

    def _integer(self, operation: str, *args: object) -> int:
        value = self._call_required(operation, *args)
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise self._payload_error(operation, exc) from exc

    def _number(self, operation: str, *args: object) -> float:
        value = self._call_required(operation, *args)
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise self._payload_error(operation, exc) from exc

    @staticmethod
    def _mapping(value: object) -> Mapping[str, object]:
        if isinstance(value, Mapping):
            mapping = cast(Mapping[str, object], value)
        elif hasattr(value, "_asdict"):
            mapping = cast(Mapping[str, object], value._asdict())
        elif hasattr(value, "__dict__"):
            mapping = cast(Mapping[str, object], vars(value))
        else:
            dtype = getattr(value, "dtype", None)
            names = getattr(dtype, "names", None)
            if not names:
                raise TypeError(
                    f"expected a record-like payload, got {type(value).__name__}"
                )
            record = cast(Any, value)
            mapping = {
                name: record[name].item()
                if hasattr(record[name], "item")
                else record[name]
                for name in names
            }
        return {name: SyntiqMT5._normalize(field) for name, field in mapping.items()}

    @staticmethod
    def _normalize(value: object) -> object:
        if hasattr(value, "_asdict"):
            mapping = cast(Mapping[str, object], value._asdict())
            return {
                name: SyntiqMT5._normalize(field) for name, field in mapping.items()
            }
        return value

    @staticmethod
    def _utc(value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.astimezone(UTC)

    @classmethod
    def _range(cls, start: datetime, end: datetime) -> tuple[datetime, datetime]:
        normalized = cls._utc(start), cls._utc(end)
        if normalized[0] > normalized[1]:
            raise ValueError("date_from must be before or equal to date_to")
        return normalized

    @classmethod
    def _history_query(
        cls,
        date_from: datetime | None,
        date_to: datetime | None,
        group: str | None,
        ticket: int | None,
        position: int | None,
    ) -> tuple[tuple[object, ...], dict[str, object]]:
        has_range = date_from is not None or date_to is not None
        selectors = int(has_range) + int(ticket is not None) + int(position is not None)
        if selectors != 1:
            raise ValueError(
                "provide exactly one date range, ticket, or position query"
            )
        if has_range:
            if date_from is None or date_to is None:
                raise ValueError("date_from and date_to must be provided together")
            start, end = cls._range(date_from, date_to)
            return (start, end), ({"group": group} if group is not None else {})
        if group is not None:
            raise ValueError("group is only valid with date_from and date_to")
        if ticket is not None:
            return (), {"ticket": ticket}
        return (), {"position": position}

    def _require_active(self, operation: str) -> None:
        if not self._active:
            raise MT5StateError(operation, -10, "MT5 is not initialized")

    @staticmethod
    def _payload_error(operation: str, exc: Exception) -> MT5PayloadError:
        return MT5PayloadError(operation, -3, f"invalid MT5 payload: {exc}")

    def _release_lease(self) -> None:
        if self._owns_lease:
            self._owns_lease = False
            self._lease.release()


MT5 = SyntiqMT5
"""Concise alias for :class:`SyntiqMT5`."""
