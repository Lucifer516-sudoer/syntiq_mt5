from collections import namedtuple

from metatrader5_wrapper._core.results import (
    MT5BoolCallResult,
    MT5DataCallResult,
    MT5ErrorResult,
)
from metatrader5_wrapper.symbols.service import (
    symbol_info,
    symbol_info_tick,
    symbol_select,
    symbols_get,
    symbols_total,
)


def test_symbols_total_success(monkeypatch) -> None:
    def fake_symbols_total() -> MT5DataCallResult:
        return MT5DataCallResult(
            data=42,
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.symbols.service.mt5_symbols.symbols_total",
        fake_symbols_total,
    )

    result = symbols_total()

    assert result.success is True
    assert result.data == 42


def test_symbol_info_success(monkeypatch) -> None:
    raw_symbol = namedtuple("RawSymbol", ["name", "digits", "spread", "bid", "ask"])

    def fake_symbol_info(symbol: str) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        return MT5DataCallResult(
            data=raw_symbol("EURUSD", 5, 10, 1.1, 1.2),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.symbols.service.mt5_symbols.symbol_info",
        fake_symbol_info,
    )

    result = symbol_info("EURUSD")

    assert result.success is True
    assert result.data is not None
    assert result.data.name == "EURUSD"
    assert result.data.digits == 5


def test_symbols_get_success(monkeypatch) -> None:
    raw_symbol = namedtuple("RawSymbol", ["name", "description"])

    def fake_symbols_get(*, group: str | None = None) -> MT5DataCallResult:
        assert group == "*USD*"
        return MT5DataCallResult(
            data=(raw_symbol("EURUSD", "Euro vs US Dollar"),),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.symbols.service.mt5_symbols.symbols_get",
        fake_symbols_get,
    )

    result = symbols_get(group="*USD*")

    assert result.success is True
    assert result.data is not None
    assert result.data[0].name == "EURUSD"


def test_symbol_info_tick_success(monkeypatch) -> None:
    raw_tick = namedtuple(
        "RawTick",
        ["time", "bid", "ask", "last", "volume", "time_msc", "flags", "volume_real"],
    )

    def fake_symbol_info_tick(symbol: str) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        return MT5DataCallResult(
            data=raw_tick(1, 1.1, 1.2, 1.15, 100, 1000, 2, 100.0),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.symbols.service.mt5_symbols.symbol_info_tick",
        fake_symbol_info_tick,
    )

    result = symbol_info_tick("EURUSD")

    assert result.success is True
    assert result.data is not None
    assert result.data.bid == 1.1


def test_symbol_select_failure_preserves_error(monkeypatch) -> None:
    def fake_symbol_select(symbol: str, enable: bool) -> MT5BoolCallResult:
        assert symbol == "MISSING"
        assert enable is True
        return MT5BoolCallResult(
            success=False,
            error=MT5ErrorResult(code=-1, message="Unknown symbol"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.symbols.service.mt5_symbols.symbol_select",
        fake_symbol_select,
    )

    result = symbol_select("MISSING")

    assert result.failed is True
    assert result.error_code == -1
    assert result.error_message == "Unknown symbol"
