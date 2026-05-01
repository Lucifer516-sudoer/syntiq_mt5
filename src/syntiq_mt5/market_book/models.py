"""Market depth (DOM) entry model."""

from pydantic import BaseModel

from syntiq_mt5.enums import BookType


class BookEntry(BaseModel):
    """A single entry in the market depth (Depth of Market) for a symbol.

    Wraps the raw ``BookInfo`` struct returned by ``mt5.market_book_get()``.
    Each entry represents one price level in the order book, which may be
    a limit order or a market order on either the buy or sell side.

    Attributes:
        type: Whether this entry is a buy or sell order, and whether it is
            a limit or market order.
        price: Price level of this order book entry.
        volume: Volume available at this price level (integer lots).
        volume_real: Volume available at this price level (fractional lots).
    """

    type: BookType
    price: float
    volume: int
    volume_real: float

    @property
    def is_buy(self) -> bool:
        """Whether this entry is on the buy side (limit or market)."""
        return self.type in (BookType.BUY, BookType.BUY_MARKET)

    @property
    def is_sell(self) -> bool:
        """Whether this entry is on the sell side (limit or market)."""
        return self.type in (BookType.SELL, BookType.SELL_MARKET)

    @property
    def is_market(self) -> bool:
        """Whether this entry represents a market order rather than a limit order."""
        return self.type in (BookType.BUY_MARKET, BookType.SELL_MARKET)
