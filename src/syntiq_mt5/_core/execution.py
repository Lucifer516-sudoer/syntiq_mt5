"""Result monad for all SDK operations.

Every public method in the SDK returns ``Result[T]`` instead of raising
exceptions.  This makes error handling explicit and composable — callers
always check ``result.success`` before accessing ``result.data``.

Typical usage::

    result = client.positions()
    if result.success:
        for pos in result.data:
            print(pos.symbol, pos.pips_profit)
    else:
        print(f"Error {result.error_code}: {result.error_message}")
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, model_validator

from .errors import MT5ErrorInfo

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    """Typed outcome of an SDK operation.

    A ``Result`` is either successful (``success=True``, ``data`` is set)
    or failed (``success=False``, ``error_code`` and ``error_message`` are
    set).  The model validator enforces this invariant at construction time
    so an invalid state is impossible to construct.

    Attributes:
        success: ``True`` if the operation completed without error.
        data: The operation's return value.  Always ``None`` on failure.
        error_code: MT5 error code on failure; ``None`` on success.
        error_message: Human-readable error description; ``None`` on success.
        context: The MT5 API function name that was called (e.g. ``"positions_get"``).
        operation: Logical operation name, usually the same as ``context``.
    """

    success: bool
    data: T | None = None
    error_code: int | None = None
    error_message: str | None = None
    context: str | None = None
    operation: str | None = None

    @model_validator(mode="after")
    def _validate_state(self) -> Result[T]:
        """Enforce the success/failure invariant.

        Raises:
            ValueError: If ``success=False`` but ``data`` is set, or if
                ``error_code`` / ``error_message`` are missing.
        """
        if self.success:
            return self
        if self.data is not None:
            raise ValueError("Result.data must be None when success=False")
        if self.error_code is None or self.error_message is None:
            raise ValueError(
                "Result.error_code and Result.error_message are required when success=False"
            )
        return self

    @classmethod
    def ok(
        cls, data: T, context: str | None = None, operation: str | None = None
    ) -> Result[T]:
        """Construct a successful result.

        Args:
            data: The value to carry.  May be ``None`` for void operations.
            context: MT5 API function name for tracing.
            operation: Logical operation name for tracing.

        Returns:
            A ``Result`` with ``success=True`` and ``data`` set.
        """
        return cls(success=True, data=data, context=context, operation=operation)

    @classmethod
    def fail(
        cls, error: MT5ErrorInfo, context: str, operation: str | None = None
    ) -> Result[T]:
        """Construct a failed result from an ``MT5ErrorInfo``.

        Args:
            error: The error captured from ``mt5.last_error()`` or an
                SDK-internal sentinel.
            context: MT5 API function name where the failure occurred.
            operation: Logical operation name for tracing.

        Returns:
            A ``Result`` with ``success=False``, ``data=None``, and the
            error fields populated from ``error``.
        """
        return cls(
            success=False,
            data=None,
            error_code=error.code,
            error_message=error.message,
            context=context,
            operation=operation,
        )
