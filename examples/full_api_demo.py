"""Read-only tour of the primary syntiq-mt5 interface."""

from datetime import UTC, datetime, timedelta

from syntiq_mt5 import MT5, constants


def main() -> None:
    with MT5() as mt5:
        account = mt5.account_info()
        print(f"Account {account.login}: {account.balance} {account.currency}")

        terminal = mt5.terminal_info()
        print(f"Terminal build {terminal.build}; connected={terminal.connected}")

        quote = mt5.symbol_info_tick("EURUSD")
        print(f"EURUSD {quote.bid}/{quote.ask}")

        print(f"Open positions: {len(mt5.positions())}")
        print(f"Pending orders: {len(mt5.orders_get())}")
        print(f"Symbols: {len(mt5.symbols_get())}")

        candles = mt5.candles("EURUSD", constants.TIMEFRAME_H1, 10)
        print(f"Completed H1 candles: {len(candles)}")

        end = datetime.now(UTC)
        ticks = mt5.copy_ticks_range(
            "EURUSD",
            end - timedelta(minutes=5),
            end,
            constants.COPY_TICKS_ALL,
        )
        print(f"Ticks in last five minutes: {len(ticks)}")

        orders = mt5.history_orders_get(
            date_from=end - timedelta(days=30),
            date_to=end,
        )
        deals = mt5.history_deals_get(
            date_from=end - timedelta(days=30),
            date_to=end,
        )
        print(f"30-day history: {len(orders)} orders, {len(deals)} deals")


if __name__ == "__main__":
    main()
