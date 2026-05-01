"""Pricing utility functions shared across the SDK."""


def calculate_pip_size(digits: int, point: float) -> float:
    """Calculate the pip size for a symbol.

    MT5 uses fractional pips (pipettes) for 3- and 5-digit pricing.
    In those cases one pip equals 10 points, so we multiply accordingly.

    Args:
        digits: Number of decimal places for the symbol price (e.g. 5 for EURUSD).
        point:  Smallest price increment for the symbol (e.g. 0.00001 for EURUSD).

    Returns:
        Pip size in price units.
            - digits in (3, 5) → point * 10  (fractional-pip symbols)
            - otherwise        → point        (standard symbols)
    """
    return point * 10 if digits in (3, 5) else point
