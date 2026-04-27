from metatrader5_wrapper.account import AccountInfo
from metatrader5_wrapper.account import account_info as get_account_info
from metatrader5_wrapper.connection import ConnectionResult, LoginCredential
from metatrader5_wrapper.connection import initialize as initialize_connection
from metatrader5_wrapper.connection import login as login_account
from metatrader5_wrapper.models import OperationResult
from metatrader5_wrapper.positions import Position
from metatrader5_wrapper.positions import positions_get as get_positions
from metatrader5_wrapper.positions import positions_total as get_positions_total
from metatrader5_wrapper.symbols import SymbolInfo, Tick
from metatrader5_wrapper.symbols import symbol_info as get_symbol_info
from metatrader5_wrapper.symbols import symbol_info_tick as get_symbol_info_tick
from metatrader5_wrapper.symbols import symbol_select as select_symbol
from metatrader5_wrapper.symbols import symbols_get as get_symbols
from metatrader5_wrapper.symbols import symbols_total as get_symbols_total
from metatrader5_wrapper.terminal import TerminalInfo, TerminalVersion
from metatrader5_wrapper.terminal import shutdown as shutdown_terminal
from metatrader5_wrapper.terminal import terminal_info as get_terminal_info
from metatrader5_wrapper.terminal import version as get_version


class MetaTrader5Client:
    """Pythonic client facade for typed MetaTrader 5 operations.

    Provides a clean, context-manager-friendly interface to MT5 connection,
    account, symbol, and position operations. All errors are captured as
    typed ``ConnectionResult`` or ``OperationResult`` objects—no exceptions
    are raised for normal operation failures.

    Typical usage:

        creds = LoginCredential(
            login=12345678,
            password=SecretStr("password"),
            server="Broker-Demo"
        )
        with MetaTrader5Client(creds) as mt5:
            account = mt5.account_info()
            if account.success and account.data:
                print(account.data.balance)
    """

    def __init__(self, credentials: LoginCredential | None = None) -> None:
        """Initialize a MetaTrader5 client with optional credentials.

        Args:
            credentials: Optional LoginCredential for automatic connection on
                context manager entry. If ``None``, credentials must be provided
                to ``initialize()`` or ``login()`` later.
        """
        self.credentials = credentials

    def initialize(
        self,
        credentials: LoginCredential | None = None,
    ) -> ConnectionResult:
        """Initialize the terminal and optionally log in.

        If new credentials are provided, they replace any previously configured
        credentials for this client instance.

        Args:
            credentials: Optional LoginCredential. If provided, replaces the
                credentials stored on this client and is used for login.

        Returns:
            ConnectionResult with success status, connection stage, and error details.
        """
        if credentials is not None:
            self.credentials = credentials

        return initialize_connection(self.credentials)

    def connect(
        self,
        credentials: LoginCredential | None = None,
    ) -> "MetaTrader5Client":
        """Initialize the terminal and return the client on success.

        This is a convenience alias for application code that prefers a fluent,
        fail-fast startup path.
        """
        result = self.initialize(credentials)
        result.expect("Unable to connect to MetaTrader 5")
        return self

    def account_info(self) -> OperationResult[AccountInfo]:
        """Fetch current account details as a typed model.

        Requires an active, logged-in MT5 session.

        Returns:
            OperationResult[AccountInfo] with typed account data on success.
        """
        return get_account_info()

    def account(self) -> AccountInfo:
        """Return current account details or raise on failure."""
        return self.account_info().expect("Unable to fetch account info")

    def login(self, credentials: LoginCredential | None = None) -> ConnectionResult:
        """Log in to an MT5 account.

        Use this to defer login until after the terminal is initialized, or to
        switch between accounts.

        Args:
            credentials: Optional LoginCredential. If provided, replaces the
                credentials stored on this client.

        Returns:
            ConnectionResult with success status, stage, and error details.

        Raises:
            ValueError: If no credentials have been configured on this client
                and none are provided here.
        """
        if credentials is not None:
            self.credentials = credentials
        if self.credentials is None:
            raise ValueError("credentials are required to log in")

        return login_account(self.credentials)

    def terminal_info(self) -> OperationResult[TerminalInfo]:
        """Fetch terminal information and status.

        Returns:
            OperationResult[TerminalInfo] with terminal metadata on success.
        """
        return get_terminal_info()

    def terminal(self) -> TerminalInfo:
        """Return terminal details or raise on failure."""
        return self.terminal_info().expect("Unable to fetch terminal info")

    def symbols_total(self) -> OperationResult[int]:
        """Count the total number of tradeable symbols in the terminal.

        Returns:
            OperationResult[int] with the symbol count on success.
        """
        return get_symbols_total()

    def symbols_get(
        self, group: str | None = None
    ) -> OperationResult[list[SymbolInfo]]:
        """Fetch available trading symbols, optionally filtered by group.

        Args:
            group: Optional MT5 group filter (e.g., "*USD*", "CRYPTO*").

        Returns:
            OperationResult[list[SymbolInfo]] with symbol list on success.
        """
        return get_symbols(group=group)

    def symbols(self, group: str | None = None) -> list[SymbolInfo]:
        """Return trading symbols or raise on failure."""
        return self.symbols_get(group=group).expect("Unable to fetch symbols")

    def symbol_info(self, symbol: str) -> OperationResult[SymbolInfo]:
        """Fetch detailed information for a single trading symbol.

        Args:
            symbol: Symbol name (e.g., "EURUSD").

        Returns:
            OperationResult[SymbolInfo] with typed symbol metadata on success.
        """
        return get_symbol_info(symbol)

    def symbol(self, symbol: str) -> SymbolInfo:
        """Return one trading symbol or raise on failure."""
        return self.symbol_info(symbol).expect(
            f"Unable to fetch symbol info for {symbol!r}"
        )

    def symbol_info_tick(self, symbol: str) -> OperationResult[Tick]:
        """Fetch the latest tick data for a symbol.

        Args:
            symbol: Symbol name (e.g., "EURUSD").

        Returns:
            OperationResult[Tick] with bid, ask, time, and volume on success.
        """
        return get_symbol_info_tick(symbol)

    def tick(self, symbol: str) -> Tick:
        """Return the latest tick for ``symbol`` or raise on failure."""
        return self.symbol_info_tick(symbol).expect(
            f"Unable to fetch latest tick for {symbol!r}"
        )

    def symbol_select(self, symbol: str, enable: bool = True) -> OperationResult[None]:
        """Add or remove a symbol from the terminal's MarketWatch.

        Args:
            symbol: Symbol name.
            enable: If ``True`` (default), adds to MarketWatch. If ``False``, removes.

        Returns:
            OperationResult[None] indicating success or failure.
        """
        return select_symbol(symbol, enable=enable)

    def positions_total(self) -> OperationResult[int]:
        """Count the number of currently open positions.

        Returns:
            OperationResult[int] with the position count on success.
        """
        return get_positions_total()

    def positions_get(
        self,
        *,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> OperationResult[list[Position]]:
        """Fetch open positions, optionally filtered by symbol, group, or ticket.

        The filter is applied in priority order: symbol, then group, then ticket.

        Args:
            symbol: Optional symbol name to filter positions.
            group: Optional group filter using MT5 wildcards.
            ticket: Optional position ticket number for exact lookup.

        Returns:
            OperationResult[list[Position]] with typed positions on success.
        """
        return get_positions(symbol=symbol, group=group, ticket=ticket)

    def positions(
        self,
        *,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> list[Position]:
        """Return positions or raise on failure."""
        return self.positions_get(
            symbol=symbol,
            group=group,
            ticket=ticket,
        ).expect("Unable to fetch positions")

    def version(self) -> OperationResult[TerminalVersion]:
        """Fetch terminal version and build information.

        Returns:
            OperationResult[TerminalVersion] with version details on success.
        """
        return get_version()

    def terminal_version(self) -> TerminalVersion:
        """Return terminal version details or raise on failure."""
        return self.version().expect("Unable to fetch terminal version")

    def shutdown(self) -> OperationResult[None]:
        """Cleanly disconnect from the MetaTrader 5 terminal.

        Returns:
            OperationResult[None] indicating shutdown completed.
        """
        return shutdown_terminal()

    def __enter__(self) -> "MetaTrader5Client":
        """Enter context manager: initialize the terminal.

        Raises:
            RuntimeError: If initialization fails. The error message includes
                the stage, error code, and MT5 error message.
        """
        return self.connect()

    def __exit__(self, *_exc_info: object) -> None:
        """Exit context manager: cleanly shut down the terminal."""
        self.shutdown()
