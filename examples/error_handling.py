from syntiq_mt5 import MT5Error, SyntiqMT5

try:
    with SyntiqMT5() as mt5:
        print(f"Open positions: {len(mt5.positions())}")
except MT5Error as error:
    print(f"{error.operation} failed [{error.code}]: {error.message}")
