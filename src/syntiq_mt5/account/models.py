"""Account information model."""

from pydantic import BaseModel


class AccountInfo(BaseModel):
    """Trading account details from MetaTrader 5.

    Wraps the raw ``AccountInfo`` struct returned by ``mt5.account_info()``.
    Contains both static account properties (leverage, currency) and
    live financial state (balance, equity, margin).

    Attributes:
        login: Account number.
        trade_mode: Account type (demo, contest, real) as an MT5 integer.
        leverage: Account leverage (e.g. 100 for 1:100).
        limit_orders: Maximum number of active pending orders allowed.
        margin_so_mode: Stop-out mode (percent or money) as an MT5 integer.
        trade_allowed: Whether trading is permitted on this account.
        trade_expert: Whether Expert Advisors are permitted to trade.
        margin_mode: Margin calculation mode as an MT5 integer.
        currency_digits: Number of decimal places for the account currency.
        fifo_close: Whether positions must be closed in FIFO order.
        balance: Account balance in account currency.
        credit: Credit facility amount.
        profit: Current floating profit/loss across all open positions.
        equity: Effective account value (balance + profit + credit).
        margin: Margin currently in use.
        margin_free: Free margin available for new positions.
        margin_level: Margin level as a percentage (equity / margin * 100).
        margin_so_call: Margin call level (percent or money, per ``margin_so_mode``).
        margin_so_so: Stop-out level (percent or money, per ``margin_so_mode``).
        margin_initial: Initial margin requirement.
        margin_maintenance: Maintenance margin requirement.
        assets: Total assets.
        liabilities: Total liabilities.
        commission_blocked: Commission reserved for open positions.
        name: Account holder name.
        server: Broker server name.
        currency: Account currency code (e.g. ``"USD"``).
        company: Broker company name.
    """

    login: int
    trade_mode: int
    leverage: int
    limit_orders: int
    margin_so_mode: int
    trade_allowed: bool
    trade_expert: bool
    margin_mode: int
    currency_digits: int
    fifo_close: bool
    balance: float
    credit: float
    profit: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    margin_so_call: float
    margin_so_so: float
    margin_initial: float
    margin_maintenance: float
    assets: float
    liabilities: float
    commission_blocked: float
    name: str
    server: str
    currency: str
    company: str

    @property
    def margin_used_percent(self) -> float:
        """Margin in use as a percentage of equity.

        Returns 0.0 when equity is zero to avoid division by zero.

        Returns:
            Margin usage percentage (0–100+).
        """
        if self.equity == 0:
            return 0.0
        return (self.margin / self.equity) * 100

    @property
    def equity_to_balance_ratio(self) -> float:
        """Ratio of equity to balance, indicating unrealised P&L impact.

        A value above 1.0 means open positions are in profit; below 1.0
        means they are in loss.  Returns 0.0 when balance is zero.

        Returns:
            Equity / balance ratio.
        """
        if self.balance == 0:
            return 0.0
        return self.equity / self.balance
