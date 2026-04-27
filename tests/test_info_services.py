from collections import namedtuple

from metatrader5_wrapper._core.results import MT5DataCallResult, MT5ErrorResult
from metatrader5_wrapper.account.service import account_info
from metatrader5_wrapper.terminal.service import terminal_info, version


def test_account_info_returns_typed_model(monkeypatch) -> None:
    raw_account = namedtuple(
        "RawAccount",
        [
            "login",
            "trade_mode",
            "leverage",
            "limit_orders",
            "margin_so_mode",
            "trade_allowed",
            "trade_expert",
            "margin_mode",
            "currency_digits",
            "fifo_close",
            "balance",
            "credit",
            "profit",
            "equity",
            "margin",
            "margin_free",
            "margin_level",
            "margin_so_call",
            "margin_so_so",
            "margin_initial",
            "margin_maintenance",
            "assets",
            "liabilities",
            "commission_blocked",
            "name",
            "server",
            "currency",
            "company",
        ],
    )

    def fake_account_info() -> MT5DataCallResult:
        return MT5DataCallResult(
            data=raw_account(
                123456,
                0,
                100,
                0,
                0,
                True,
                True,
                2,
                2,
                False,
                10_000.0,
                0.0,
                50.0,
                10_050.0,
                100.0,
                9_950.0,
                10050.0,
                50.0,
                30.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                "Demo",
                "Broker-Demo",
                "USD",
                "Broker",
            ),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.account.service.mt5_account.account_info",
        fake_account_info,
    )

    result = account_info()

    assert result.success is True
    assert result.data is not None
    assert result.data.login == 123456
    assert result.data.balance == 10_000.0


def test_terminal_info_returns_typed_model(monkeypatch) -> None:
    raw_terminal = namedtuple(
        "RawTerminal",
        [
            "community_account",
            "community_connection",
            "connected",
            "dlls_allowed",
            "trade_allowed",
            "tradeapi_disabled",
            "email_enabled",
            "ftp_enabled",
            "notifications_enabled",
            "mqid",
            "build",
            "maxbars",
            "codepage",
            "ping_last",
            "community_balance",
            "retransmission",
            "company",
            "name",
            "language",
            "path",
            "data_path",
            "commondata_path",
        ],
    )

    def fake_terminal_info() -> MT5DataCallResult:
        return MT5DataCallResult(
            data=raw_terminal(
                False,
                False,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                5000,
                100_000,
                1252,
                10,
                0.0,
                0.0,
                "MetaQuotes",
                "MetaTrader 5",
                "English",
                "C:/MT5",
                "C:/MT5/Data",
                "C:/MT5/Common",
            ),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.terminal.service.mt5_terminal.terminal_info",
        fake_terminal_info,
    )

    result = terminal_info()

    assert result.success is True
    assert result.data is not None
    assert result.data.connected is True
    assert result.data.build == 5000


def test_version_returns_typed_model(monkeypatch) -> None:
    def fake_version() -> MT5DataCallResult:
        return MT5DataCallResult(
            data=(500, 5000, "01 Jan 2026"),
            error=MT5ErrorResult(code=1, message="Success"),
        )

    monkeypatch.setattr(
        "metatrader5_wrapper.terminal.service.mt5_terminal.version",
        fake_version,
    )

    result = version()

    assert result.success is True
    assert result.data is not None
    assert result.data.version == 500
    assert result.data.build == 5000
