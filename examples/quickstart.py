from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as mt5:
    init_result = mt5.initialize(creds)
    if not init_result.success:
        print("initialize failed:", init_result.error_code, init_result.error_message)
        raise SystemExit(1)

    login_result = mt5.login(creds)
    if not login_result.success:
        print("login failed:", login_result.error_code, login_result.error_message)
        raise SystemExit(1)

    positions = mt5.positions()
    if positions.success and positions.data:
        p = positions.data[0]
        print(p.symbol, p.volume, round(p.pips_profit, 1))
    else:
        print(positions.error_code, positions.error_message, positions.operation)
