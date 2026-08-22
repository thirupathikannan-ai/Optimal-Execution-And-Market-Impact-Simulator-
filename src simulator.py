import numpy as np

from .execution import execute_order


def simulate_price_path(
    initial_price: float,
    volatility: float,
    horizon: float,
    steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Generate a geometric Brownian motion price path.
    """

    dt = horizon / steps

    shocks = rng.normal(
        loc=0.0,
        scale=1.0,
        size=steps,
    )

    log_returns = (
        -0.5 * volatility ** 2 * dt
        + volatility * np.sqrt(dt) * shocks
    )

    prices = np.empty(steps)

    prices[0] = initial_price

    for i in range(1, steps):
        prices[i] = prices[i - 1] * np.exp(
            log_returns[i]
        )

    return prices


def monte_carlo_execution(
    schedule: np.ndarray,
    market_parameters,
    execution_parameters,
    simulation_parameters,
    side: str = "sell",
) -> dict:
    """
    Run Monte Carlo execution simulation.
    """

    rng = np.random.default_rng(
        simulation_parameters.seed
    )

    costs = []

    for _ in range(simulation_parameters.paths):

        prices = simulate_price_path(
            initial_price=market_parameters.initial_price,
            volatility=market_parameters.volatility,
            horizon=execution_parameters.horizon,
            steps=execution_parameters.steps,
            rng=rng,
        )

        result = execute_order(
            prices=prices,
            schedule=schedule,
            market_parameters=market_parameters,
            side=side,
        )

        costs.append(
            result["implementation_shortfall"]
        )

    costs = np.asarray(costs)

    return {
        "costs": costs,
        "mean_cost": float(np.mean(costs)),
        "std_cost": float(np.std(costs, ddof=1)),
        "median_cost": float(np.median(costs)),
    }
