"""Deal model for completed MT5 trade history."""

from pydantic import BaseModel

from syntiq_mt5.enums import DealEntry, DealReason, DealType


class Deal(BaseModel):
    """A completed transaction in the MT5 trade history.

    Wraps the raw ``TradeDeal`` struct returned by ``mt5.history_deals_get()``.
    A deal is created whenever a position is opened, modified, or closed.
    Non-trade operations (balance adjustments, commissions, swaps) also
    appear as deals with non-BUY/SELL ``type`` values.

    Attributes:
        ticket: Unique deal identifier.
        order: Ticket of the order that generated this deal.
        time: Deal execution time as a Unix timestamp (seconds).
        time_msc: Deal execution time in milliseconds.
        type: Nature of the transaction (BUY, SELL, BALANCE, COMMISSION, etc.).
        entry: How this deal relates to the affected position (IN, OUT, INOUT, OUT_BY).
        magic: Expert Advisor identifier; 0 for manual trades.
        position_id: Ticket of the position this deal belongs to.
        reason: What triggered the deal.
        volume: Executed volume in lots.
        price: Execution price.
        commission: Commission charged for this deal.
        swap: Swap charged at the time of this deal.
        profit: Realised profit/loss in account currency.
        fee: Additional fee charged for this deal.
        symbol: Trading instrument name.
        comment: Arbitrary comment attached to the deal.
        external_id: Deal identifier in an external system.
    """

    ticket: int
    order: int
    time: int
    time_msc: int  # execution time in milliseconds
    type: DealType
    entry: DealEntry
    magic: int
    position_id: int
    reason: DealReason
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    fee: float
    symbol: str
    comment: str
    external_id: str

    @property
    def net_profit(self) -> float:
        """Realised profit after deducting commission, swap, and fees.

        Returns:
            Net profit in account currency.
        """
        return self.profit + self.commission + self.swap - self.fee

    @property
    def is_entry(self) -> bool:
        """Whether this deal opened a new position (``DEAL_ENTRY_IN``)."""
        return self.entry == DealEntry.IN

    @property
    def is_exit(self) -> bool:
        """Whether this deal closed an existing position (``DEAL_ENTRY_OUT``)."""
        return self.entry == DealEntry.OUT

    @property
    def is_reversal(self) -> bool:
        """Whether this deal reversed the direction of a position (``DEAL_ENTRY_INOUT``)."""
        return self.entry == DealEntry.INOUT

    @property
    def is_close_by(self) -> bool:
        """Whether this deal closed a position by an opposite position (``DEAL_ENTRY_OUT_BY``)."""
        return self.entry == DealEntry.OUT_BY

    @property
    def is_buy(self) -> bool:
        """Whether this is a buy deal (``DEAL_TYPE_BUY``)."""
        return self.type == DealType.BUY

    @property
    def is_sell(self) -> bool:
        """Whether this is a sell deal (``DEAL_TYPE_SELL``)."""
        return self.type == DealType.SELL
