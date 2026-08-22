"""Connection credential model."""

from pydantic import SecretStr

from syntiq_mt5._internal.model import MT5Model


class LoginCredential(MT5Model):
    """Credentials required to connect to a MetaTrader 5 terminal.

    The ``password`` field uses Pydantic's ``SecretStr`` type so the value
    is never accidentally logged or serialised in plain text.

    Attributes:
        login: MT5 account number.
        password: Account password (stored as a secret).
        server: Broker server name (e.g. ``"ICMarkets-Demo"``).
        path: Optional path to the ``terminal64.exe`` executable.  When
            ``None``, MT5 uses the default installation path.
        timeout: Native connection timeout in milliseconds.
        portable: Whether to launch the terminal in portable mode.

    """

    login: int
    password: SecretStr
    server: str
    path: str | None = None
    timeout: int = 60_000
    portable: bool = False
