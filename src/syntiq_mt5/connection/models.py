"""Connection credential model."""

from pydantic import BaseModel, SecretStr


class LoginCredential(BaseModel):
    """Credentials required to connect to a MetaTrader 5 terminal.

    The ``password`` field uses Pydantic's ``SecretStr`` type so the value
    is never accidentally logged or serialised in plain text.

    Attributes:
        login: MT5 account number.
        password: Account password (stored as a secret).
        server: Broker server name (e.g. ``"ICMarkets-Demo"``).
        path: Optional path to the ``terminal64.exe`` executable.  When
            ``None``, MT5 uses the default installation path.
    """

    login: int
    password: SecretStr
    server: str
    path: str | None = None


#: Alias kept for backward compatibility.
LoginCredentials = LoginCredential
