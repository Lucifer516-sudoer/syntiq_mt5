from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.symbols.models import SymbolInfo, SymbolTick


class SymbolService:
    """Retrieves symbol metadata and tick data from the MT5 terminal.

    Wraps ``mt5.symbols_total()``, ``mt5.symbols_get()``,
    ``mt5.symbol_select()``, ``mt5.symbol_info()``, and
    ``mt5.symbol_info_tick()`` via ``call_mt5``, parses the raw structs
    into ``SymbolInfo`` / ``SymbolTick`` models, and returns ``Result[T]``.
    """
    def symbols_total(self) -> Result[int]:
        raw = call_mt5(mt5.symbols_total)
        if raw.data is None:
            return Result.fail(raw.error, context="symbols_total", operation="symbols_total")
        try:
            count = int(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 symbols_total payload: {exc}",
                    }
                ),
                context="symbols_total",
                operation="symbols_total",
            )
        return Result.ok(count, context="symbols_total", operation="symbols_total")

    def symbols_get(self, group: str | None = None) -> Result[list[str]]:
        raw = call_mt5(mt5.symbols_get, group=group) if group else call_mt5(mt5.symbols_get)
        if raw.data is None:
            return Result.fail(raw.error, context="symbols_get", operation="symbols_get")
        try:
            symbols = [str(s.name) for s in raw.data]
        except (AttributeError, TypeError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 symbols_get payload: {exc}",
                    }
                ),
                context="symbols_get",
                operation="symbols_get",
            )
        return Result.ok(symbols, context="symbols_get", operation="symbols_get")

    def symbol_select(self, symbol: str, enable: bool) -> Result[bool]:
        raw = call_mt5(mt5.symbol_select, symbol, enable)
        if raw.data is None:
            return Result.fail(raw.error, context="symbol_select", operation="symbol_select")
        try:
            success = bool(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 symbol_select payload: {exc}",
                    }
                ),
                context="symbol_select",
                operation="symbol_select",
            )
        return Result.ok(success, context="symbol_select", operation="symbol_select")

    def symbol_info(self, symbol: str) -> Result[SymbolInfo]:
        raw = call_mt5(mt5.symbol_info, symbol)
        if raw.data is None:
            return Result.fail(raw.error, context="symbol_info", operation="symbol_info")
        try:
            info = SymbolInfo(
                custom=bool(raw.data.custom),
                chart_mode=int(raw.data.chart_mode),
                select=bool(raw.data.select),
                visible=bool(raw.data.visible),
                session_deals=int(raw.data.session_deals),
                session_buy_orders=int(raw.data.session_buy_orders),
                session_sell_orders=int(raw.data.session_sell_orders),
                volume=int(raw.data.volume),
                volumehigh=int(raw.data.volumehigh),
                volumelow=int(raw.data.volumelow),
                time=int(raw.data.time),
                digits=int(raw.data.digits),
                spread=int(raw.data.spread),
                spread_float=bool(raw.data.spread_float),
                ticks_bookdepth=int(raw.data.ticks_bookdepth),
                trade_calc_mode=int(raw.data.trade_calc_mode),
                trade_mode=int(raw.data.trade_mode),
                start_time=int(raw.data.start_time),
                expiration_time=int(raw.data.expiration_time),
                trade_stops_level=int(raw.data.trade_stops_level),
                trade_freeze_level=int(raw.data.trade_freeze_level),
                trade_exemode=int(raw.data.trade_exemode),
                swap_mode=int(raw.data.swap_mode),
                swap_rollover3days=int(raw.data.swap_rollover3days),
                margin_hedged_use_leg=bool(raw.data.margin_hedged_use_leg),
                expiration_mode=int(raw.data.expiration_mode),
                filling_mode=int(raw.data.filling_mode),
                order_mode=int(raw.data.order_mode),
                order_gtc_mode=int(raw.data.order_gtc_mode),
                option_mode=int(raw.data.option_mode),
                option_right=int(raw.data.option_right),
                bid=float(raw.data.bid),
                bidhigh=float(raw.data.bidhigh),
                bidlow=float(raw.data.bidlow),
                ask=float(raw.data.ask),
                askhigh=float(raw.data.askhigh),
                asklow=float(raw.data.asklow),
                last=float(raw.data.last),
                lasthigh=float(raw.data.lasthigh),
                lastlow=float(raw.data.lastlow),
                volume_real=float(raw.data.volume_real),
                volumehigh_real=float(raw.data.volumehigh_real),
                volumelow_real=float(raw.data.volumelow_real),
                option_strike=float(raw.data.option_strike),
                point=float(raw.data.point),
                trade_tick_value=float(raw.data.trade_tick_value),
                trade_tick_value_profit=float(raw.data.trade_tick_value_profit),
                trade_tick_value_loss=float(raw.data.trade_tick_value_loss),
                trade_tick_size=float(raw.data.trade_tick_size),
                trade_contract_size=float(raw.data.trade_contract_size),
                trade_accrued_interest=float(raw.data.trade_accrued_interest),
                trade_face_value=float(raw.data.trade_face_value),
                trade_liquidity_rate=float(raw.data.trade_liquidity_rate),
                volume_min=float(raw.data.volume_min),
                volume_max=float(raw.data.volume_max),
                volume_step=float(raw.data.volume_step),
                volume_limit=float(raw.data.volume_limit),
                swap_long=float(raw.data.swap_long),
                swap_short=float(raw.data.swap_short),
                margin_initial=float(raw.data.margin_initial),
                margin_maintenance=float(raw.data.margin_maintenance),
                session_volume=float(raw.data.session_volume),
                session_turnover=float(raw.data.session_turnover),
                session_interest=float(raw.data.session_interest),
                session_buy_orders_volume=float(raw.data.session_buy_orders_volume),
                session_sell_orders_volume=float(raw.data.session_sell_orders_volume),
                session_open=float(raw.data.session_open),
                session_close=float(raw.data.session_close),
                session_aw=float(raw.data.session_aw),
                session_price_settlement=float(raw.data.session_price_settlement),
                session_price_limit_min=float(raw.data.session_price_limit_min),
                session_price_limit_max=float(raw.data.session_price_limit_max),
                margin_hedged=float(raw.data.margin_hedged),
                price_change=float(raw.data.price_change),
                price_volatility=float(raw.data.price_volatility),
                price_theoretical=float(raw.data.price_theoretical),
                price_greeks_delta=float(raw.data.price_greeks_delta),
                price_greeks_theta=float(raw.data.price_greeks_theta),
                price_greeks_gamma=float(raw.data.price_greeks_gamma),
                price_greeks_vega=float(raw.data.price_greeks_vega),
                price_greeks_rho=float(raw.data.price_greeks_rho),
                price_greeks_omega=float(raw.data.price_greeks_omega),
                price_sensitivity=float(raw.data.price_sensitivity),
                basis=str(raw.data.basis),
                category=str(raw.data.category),
                currency_base=str(raw.data.currency_base),
                currency_profit=str(raw.data.currency_profit),
                currency_margin=str(raw.data.currency_margin),
                bank=str(raw.data.bank),
                description=str(raw.data.description),
                exchange=str(raw.data.exchange),
                formula=str(raw.data.formula),
                isin=str(raw.data.isin),
                name=str(raw.data.name),
                page=str(raw.data.page),
                path=str(raw.data.path),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 symbol_info payload: {exc}",
                    }
                ),
                context="symbol_info",
                operation="symbol_info",
            )
        return Result.ok(info, context="symbol_info", operation="symbol_info")

    def symbol_info_tick(self, symbol: str) -> Result[SymbolTick]:
        raw = call_mt5(mt5.symbol_info_tick, symbol)
        if raw.data is None:
            return Result.fail(raw.error, context="symbol_info_tick", operation="symbol_info_tick")
        try:
            tick = SymbolTick(
                time=int(raw.data.time),
                bid=float(raw.data.bid),
                ask=float(raw.data.ask),
                last=float(raw.data.last),
                volume=int(raw.data.volume),
                time_msc=int(raw.data.time_msc),
                flags=int(raw.data.flags),
                volume_real=float(raw.data.volume_real),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -3,
                        "message": f"Invalid MT5 symbol_info_tick payload: {exc}",
                    }
                ),
                context="symbol_info_tick",
                operation="symbol_info_tick",
            )
        return Result.ok(tick, context="symbol_info_tick", operation="symbol_info_tick")
