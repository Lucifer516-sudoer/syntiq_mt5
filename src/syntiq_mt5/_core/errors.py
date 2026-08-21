"""Exception hierarchy and error data model for the SDK.

All errors that originate from the MT5 C extension are captured as
``MT5ErrorInfo`` values and surfaced through ``Result.fail()``.  The
exception classes are reserved for truly unrecoverable situations where
a ``Result`` cannot be returned (e.g. during object construction).
"""

from pydantic import BaseModel


class MT5Error(Exception):
    """Base exception for all SDK-level errors."""

    def __init__(self, operation: str, code: int, message: str) -> None:
        self.operation = operation
        self.code = code
        self.message = message
        super().__init__(f"{operation} failed [{code}]: {message}")


class MT5ConnectionError(MT5Error):
    """Raised when a connection lifecycle operation fails unrecoverably."""


class MT5ExecutionError(MT5Error):
    """Raised when a data retrieval or trade execution fails unrecoverably."""


class MT5PlatformError(MT5Error):
    """Raised when the native MetaTrader5 package is unavailable."""


class MT5CallError(MT5Error):
    """Raised when MT5 returns an operation-specific failure sentinel."""


class MT5PayloadError(MT5Error):
    """Raised when MT5 returns a payload that violates its documented shape."""


class MT5StateError(MT5Error):
    """Raised when an operation is invalid for the client lifecycle state."""


class MT5ErrorInfo(BaseModel):
    """Structured representation of an MT5 error.

    Produced by ``mt5.last_error()`` after every MT5 API call and carried
    inside ``Result`` objects so callers can inspect failure details without
    catching exceptions.

    Attributes:
        code: MT5 error code (0 means no error; negative codes are SDK-internal).
        message: Human-readable description of the error.
    """

    code: int
    message: str
