from collections import namedtuple

from metatrader5_wrapper._core.results import MT5DataCallResult, MT5ErrorResult
from metatrader5_wrapper.orders.service import (
    order_calc_margin,
    order_calc_profit,
    order_check,
    order_send,
    orders_get,
    orders_total,
)


def test_orders_total_success(monkeypatch) -> None:
    def fake_orders_total() -> MT5DataCallResult:
        return MT5DataCallResult(
            data=5, error=MT5ErrorResult(code=1, message="Success")
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.orders.service.mt5_orders.orders_total",
        fake_orders_total,
    )

    result = orders_total()

    assert result.success is True
    assert result.data == 5


def test_orders_get_success(monkeypatch) -> None:
    raw_order = namedtuple("RawOrder", ["ticket", "symbol"])

    def fake_orders_get(*, symbol=None, group=None, ticket=None) -> MT5DataCallResult:
        assert symbol is None
        assert group is None
        assert ticket == 12345
        return MT5DataCallResult(
            data=(raw_order(12345, "EURUSD"),),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.orders.service.mt5_orders.orders_get",
        fake_orders_get,
    )

    result = orders_get(ticket=12345)

    assert result.success is True
    assert result.data is not None
    assert result.data[0].ticket == 12345


def test_order_calc_margin_success(monkeypatch) -> None:
    def fake_order_calc_margin(
        action: int, symbol: str, volume: float, price: float
    ) -> MT5DataCallResult:
        assert action == 0
        assert symbol == "EURUSD"
        assert volume == 1.0
        assert price == 1.1
        return MT5DataCallResult(
            data=12.5, error=MT5ErrorResult(code=1, message="Success")
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.orders.service.mt5_orders.order_calc_margin",
        fake_order_calc_margin,
    )

    result = order_calc_margin(0, "EURUSD", 1.0, 1.1)

    assert result.success is True
    assert result.data == 12.5


def test_order_calc_profit_success(monkeypatch) -> None:
    def fake_order_calc_profit(
        action: int, symbol: str, volume: float, price_open: float, price_close: float
    ) -> MT5DataCallResult:
        assert action == 0
        assert symbol == "EURUSD"
        assert volume == 1.0
        assert price_open == 1.1
        assert price_close == 1.2
        return MT5DataCallResult(
            data=8.25, error=MT5ErrorResult(code=1, message="Success")
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.orders.service.mt5_orders.order_calc_profit",
        fake_order_calc_profit,
    )

    result = order_calc_profit(0, "EURUSD", 1.0, 1.1, 1.2)

    assert result.success is True
    assert result.data == 8.25


def test_order_check_success(monkeypatch) -> None:
    raw_check = namedtuple("RawCheck", ["retcode", "comment"])

    def fake_order_check(request: dict[str, object]) -> MT5DataCallResult:
        assert request["symbol"] == "EURUSD"
        return MT5DataCallResult(
            data=raw_check(0, "ok"),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.orders.service.mt5_orders.order_check",
        fake_order_check,
    )

    result = order_check({"symbol": "EURUSD"})

    assert result.success is True
    assert result.data is not None
    assert result.data.comment == "ok"


def test_order_send_success(monkeypatch) -> None:
    raw_send = namedtuple("RawSend", ["retcode", "comment"])

    def fake_order_send(request: dict[str, object]) -> MT5DataCallResult:
        assert request["symbol"] == "EURUSD"
        return MT5DataCallResult(
            data=raw_send(0, "sent"),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.orders.service.mt5_orders.order_send",
        fake_order_send,
    )

    result = order_send({"symbol": "EURUSD"})

    assert result.success is True
    assert result.data is not None
    assert result.data.comment == "sent"
