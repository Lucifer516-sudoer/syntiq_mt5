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
from importlib import import_module
from threading import RLock
from typing import Any, Protocol

from syntiq_mt5._core.mt5_import import mt5

from .errors import MT5ErrorInfo


@dataclass(frozen=True, slots=True)
class RawCallResult:
    """Outcome of a single MT5 API call.

    Attributes:
        data: The value returned by the MT5 function, or ``None`` on failure.
        error: The error state captured from ``mt5.last_error()`` immediately
            after the call. The official generic success code is ``1``.
        failed: Whether the adapter itself failed to complete the call.
        platform_unavailable: Whether failure was caused by the missing package.
    """

    data: Any
    error: MT5ErrorInfo
    failed: bool = False
    platform_unavailable: bool = False


class MT5Adapter(Protocol):
    """Seam around the process-global MetaTrader5 extension."""

    def call(self, operation: str, /, *args: Any, **kwargs: Any) -> RawCallResult:
        """Invoke one MT5 operation and capture its error state."""


class NativeMT5Adapter:
    """Thread-safe, lazy adapter for the native MetaTrader5 package."""

    _lock = RLock()

    def __init__(self, module: Any | None = None) -> None:
        self._module = module
        self._import_error: Exception | None = None

    def _load(self) -> Any | None:
        if self._module is not None:
            return self._module
        if self._import_error is not None:
            return None
        try:
            self._module = import_module("MetaTrader5")
        except (ImportError, OSError) as exc:
            self._import_error = exc
        return self._module

    def call(self, operation: str, /, *args: Any, **kwargs: Any) -> RawCallResult:
        """Call the extension while serializing access to global error state."""
        with self._lock:
            module = self._load()
            if module is None:
                detail = (
                    str(self._import_error) if self._import_error else "not installed"
                )
                return RawCallResult(
                    data=None,
                    error=MT5ErrorInfo(
                        code=-100000,
                        message=f"MetaTrader5 is unavailable: {detail}",
                    ),
                    failed=True,
                    platform_unavailable=True,
                )

            try:
                function = getattr(module, operation)
                data = function(*args, **kwargs)
            except Exception as exc:  # pragma: no cover - native boundary
                error = self._last_error(module)
                return RawCallResult(
                    data=None,
                    error=MT5ErrorInfo(
                        code=error.code if error.code not in (0, 1) else -2,
                        message=f"MT5 {operation} raised {type(exc).__name__}: {exc}",
                    ),
                    failed=True,
                )

            return RawCallResult(data=data, error=self._last_error(module))

    @staticmethod
    def _last_error(module: Any) -> MT5ErrorInfo:
        try:
            code, message = module.last_error()
            return MT5ErrorInfo(code=int(code), message=str(message))
        except Exception as exc:  # pragma: no cover - native boundary
            return MT5ErrorInfo(
                code=-1,
                message=f"MetaTrader5.last_error unavailable: {exc}",
            )


DEFAULT_ADAPTER = NativeMT5Adapter()


def call_mt5(
    operation: str | Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> RawCallResult:
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
    if isinstance(operation, str):
        return DEFAULT_ADAPTER.call(operation, *args, **kwargs)

    # Compatibility path for third-party callers using the old callable interface.
    data: Any = None
    call_exception: Exception | None = None
    try:
        data = operation(*args, **kwargs)
    except Exception as exc:  # pragma: no cover - defensive boundary
        call_exception = exc

    try:
        code, message = mt5.last_error()
        error = MT5ErrorInfo(code=int(code), message=str(message))
    except (AttributeError, TypeError, ValueError):
        error = MT5ErrorInfo(code=-1, message="MetaTrader5.last_error unavailable")

    if call_exception is not None:
        return RawCallResult(
            data=None,
            error=MT5ErrorInfo(
                code=error.code if error.code != 0 else -2,
                message=f"MT5 call raised {type(call_exception).__name__}: {call_exception}",
            ),
            failed=True,
        )
    return RawCallResult(data=data, error=error)
