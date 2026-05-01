from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.account.models import AccountInfo


class AccountService:
    """Retrieves trading account information from the MT5 terminal.

    Wraps ``mt5.account_info()`` via ``call_mt5``, parses the raw
    ``AccountInfo`` struct into a typed model, and returns
    ``Result[AccountInfo]``.
    """
    def account_info(self) -> Result[AccountInfo]:
        raw = call_mt5(mt5.account_info)
        if raw.data is None:
            return Result.fail(raw.error, context="account_info", operation="account_info")
        try:
            info = AccountInfo(
                login=int(raw.data.login),
                trade_mode=int(raw.data.trade_mode),
                leverage=int(raw.data.leverage),
                limit_orders=int(raw.data.limit_orders),
                margin_so_mode=int(raw.data.margin_so_mode),
                trade_allowed=bool(raw.data.trade_allowed),
                trade_expert=bool(raw.data.trade_expert),
                margin_mode=int(raw.data.margin_mode),
                currency_digits=int(raw.data.currency_digits),
                fifo_close=bool(raw.data.fifo_close),
                balance=float(raw.data.balance),
                credit=float(raw.data.credit),
                profit=float(raw.data.profit),
                equity=float(raw.data.equity),
                margin=float(raw.data.margin),
                margin_free=float(raw.data.margin_free),
                margin_level=float(raw.data.margin_level),
                margin_so_call=float(raw.data.margin_so_call),
                margin_so_so=float(raw.data.margin_so_so),
                margin_initial=float(raw.data.margin_initial),
                margin_maintenance=float(raw.data.margin_maintenance),
                assets=float(raw.data.assets),
                liabilities=float(raw.data.liabilities),
                commission_blocked=float(raw.data.commission_blocked),
                name=str(raw.data.name),
                server=str(raw.data.server),
                currency=str(raw.data.currency),
                company=str(raw.data.company),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 account_info payload: {exc}",
                    }
                ),
                context="account_info",
                operation="account_info",
            )
        return Result.ok(info, context="account_info", operation="account_info")
