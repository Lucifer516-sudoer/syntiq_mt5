from types import SimpleNamespace

import syntiq_mt5.connection.service as connection_service
import syntiq_mt5.market.symbols as market_service
import syntiq_mt5.positions.service as positions_service
import syntiq_mt5._core.raw as raw_mod
from syntiq_mt5.connection.models import LoginCredential
from syntiq_mt5.client import MetaTrader5Client
from syntiq_mt5.positions.models import Position
from pydantic import SecretStr


class FakeMT5:
    def __init__(self):
        self.err = (0, "OK")

    def last_error(self):
        return self.err


def test_connection_success(monkeypatch):
    fake = FakeMT5()
    fake.initialize = lambda **_: True
    fake.login = lambda **_: True
    fake.shutdown = lambda: True
    monkeypatch.setattr(connection_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)

    svc = connection_service.ConnectionService()
    creds = LoginCredential(login=1, password=SecretStr("x"), server="demo")
    assert svc.initialize(creds).success
    assert svc.login(creds).success
    assert svc.shutdown().success


def test_connection_failure(monkeypatch):
    fake = FakeMT5()
    fake.initialize = lambda **_: False
    fake.err = (100, "init failed")
    monkeypatch.setattr(connection_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    svc = connection_service.ConnectionService()
    res = svc.initialize()
    assert not res.success
    assert res.error_code == 100


def test_position_parsing_and_pricing(monkeypatch):
    fake = FakeMT5()
    fake.positions_get = lambda **_: [SimpleNamespace(ticket=1, symbol="EURUSD", price_open=1.1, price_current=1.101, tp=1.102, sl=1.0, volume=0.1, type=0)]
    fake.symbol_info = lambda s: SimpleNamespace(digits=5, point=0.00001)
    monkeypatch.setattr(positions_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    svc = positions_service.PositionService()
    res = svc.positions()
    assert res.success
    p: Position = res.data[0]
    assert round(p.pips_profit, 2) == 10.0


def test_candle_conversion(monkeypatch):
    fake = FakeMT5()
    fake.copy_rates_from_pos = lambda *args: [{"time": 1, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5}]
    monkeypatch.setattr(market_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    svc = market_service.MarketService()
    res = svc.get_candles("EURUSD", 1, 1)
    assert res.success
    assert res.data[0].close == 1.5


def test_error_propagation(monkeypatch):
    fake = FakeMT5()
    fake.positions_get = lambda **_: None
    fake.err = (404, "positions error")
    monkeypatch.setattr(positions_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    svc = positions_service.PositionService()
    res = svc.positions()
    assert not res.success
    assert res.error_message == "positions error"


def test_empty_positions_are_success(monkeypatch):
    fake = FakeMT5()
    fake.positions_get = lambda **_: []
    monkeypatch.setattr(positions_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    res = positions_service.PositionService().positions()
    assert res.success
    assert res.data == []


def test_candle_malformed_payload_returns_failure(monkeypatch):
    fake = FakeMT5()
    fake.copy_rates_from_pos = lambda *args: [{"time": 1, "open": 1.0, "high": 2.0, "low": 0.5}]
    monkeypatch.setattr(market_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    res = market_service.MarketService().get_candles("EURUSD", 1, 1)
    assert not res.success
    assert res.error_code == -4


def test_client_guards_before_initialize():
    client = MetaTrader5Client()
    res = client.positions()
    assert not res.success
    assert res.error_code == -10


def test_empty_candle_data_success(monkeypatch):
    fake = FakeMT5()
    fake.initialize = lambda **_: True
    fake.copy_rates_from_pos = lambda *args: []
    fake.shutdown = lambda: True
    monkeypatch.setattr(market_service, "mt5", fake)
    monkeypatch.setattr(raw_mod, "mt5", fake)
    import syntiq_mt5.connection.service as connection_service

    monkeypatch.setattr(connection_service, "mt5", fake)
    client = MetaTrader5Client()
    assert client.initialize().success
    candles = client.get_candles("EURUSD", 1, 10)
    assert candles.success
    assert candles.data == []
