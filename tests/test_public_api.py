import metatrader5_wrapper as mt5w
from metatrader5_wrapper.client import MetaTrader5Client
from metatrader5_wrapper.connection.models import ConnectionResult, ConnectionStage
from metatrader5_wrapper.models import OperationResult


def test_public_api_exports_client_and_constants() -> None:
    assert mt5w.MetaTrader5Client is not None
    assert isinstance(mt5w.TIMEFRAME_M1, int)
    assert mt5w.symbol_info is not None
    assert mt5w.positions_get is not None


def test_operation_result_expect_returns_data() -> None:
    result = OperationResult[int](success=True, data=7)

    assert result.expect("value required") == 7
    assert result.unwrap() == 7


def test_operation_result_expect_raises_runtime_error() -> None:
    result = OperationResult[int](
        success=False,
        error_code=-1,
        error_message="Unknown symbol",
        message="Unable to fetch symbol info.",
    )

    try:
        result.expect("Symbol lookup failed")
    except RuntimeError as exc:
        assert str(exc) == (
            "Symbol lookup failed: Unable to fetch symbol info. [-1] Unknown symbol"
        )
    else:
        raise AssertionError("Expected RuntimeError")


def test_client_connect_returns_self(monkeypatch) -> None:
    client = MetaTrader5Client()

    def fake_initialize(_credentials=None) -> ConnectionResult:
        return ConnectionResult(
            success=True,
            error_code=1,
            error_message="Success",
            stage=ConnectionStage.INITIALIZE,
            message="MetaTrader 5 terminal initialized successfully.",
        )

    monkeypatch.setattr(client, "initialize", fake_initialize)

    assert client.connect() is client
