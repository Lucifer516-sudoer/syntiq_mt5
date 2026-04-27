from collections import namedtuple

from metatrader5_wrapper._core.results import MT5DataCallResult, MT5ErrorResult
from metatrader5_wrapper.positions.service import positions_get, positions_total


def test_positions_total_success(monkeypatch) -> None:
    def fake_positions_total() -> MT5DataCallResult:
        return MT5DataCallResult(
            data=3,
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.positions.service.mt5_positions.positions_total",
        fake_positions_total,
    )

    result = positions_total()

    assert result.success is True
    assert result.data == 3


def test_positions_get_success(monkeypatch) -> None:
    raw_position = namedtuple(
        "RawPosition",
        [
            "ticket",
            "time",
            "time_update",
            "type",
            "magic",
            "identifier",
            "volume",
            "price_open",
            "sl",
            "tp",
            "price_current",
            "swap",
            "profit",
            "symbol",
            "comment",
        ],
    )

    def fake_positions_get(
        *,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        assert group is None
        assert ticket is None
        return MT5DataCallResult(
            data=(
                raw_position(
                    1001,
                    1,
                    2,
                    0,
                    123,
                    1001,
                    0.1,
                    1.1,
                    1.0,
                    1.2,
                    1.15,
                    0.0,
                    25.0,
                    "EURUSD",
                    "test",
                ),
            ),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.positions.service.mt5_positions.positions_get",
        fake_positions_get,
    )

    result = positions_get(symbol="EURUSD")

    assert result.success is True
    assert result.data is not None
    assert result.data[0].ticket == 1001
    assert result.data[0].profit == 25.0
