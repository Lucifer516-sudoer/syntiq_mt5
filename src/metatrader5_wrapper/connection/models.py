from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, PositiveInt, SecretStr


class LoginCredential(BaseModel):
    """Credentials and terminal options used to connect to an MT5 account."""

    terminal_path: Path | None = Field(default=None, description="MT5 terminal path")
    login: int = Field(description="MT5 account number")
    password: SecretStr = Field(description="MT5 account password")
    server: str = Field(description="MT5 trade server name")
    timeout: PositiveInt = Field(
        default=60, description="Connection timeout in seconds"
    )
    portable: bool = Field(
        default=False,
        description="Launch the terminal in portable mode",
    )

    @property
    def timeout_ms(self) -> int:
        """Return the configured timeout in milliseconds for the MT5 API."""
        return self.timeout * 1_000


class ConnectionStage(StrEnum):
    """Connection operation stage associated with the result."""

    INITIALIZE = "initialize"
    LOGIN = "login"


class ConnectionResult(BaseModel):
    """Structured result for an MT5 connection attempt."""

    success: bool
    error_code: int | None
    error_message: str | None
    stage: ConnectionStage
    message: str | None = None

    @property
    def failed(self) -> bool:
        """Return ``True`` when the connection operation did not succeed."""
        return not self.success

    def unwrap(self) -> None:
        """Return ``None`` on success or raise ``RuntimeError`` on failure."""
        if self.success:
            return
        raise RuntimeError(self.describe_error())

    def expect(self, message: str) -> None:
        """Return ``None`` on success or raise ``RuntimeError`` with context."""
        if self.success:
            return
        raise RuntimeError(f"{message}: {self.describe_error()}")

    def describe_error(self) -> str:
        """Return a human-readable summary of the connection failure."""
        base_message = self.message or "MetaTrader 5 connection failed"
        return (
            f"{base_message} during {self.stage} [{self.error_code}]"
            f" {self.error_message}"
        )
