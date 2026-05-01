"""Terminal information model."""

from pydantic import BaseModel


class TerminalInfo(BaseModel):
    """State and configuration of the connected MetaTrader 5 terminal.

    Wraps the raw ``TerminalInfo`` struct returned by ``mt5.terminal_info()``.
    Useful for verifying that the terminal is ready for trading before
    submitting orders.

    Attributes:
        community_account: Whether the terminal is connected with a MQL5 community account.
        community_connection: Whether the MQL5 community server is reachable.
        connected: Whether the terminal is connected to the broker server.
        dlls_allowed: Whether DLL imports are permitted.
        trade_allowed: Whether trading is enabled in the terminal settings.
        tradeapi_disabled: Whether the trade API has been disabled by the broker.
        email_enabled: Whether email notifications are enabled.
        ftp_enabled: Whether FTP report delivery is enabled.
        notifications_enabled: Whether push notifications are enabled.
        mqid: Whether the terminal has a valid MQL5 ID.
        build: Terminal build number.
        maxbars: Maximum number of bars in a chart.
        codepage: Code page used for string encoding.
        ping_last: Last measured round-trip latency to the broker server (ms).
        community_balance: MQL5 community account balance.
        retransmission: Network packet retransmission ratio (0.0–1.0).
        company: Broker company name as shown in the terminal.
        name: Terminal product name.
        language: Terminal interface language.
        path: Path to the terminal executable.
        data_path: Path to the terminal data directory.
        commondata_path: Path to the shared data directory for all terminals.
    """

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
    ping_last: int  # last ping in milliseconds
    community_balance: float
    retransmission: float
    company: str
    name: str
    language: str
    path: str
    data_path: str
    commondata_path: str

    @property
    def version(self) -> str:
        """Terminal version as a human-readable string (e.g. ``"Build 4000"``).

        Returns:
            Version string derived from the build number.
        """
        return f"Build {self.build}"

    @property
    def is_ready_for_trading(self) -> bool:
        """Whether the terminal is in a state where trade requests can be submitted.

        All three conditions must hold: the terminal must be connected to the
        broker, trading must be enabled in the terminal settings, and the
        trade API must not have been disabled by the broker.

        Returns:
            ``True`` if the terminal can accept trade requests.
        """
        return self.connected and self.trade_allowed and not self.tradeapi_disabled
