from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.terminal.models import TerminalInfo


class TerminalService:
    """Retrieves terminal state and configuration from MT5.

    Wraps ``mt5.terminal_info()`` via ``call_mt5``, parses the raw
    ``TerminalInfo`` struct into a typed model, and returns
    ``Result[TerminalInfo]``.
    """
    def terminal_info(self) -> Result[TerminalInfo]:
        raw = call_mt5(mt5.terminal_info)
        if raw.data is None:
            return Result.fail(raw.error, context="terminal_info", operation="terminal_info")
        try:
            info = TerminalInfo(
                community_account=bool(raw.data.community_account),
                community_connection=bool(raw.data.community_connection),
                connected=bool(raw.data.connected),
                dlls_allowed=bool(raw.data.dlls_allowed),
                trade_allowed=bool(raw.data.trade_allowed),
                tradeapi_disabled=bool(raw.data.tradeapi_disabled),
                email_enabled=bool(raw.data.email_enabled),
                ftp_enabled=bool(raw.data.ftp_enabled),
                notifications_enabled=bool(raw.data.notifications_enabled),
                mqid=bool(raw.data.mqid),
                build=int(raw.data.build),
                maxbars=int(raw.data.maxbars),
                codepage=int(raw.data.codepage),
                ping_last=int(raw.data.ping_last),
                community_balance=float(raw.data.community_balance),
                retransmission=float(raw.data.retransmission),
                company=str(raw.data.company),
                name=str(raw.data.name),
                language=str(raw.data.language),
                path=str(raw.data.path),
                data_path=str(raw.data.data_path),
                commondata_path=str(raw.data.commondata_path),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 terminal_info payload: {exc}",
                    }
                ),
                context="terminal_info",
                operation="terminal_info",
            )
        return Result.ok(info, context="terminal_info", operation="terminal_info")
