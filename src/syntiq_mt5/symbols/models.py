"""Typed symbol specification and quote models."""

from syntiq_mt5._internal.model import MT5Model
from syntiq_mt5._internal.pricing import calculate_pip_size


class SymbolInfo(MT5Model):
    """Complete symbol specification returned by ``symbol_info``.

    Field names intentionally mirror the official ``SymbolInfo`` record so
    developers can cross-reference MQL5 documentation directly. Prices and
    session statistics use broker-defined symbol units; volume constraints are
    expressed in the instrument's trading-volume units. Integer mode fields are
    native MT5 enum values or bit masks.

    Attributes:
        name: Broker-defined symbol name.
        description: Human-readable instrument description.
        digits: Number of decimal places in quoted prices.
        point: Smallest quoted price increment.
        spread: Current spread in points.
        bid: Current bid price.
        ask: Current ask price.
        trade_contract_size: Contract quantity represented by one trading unit.
        volume_min: Minimum accepted order volume.
        volume_max: Maximum accepted order volume.
        volume_step: Permitted increment between order volumes.
        filling_mode: Bit mask of supported order filling policies.
        order_mode: Bit mask of supported order types.
    """

    custom: bool
    chart_mode: int
    select: bool
    visible: bool
    session_deals: int
    session_buy_orders: int
    session_sell_orders: int
    volume: int
    volumehigh: int
    volumelow: int
    time: int
    digits: int
    spread: int
    spread_float: bool
    ticks_bookdepth: int
    trade_calc_mode: int
    trade_mode: int
    start_time: int
    expiration_time: int
    trade_stops_level: int
    trade_freeze_level: int
    trade_exemode: int
    swap_mode: int
    swap_rollover3days: int
    margin_hedged_use_leg: bool
    expiration_mode: int
    filling_mode: int
    order_mode: int
    order_gtc_mode: int
    option_mode: int
    option_right: int
    bid: float
    bidhigh: float
    bidlow: float
    ask: float
    askhigh: float
    asklow: float
    last: float
    lasthigh: float
    lastlow: float
    volume_real: float
    volumehigh_real: float
    volumelow_real: float
    option_strike: float
    point: float
    trade_tick_value: float
    trade_tick_value_profit: float
    trade_tick_value_loss: float
    trade_tick_size: float
    trade_contract_size: float
    trade_accrued_interest: float
    trade_face_value: float
    trade_liquidity_rate: float
    volume_min: float
    volume_max: float
    volume_step: float
    volume_limit: float
    swap_long: float
    swap_short: float
    margin_initial: float
    margin_maintenance: float
    session_volume: float
    session_turnover: float
    session_interest: float
    session_buy_orders_volume: float
    session_sell_orders_volume: float
    session_open: float
    session_close: float
    session_aw: float
    session_price_settlement: float
    session_price_limit_min: float
    session_price_limit_max: float
    margin_hedged: float
    price_change: float
    price_volatility: float
    price_theoretical: float
    price_greeks_delta: float
    price_greeks_theta: float
    price_greeks_gamma: float
    price_greeks_vega: float
    price_greeks_rho: float
    price_greeks_omega: float
    price_sensitivity: float
    basis: str
    category: str
    currency_base: str
    currency_profit: str
    currency_margin: str
    bank: str
    description: str
    exchange: str
    formula: str
    isin: str
    name: str
    page: str
    path: str

    @property
    def pip_size(self) -> float:
        """Pip size in price units. Accounts for fractional-pip (3/5-digit) symbols."""
        return calculate_pip_size(self.digits, self.point)

    @property
    def spread_pips(self) -> float:
        """Calculate spread in pips."""
        return self.spread * self.point / self.pip_size

    @property
    def contract_size(self) -> float:
        """Alias for trade_contract_size."""
        return self.trade_contract_size


class SymbolTick(MT5Model):
    """Latest bid, ask, last price, and volume snapshot for a symbol.

    Attributes:
        time: Tick time as Unix seconds in UTC.
        bid: Current bid price.
        ask: Current ask price.
        last: Last traded price.
        volume: Integer volume representation.
        time_msc: Tick time as Unix milliseconds in UTC.
        flags: Native ``TICK_FLAG_*`` bit mask describing changed fields.
        volume_real: Floating-point volume representation.
    """

    time: int
    bid: float
    ask: float
    last: float
    volume: int
    time_msc: int
    flags: int
    volume_real: float

    @property
    def spread(self) -> float:
        """Calculate spread as ask - bid."""
        return self.ask - self.bid

    @property
    def mid_price(self) -> float:
        """Calculate mid price."""
        return (self.bid + self.ask) / 2
