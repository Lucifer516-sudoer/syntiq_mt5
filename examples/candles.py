from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as client:
    client.initialize(creds)
    client.login(creds)
    candles = client.get_candles("EURUSD", timeframe=1, count=50)
    print(candles)
