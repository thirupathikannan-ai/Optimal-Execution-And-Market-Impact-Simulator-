import numpy as np


def temporary_market_impact(
    price: float,
    quantity: float,
    volume: float,
    coefficient: float,
    exponent: float = 1.0
) -> float:
    """
    Calculate temporary market impact in price units.
    """

    if volume <= 0:
        raise ValueError("volume must be positive")

    participation = abs(quantity) / volume

    return (
        price
        * coefficient
        * participation ** exponent
    )


def permanent_market_impact(
    price: float,
    cumulative_quantity: float,
    coefficient: float
) -> float:
    """
    Calculate permanent market impact in price units.
    """

    return price * coefficient * abs(cumulative_quantity)


def execution_price(
    unaffected_price: float,
    quantity: float,
    temporary_impact: float,
    permanent_impact: float,
    side: str = "sell"
) -> float:
    """
    Calculate execution price.

    For a sell:
        execution price = market price - impact

    For a buy:
        execution price = market price + impact
    """

    side = side.lower()

    if side not in {"buy", "sell"}:
        raise ValueError("side must be 'buy' or 'sell'")

    total_impact = temporary_impact + permanent_impact

    if side == "sell":
        return unaffected_price - total_impact

    return unaffected_price + total_impact
