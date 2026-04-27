from metatrader5_wrapper.models import MT5NamedTupleModel


class TerminalInfo(MT5NamedTupleModel):
    """Typed terminal details returned by ``MetaTrader5.terminal_info()``."""

    community_account: bool
    community_connection: bool
    connected: bool
    dlls_allowed: bool
    trade_allowed: bool
    tradeapi_disabled: bool
    email_enabled: bool
    ftp_enabled: bool
    notifications_enabled: bool
    mqid: bool
    build: int
    maxbars: int
    codepage: int
    ping_last: int
    community_balance: float
    retransmission: float
    company: str
    name: str
    language: str
    path: str
    data_path: str
    commondata_path: str


class TerminalVersion(MT5NamedTupleModel):
    """Typed terminal version payload returned by ``MetaTrader5.version()``."""

    version: int
    build: int
    release_date: str
