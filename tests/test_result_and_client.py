from pydantic import ValidationError, SecretStr

from syntiq_mt5._core.errors import MT5ErrorInfo
from syntiq_mt5._core.execution import Result
from syntiq_mt5.client import MetaTrader5Client
from syntiq_mt5.connection.models import LoginCredential


class FakeConnectionService:
    def __init__(self, *, init_ok=True, login_ok=True, shutdown_ok=True):
        self.init_ok = init_ok
        self.login_ok = login_ok
        self.shutdown_ok = shutdown_ok

    def initialize(self, credentials=None):
        if self.init_ok:
            return Result.ok(None, context="initialize", operation="initialize")
        return Result.fail(
            MT5ErrorInfo(code=100, message="init failed"),
            context="initialize",
            operation="initialize",
        )

    def login(self, credentials):
        if self.login_ok:
            return Result.ok(None, context="login", operation="login")
        return Result.fail(
            MT5ErrorInfo(code=200, message="login failed"),
            context="login",
            operation="login",
        )

    def shutdown(self):
        if self.shutdown_ok:
            return Result.ok(None, context="shutdown", operation="shutdown")
        return Result.fail(
            MT5ErrorInfo(code=300, message="shutdown failed"),
            context="shutdown",
            operation="shutdown",
        )


def test_result_success_integrity():
    res = Result.ok([1, 2, 3], context="demo", operation="op")
    assert res.success
    assert res.data == [1, 2, 3]
    assert res.error_code is None
    assert res.error_message is None


def test_result_failure_integrity():
    err = MT5ErrorInfo(code=42, message="boom")
    res = Result.fail(err, context="ctx", operation="op")
    assert not res.success
    assert res.data is None
    assert res.error_code == 42
    assert res.error_message == "boom"


def test_result_invariant_rejects_invalid_failure_state():
    try:
        Result(success=False, data=[1], error_code=None, error_message=None)
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True


def test_client_login_before_initialize_is_rejected():
    client = MetaTrader5Client()
    creds = LoginCredential(login=1, password=SecretStr("x"), server="demo")
    res = client.login(creds)
    assert not res.success
    assert res.error_code == -10
    assert res.operation == "login"


def test_client_initialize_failure_blocks_positions(monkeypatch):
    client = MetaTrader5Client()
    client.connection = FakeConnectionService(init_ok=False)
    res = client.initialize()
    assert not res.success
    assert res.error_code == 100

    positions = client.positions()
    assert not positions.success
    assert positions.error_code == -10


def test_shutdown_idempotent_from_client_state(monkeypatch):
    client = MetaTrader5Client()
    client.connection = FakeConnectionService(shutdown_ok=True)
    first = client.shutdown()
    second = client.shutdown()
    assert first.success
    assert second.success
