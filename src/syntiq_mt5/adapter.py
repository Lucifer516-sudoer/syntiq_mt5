"""Public adapter seam for deterministic tests and alternate transports."""

from syntiq_mt5._core.errors import MT5ErrorInfo as ErrorInfo
from syntiq_mt5._core.raw import MT5Adapter
from syntiq_mt5._core.raw import RawCallResult as AdapterReply

__all__ = ["AdapterReply", "ErrorInfo", "MT5Adapter"]
