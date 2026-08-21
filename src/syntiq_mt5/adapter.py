"""Public adapter seam for deterministic tests and alternate transports."""

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from syntiq_mt5.errors import ErrorInfo


@dataclass(frozen=True, slots=True)
class AdapterReply:
    """Raw outcome returned by an :class:`MT5Adapter`.

    ``data`` preserves the native return value. ``failed`` describes adapter
    execution failure and is distinct from operation-specific ``None`` or
    ``False`` sentinels, which the session interprets using each MT5 contract.

    Attributes:
        data: Value returned by the native operation.
        error: Error state captured immediately after the operation.
        failed: Whether the adapter could not complete the operation.
        platform_unavailable: Whether the native package could not be loaded.

    """

    data: Any
    error: ErrorInfo
    failed: bool = False
    platform_unavailable: bool = False


@runtime_checkable
class MT5Adapter(Protocol):
    """Transport interface consumed by :class:`syntiq_mt5.SyntiqMT5`.

    Implementations must capture the operation's error state before another
    MT5 call can overwrite it. The production adapter serializes this sequence;
    test adapters can return deterministic native-shaped replies.
    """

    def call(
        self,
        operation: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> AdapterReply:
        """Invoke one named MT5 operation and return its raw outcome.

        Args:
            operation: Exact function name exposed by the MetaTrader5 package.
            *args: Positional arguments forwarded unchanged to the operation.
            **kwargs: Keyword arguments forwarded unchanged to the operation.

        Returns:
            The native value, immediate error state, and adapter failure flags.
            Implementations must not classify operation-specific ``None`` or
            ``False`` values as adapter failure; the session owns that policy.
        """


__all__ = ["AdapterReply", "ErrorInfo", "MT5Adapter"]
