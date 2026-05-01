"""Connection lifecycle service for the MT5 terminal."""

from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.connection.models import LoginCredential


class ConnectionService:
    """Manages the MT5 terminal connection lifecycle.

    Wraps ``mt5.initialize()``, ``mt5.login()``, ``mt5.shutdown()``, and
    ``mt5.version()``.  Tracks initialisation state internally so that
    calling ``initialize()`` a second time is a no-op rather than an error.

    Typical usage follows the sequence:
    ``initialize`` → ``login`` → (operations) → ``shutdown``.
    """

    def __init__(self) -> None:
        self._initialized = False

    def initialize(self, credentials: LoginCredential | None = None) -> Result[None]:
        """Connect to the MetaTrader 5 terminal.

        If the terminal is already initialised, returns success immediately
        without making another MT5 call.  Optionally accepts a path to the
        terminal executable via ``credentials.path``.

        Args:
            credentials: Optional credentials whose ``path`` field is used
                to locate the terminal executable.  All other fields are
                ignored here — call ``login()`` separately to authenticate.

        Returns:
            ``Result[None]``: Success if the terminal connected; failure with
            the MT5 error code and message otherwise.
        """
        if self._initialized:
            return Result.ok(None, context="initialize", operation="initialize")
        kwargs = {"path": credentials.path} if credentials and credentials.path else {}
        raw = call_mt5(mt5.initialize, **kwargs)
        if not raw.data:
            return Result.fail(raw.error, context="initialize", operation="initialize")
        self._initialized = True
        return Result.ok(None, context="initialize", operation="initialize")

    def login(self, credentials: LoginCredential) -> Result[None]:
        """Authenticate with the broker using the provided credentials.

        Must be called after a successful ``initialize()``.  The password
        is extracted from the ``SecretStr`` field and never logged.

        Args:
            credentials: Account number, password, and server name.

        Returns:
            ``Result[None]``: Success if authentication succeeded; failure
            with the MT5 error code otherwise.
        """
        raw = call_mt5(
            mt5.login,
            login=credentials.login,
            password=credentials.password.get_secret_value(),
            server=credentials.server,
        )
        if not raw.data:
            return Result.fail(raw.error, context="login", operation="login")
        return Result.ok(None, context="login", operation="login")

    def shutdown(self) -> Result[None]:
        """Disconnect from the MetaTrader 5 terminal.

        Resets the internal initialisation flag regardless of whether the
        MT5 call succeeds, so subsequent calls to ``initialize()`` will
        attempt a fresh connection.

        Returns:
            ``Result[None]``: Success in almost all cases; failure only if
            MT5 explicitly returns ``False`` from ``shutdown()``.
        """
        raw = call_mt5(mt5.shutdown)
        self._initialized = False
        if raw.data is False:
            return Result.fail(raw.error, context="shutdown", operation="shutdown")
        return Result.ok(None, context="shutdown", operation="shutdown")

    def version(self) -> Result[tuple[int, int, str]]:
        """Retrieve the MetaTrader 5 terminal version.

        Returns:
            ``Result[tuple[int, int, str]]``: A 3-tuple of
            ``(build_number, build_date, version_string)`` on success, or
            a failure result if the terminal is not connected or returns an
            unexpected payload.
        """
        raw = call_mt5(mt5.version)
        if raw.data is None:
            return Result.fail(raw.error, context="version", operation="version")
        try:
            # MT5 version() returns tuple: (build, date, version_string)
            version_tuple = tuple(raw.data)
            if len(version_tuple) != 3:
                return Result.fail(
                    raw.error.model_copy(
                        update={
                            "code": raw.error.code if raw.error.code != 0 else -1003,
                            "message": f"Invalid MT5 version payload: expected 3 elements, got {len(version_tuple)}",
                        }
                    ),
                    context="version",
                    operation="version",
                )
            result = (int(version_tuple[0]), int(version_tuple[1]), str(version_tuple[2]))
        except (TypeError, ValueError, IndexError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1003,
                        "message": f"Invalid MT5 version payload: {exc}",
                    }
                ),
                context="version",
                operation="version",
            )
        return Result.ok(result, context="version", operation="version")
