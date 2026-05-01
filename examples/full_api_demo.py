"""
Full API demonstration showing all syntiq-mt5 capabilities.
"""

from datetime import datetime, timedelta, timezone

from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MetaTrader5Client, TradeRequest, constants

# Setup credentials
creds = LoginCredential(
    login=12345678, password=SecretStr("your-password"), server="Broker-Demo"
)


def main() -> None:
    with MetaTrader5Client(debug=True) as mt5:
        # Initialize and login
        init_result = mt5.initialize(creds)
        if not init_result.success:
            print(f"Initialize failed: {init_result.error_message}")
            return

        login_result = mt5.login(creds)
        if not login_result.success:
            print(f"Login failed: {login_result.error_message}")
            return

        # Account Information
        print("\n=== Account Information ===")
        acc_result = mt5.account_info()
        if acc_result.success:
            acc = acc_result.data
            print(f"Balance: {acc.balance} {acc.currency}")
            print(f"Equity: {acc.equity}")
            print(f"Margin: {acc.margin}")
            print(f"Leverage: 1:{acc.leverage}")

        # Terminal Information
        print("\n=== Terminal Information ===")
        term_result = mt5.terminal_info()
        if term_result.success:
            term = term_result.data
            print(f"Build: {term.build}")
            print(f"Connected: {term.connected}")
            print(f"Trade allowed: {term.trade_allowed}")

        # Symbol Operations
        print("\n=== Symbol Operations ===")
        symbols_result = mt5.symbols_get()
        if symbols_result.success:
            print(f"Total symbols: {len(symbols_result.data)}")
            print(f"First 5: {symbols_result.data[:5]}")

        symbol_info_result = mt5.symbol_info("EURUSD")
        if symbol_info_result.success:
            info = symbol_info_result.data
            print(f"\nEURUSD Info:")
            print(f"  Digits: {info.digits}")
            print(f"  Spread: {info.spread_pips} pips")
            print(f"  Contract size: {info.contract_size}")

        tick_result = mt5.symbol_info_tick("EURUSD")
        if tick_result.success:
            tick = tick_result.data
            print(f"\nCurrent tick:")
            print(f"  Bid: {tick.bid}")
            print(f"  Ask: {tick.ask}")
            print(f"  Spread: {tick.spread}")

        # Positions
        print("\n=== Positions ===")
        pos_result = mt5.positions()
        if pos_result.success:
            print(f"Open positions: {len(pos_result.data)}")
            for pos in pos_result.data[:3]:
                print(f"  {pos.symbol}: {pos.volume} lots, {pos.pips_profit:.1f} pips")

        # Candles
        print("\n=== Candles ===")
        candles_result = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_M1, count=10)
        if candles_result.success:
            print(f"Recent candles: {len(candles_result.data)}")
            if candles_result.data:
                c = candles_result.data[-1]
                print(f"  Last: O={c.open} H={c.high} L={c.low} C={c.close}")

        # Historical rates with date range
        date_from = datetime.now(timezone.utc) - timedelta(days=7)
        date_to = datetime.now(timezone.utc)
        rates_result = mt5.copy_rates_range("EURUSD", constants.TIMEFRAME_H1, date_from, date_to)
        if rates_result.success:
            print(f"Historical rates (7 days): {len(rates_result.data)}")

        # Tick data
        print("\n=== Tick Data ===")
        tick_date = datetime.now(timezone.utc) - timedelta(hours=1)
        ticks_result = mt5.copy_ticks_from("EURUSD", tick_date, count=100, flags=constants.COPY_TICKS_ALL)
        if ticks_result.success:
            print(f"Ticks retrieved: {len(ticks_result.data)}")
            if ticks_result.data:
                t = ticks_result.data[0]
                print(f"  First tick: Bid={t.bid} Ask={t.ask}")

        # Orders
        print("\n=== Orders ===")
        orders_result = mt5.orders_get()
        if orders_result.success:
            print(f"Pending orders: {len(orders_result.data)}")

        # Order calculations
        margin_result = mt5.order_calc_margin(constants.ORDER_TYPE_BUY, "EURUSD", 0.1, 1.08500)
        if margin_result.success:
            print(f"Required margin for 0.1 lot: {margin_result.data}")

        profit_result = mt5.order_calc_profit(constants.ORDER_TYPE_BUY, "EURUSD", 0.1, 1.08500, 1.09000)
        if profit_result.success:
            print(f"Expected profit (50 pips): {profit_result.data}")

        # Order check (validation only, not sending)
        print("\n=== Order Validation ===")
        request = TradeRequest(
            action=constants.TRADE_ACTION_DEAL,
            symbol="EURUSD",
            volume=0.01,
            type=constants.ORDER_TYPE_BUY,
            price=1.08500,
            sl=1.08000,
            tp=1.09000,
            deviation=10,
            comment="Demo order",
        )
        check_result = mt5.order_check(request)
        if check_result.success:
            result = check_result.data
            if result.is_successful:
                print("Order validation passed")
            else:
                print(f"Order validation failed: {result.comment}")

        # Historical orders and deals
        print("\n=== Trading History ===")
        hist_date_from = datetime.now(timezone.utc) - timedelta(days=30)
        hist_date_to = datetime.now(timezone.utc)

        hist_orders_result = mt5.history_orders_get(hist_date_from, hist_date_to)
        if hist_orders_result.success:
            print(f"Historical orders (30 days): {len(hist_orders_result.data)}")

        hist_deals_result = mt5.history_deals_get(hist_date_from, hist_date_to)
        if hist_deals_result.success:
            print(f"Historical deals (30 days): {len(hist_deals_result.data)}")
            if hist_deals_result.data:
                deal = hist_deals_result.data[0]
                print(f"  Last deal: {deal.symbol}, profit={deal.net_profit}")

        # Market book (if supported)
        print("\n=== Market Book ===")
        book_add_result = mt5.market_book_add("EURUSD")
        if book_add_result.success and book_add_result.data:
            print("Subscribed to market book")

            book_result = mt5.market_book_get("EURUSD")
            if book_result.success:
                print(f"Book entries: {len(book_result.data)}")
                for entry in book_result.data[:3]:
                    side = "BUY" if entry.is_buy else "SELL"
                    print(f"  {side}: {entry.price} @ {entry.volume_real}")

            mt5.market_book_release("EURUSD")

        print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
