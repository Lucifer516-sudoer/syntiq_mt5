"""Low-level MT5 call wrapper.

Every interaction with the MT5 C extension goes through ``call_mt5``.
This single entry point ensures that:

1. ``mt5.last_error()`` is always read *after* the call completes, not
   before — the extension only updates the error state on each call.
2. Unexpected Python exceptions raised by the extension are caught and
   converted into structured ``MT5ErrorInfo`` values rather than
   propagating as bare exceptions.
3. Callers always receive a ``RawCallResult`` with a consistent shape,
   regardless of whether the call succeeded, returned ``None``, or raised.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from syntiq_mt5._core.mt5_import import mt5

from .errors import MT5ErrorInfo


@dataclass(frozen=True, slots=True)
class RawCallResult:
    """Outcome of a single MT5 API call.

    Attributes:
        data: The value returned by the MT5 function, or ``None`` on failure.
        error: The error state captured from ``mt5.last_error()`` immediately
            after the call.  ``error.code == 0`` means no error occurred.
    """

    data: Any
    error: MT5ErrorInfo


def call_mt5(operation: Callable[..., Any], *args: Any, **kwargs: Any) -> RawCallResult:
    """Execute an MT5 API function and return a structured result.

    Calls ``operation(*args, **kwargs)``, then immediately reads
    ``mt5.last_error()`` to capture the error state.  If the call raises
    a Python exception (rare but possible with some MT5 builds), the
    exception is wrapped in an ``MT5ErrorInfo`` and returned as a failure
    rather than propagated.

    The error code precedence when an exception is raised:
    - Use ``last_error().code`` if it is non-zero (MT5 set an error).
    - Fall back to ``-2`` if ``last_error()`` reports 0 (no MT5 error was
      set, but the call still raised — SDK-internal sentinel).

    Args:
        operation: The MT5 API callable (e.g. ``mt5.positions_get``).
        *args: Positional arguments forwarded to ``operation``.
        **kwargs: Keyword arguments forwarded to ``operation``.

    Returns:
        A ``RawCallResult`` containing the return value and the error state.
        ``data`` is ``None`` when the call failed or returned nothing useful.
    """
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
