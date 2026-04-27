from metatrader5_wrapper._core.results import (
    MT5BoolCallResult,
    MT5DataCallResult,
    MT5ErrorResult,
)
from metatrader5_wrapper.market_book.service import (
    market_book_add,
    market_book_get,
    market_book_release,
)


def test_market_book_add_success(monkeypatch) -> None:
    def fake_market_book_add(symbol: str) -> MT5BoolCallResult:
        assert symbol == "EURUSD"
        return MT5BoolCallResult(
            success=True,
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.market_book.service.mt5_market_book.market_book_add",
        fake_market_book_add,
    )

    result = market_book_add("EURUSD")

    assert result.success is True


def test_market_book_get_success(monkeypatch) -> None:
    def fake_market_book_get(symbol: str) -> MT5DataCallResult:
        assert symbol == "EURUSD"
        return MT5DataCallResult(
            data=({"bid": 1.1, "ask": 1.2},),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.market_book.service.mt5_market_book.market_book_get",
        fake_market_book_get,
    )

    result = market_book_get("EURUSD")

    assert result.success is True
    assert result.data == [{"bid": 1.1, "ask": 1.2}]


def test_market_book_release_success(monkeypatch) -> None:
    def fake_market_book_release(symbol: str) -> MT5BoolCallResult:
        assert symbol == "EURUSD"
        return MT5BoolCallResult(
            success=True,
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.market_book.service.mt5_market_book.market_book_release",
        fake_market_book_release,
    )

    result = market_book_release("EURUSD")

    assert result.success is True
