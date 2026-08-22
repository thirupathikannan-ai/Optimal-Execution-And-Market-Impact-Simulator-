import numpy as np

from .impact import (
    temporary_market_impact,
    permanent_market_impact,
    execution_price,
)


def execute_order(
    prices: np.ndarray,
    schedule: np.ndarray,
    market_parameters,
    side: str = "sell"
) -> dict:
    """
    Execute a complete schedule against a price path.
    """

    if len(prices) != len(schedule):
        raise ValueError(
            "prices and schedule must have identical lengths"
        )

    initial_price = prices[0]

    cumulative_quantity = 0.0

    execution_prices = []
    temporary_impacts = []
    permanent_impacts = []

    for price, quantity in zip(prices, schedule):

        cumulative_quantity += quantity

        temp = temporary_market_impact(
            price=price,
            quantity=quantity,
            volume=market_parameters.volume_per_period,
            coefficient=market_parameters.temporary_impact,
            exponent=market_parameters.impact_exponent,
        )

        perm = permanent_market_impact(
            price=price,
            cumulative_quantity=cumulative_quantity,
            coefficient=market_parameters.permanent_impact,
        )

        exec_price = execution_price(
            unaffected_price=price,
            quantity=quantity,
            temporary_impact=temp,
            permanent_impact=perm,
            side=side,
        )

        execution_prices.append(exec_price)
        temporary_impacts.append(temp)
        permanent_impacts.append(perm)

    execution_prices = np.asarray(execution_prices)

    quantity = schedule.sum()

    if side == "sell":
        implementation_shortfall = (
            quantity * initial_price
            - np.sum(schedule * execution_prices)
        )
    else:
        implementation_shortfall = (
            np.sum(schedule * execution_prices)
            - quantity * initial_price
        )

    average_execution_price = (
        np.sum(schedule * execution_prices)
        / quantity
    )

    return {
        "execution_prices": execution_prices,
        "temporary_impacts": np.asarray(temporary_impacts),
        "permanent_impacts": np.asarray(permanent_impacts),
        "implementation_shortfall": implementation_shortfall,
        "average_execution_price": average_execution_price,
        "quantity": quantity,
    }
