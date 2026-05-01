from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.orders.models import Order, TradeRequest, TradeResult


class OrderService:
    """Manages active orders and trade execution for the MT5 terminal.

    Wraps the MT5 order API (``orders_total``, ``orders_get``,
    ``order_calc_margin``, ``order_calc_profit``, ``order_check``,
    ``order_send``) via ``call_mt5``, parses raw structs into ``Order``
    and ``TradeResult`` models, and returns ``Result[T]``.
    """
    def orders_total(self) -> Result[int]:
        raw = call_mt5(mt5.orders_total)
        if raw.data is None:
            return Result.fail(raw.error, context="orders_total", operation="orders_total")
        try:
            count = int(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 orders_total payload: {exc}",
                    }
                ),
                context="orders_total",
                operation="orders_total",
            )
        return Result.ok(count, context="orders_total", operation="orders_total")

    def orders_get(self, symbol: str | None = None, group: str | None = None, ticket: int | None = None) -> Result[list[Order]]:
        if symbol:
            raw = call_mt5(mt5.orders_get, symbol=symbol)
        elif group:
            raw = call_mt5(mt5.orders_get, group=group)
        elif ticket:
            raw = call_mt5(mt5.orders_get, ticket=ticket)
        else:
            raw = call_mt5(mt5.orders_get)

        if raw.data is None:
            return Result.fail(raw.error, context="orders_get", operation="orders_get")

        try:
            orders = [
                Order(
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
                        "message": f"Invalid MT5 orders_get payload: {exc}",
                    }
                ),
                context="orders_get",
                operation="orders_get",
            )
        return Result.ok(orders, context="orders_get", operation="orders_get")

    def order_calc_margin(self, action: int, symbol: str, volume: float, price: float) -> Result[float]:
        raw = call_mt5(mt5.order_calc_margin, action, symbol, volume, price)
        if raw.data is None:
            return Result.fail(raw.error, context="order_calc_margin", operation="order_calc_margin")
        try:
            margin = float(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 order_calc_margin payload: {exc}",
                    }
                ),
                context="order_calc_margin",
                operation="order_calc_margin",
            )
        return Result.ok(margin, context="order_calc_margin", operation="order_calc_margin")

    def order_calc_profit(
        self, action: int, symbol: str, volume: float, price_open: float, price_close: float
    ) -> Result[float]:
        raw = call_mt5(mt5.order_calc_profit, action, symbol, volume, price_open, price_close)
        if raw.data is None:
            return Result.fail(raw.error, context="order_calc_profit", operation="order_calc_profit")
        try:
            profit = float(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 order_calc_profit payload: {exc}",
                    }
                ),
                context="order_calc_profit",
                operation="order_calc_profit",
            )
        return Result.ok(profit, context="order_calc_profit", operation="order_calc_profit")

    def order_check(self, request: TradeRequest) -> Result[TradeResult]:
        raw = call_mt5(mt5.order_check, request.model_dump())
        if raw.data is None:
            return Result.fail(raw.error, context="order_check", operation="order_check")
        try:
            result = TradeResult(
                retcode=int(raw.data.retcode),
                deal=int(raw.data.deal),
                order=int(raw.data.order),
                volume=float(raw.data.volume),
                price=float(raw.data.price),
                bid=float(raw.data.bid),
                ask=float(raw.data.ask),
                comment=str(raw.data.comment),
                request_id=int(raw.data.request_id),
                retcode_external=int(raw.data.retcode_external),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 order_check payload: {exc}",
                    }
                ),
                context="order_check",
                operation="order_check",
            )
        return Result.ok(result, context="order_check", operation="order_check")

    def order_send(self, request: TradeRequest) -> Result[TradeResult]:
        raw = call_mt5(mt5.order_send, request.model_dump())
        if raw.data is None:
            return Result.fail(raw.error, context="order_send", operation="order_send")
        try:
            result = TradeResult(
                retcode=int(raw.data.retcode),
                deal=int(raw.data.deal),
                order=int(raw.data.order),
                volume=float(raw.data.volume),
                price=float(raw.data.price),
                bid=float(raw.data.bid),
                ask=float(raw.data.ask),
                comment=str(raw.data.comment),
                request_id=int(raw.data.request_id),
                retcode_external=int(raw.data.retcode_external),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 order_send payload: {exc}",
                    }
                ),
                context="order_send",
                operation="order_send",
            )
        return Result.ok(result, context="order_send", operation="order_send")
