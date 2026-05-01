"""OHLCV candle model for MT5 rate data."""

from pydantic import BaseModel


class Candle(BaseModel):
    """A single OHLCV bar from the MT5 price history.

    Wraps one row of the numpy structured array returned by
    ``mt5.copy_rates_from_pos()``, ``mt5.copy_rates_from()``, and
    ``mt5.copy_rates_range()``.

    Attributes:
        time: Bar open time as a Unix timestamp (seconds).
        open: Opening price of the bar.
        high: Highest price reached during the bar.
        low: Lowest price reached during the bar.
        close: Closing price of the bar.
        tick_volume: Number of price ticks during the bar.
        spread: Spread in points at bar open.
        real_volume: Traded volume (exchange instruments only; 0 for Forex).
    """

    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: int = 0
    spread: int = 0
    real_volume: int = 0
