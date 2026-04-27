from dataclasses import dataclass
from typing import Any

import MetaTrader5 as mt5  # type: ignore[import-untyped]
from pydantic import BaseModel


class MT5ErrorResult(BaseModel):
    """Raw error state captured from ``MetaTrader5.last_error()``."""

    code: int
    message: str

    def __str__(self) -> str:
        return f"MT5Error::[{self.code}]::{self.message}"


@dataclass(frozen=True, slots=True)
class MT5DataCallResult:
    """Raw MT5 payload with the immediately captured global error state."""

    data: Any
    error: MT5ErrorResult

    @property
    def success(self) -> bool:
        """Return ``True`` when MT5 returned a payload."""
        return self.data is not None


@dataclass(frozen=True, slots=True)
class MT5BoolCallResult:
    """Raw boolean MT5 result with the captured global error state."""

    success: bool
    error: MT5ErrorResult


def capture_last_error() -> MT5ErrorResult:
    """Capture MT5's global error state exactly once for the current operation."""
    code, message = mt5.last_error()
    return MT5ErrorResult(code=code, message=message)
