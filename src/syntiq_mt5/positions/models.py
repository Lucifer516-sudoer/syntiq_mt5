from pydantic import BaseModel


class Position(BaseModel):
    ticket: int
    symbol: str
    price_open: float
    price_current: float
    tp: float
    sl: float
    volume: float
    digits: int
    point: float
    type: int

    @property
    def pip_size(self) -> float:
        return self.point * 10 if self.digits in (3, 5) else self.point

    @property
    def pips_profit(self) -> float:
        direction = 1 if self.type == 0 else -1
        return ((self.price_current - self.price_open) * direction) / self.pip_size

    @property
    def pips_to_tp(self) -> float:
        if self.tp == 0:
            return 0.0
        direction = 1 if self.type == 0 else -1
        return ((self.tp - self.price_current) * direction) / self.pip_size
