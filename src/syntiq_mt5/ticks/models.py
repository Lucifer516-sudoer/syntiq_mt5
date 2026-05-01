"""Tick model for raw MT5 price feed data."""

from pydantic import BaseModel

from syntiq_mt5 import constants


class Tick(BaseModel):
    """A single price tick from the MT5 market data feed.

    Wraps the raw tick struct returned by ``mt5.copy_ticks_from()`` and
    ``mt5.copy_ticks_range()``.  Each tick represents one price update
    event; not all fields are updated on every tick — the ``flags``
    bitmask indicates which prices changed.

    Attributes:
        time: Tick time as a Unix timestamp (seconds).
        bid: Current bid price.
        ask: Current ask price.
        last: Last trade price (exchange instruments only; 0.0 for Forex).
        volume: Last trade volume (exchange instruments only; 0 for Forex).
        time_msc: Tick time in milliseconds.
        flags: Bitmask of ``TICK_FLAG_*`` constants indicating which fields
            were updated in this tick.
        volume_real: Last trade volume as a fractional value.
    """

    time: int
    bid: float
    ask: float
    last: float
    volume: int
    time_msc: int  # tick time in milliseconds
    flags: int     # bitmask: see TICK_FLAG_* constants
    volume_real: float

    @property
    def spread(self) -> float:
        """Current bid-ask spread in price units."""
        return self.ask - self.bid

    @property
    def mid_price(self) -> float:
        """Mid-point between bid and ask."""
        return (self.bid + self.ask) / 2

    @property
    def has_bid(self) -> bool:
        """Whether this tick carries a bid price update (``TICK_FLAG_BID``)."""
        return bool(self.flags & constants.TICK_FLAG_BID)

    @property
    def has_ask(self) -> bool:
        """Whether this tick carries an ask price update (``TICK_FLAG_ASK``)."""
        return bool(self.flags & constants.TICK_FLAG_ASK)

    @property
    def has_last(self) -> bool:
        """Whether this tick carries a last trade price update (``TICK_FLAG_LAST``)."""
        return bool(self.flags & constants.TICK_FLAG_LAST)
