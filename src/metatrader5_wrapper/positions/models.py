from metatrader5_wrapper.models import MT5NamedTupleModel


class Position(MT5NamedTupleModel):
    """Typed position payload returned by ``MetaTrader5.positions_get()``."""

    ticket: int
    time: int
    time_msc: int | None = None
    time_update: int
    time_update_msc: int | None = None
    type: int
    magic: int
    identifier: int
    reason: int | None = None
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float
    profit: float
    symbol: str
    comment: str
    external_id: str | None = None
