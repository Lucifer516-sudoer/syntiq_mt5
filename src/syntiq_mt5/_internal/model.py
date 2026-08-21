"""Shared configuration for validated syntiq-mt5 models."""

from pydantic import BaseModel, ConfigDict


class MT5Model(BaseModel):
    """Immutable base for request values and terminal snapshots."""

    model_config = ConfigDict(frozen=True)
