from collections.abc import Iterable
from typing import Any, Protocol, TypeVar, cast

from metatrader5_wrapper.models import MT5NamedTupleModel

ModelT = TypeVar("ModelT", bound=MT5NamedTupleModel)


class SupportsAsDict(Protocol):
    def _asdict(self) -> dict[str, Any]: ...


def model_from_namedtuple(model: type[ModelT], payload: object) -> ModelT:
    """Build a Pydantic model from an MT5 namedtuple-like payload."""
    return model.model_validate(cast(SupportsAsDict, payload)._asdict())


def models_from_namedtuples(
    model: type[ModelT], payloads: Iterable[object]
) -> list[ModelT]:
    """Build Pydantic models from MT5 namedtuple-like payloads."""
    return [model_from_namedtuple(model, payload) for payload in payloads]
