from syntiq_mt5 import MT5, constants

with MT5() as mt5:
    candles = mt5.candles("EURUSD", constants.TIMEFRAME_M1, 50)
    for candle in candles:
        print(candle.time, candle.open, candle.high, candle.low, candle.close)
