from collections import namedtuple
from datetime import datetime

from metatrader5_wrapper._core.results import MT5DataCallResult, MT5ErrorResult
from metatrader5_wrapper.history.service import (
    history_deals_get,
    history_deals_total,
    history_orders_get,
    history_orders_total,
)


def test_history_orders_total_returns_int(monkeypatch) -> None:
    def fake_history_orders_total(
        _date_from: datetime, _date_to: datetime
    ) -> MT5DataCallResult:
        return MT5DataCallResult(
            data=12,
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.history.service.mt5_history.history_orders_total",
        fake_history_orders_total,
    )

    result = history_orders_total(datetime(2026, 1, 1), datetime(2026, 1, 31))

    assert result.success is True
    assert result.data == 12
    assert result.message == "MetaTrader 5 history orders total fetched successfully."


def test_history_orders_get_returns_typed_models(monkeypatch) -> None:
    raw_order = namedtuple(
        "RawHistoryOrder",
        [
            "ticket",
            "time_setup",
            "time_done",
            "type",
            "state",
            "magic",
            "position_id",
            "volume_initial",
            "volume_current",
            "price_open",
            "sl",
            "tp",
            "symbol",
            "comment",
        ],
    )

    def fake_history_orders_get(
        _date_from: datetime,
        _date_to: datetime,
        *,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> MT5DataCallResult:
        assert group == "*USD*"
        assert ticket is None
        assert position is None
        return MT5DataCallResult(
            data=[
                raw_order(
                    1001,
                    1_700_000_000,
                    1_700_000_010,
                    0,
                    1,
                    42,
                    777,
                    0.5,
                    0.0,
                    1.101,
                    1.09,
                    1.12,
                    "EURUSD",
                    "filled",
                )
            ],
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.history.service.mt5_history.history_orders_get",
        fake_history_orders_get,
    )

    result = history_orders_get(
        datetime(2026, 1, 1),
        datetime(2026, 1, 31),
        group="*USD*",
    )

    assert result.success is True
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].ticket == 1001
    assert result.data[0].symbol == "EURUSD"


def test_history_deals_total_failure_preserves_error(monkeypatch) -> None:
    def fake_history_deals_total(
        _date_from: datetime, _date_to: datetime
    ) -> MT5DataCallResult:
        return MT5DataCallResult(
            data=None,
            error=MT5ErrorResult(code=-1, message="History unavailable"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.history.service.mt5_history.history_deals_total",
        fake_history_deals_total,
    )

    result = history_deals_total(datetime(2026, 1, 1), datetime(2026, 1, 31))

    assert result.success is False
    assert result.error_code == -1
    assert result.error_message == "History unavailable"
    assert result.message == "Unable to fetch MetaTrader 5 history deals total."


def test_history_deals_get_uses_ticket_filter(monkeypatch) -> None:
    raw_deal = namedtuple(
        "RawHistoryDeal",
        [
            "ticket",
            "order",
            "time",
            "type",
            "entry",
            "magic",
            "position_id",
            "volume",
            "price",
            "commission",
            "swap",
            "profit",
            "fee",
            "symbol",
            "comment",
        ],
    )

    def fake_history_deals_get(
        _date_from: datetime,
        _date_to: datetime,
        *,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> MT5DataCallResult:
        assert group is None
        assert ticket == 99
        assert position is None
        return MT5DataCallResult(
            data=[
                raw_deal(
                    2001,
                    1001,
                    1_700_000_100,
                    1,
                    0,
                    42,
                    777,
                    0.5,
                    1.102,
                    0.0,
                    0.0,
                    10.5,
                    0.0,
                    "EURUSD",
                    "closed",
                )
            ],
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.history.service.mt5_history.history_deals_get",
        fake_history_deals_get,
    )

    result = history_deals_get(
        datetime(2026, 1, 1),
        datetime(2026, 1, 31),
        ticket=99,
    )

    assert result.success is True
    assert result.data is not None
    assert result.data[0].ticket == 2001
    assert result.data[0].profit == 10.5
