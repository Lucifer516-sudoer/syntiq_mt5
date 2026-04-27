from datetime import datetime

from metatrader5_wrapper._core.results import MT5DataCallResult, MT5ErrorResult
from metatrader5_wrapper.rates.service import (
    copy_rates_from,
    copy_rates_from_pos,
    copy_rates_range,
    copy_ticks_from,
    copy_ticks_range,
)


def test_copy_rates_from_success(monkeypatch) -> None:
    def fake_copy_rates_from(
        symbol: str, timeframe: int, date_from: datetime, count: int
    ) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        assert timeframe == 1
        assert date_from == datetime(2021, 1, 1)
        assert count == 10
        return MT5DataCallResult(
            data=({"time": 1, "open": 1.1, "close": 1.2},),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.rates.service.mt5_rates.copy_rates_from",
        fake_copy_rates_from,
    )

    result = copy_rates_from("EURUSD", 1, datetime(2021, 1, 1), 10)

    assert result.success is True
    assert result.data is not None
    assert result.data[0]["open"] == 1.1


def test_copy_rates_from_pos_success(monkeypatch) -> None:
    def fake_copy_rates_from_pos(
        symbol: str, timeframe: int, start_pos: int, count: int
    ) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        assert timeframe == 1
        assert start_pos == 0
        assert count == 10
        return MT5DataCallResult(
            data=({"time": 1, "open": 1.1, "close": 1.2},),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.rates.service.mt5_rates.copy_rates_from_pos",
        fake_copy_rates_from_pos,
    )

    result = copy_rates_from_pos("EURUSD", 1, 0, 10)

    assert result.success is True


def test_copy_rates_range_success(monkeypatch) -> None:
    def fake_copy_rates_range(
        symbol: str, timeframe: int, date_from: datetime, date_to: datetime
    ) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        assert timeframe == 1
        assert date_from == datetime(2021, 1, 1)
        assert date_to == datetime(2021, 1, 10)
        return MT5DataCallResult(
            data=({"time": 1, "open": 1.1, "close": 1.2},),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.rates.service.mt5_rates.copy_rates_range",
        fake_copy_rates_range,
    )

    result = copy_rates_range("EURUSD", 1, datetime(2021, 1, 1), datetime(2021, 1, 10))

    assert result.success is True


def test_copy_ticks_from_success(monkeypatch) -> None:
    def fake_copy_ticks_from(
        symbol: str, date_from: datetime, count: int, flags: int
    ) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        assert date_from == datetime(2021, 1, 1)
        assert count == 10
        assert flags == 0
        return MT5DataCallResult(
            data=({"time": 1, "bid": 1.1, "ask": 1.2},),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.rates.service.mt5_rates.copy_ticks_from",
        fake_copy_ticks_from,
    )

    result = copy_ticks_from("EURUSD", datetime(2021, 1, 1), 10, 0)

    assert result.success is True


def test_copy_ticks_range_success(monkeypatch) -> None:
    def fake_copy_ticks_range(
        symbol: str, date_from: datetime, date_to: datetime, flags: int
    ) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        assert date_from == datetime(2021, 1, 1)
        assert date_to == datetime(2021, 1, 10)
        assert flags == 0
        return MT5DataCallResult(
            data=({"time": 1, "bid": 1.1, "ask": 1.2},),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.rates.service.mt5_rates.copy_ticks_range",
        fake_copy_ticks_range,
    )

    result = copy_ticks_range("EURUSD", datetime(2021, 1, 1), datetime(2021, 1, 10), 0)

    assert result.success is True
