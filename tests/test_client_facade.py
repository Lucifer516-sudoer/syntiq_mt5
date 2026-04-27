from pydantic import SecretStr

from metatrader5_wrapper.client import MetaTrader5Client
from metatrader5_wrapper.connection.models import (
    ConnectionResult,
    ConnectionStage,
    LoginCredential,
)
from metatrader5_wrapper.models import OperationResult


def test_client_initialize_updates_credentials(monkeypatch) -> None:
    captured: list[LoginCredential | None] = []
    client = MetaTrader5Client()
    credentials = LoginCredential(
        login=123456,
        password=SecretStr("secret"),
        server="Demo-Server",
    )

    def fake_initialize_connection(
        passed_credentials: LoginCredential | None,
    ) -> ConnectionResult:
        captured.append(passed_credentials)
        return ConnectionResult(
            success=True,
            error_code=1,
            error_message="Success",
            stage=ConnectionStage.INITIALIZE,
            message="Initialized",
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.client.initialize_connection",
        fake_initialize_connection,
    )

    result = client.initialize(credentials)

    assert result.success is True
    assert client.credentials == credentials
    assert captured == [credentials]


def test_client_login_requires_credentials() -> None:
    client = MetaTrader5Client()

    try:
        client.login()
    except ValueError as exc:
        assert str(exc) == "credentials are required to log in"
    else:
        raise AssertionError("Expected ValueError")


def test_client_symbol_and_positions_helpers_use_expect(monkeypatch) -> None:
    client = MetaTrader5Client()

    def fake_symbol_info(symbol: str) -> OperationResult[object]:
        assert symbol == "EURUSD"
        return OperationResult(success=True, data={"symbol": symbol})

    def fake_positions_get(
        *, symbol=None, group=None, ticket=None
    ) -> OperationResult[object]:
        assert symbol == "EURUSD"
        assert group is None
        assert ticket is None
        return OperationResult(success=True, data=[{"ticket": 1}])

    monkeypatch.setattr("metatrader5_wrapper.client.get_symbol_info", fake_symbol_info)
    monkeypatch.setattr("metatrader5_wrapper.client.get_positions", fake_positions_get)

    assert client.symbol("EURUSD") == {"symbol": "EURUSD"}
    assert client.positions(symbol="EURUSD") == [{"ticket": 1}]


def test_client_context_manager_shuts_down(monkeypatch) -> None:
    client = MetaTrader5Client()
    events: list[str] = []

    def fake_initialize(_credentials=None) -> ConnectionResult:
        events.append("connect")
        return ConnectionResult(
            success=True,
            error_code=1,
            error_message="Success",
            stage=ConnectionStage.INITIALIZE,
            message="Initialized",
        )

    def fake_shutdown() -> OperationResult[None]:
        events.append("shutdown")
        return OperationResult(success=True, message="Stopped")

    monkeypatch.setattr(client, "initialize", fake_initialize)
    monkeypatch.setattr(client, "shutdown", fake_shutdown)

    with client as connected:
        assert connected is client

    assert events == ["connect", "shutdown"]
