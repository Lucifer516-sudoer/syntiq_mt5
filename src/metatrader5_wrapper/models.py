from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class OperationResult(BaseModel, Generic[T]):
    """Generic structured result for MT5 operations.

    The model keeps MT5's explicit success and error semantics, while adding a
    few convenience helpers for application code.
    """

    success: bool
    data: T | None = None
    error_code: int | None = None
    error_message: str | None = None
    message: str | None = None

    @property
    def failed(self) -> bool:
        """Return ``True`` when the operation did not succeed."""
        return not self.success

    def unwrap(self) -> T:
        """Return data or raise ``RuntimeError`` with MT5 error details."""
        if self.success and self.data is not None:
            return self.data
        raise RuntimeError(self.describe_error())

    def expect(self, message: str) -> T:
        """Return data or raise ``RuntimeError`` prefixed with ``message``."""
        if self.success and self.data is not None:
            return self.data
        raise RuntimeError(f"{message}: {self.describe_error()}")

    def describe_error(self) -> str:
        """Return a human-readable error summary for logs and exceptions."""
        base_message = self.message or "MetaTrader 5 operation failed"
        if self.error_code is None and self.error_message is None:
            return base_message
        return f"{base_message} [{self.error_code}] {self.error_message}"


class MT5NamedTupleModel(BaseModel):
    """Base model for MT5 namedtuple payloads."""

    model_config = ConfigDict(extra="allow")
