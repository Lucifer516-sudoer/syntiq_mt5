from types import SimpleNamespace

try:
    import MetaTrader5 as mt5  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover
    mt5 = SimpleNamespace()  # monkeypatched in tests
