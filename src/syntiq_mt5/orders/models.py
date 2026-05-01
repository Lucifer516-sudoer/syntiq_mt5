"""Order models for active, historical, and trade request/result data."""

from pydantic import BaseModel

from syntiq_mt5 import constants
from syntiq_mt5.enums import (
    OrderFilling,
    OrderReason,
    OrderState,
    OrderTime,
    OrderType,
    TradeAction,
)


class Order(BaseModel):
    """An active (pending) order in MetaTrader 5.

    Wraps the raw ``TradeOrder`` struct returned by ``mt5.orders_get()``.
    Only orders that have not yet been executed, cancelled, or expired
    appear here — completed orders are in ``HistoricalOrder``.

    Attributes:
        ticket: Unique order identifier.
        time_setup: Time the order was placed (Unix seconds).
        time_setup_msc: Time the order was placed (milliseconds).
        time_done: Time the order was executed or cancelled (Unix seconds).
        time_done_msc: Execution/cancellation time in milliseconds.
        time_expiration: Expiry time for ``ORDER_TIME_SPECIFIED`` orders; 0 otherwise.
        type: Order type (BUY, SELL, BUY_LIMIT, etc.).
        type_time: Expiry policy (GTC, DAY, SPECIFIED, etc.).
        type_filling: Fill policy (FOK, IOC, RETURN, BOC).
        state: Current lifecycle state of the order.
        magic: Expert Advisor identifier; 0 for manual orders.
        position_id: Ticket of the position this order is linked to.
        position_by_id: Ticket of the opposite position for CLOSE_BY orders.
        reason: What triggered the order placement.
        volume_initial: Original order volume in lots.
        volume_current: Remaining unfilled volume in lots.
        price_open: Requested execution price.
        sl: Stop loss price; 0.0 if not set.
        tp: Take profit price; 0.0 if not set.
        price_current: Current market price for the order's symbol.
        price_stoplimit: Stop-limit price for ``BUY_STOP_LIMIT`` / ``SELL_STOP_LIMIT`` orders.
        symbol: Trading instrument name.
        comment: Arbitrary comment attached to the order.
        external_id: Order identifier in an external system.
    """

    ticket: int
    time_setup: int
    time_setup_msc: int       # placement time in milliseconds
    time_done: int
    time_done_msc: int        # completion time in milliseconds
    time_expiration: int
    type: OrderType
    type_time: OrderTime
    type_filling: OrderFilling
    state: OrderState
    magic: int
    position_id: int
    position_by_id: int
    reason: OrderReason
    volume_initial: float
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    price_stoplimit: float
    symbol: str
    comment: str
    external_id: str

    @property
    def is_pending(self) -> bool:
        """Whether the order is waiting to be filled (placed or partially filled)."""
        return self.state in (OrderState.PLACED, OrderState.PARTIAL)

    @property
    def is_filled(self) -> bool:
        """Whether the order has been fully executed."""
        return self.state == OrderState.FILLED

    @property
    def is_cancelled(self) -> bool:
        """Whether the order was cancelled before execution."""
        return self.state == OrderState.CANCELED


class HistoricalOrder(BaseModel):
    """A completed order retrieved from the MT5 trade history.

    Wraps the raw ``TradeOrder`` struct returned by
    ``mt5.history_orders_get()``.  Unlike ``Order``, historical orders
    include all terminal states (filled, cancelled, expired, rejected).

    Attributes:
        ticket: Unique order identifier.
        time_setup: Time the order was placed (Unix seconds).
        time_setup_msc: Placement time in milliseconds.
        time_done: Time the order reached its terminal state (Unix seconds).
        time_done_msc: Terminal state time in milliseconds.
        time_expiration: Expiry time for time-limited orders; 0 otherwise.
        type: Order type at the time of placement.
        type_time: Expiry policy used.
        type_filling: Fill policy used.
        state: Final state of the order.
        magic: Expert Advisor identifier; 0 for manual orders.
        position_id: Ticket of the position this order created or affected.
        position_by_id: Ticket of the opposite position for CLOSE_BY orders.
        reason: What triggered the order.
        volume_initial: Original order volume in lots.
        volume_current: Remaining unfilled volume (0.0 for fully filled orders).
        price_open: Requested execution price.
        sl: Stop loss price at the time of the order.
        tp: Take profit price at the time of the order.
        price_current: Price at the time the order reached its terminal state.
        price_stoplimit: Stop-limit activation price, if applicable.
        symbol: Trading instrument name.
        comment: Arbitrary comment attached to the order.
        external_id: Order identifier in an external system.
    """

    ticket: int
    time_setup: int
    time_setup_msc: int
    time_done: int
    time_done_msc: int
    time_expiration: int
    type: OrderType
    type_time: OrderTime
    type_filling: OrderFilling
    state: OrderState
    magic: int
    position_id: int
    position_by_id: int
    reason: OrderReason
    volume_initial: float
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    price_stoplimit: float
    symbol: str
    comment: str
    external_id: str

    @property
    def duration_seconds(self) -> int:
        """Time between order placement and completion, in seconds."""
        return self.time_done - self.time_setup

    @property
    def was_filled(self) -> bool:
        """Whether the order was fully executed before reaching a terminal state."""
        return self.state == OrderState.FILLED


class TradeRequest(BaseModel):
    """Parameters for a trade operation sent to MT5 via ``order_send`` or ``order_check``.

    All enum-typed fields accept either the typed enum member or a raw
    integer — Pydantic coerces integers to the matching enum and rejects
    unknown values at construction time.

    ``model_dump()`` is overridden to cast enum fields back to plain
    ``int`` before the dict is passed to the MT5 C extension, which
    expects native integers.

    Attributes:
        action: Trade action type (DEAL, PENDING, SLTP, MODIFY, REMOVE, CLOSE_BY).
        magic: Expert Advisor identifier; 0 for manual requests.
        order: Ticket of the order to modify or remove (for MODIFY/REMOVE actions).
        symbol: Trading instrument name.
        volume: Trade volume in lots.
        price: Requested execution price (0.0 for market orders).
        stoplimit: Stop-limit activation price for stop-limit orders.
        sl: Stop loss price; 0.0 to leave unset.
        tp: Take profit price; 0.0 to leave unset.
        deviation: Maximum allowed price deviation in points.
        type: Order type (BUY, SELL, BUY_LIMIT, etc.).
        type_filling: Fill policy (FOK, IOC, RETURN, BOC).
        type_time: Expiry policy (GTC, DAY, SPECIFIED, etc.).
        expiration: Expiry time for ``ORDER_TIME_SPECIFIED`` orders (Unix seconds).
        comment: Arbitrary comment to attach to the order.
        position: Ticket of the position to modify (for SLTP action).
        position_by: Ticket of the opposite position (for CLOSE_BY action).
    """

    action: TradeAction
    magic: int = 0
    order: int = 0
    symbol: str = ""
    volume: float = 0.0
    price: float = 0.0
    stoplimit: float = 0.0
    sl: float = 0.0
    tp: float = 0.0
    deviation: int = 0
    type: OrderType = OrderType.BUY
    type_filling: OrderFilling = OrderFilling.FOK
    type_time: OrderTime = OrderTime.GTC
    expiration: int = 0
    comment: str = ""
    position: int = 0
    position_by: int = 0

    def model_dump(self, **kwargs: object) -> dict[str, object]:  # type: ignore[override]
        """Serialize to a plain dict with integer enum values for the MT5 API.

        The MT5 C extension's ``order_send`` and ``order_check`` functions
        expect a dict of plain Python ints.  ``IntEnum`` members *are* ints,
        but some MT5 builds reject non-``int`` types, so enum fields are
        explicitly cast here.

        Returns:
            A dict suitable for passing directly to ``mt5.order_send()``
            or ``mt5.order_check()``.
        """
        data = super().model_dump(**kwargs)
        for key in ("action", "type", "type_filling", "type_time"):
            if key in data:
                data[key] = int(data[key])
        return data


class TradeResult(BaseModel):
    """Outcome of a trade request returned by ``order_send`` or ``order_check``.

    Wraps the raw ``OrderSendResult`` struct from the MT5 C extension.
    The ``retcode`` field is kept as a plain ``int`` rather than an enum
    because brokers can return custom codes outside the standard MT5 set —
    enforcing a strict enum would cause ``ValidationError`` on valid
    broker-specific responses.

    Attributes:
        retcode: MT5 return code (e.g. 10009 = DONE, 10006 = REJECT).
        deal: Ticket of the deal created by this request; 0 if none.
        order: Ticket of the order created by this request; 0 if none.
        volume: Volume actually executed in lots.
        price: Price at which the trade was executed.
        bid: Current bid price at the time of execution.
        ask: Current ask price at the time of execution.
        comment: Broker comment on the result.
        request_id: Identifier assigned to the request by the client terminal.
        retcode_external: Return code from an external trading system, if any.
        request: Echo of the original ``TradeRequest`` dict, if available.
    """

    retcode: int
    deal: int
    order: int
    volume: float
    price: float
    bid: float
    ask: float
    comment: str
    request_id: int
    retcode_external: int
    request: dict[str, object] | None = None

    @property
    def is_successful(self) -> bool:
        """Whether the trade was accepted by the broker.

        Returns ``True`` for ``TRADE_RETCODE_PLACED`` (10008),
        ``TRADE_RETCODE_DONE`` (10009), and
        ``TRADE_RETCODE_DONE_PARTIAL`` (10010).
        """
        return self.retcode in (
            constants.TRADE_RETCODE_PLACED,
            constants.TRADE_RETCODE_DONE,
            constants.TRADE_RETCODE_DONE_PARTIAL,
        )

    @property
    def is_rejected(self) -> bool:
        """Whether the trade was explicitly rejected by the broker (``TRADE_RETCODE_REJECT``)."""
        return self.retcode == constants.TRADE_RETCODE_REJECT

    @property
    def requires_requote(self) -> bool:
        """Whether the broker requires a new price before the trade can proceed (``TRADE_RETCODE_REQUOTE``)."""
        return self.retcode == constants.TRADE_RETCODE_REQUOTE
