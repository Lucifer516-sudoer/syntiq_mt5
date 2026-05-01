"""Central import point for the MetaTrader5 C extension.

Importing ``mt5`` from here instead of directly from ``MetaTrader5``
keeps the rest of the SDK decoupled from the platform dependency.
On non-Windows environments (CI, unit tests) the import fails gracefully
and ``mt5`` is replaced with an empty ``SimpleNamespace`` that tests can
monkeypatch freely.
"""

from types import SimpleNamespace

try:
    import MetaTrader5 as mt5  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover
    mt5 = SimpleNamespace()  # monkeypatched in tests

__all__ = ["mt5"]
