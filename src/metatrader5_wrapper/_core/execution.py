from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic import model_validator

from .errors import MT5ErrorInfo

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error_code: int | None = None
    error_message: str | None = None
    context: str | None = None

    @model_validator(mode="after")
    def _validate_state(self) -> "Result[T]":
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
    def ok(cls, data: T, context: str | None = None) -> "Result[T]":
        return cls(success=True, data=data, context=context)

    @classmethod
    def fail(cls, error: MT5ErrorInfo, context: str) -> "Result[T]":
        return cls(
            success=False,
            data=None,
            error_code=error.code,
            error_message=error.message,
            context=context,
        )
