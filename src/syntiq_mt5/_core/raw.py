from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from syntiq_mt5._core.mt5_import import mt5

from .errors import MT5ErrorInfo


@dataclass(frozen=True, slots=True)
class RawCallResult:
    data: Any
    error: MT5ErrorInfo


def call_mt5(operation: Callable[..., Any], *args: Any, **kwargs: Any) -> RawCallResult:
    data: Any = None
    call_exception: Exception | None = None
    try:
        data = operation(*args, **kwargs)
    except Exception as exc:  # pragma: no cover - defensive boundary
        call_exception = exc

    if hasattr(mt5, "last_error"):
        code, message = mt5.last_error()
        error = MT5ErrorInfo(code=code, message=message)
    else:
        error = MT5ErrorInfo(code=-1, message="MetaTrader5.last_error unavailable")

    if call_exception is not None:
        return RawCallResult(
            data=None,
            error=MT5ErrorInfo(
                code=error.code if error.code != 0 else -2,
                message=f"MT5 call raised {type(call_exception).__name__}: {call_exception}",
            ),
        )
    return RawCallResult(data=data, error=error)
