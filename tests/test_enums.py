"""Tests for typed enum enforcement across all SDK models.

Covers:
- Valid enum parsing from raw integers (backward compatibility)
- Valid enum parsing from enum members (explicit usage)
- Rejection of invalid integers at model construction time
- Correct enum semantics (is_buy, is_sell, is_pending, etc.)
- TradeRequest.model_dump() produces plain ints for the MT5 API
"""

import pytest
from pydantic import ValidationError

from syntiq_mt5.enums import (
    BookType,
    DealEntry,
    DealReason,
    DealType,
    OrderFilling,
    OrderReason,
    OrderState,
    OrderTime,
    OrderType,
    PositionReason,
    PositionType,
    TradeAction,
)
from syntiq_mt5.history.models import Deal
from syntiq_mt5.market_book.models import BookEntry
from syntiq_mt5.orders.models import HistoricalOrder, Order, TradeRequest, TradeResult
from syntiq_mt5.positions.models import Position
from syntiq_mt5.ticks.models import Tick


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_position(**overrides):
    defaults = dict(
        ticket=1, symbol="EURUSD", price_open=1.1, price_current=1.101,
        tp=1.102, sl=1.09, volume=0.1, digits=5, point=0.00001,
        type=PositionType.BUY,
    )
    return Position(**{**defaults, **overrides})


def make_order(**overrides):
    defaults = dict(
        ticket=1, time_setup=0, time_setup_msc=0, time_done=0, time_done_msc=0,
        time_expiration=0, type=OrderType.BUY, type_time=OrderTime.GTC,
        type_filling=OrderFilling.FOK, state=OrderState.PLACED, magic=0,
        position_id=0, position_by_id=0, reason=OrderReason.CLIENT,
        volume_initial=0.1, volume_current=0.1, price_open=1.1, sl=0.0,
        tp=0.0, price_current=1.1, price_stoplimit=0.0, symbol="EURUSD",
        comment="", external_id="",
    )
    return Order(**{**defaults, **overrides})


def make_deal(**overrides):
    defaults = dict(
        ticket=1, order=1, time=0, time_msc=0, type=DealType.BUY,
        entry=DealEntry.IN, magic=0, position_id=1, reason=DealReason.CLIENT,
        volume=0.1, price=1.1, commission=0.0, swap=0.0, profit=10.0,
        fee=0.0, symbol="EURUSD", comment="", external_id="",
    )
    return Deal(**{**defaults, **overrides})


def make_book_entry(**overrides):
    defaults = dict(type=BookType.BUY, price=1.1, volume=10, volume_real=10.0)
    return BookEntry(**{**defaults, **overrides})


# ── PositionType ──────────────────────────────────────────────────────────────

class TestPositionType:
    def test_raw_int_buy_coerced(self):
        p = make_position(type=0)
        assert p.type == PositionType.BUY
        assert isinstance(p.type, PositionType)

    def test_raw_int_sell_coerced(self):
        p = make_position(type=1)
        assert p.type == PositionType.SELL

    def test_enum_member_accepted(self):
        p = make_position(type=PositionType.SELL)
        assert p.type == PositionType.SELL

    def test_invalid_int_rejected(self):
        with pytest.raises(ValidationError):
            make_position(type=99)

    def test_is_buy_true_for_buy(self):
        assert make_position(type=PositionType.BUY).is_buy is True

    def test_is_sell_false_for_buy(self):
        assert make_position(type=PositionType.BUY).is_sell is False

    def test_is_sell_true_for_sell(self):
        assert make_position(type=PositionType.SELL).is_sell is True

    def test_is_buy_false_for_sell(self):
        assert make_position(type=PositionType.SELL).is_buy is False


# ── PositionReason ────────────────────────────────────────────────────────────

class TestPositionReason:
    @pytest.mark.parametrize("raw,expected", [
        (0, PositionReason.CLIENT),
        (1, PositionReason.MOBILE),
        (2, PositionReason.WEB),
        (3, PositionReason.EXPERT),
    ])
    def test_all_valid_reasons_coerced(self, raw, expected):
        p = make_position(reason=raw)
        assert p.reason == expected

    def test_invalid_reason_rejected(self):
        with pytest.raises(ValidationError):
            make_position(reason=99)


# ── OrderType ─────────────────────────────────────────────────────────────────

class TestOrderType:
    @pytest.mark.parametrize("raw,expected", [
        (0, OrderType.BUY),
        (1, OrderType.SELL),
        (2, OrderType.BUY_LIMIT),
        (3, OrderType.SELL_LIMIT),
        (4, OrderType.BUY_STOP),
        (5, OrderType.SELL_STOP),
        (6, OrderType.BUY_STOP_LIMIT),
        (7, OrderType.SELL_STOP_LIMIT),
        (8, OrderType.CLOSE_BY),
    ])
    def test_all_order_types_coerced(self, raw, expected):
        o = make_order(type=raw)
        assert o.type == expected

    def test_invalid_order_type_rejected(self):
        with pytest.raises(ValidationError):
            make_order(type=99)


# ── OrderState ────────────────────────────────────────────────────────────────

class TestOrderState:
    def test_placed_is_pending(self):
        assert make_order(state=OrderState.PLACED).is_pending is True

    def test_partial_is_pending(self):
        assert make_order(state=OrderState.PARTIAL).is_pending is True

    def test_filled_is_not_pending(self):
        assert make_order(state=OrderState.FILLED).is_pending is False

    def test_filled_is_filled(self):
        assert make_order(state=OrderState.FILLED).is_filled is True

    def test_canceled_is_cancelled(self):
        assert make_order(state=OrderState.CANCELED).is_cancelled is True

    def test_raw_int_state_coerced(self):
        o = make_order(state=4)  # ORDER_STATE_FILLED
        assert o.state == OrderState.FILLED

    def test_invalid_state_rejected(self):
        with pytest.raises(ValidationError):
            make_order(state=99)

    @pytest.mark.parametrize("raw,expected", [
        (0, OrderState.STARTED),
        (1, OrderState.PLACED),
        (2, OrderState.CANCELED),
        (3, OrderState.PARTIAL),
        (4, OrderState.FILLED),
        (5, OrderState.REJECTED),
        (6, OrderState.EXPIRED),
        (7, OrderState.REQUEST_ADD),
        (8, OrderState.REQUEST_MODIFY),
        (9, OrderState.REQUEST_CANCEL),
    ])
    def test_all_states_coerced(self, raw, expected):
        assert make_order(state=raw).state == expected


# ── OrderFilling ──────────────────────────────────────────────────────────────

class TestOrderFilling:
    @pytest.mark.parametrize("raw,expected", [
        (0, OrderFilling.FOK),
        (1, OrderFilling.IOC),
        (2, OrderFilling.RETURN),
        (3, OrderFilling.BOC),
    ])
    def test_all_filling_types_coerced(self, raw, expected):
        assert make_order(type_filling=raw).type_filling == expected

    def test_invalid_filling_rejected(self):
        with pytest.raises(ValidationError):
            make_order(type_filling=99)


# ── OrderTime ─────────────────────────────────────────────────────────────────

class TestOrderTime:
    @pytest.mark.parametrize("raw,expected", [
        (0, OrderTime.GTC),
        (1, OrderTime.DAY),
        (2, OrderTime.SPECIFIED),
        (3, OrderTime.SPECIFIED_DAY),
    ])
    def test_all_time_types_coerced(self, raw, expected):
        assert make_order(type_time=raw).type_time == expected

    def test_invalid_time_rejected(self):
        with pytest.raises(ValidationError):
            make_order(type_time=99)


# ── OrderReason ───────────────────────────────────────────────────────────────

class TestOrderReason:
    @pytest.mark.parametrize("raw,expected", [
        (0, OrderReason.CLIENT),
        (1, OrderReason.MOBILE),
        (2, OrderReason.WEB),
        (3, OrderReason.EXPERT),
        (4, OrderReason.SL),
        (5, OrderReason.TP),
        (6, OrderReason.SO),
    ])
    def test_all_order_reasons_coerced(self, raw, expected):
        assert make_order(reason=raw).reason == expected

    def test_invalid_reason_rejected(self):
        with pytest.raises(ValidationError):
            make_order(reason=99)


# ── DealType ──────────────────────────────────────────────────────────────────

class TestDealType:
    @pytest.mark.parametrize("raw,expected", [
        (0, DealType.BUY),
        (1, DealType.SELL),
        (2, DealType.BALANCE),
        (3, DealType.CREDIT),
        (4, DealType.CHARGE),
        (5, DealType.CORRECTION),
        (6, DealType.BONUS),
        (7, DealType.COMMISSION),
        (8, DealType.COMMISSION_DAILY),
        (9, DealType.COMMISSION_MONTHLY),
        (10, DealType.COMMISSION_AGENT_DAILY),
        (11, DealType.COMMISSION_AGENT_MONTHLY),
        (12, DealType.INTEREST),
        (13, DealType.BUY_CANCELED),
        (14, DealType.SELL_CANCELED),
        (15, DealType.DIVIDEND),
        (16, DealType.DIVIDEND_FRANKED),
        (17, DealType.TAX),
    ])
    def test_all_deal_types_coerced(self, raw, expected):
        assert make_deal(type=raw).type == expected

    def test_invalid_deal_type_rejected(self):
        with pytest.raises(ValidationError):
            make_deal(type=99)

    def test_is_buy(self):
        assert make_deal(type=DealType.BUY).is_buy is True
        assert make_deal(type=DealType.BUY).is_sell is False

    def test_is_sell(self):
        assert make_deal(type=DealType.SELL).is_sell is True
        assert make_deal(type=DealType.SELL).is_buy is False

    def test_non_trade_deal_is_neither_buy_nor_sell(self):
        d = make_deal(type=DealType.BALANCE)
        assert d.is_buy is False
        assert d.is_sell is False


# ── DealEntry ─────────────────────────────────────────────────────────────────

class TestDealEntry:
    @pytest.mark.parametrize("raw,expected", [
        (0, DealEntry.IN),
        (1, DealEntry.OUT),
        (2, DealEntry.INOUT),
        (3, DealEntry.OUT_BY),
    ])
    def test_all_entries_coerced(self, raw, expected):
        assert make_deal(entry=raw).entry == expected

    def test_invalid_entry_rejected(self):
        with pytest.raises(ValidationError):
            make_deal(entry=99)

    def test_is_entry(self):
        assert make_deal(entry=DealEntry.IN).is_entry is True
        assert make_deal(entry=DealEntry.IN).is_exit is False

    def test_is_exit(self):
        assert make_deal(entry=DealEntry.OUT).is_exit is True
        assert make_deal(entry=DealEntry.OUT).is_entry is False

    def test_is_reversal(self):
        assert make_deal(entry=DealEntry.INOUT).is_reversal is True

    def test_is_close_by(self):
        assert make_deal(entry=DealEntry.OUT_BY).is_close_by is True


# ── DealReason ────────────────────────────────────────────────────────────────

class TestDealReason:
    @pytest.mark.parametrize("raw,expected", [
        (0, DealReason.CLIENT),
        (1, DealReason.MOBILE),
        (2, DealReason.WEB),
        (3, DealReason.EXPERT),
        (4, DealReason.SL),
        (5, DealReason.TP),
        (6, DealReason.SO),
        (7, DealReason.ROLLOVER),
        (8, DealReason.VMARGIN),
        (9, DealReason.SPLIT),
    ])
    def test_all_deal_reasons_coerced(self, raw, expected):
        assert make_deal(reason=raw).reason == expected

    def test_invalid_deal_reason_rejected(self):
        with pytest.raises(ValidationError):
            make_deal(reason=99)


# ── BookType ──────────────────────────────────────────────────────────────────

class TestBookType:
    @pytest.mark.parametrize("raw,expected", [
        (1, BookType.SELL),
        (2, BookType.BUY),
        (3, BookType.SELL_MARKET),
        (4, BookType.BUY_MARKET),
    ])
    def test_all_book_types_coerced(self, raw, expected):
        assert make_book_entry(type=raw).type == expected

    def test_invalid_book_type_rejected(self):
        with pytest.raises(ValidationError):
            make_book_entry(type=99)

    def test_buy_limit_is_buy(self):
        e = make_book_entry(type=BookType.BUY)
        assert e.is_buy is True
        assert e.is_sell is False
        assert e.is_market is False

    def test_buy_market_is_buy_and_market(self):
        e = make_book_entry(type=BookType.BUY_MARKET)
        assert e.is_buy is True
        assert e.is_market is True

    def test_sell_limit_is_sell(self):
        e = make_book_entry(type=BookType.SELL)
        assert e.is_sell is True
        assert e.is_buy is False
        assert e.is_market is False

    def test_sell_market_is_sell_and_market(self):
        e = make_book_entry(type=BookType.SELL_MARKET)
        assert e.is_sell is True
        assert e.is_market is True


# ── TradeAction ───────────────────────────────────────────────────────────────

class TestTradeAction:
    @pytest.mark.parametrize("raw,expected", [
        (1, TradeAction.DEAL),
        (5, TradeAction.PENDING),
        (6, TradeAction.SLTP),
        (7, TradeAction.MODIFY),
        (8, TradeAction.REMOVE),
        (10, TradeAction.CLOSE_BY),
    ])
    def test_all_trade_actions_coerced(self, raw, expected):
        req = TradeRequest(action=raw, type=OrderType.BUY)
        assert req.action == expected

    def test_invalid_trade_action_rejected(self):
        with pytest.raises(ValidationError):
            TradeRequest(action=99, type=OrderType.BUY)


# ── TradeRequest serialization ────────────────────────────────────────────────

class TestTradeRequestSerialization:
    def test_model_dump_produces_plain_ints(self):
        req = TradeRequest(
            action=TradeAction.DEAL,
            type=OrderType.BUY,
            type_filling=OrderFilling.IOC,
            type_time=OrderTime.DAY,
            symbol="EURUSD",
            volume=0.1,
            price=1.1,
        )
        data = req.model_dump()
        assert type(data["action"]) is int
        assert type(data["type"]) is int
        assert type(data["type_filling"]) is int
        assert type(data["type_time"]) is int
        assert data["action"] == 1   # TRADE_ACTION_DEAL
        assert data["type"] == 0     # ORDER_TYPE_BUY
        assert data["type_filling"] == 1  # ORDER_FILLING_IOC
        assert data["type_time"] == 1     # ORDER_TIME_DAY

    def test_raw_int_inputs_serialize_correctly(self):
        req = TradeRequest(action=1, type=0)
        data = req.model_dump()
        assert data["action"] == 1
        assert data["type"] == 0


# ── TradeResult retcode ───────────────────────────────────────────────────────

class TestTradeResult:
    def _make(self, retcode: int) -> TradeResult:
        return TradeResult(
            retcode=retcode, deal=0, order=0, volume=0.0, price=0.0,
            bid=0.0, ask=0.0, comment="", request_id=0, retcode_external=0,
        )

    def test_done_is_successful(self):
        assert self._make(10009).is_successful is True

    def test_done_partial_is_successful(self):
        assert self._make(10010).is_successful is True

    def test_placed_is_successful(self):
        assert self._make(10008).is_successful is True

    def test_reject_is_rejected(self):
        assert self._make(10006).is_rejected is True

    def test_requote_requires_requote(self):
        assert self._make(10004).requires_requote is True

    def test_unknown_broker_retcode_accepted(self):
        # retcode is kept as plain int — broker-specific codes must not be rejected
        r = self._make(20001)
        assert r.retcode == 20001
        assert r.is_successful is False
        assert r.is_rejected is False


# ── Tick flags (bitmask — not enum) ──────────────────────────────────────────

class TestTickFlags:
    def _make(self, flags: int) -> Tick:
        return Tick(time=0, bid=1.1, ask=1.101, last=0.0, volume=0,
                    time_msc=0, flags=flags, volume_real=0.0)

    def test_bid_flag(self):
        t = self._make(2)  # TICK_FLAG_BID
        assert t.has_bid is True
        assert t.has_ask is False
        assert t.has_last is False

    def test_ask_flag(self):
        t = self._make(4)  # TICK_FLAG_ASK
        assert t.has_ask is True
        assert t.has_bid is False

    def test_last_flag(self):
        t = self._make(8)  # TICK_FLAG_LAST
        assert t.has_last is True

    def test_combined_flags(self):
        t = self._make(2 | 4)  # BID + ASK
        assert t.has_bid is True
        assert t.has_ask is True
        assert t.has_last is False

    def test_zero_flags(self):
        t = self._make(0)
        assert t.has_bid is False
        assert t.has_ask is False
        assert t.has_last is False


# ── HistoricalOrder ───────────────────────────────────────────────────────────

class TestHistoricalOrder:
    def _make(self, state: OrderState) -> HistoricalOrder:
        return HistoricalOrder(
            ticket=1, time_setup=100, time_setup_msc=0, time_done=200,
            time_done_msc=0, time_expiration=0, type=OrderType.BUY,
            type_time=OrderTime.GTC, type_filling=OrderFilling.FOK,
            state=state, magic=0, position_id=0, position_by_id=0,
            reason=OrderReason.CLIENT, volume_initial=0.1, volume_current=0.0,
            price_open=1.1, sl=0.0, tp=0.0, price_current=1.1,
            price_stoplimit=0.0, symbol="EURUSD", comment="", external_id="",
        )

    def test_was_filled(self):
        assert self._make(OrderState.FILLED).was_filled is True

    def test_was_not_filled(self):
        assert self._make(OrderState.CANCELED).was_filled is False

    def test_duration_seconds(self):
        o = self._make(OrderState.FILLED)
        assert o.duration_seconds == 100

    def test_invalid_state_rejected(self):
        with pytest.raises(ValidationError):
            self._make(99)  # type: ignore[arg-type]


# ── Enum identity and int compatibility ───────────────────────────────────────

class TestEnumIntCompatibility:
    """IntEnum members must compare equal to their integer values."""

    def test_position_type_int_equality(self):
        assert PositionType.BUY == 0
        assert PositionType.SELL == 1

    def test_order_type_int_equality(self):
        assert OrderType.BUY == 0
        assert OrderType.SELL == 1

    def test_deal_type_int_equality(self):
        assert DealType.BUY == 0
        assert DealType.SELL == 1

    def test_deal_entry_int_equality(self):
        assert DealEntry.IN == 0
        assert DealEntry.OUT == 1
        assert DealEntry.INOUT == 2
        assert DealEntry.OUT_BY == 3

    def test_book_type_int_equality(self):
        assert BookType.SELL == 1
        assert BookType.BUY == 2
        assert BookType.SELL_MARKET == 3
        assert BookType.BUY_MARKET == 4

    def test_trade_action_int_equality(self):
        assert TradeAction.DEAL == 1
        assert TradeAction.PENDING == 5
