from __future__ import annotations

from datetime import datetime

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.history.models import Deal
from syntiq_mt5.orders.models import HistoricalOrder


class HistoryService:
    """Retrieves historical orders and deals from the MT5 trade history.

    Wraps ``mt5.history_orders_total()``, ``mt5.history_orders_get()``,
    ``mt5.history_deals_total()``, and ``mt5.history_deals_get()`` via
    ``call_mt5``, parses raw structs into ``HistoricalOrder`` and ``Deal``
    models, and returns ``Result[T]``.
    """
    def history_orders_total(self, date_from: datetime, date_to: datetime) -> Result[int]:
        raw = call_mt5(mt5.history_orders_total, date_from, date_to)
        if raw.data is None:
            return Result.fail(raw.error, context="history_orders_total", operation="history_orders_total")
        try:
            count = int(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 history_orders_total payload: {exc}",
                    }
                ),
                context="history_orders_total",
                operation="history_orders_total",
            )
        return Result.ok(count, context="history_orders_total", operation="history_orders_total")

    def history_orders_get(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Result[list[HistoricalOrder]]:
        if date_from and date_to:
            raw = call_mt5(mt5.history_orders_get, date_from, date_to)
        elif group:
            raw = call_mt5(mt5.history_orders_get, group=group)
        elif ticket:
            raw = call_mt5(mt5.history_orders_get, ticket=ticket)
        elif position:
            raw = call_mt5(mt5.history_orders_get, position=position)
        else:
            from syntiq_mt5._core.errors import MT5ErrorInfo
            return Result.fail(
                MT5ErrorInfo(code=-5, message="Must provide date_from/date_to, group, ticket, or position"),
                context="history_orders_get",
                operation="history_orders_get",
            )

        if raw.data is None:
            return Result.fail(raw.error, context="history_orders_get", operation="history_orders_get")

        try:
            orders = [
                HistoricalOrder(
                    ticket=int(order.ticket),
                    time_setup=int(order.time_setup),
                    time_setup_msc=int(order.time_setup_msc),
                    time_done=int(order.time_done),
                    time_done_msc=int(order.time_done_msc),
                    time_expiration=int(order.time_expiration),
                    type=int(order.type),
                    type_time=int(order.type_time),
                    type_filling=int(order.type_filling),
                    state=int(order.state),
                    magic=int(order.magic),
                    position_id=int(order.position_id),
                    position_by_id=int(order.position_by_id),
                    reason=int(order.reason),
                    volume_initial=float(order.volume_initial),
                    volume_current=float(order.volume_current),
                    price_open=float(order.price_open),
                    sl=float(order.sl),
                    tp=float(order.tp),
                    price_current=float(order.price_current),
                    price_stoplimit=float(order.price_stoplimit),
                    symbol=str(order.symbol),
                    comment=str(order.comment),
                    external_id=str(order.external_id),
                )
                for order in raw.data
            ]
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 history_orders_get payload: {exc}",
                    }
                ),
                context="history_orders_get",
                operation="history_orders_get",
            )
        return Result.ok(orders, context="history_orders_get", operation="history_orders_get")

    def history_deals_total(self, date_from: datetime, date_to: datetime) -> Result[int]:
        raw = call_mt5(mt5.history_deals_total, date_from, date_to)
        if raw.data is None:
            return Result.fail(raw.error, context="history_deals_total", operation="history_deals_total")
        try:
            count = int(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 history_deals_total payload: {exc}",
                    }
                ),
                context="history_deals_total",
                operation="history_deals_total",
            )
        return Result.ok(count, context="history_deals_total", operation="history_deals_total")

    def history_deals_get(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Result[list[Deal]]:
        if date_from and date_to:
            raw = call_mt5(mt5.history_deals_get, date_from, date_to)
        elif group:
            raw = call_mt5(mt5.history_deals_get, group=group)
        elif ticket:
            raw = call_mt5(mt5.history_deals_get, ticket=ticket)
        elif position:
            raw = call_mt5(mt5.history_deals_get, position=position)
        else:
            from syntiq_mt5._core.errors import MT5ErrorInfo
            return Result.fail(
                MT5ErrorInfo(code=-5, message="Must provide date_from/date_to, group, ticket, or position"),
                context="history_deals_get",
                operation="history_deals_get",
            )

        if raw.data is None:
            return Result.fail(raw.error, context="history_deals_get", operation="history_deals_get")

        try:
            deals = [
                Deal(
                    ticket=int(deal.ticket),
                    order=int(deal.order),
                    time=int(deal.time),
                    time_msc=int(deal.time_msc),
                    type=int(deal.type),
                    entry=int(deal.entry),
                    magic=int(deal.magic),
                    position_id=int(deal.position_id),
                    reason=int(deal.reason),
                    volume=float(deal.volume),
                    price=float(deal.price),
                    commission=float(deal.commission),
                    swap=float(deal.swap),
                    profit=float(deal.profit),
                    fee=float(deal.fee),
                    symbol=str(deal.symbol),
                    comment=str(deal.comment),
                    external_id=str(deal.external_id),
                )
                for deal in raw.data
            ]
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 history_deals_get payload: {exc}",
                    }
                ),
                context="history_deals_get",
                operation="history_deals_get",
            )
        return Result.ok(deals, context="history_deals_get", operation="history_deals_get")
