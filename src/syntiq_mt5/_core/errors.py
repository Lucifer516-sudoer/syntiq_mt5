from pydantic import BaseModel


class MT5Error(Exception):
    """Base exception for wrapper errors."""


class MT5ConnectionError(MT5Error):
    """Raised for connection lifecycle failures."""


class MT5ExecutionError(MT5Error):
    """Raised for execution/data retrieval failures."""


class MT5ErrorInfo(BaseModel):
    code: int
    message: str
