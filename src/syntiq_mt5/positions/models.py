"""Position model for open MT5 trading positions."""

from pydantic import BaseModel

from syntiq_mt5._core.pricing import calculate_pip_size
from syntiq_mt5.enums import PositionReason, PositionType


class Position(BaseModel):
    """An open trading position in MetaTrader 5.

    Wraps the raw ``TradePosition`` struct returned by ``mt5.positions_get()``.
    In addition to the raw fields, computed properties expose pip-based
    profit metrics that are commonly needed for position management.

    ``digits`` and ``point`` are not part of the MT5 position struct — they
    are fetched from ``mt5.symbol_info()`` by ``PositionService`` and
    attached here so that pip calculations are self-contained.

    Attributes:
        ticket: Unique position identifier.
        time: Position open time as a Unix timestamp (seconds).
        time_msc: Position open time in milliseconds.
        time_update: Last modification time as a Unix timestamp (seconds).
        time_update_msc: Last modification time in milliseconds.
        type: Direction of the position (BUY or SELL).
        magic: Expert Advisor identifier; 0 for manual trades.
        identifier: Position identifier matching the opening order ticket.
        reason: How the position was opened (terminal, EA, etc.).
        volume: Current position size in lots.
        price_open: Price at which the position was opened.
        sl: Stop loss price; 0.0 if not set.
        tp: Take profit price; 0.0 if not set.
        price_current: Current market price for the position's symbol.
        swap: Accumulated swap charges.
        profit: Floating profit/loss in account currency.
        symbol: Trading instrument name (e.g. ``"EURUSD"``).
        comment: Arbitrary comment attached to the position.
        external_id: Position identifier in an external system.
        digits: Number of decimal places for the symbol's price.
        point: Smallest price increment for the symbol.
    """

    ticket: int
    time: int = 0
    time_msc: int = 0       # open time in milliseconds
    time_update: int = 0
    time_update_msc: int = 0  # last update time in milliseconds
    type: PositionType
    magic: int = 0
    identifier: int = 0
    reason: PositionReason = PositionReason.CLIENT
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float = 0.0
    profit: float = 0.0
    symbol: str
    comment: str = ""
    external_id: str = ""
    digits: int
    point: float

    @property
    def is_buy(self) -> bool:
        """Whether this is a long (buy) position."""
        return self.type == PositionType.BUY

    @property
    def is_sell(self) -> bool:
        """Whether this is a short (sell) position."""
        return self.type == PositionType.SELL

    @property
    def pip_size(self) -> float:
        """Pip size in price units for this symbol.

        Delegates to ``calculate_pip_size`` which accounts for the
        fractional-pip convention used by 3- and 5-digit symbols.
        """
        return calculate_pip_size(self.digits, self.point)

    @property
    def pips_profit(self) -> float:
        """Current floating profit expressed in pips.

        Positive values indicate profit; negative values indicate loss.
        Direction is taken from ``type`` so the sign is always correct
        for both long and short positions.

        Returns:
            Profit in pips relative to the open price.
        """
        direction = 1 if self.is_buy else -1
        return ((self.price_current - self.price_open) * direction) / self.pip_size

    @property
    def pips_to_tp(self) -> float:
        """Distance from the current price to the take profit level in pips.

        Returns 0.0 when no take profit is set (``tp == 0``).  A positive
        value means the TP has not yet been reached; a negative value means
        the price has already passed the TP level.

        Returns:
            Distance to take profit in pips, or 0.0 if TP is not set.
        """
        if self.tp == 0:
            return 0.0
        direction = 1 if self.is_buy else -1
        return ((self.tp - self.price_current) * direction) / self.pip_size
