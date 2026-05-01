from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MetaTrader5Client, constants

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as client:
    init_result = client.initialize(creds)
    if not init_result.success:
        print("Initialize failed:", init_result.error_message)
        raise SystemExit(1)
    
    login_result = client.login(creds)
    if not login_result.success:
        print("Login failed:", login_result.error_message)
        raise SystemExit(1)
    
    candles = client.get_candles("EURUSD", timeframe=constants.TIMEFRAME_M1, count=50)
    print(candles)
