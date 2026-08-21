"""Production adapter for the process-global MetaTrader5 extension."""

from importlib import import_module
from threading import RLock
from typing import Any

from syntiq_mt5.adapter import AdapterReply
from syntiq_mt5.errors import ErrorInfo


class NativeMT5Adapter:
    """Lazy, serialized adapter for the official MetaTrader5 package.

    MetaTrader5 stores connection and error state at process scope. A shared
    reentrant lock therefore covers both the native operation and the immediate
    ``last_error()`` read, preserving the relationship between them.

    Args:
        module: Optional native-compatible module, primarily for contract tests.

    """

    _lock = RLock()

    def __init__(self, module: Any | None = None) -> None:
        self._module = module
        self._import_error: Exception | None = None

    def call(
        self,
        operation: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> AdapterReply:
        """Invoke an operation and atomically capture its native error state."""
        with self._lock:
            module = self._load()
            if module is None:
                detail = (
                    str(self._import_error) if self._import_error else "not installed"
                )
                return AdapterReply(
                    data=None,
                    error=ErrorInfo(
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
                return AdapterReply(
                    data=None,
                    error=ErrorInfo(
                        code=error.code if error.code not in (0, 1) else -2,
                        message=f"MT5 {operation} raised {type(exc).__name__}: {exc}",
                    ),
                    failed=True,
                )

            return AdapterReply(data=data, error=self._last_error(module))

    def _load(self) -> Any | None:
        """Import MetaTrader5 once and retain any platform/import failure."""
        if self._module is not None:
            return self._module
        if self._import_error is not None:
            return None
        try:
            self._module = import_module("MetaTrader5")
        except (ImportError, OSError) as exc:
            self._import_error = exc
        return self._module

    @staticmethod
    def _last_error(module: Any) -> ErrorInfo:
        """Read native error state without allowing boundary exceptions out."""
        try:
            code, message = module.last_error()
            return ErrorInfo(code=int(code), message=str(message))
        except Exception as exc:  # pragma: no cover - native boundary
            return ErrorInfo(
                code=-1,
                message=f"MetaTrader5.last_error unavailable: {exc}",
            )


DEFAULT_ADAPTER = NativeMT5Adapter()
"""Shared production adapter used when callers do not inject another adapter."""
