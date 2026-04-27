from pydantic import SecretStr

from metatrader5_wrapper._core.connection import MT5CallResult
from metatrader5_wrapper._core.results import MT5ErrorResult
from metatrader5_wrapper.connection.models import (
    ConnectionResult,
    ConnectionStage,
    LoginCredential,
)
from metatrader5_wrapper.connection.service import initialize


def test_initialize_without_credentials_success(monkeypatch) -> None:
    def fake_initialize_terminal(**kwargs) -> MT5CallResult:
        assert kwargs == {
            "terminal_path": None,
            "timeout_ms": 60_000,
            "portable": False,
        }
        return MT5CallResult(
            success=True,
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.connection.service.mt5_connection.initialize_terminal",
        fake_initialize_terminal,
    )

    result = initialize()

    assert result.success is True
    assert result.error_code == 1
    assert result.error_message == "Success"
    assert result.stage is ConnectionStage.INITIALIZE


def test_initialize_with_credentials_success(monkeypatch) -> None:
    calls: list[str] = []
    credentials = LoginCredential(
        login=123456,
        password=SecretStr("secret"),
        server="Demo-Server",
        timeout=30,
        portable=True,
    )

    def fake_initialize_terminal(**kwargs) -> MT5CallResult:
        calls.append("initialize")
        assert kwargs == {
            "terminal_path": None,
            "timeout_ms": 30_000,
            "portable": True,
        }
        return MT5CallResult(
            success=True,
            error=MT5ErrorResult(code=1, message="Initialized"),
        )

    def fake_login_account(**kwargs) -> MT5CallResult:
        calls.append("login")
        assert kwargs == {
            "login": 123456,
            "password": "secret",
            "server": "Demo-Server",
            "timeout_ms": 30_000,
        }
        return MT5CallResult(
            success=True,
            error=MT5ErrorResult(code=1, message="Logged in"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.connection.service.mt5_connection.initialize_terminal",
        fake_initialize_terminal,
    )
    monkeypatch.setattr(
        "metatrader5_wrapper.connection.service.mt5_connection.login_account",
        fake_login_account,
    )

    result = initialize(credentials)

    assert calls == ["initialize", "login"]
    assert result.success is True
    assert result.error_code == 1
    assert result.error_message == "Logged in"
    assert result.stage is ConnectionStage.LOGIN


def test_initialize_failure_preserves_raw_error(monkeypatch) -> None:
    def fake_initialize_terminal(**_kwargs) -> MT5CallResult:
        return MT5CallResult(
            success=False,
            error=MT5ErrorResult(code=-10003, message="Terminal not found"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.connection.service.mt5_connection.initialize_terminal",
        fake_initialize_terminal,
    )

    result = initialize()

    assert result.success is False
    assert result.error_code == -10003
    assert result.error_message == "Terminal not found"
    assert result.stage is ConnectionStage.INITIALIZE


def test_login_failure_preserves_raw_error(monkeypatch) -> None:
    credentials = LoginCredential(
        login=123456,
        password=SecretStr("wrong"),
        server="Demo-Server",
    )

    def fake_initialize_terminal(**_kwargs) -> MT5CallResult:
        return MT5CallResult(
            success=True,
            error=MT5ErrorResult(code=1, message="Initialized"),
        )

    def fake_login_account(**_kwargs) -> MT5CallResult:
        return MT5CallResult(
            success=False,
            error=MT5ErrorResult(code=-6, message="Authorization failed"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.connection.service.mt5_connection.initialize_terminal",
        fake_initialize_terminal,
    )
    monkeypatch.setattr(
        "metatrader5_wrapper.connection.service.mt5_connection.login_account",
        fake_login_account,
    )

    result = initialize(credentials)

    assert result.success is False
    assert result.error_code == -6
    assert result.error_message == "Authorization failed"
    assert result.stage is ConnectionStage.LOGIN


def test_connection_result_expect_raises_runtime_error() -> None:
    result = ConnectionResult(
        success=False,
        error_code=-6,
        error_message="Authorization failed",
        stage=ConnectionStage.LOGIN,
        message="Unable to log in to the MetaTrader 5 account.",
    )

    try:
        result.expect("Startup failed")
    except RuntimeError as exc:
        assert str(exc) == (
            "Startup failed: Unable to log in to the MetaTrader 5 account. "
            "during login [-6] Authorization failed"
        )
    else:
        raise AssertionError("Expected RuntimeError")
