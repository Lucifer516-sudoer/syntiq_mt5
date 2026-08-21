"""Public exception and error-detail types for syntiq-mt5."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErrorInfo:
    """Error state captured immediately after a native MT5 operation.

    Attributes:
        code: Numeric code reported by ``MetaTrader5.last_error()``.
        message: Human-readable description reported by the terminal package.

    """

    code: int
    message: str


class MT5Error(Exception):
    """Base class for failures exposed by the public session interface.

    Attributes:
        operation: Native MT5 operation that failed.
        code: Native or wrapper-specific failure code.
        message: Human-readable failure description.

    """

    def __init__(self, operation: str, code: int, message: str) -> None:
        """Initialize an operation-scoped MT5 failure."""
        self.operation = operation
        self.code = code
        self.message = message
        super().__init__(f"{operation} failed [{code}]: {message}")


class MT5PlatformError(MT5Error):
    """The official MetaTrader5 package is unavailable on this platform."""


class MT5CallError(MT5Error):
    """MT5 raised or returned the documented failure sentinel."""


class MT5PayloadError(MT5Error):
    """MT5 returned a payload that does not match its documented shape."""


class MT5StateError(MT5Error):
    """An operation is invalid for the current terminal lifecycle state."""
