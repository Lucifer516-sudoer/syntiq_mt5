import os

from pydantic import SecretStr

from syntiq_mt5 import MT5, LoginCredential

credentials = LoginCredential(
    login=int(os.environ["MT5_LOGIN"]),
    password=SecretStr(os.environ["MT5_PASSWORD"]),
    server=os.environ["MT5_SERVER"],
)

with MT5(credentials) as mt5:
    for position in mt5.positions():
        print(position.symbol, position.volume, round(position.pips_profit, 1))
