from syntiq_mt5 import MT5, MT5Error

try:
    with MT5() as mt5:
        print(f"Open positions: {len(mt5.positions())}")
except MT5Error as error:
    print(f"{error.operation} failed [{error.code}]: {error.message}")
