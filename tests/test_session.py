from collections import defaultdict
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from syntiq_mt5 import (
    MT5,
    AdapterReply,
    ErrorInfo,
    MT5CallError,
    MT5PayloadError,
    MT5StateError,
    OrderType,
    TradeAction,
    TradeRequest,
)


class FakeAdapter:
    def __init__(self, **responses):
        self.responses = defaultdict(
            list, {name: list(values) for name, values in responses.items()}
        )
        self.calls = []

    def call(self, operation, /, *args, **kwargs):
        self.calls.append((operation, args, kwargs))
        value = self.responses[operation].pop(0) if self.responses[operation] else None
        if isinstance(value, AdapterReply):
            return value
        return AdapterReply(value, ErrorInfo(code=1, message="Success"))


def adapter(**responses):
    return FakeAdapter(initialize=[True], shutdown=[None], **responses)


def test_context_manager_owns_lifecycle():
    fake = adapter(version=[(500, 5735, "22 Aug 2026")])

    with MT5(adapter=fake) as mt5:
        assert mt5.connected
        assert mt5.version() == (500, 5735, "22 Aug 2026")

    assert not mt5.connected
    assert [call[0] for call in fake.calls] == ["initialize", "version", "shutdown"]


def test_operations_require_an_active_session():
    with pytest.raises(MT5StateError, match="not initialized"):
        MT5(adapter=FakeAdapter()).positions_total()


def test_shutdown_adapter_failure_is_reported_and_releases_lease():
    failure = AdapterReply(
        None,
        ErrorInfo(code=-2, message="shutdown raised"),
        failed=True,
    )
    fake = FakeAdapter(initialize=[True], shutdown=[failure])

    mt5 = MT5(adapter=fake)
    mt5.initialize()
    with pytest.raises(MT5CallError, match="shutdown raised"):
        mt5.shutdown()

    assert not mt5.connected
    with MT5(adapter=adapter()):
        pass


def test_false_boolean_response_raises_with_captured_error():
    failure = AdapterReply(False, ErrorInfo(code=-4, message="not found"))
    fake = adapter(symbol_select=[failure])

    with MT5(adapter=fake) as mt5, pytest.raises(MT5CallError) as caught:
        mt5.symbol_select("EURUSD")

    assert caught.value.operation == "symbol_select"
    assert caught.value.code == -4


def test_empty_collection_is_not_a_failure():
    fake = adapter(orders_get=[()])

    with MT5(adapter=fake) as mt5:
        assert mt5.orders_get() == ()


def test_malformed_position_row_raises_payload_error():
    fake = adapter(positions_get=[[{"ticket": 1}]])

    with MT5(adapter=fake) as mt5, pytest.raises(MT5PayloadError):
        mt5.positions()


def test_recent_candles_exclude_current_bar_by_default():
    row = {
        "time": 1,
        "open": 1.0,
        "high": 1.2,
        "low": 0.9,
        "close": 1.1,
        "tick_volume": 10,
        "spread": 2,
        "real_volume": 5,
    }
    fake = adapter(copy_rates_from_pos=[[row]])

    with MT5(adapter=fake) as mt5:
        candles = mt5.candles("EURUSD", 60, 1)

    assert candles[0].close == 1.1
    assert fake.calls[1][1] == ("EURUSD", 60, 1, 1)


def test_market_book_context_always_releases_subscription():
    fake = adapter(market_book_add=[True], market_book_release=[True])

    with (
        MT5(adapter=fake) as mt5,
        pytest.raises(RuntimeError, match="strategy failed"),
        mt5.market_book("EURUSD"),
    ):
        raise RuntimeError("strategy failed")

    assert [call[0] for call in fake.calls] == [
        "initialize",
        "market_book_add",
        "market_book_release",
        "shutdown",
    ]


def test_order_check_uses_its_own_response_model():
    response = SimpleNamespace(
        retcode=0,
        balance=10_000.0,
        equity=10_010.0,
        profit=10.0,
        margin=50.0,
        margin_free=9_960.0,
        margin_level=20_020.0,
        comment="Done",
        request=None,
    )
    fake = adapter(order_check=[response])
    request = TradeRequest(action=TradeAction.DEAL, symbol="EURUSD", volume=0.1)

    with MT5(adapter=fake) as mt5:
        checked = mt5.order_check(request)

    assert checked.accepted
    assert checked.margin_free == 9_960.0


def test_order_calc_uses_order_type_not_trade_action():
    fake = adapter(order_calc_margin=[123.45])

    with MT5(adapter=fake) as mt5:
        assert mt5.order_calc_margin(OrderType.BUY, "EURUSD", 0.1, 1.1) == 123.45

    assert fake.calls[1][1][0] == int(OrderType.BUY)


def test_history_group_is_only_sent_with_a_date_range():
    fake = adapter(history_orders_get=[()])
    end = datetime.now(UTC)

    with MT5(adapter=fake) as mt5:
        assert (
            mt5.history_orders_get(
                date_from=end - timedelta(days=1),
                date_to=end,
                group="*USD*,!USDJPY",
            )
            == ()
        )

    operation, args, kwargs = fake.calls[1]
    assert operation == "history_orders_get"
    assert args[0].tzinfo is UTC
    assert kwargs == {"group": "*USD*,!USDJPY"}


def test_naive_datetimes_are_rejected_before_adapter_call():
    fake = adapter(copy_ticks_from=[()])

    with MT5(adapter=fake) as mt5, pytest.raises(ValueError, match="timezone-aware"):
        mt5.copy_ticks_from("EURUSD", datetime(2026, 1, 1), 10, 0)

    assert [call[0] for call in fake.calls] == ["initialize", "shutdown"]
