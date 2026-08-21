from types import SimpleNamespace

import pytest

import syntiq_mt5
from syntiq_mt5 import MT5, MT5CallError, MT5PlatformError, SyntiqMT5
from syntiq_mt5._internal.native import NativeMT5Adapter


def test_public_surface_has_one_operational_interface() -> None:
    assert MT5 is SyntiqMT5
    assert SyntiqMT5.__name__ == "SyntiqMT5"
    assert syntiq_mt5.__all__.count("MT5") == 1
    assert syntiq_mt5.__all__.count("SyntiqMT5") == 1
    assert not hasattr(syntiq_mt5, "MetaTrader5Client")
    assert not hasattr(syntiq_mt5, "Result")


def test_native_adapter_captures_error_immediately() -> None:
    events: list[str] = []
    module = SimpleNamespace(
        positions_total=lambda: events.append("operation") or 3,
        last_error=lambda: events.append("last_error") or (1, "Success"),
    )

    reply = NativeMT5Adapter(module).call("positions_total")

    assert reply.data == 3
    assert reply.error.code == 1
    assert events == ["operation", "last_error"]


def test_native_exception_becomes_adapter_failure() -> None:
    def fail() -> None:
        raise RuntimeError("IPC disconnected")

    module = SimpleNamespace(
        positions_total=fail,
        last_error=lambda: (-10005, "IPC timeout"),
    )

    reply = NativeMT5Adapter(module).call("positions_total")

    assert reply.failed
    assert reply.error.code == -10005
    assert "RuntimeError" in reply.error.message


def test_missing_native_package_becomes_platform_error(monkeypatch) -> None:
    def unavailable(_: str) -> None:
        raise ImportError("not installed")

    monkeypatch.setattr("syntiq_mt5._internal.native.import_module", unavailable)

    with pytest.raises(MT5PlatformError, match="not installed"):
        MT5(adapter=NativeMT5Adapter()).initialize()


def test_malformed_last_error_is_reported_on_failed_operation() -> None:
    module = SimpleNamespace(
        initialize=lambda: False,
        last_error=lambda: "invalid",
    )

    with pytest.raises(MT5CallError) as caught:
        MT5(adapter=NativeMT5Adapter(module)).initialize()

    assert caught.value.code == -1
    assert "last_error unavailable" in caught.value.message
