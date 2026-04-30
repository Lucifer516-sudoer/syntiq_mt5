import inspect
from types import SimpleNamespace

from pydantic import SecretStr, ValidationError

import syntiq_mt5
import syntiq_mt5.connection.service as connection_service
import syntiq_mt5.market.symbols as market_service
import syntiq_mt5.positions.service as positions_service
import syntiq_mt5._core.raw as raw_mod
from syntiq_mt5._core.execution import Result
from syntiq_mt5.client import MetaTrader5Client
from syntiq_mt5.connection.models import LoginCredential


class SeqMT5:
    def __init__(self):
        self.err = (0, "OK")
        self.init_calls = 0
        self.position_price = 1.1010

    def last_error(self):
        return self.err

    def initialize(self, **kwargs):
        self.init_calls += 1
        if self.init_calls == 1:
            self.err = (100, "init temporary failure")
            return False
        self.err = (0, "OK")
        return True

    def login(self, **kwargs):
        self.err = (0, "OK")
        return True

    def shutdown(self):
        self.err = (0, "OK")
        return True

    def positions_get(self, **kwargs):
        row = SimpleNamespace(
            ticket=1,
            symbol="EURUSD",
            price_open=1.1000,
            price_current=self.position_price,
            tp=1.1020,
            sl=1.0900,
            volume=0.1,
            type=0,
        )
        self.position_price += 0.0001
        self.err = (0, "OK")
        return [row]

    def symbol_info(self, symbol):
        self.err = (0, "OK")
        return SimpleNamespace(digits=5, point=0.00001)

    def copy_rates_from_pos(self, *args):
        self.err = (0, "OK")
        return [{"time": 1, "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.05}]


def test_realistic_flow_with_retry_and_shutdown(monkeypatch):
    fake = SeqMT5()
    monkeypatch.setattr(raw_mod, "mt5", fake)
    monkeypatch.setattr(connection_service, "mt5", fake)
    monkeypatch.setattr(positions_service, "mt5", fake)
    monkeypatch.setattr(market_service, "mt5", fake)

    client = MetaTrader5Client()
    creds = LoginCredential(login=1, password=SecretStr("x"), server="demo")

    first_init = client.initialize(creds)
    assert not first_init.success
    second_init = client.initialize(creds)
    assert second_init.success

    assert client.login(creds).success
    pos = client.positions()
    assert pos.success and len(pos.data) == 1
    candles = client.get_candles("EURUSD", timeframe=1, count=1)
    assert candles.success and len(candles.data) == 1
    assert client.shutdown().success


def test_multiple_positions_calls_are_stable(monkeypatch):
    fake = SeqMT5()
    fake.init_calls = 2
    monkeypatch.setattr(raw_mod, "mt5", fake)
    monkeypatch.setattr(connection_service, "mt5", fake)
    monkeypatch.setattr(positions_service, "mt5", fake)

    client = MetaTrader5Client()
    client.initialize()
    first = client.positions()
    second = client.positions()
    assert first.success and second.success
    assert second.data[0].price_current > first.data[0].price_current


def test_pip_variations_and_direction_awareness():
    eur = syntiq_mt5.Position(
        ticket=1, symbol="EURUSD", price_open=1.1000, price_current=1.1010, tp=1.1020, sl=1.0,
        volume=0.1, digits=5, point=0.00001, type=0
    )
    jpy = syntiq_mt5.Position(
        ticket=2, symbol="USDJPY", price_open=150.00, price_current=149.90, tp=149.80, sl=151.0,
        volume=0.1, digits=3, point=0.001, type=1
    )
    assert eur.pip_size == 0.0001
    assert round(eur.pips_profit, 2) == 10.0
    assert round(eur.pips_to_tp, 2) == 10.0
    assert jpy.pip_size == 0.01
    assert round(jpy.pips_profit, 2) == 10.0
    assert round(jpy.pips_to_tp, 2) == 10.0


def test_position_tp_zero_edge_case():
    p = syntiq_mt5.Position(
        ticket=3, symbol="EURUSD", price_open=1.0, price_current=1.0, tp=0.0, sl=0.0,
        volume=0.1, digits=5, point=0.00001, type=0
    )
    assert p.pips_to_tp == 0.0


def test_public_api_and_signatures_are_stable():
    assert hasattr(syntiq_mt5, "MetaTrader5Client")
    assert hasattr(syntiq_mt5, "LoginCredential")
    assert hasattr(syntiq_mt5, "Result")
    assert hasattr(syntiq_mt5, "Position")
    assert hasattr(syntiq_mt5, "Candle")

    sig = inspect.signature(MetaTrader5Client.get_candles)
    assert list(sig.parameters.keys()) == ["self", "symbol", "timeframe", "count"]


def test_result_failure_requires_error_fields():
    try:
        Result(success=False)
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True


def test_result_success_does_not_leak_errors():
    res = Result.ok(data={"x": 1}, context="ctx", operation="op")
    assert res.success
    assert res.error_code is None
    assert res.error_message is None
