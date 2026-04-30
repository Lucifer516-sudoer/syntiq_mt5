from pydantic import SecretStr

from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as client:
    result = client.positions()
    if not result.success:
        print("Expected failure before initialize:", result.error_code, result.error_message)

    client.initialize(creds)
    login = client.login(creds)

    if login.success:
        ok = client.positions()
        print("Success:", ok.success, "count:", len(ok.data or []))
    else:
        print("Failure:", login.error_code, login.error_message, login.context)
