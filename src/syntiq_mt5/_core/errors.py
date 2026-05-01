"""Exception hierarchy and error data model for the SDK.

All errors that originate from the MT5 C extension are captured as
``MT5ErrorInfo`` values and surfaced through ``Result.fail()``.  The
exception classes are reserved for truly unrecoverable situations where
a ``Result`` cannot be returned (e.g. during object construction).
"""

from pydantic import BaseModel


class MT5Error(Exception):
    """Base exception for all SDK-level errors."""


class MT5ConnectionError(MT5Error):
    """Raised when a connection lifecycle operation fails unrecoverably."""


class MT5ExecutionError(MT5Error):
    """Raised when a data retrieval or trade execution fails unrecoverably."""


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
