from pydantic import Field

from metatrader5_wrapper.models import MT5NamedTupleModel


class SymbolInfo(MT5NamedTupleModel):
    """Typed symbol details returned by ``MetaTrader5.symbol_info()``."""

    name: str
    description: str | None = None
    path: str | None = None
    currency_base: str | None = None
    currency_profit: str | None = None
    currency_margin: str | None = None
    digits: int | None = None
    spread: int | None = None
    spread_float: bool | None = None
    visible: bool | None = None
    select: bool | None = None
    trade_mode: int | None = None
    trade_calc_mode: int | None = None
    trade_exemode: int | None = None
    volume_min: float | None = None
    volume_max: float | None = None
    volume_step: float | None = None
    point: float | None = None
    bid: float | None = None
    ask: float | None = None
    last: float | None = None


class Tick(MT5NamedTupleModel):
    """Typed latest-tick payload returned by ``MetaTrader5.symbol_info_tick()``."""

    time: int
    bid: float
    ask: float
    last: float
    volume: int
    time_msc: int
    flags: int
    volume_real: float = Field(default=0.0)
