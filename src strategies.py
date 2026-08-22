import numpy as np


def twap_schedule(total_quantity: float, steps: int) -> np.ndarray:
    """
    Equal-size execution schedule.
    """
    if steps <= 0:
        raise ValueError("steps must be positive")

    return np.full(steps, total_quantity / steps)


def front_loaded_schedule(
    total_quantity: float,
    steps: int,
    strength: float = 2.0
) -> np.ndarray:
    """
    Front-loaded execution schedule.

    Higher strength places more quantity into earlier periods.
    """
    if steps <= 0:
        raise ValueError("steps must be positive")

    weights = np.exp(-strength * np.arange(steps) / steps)
    weights /= weights.sum()

    return total_quantity * weights


def optimal_execution_schedule(
    total_quantity: float,
    volatility: float,
    temporary_impact: float,
    risk_aversion: float,
    horizon: float,
    steps: int
) -> np.ndarray:
    """
    Almgren-Chriss-inspired optimal execution trajectory.

    Returns quantities executed during each interval.
    """

    if total_quantity <= 0:
        raise ValueError("total_quantity must be positive")

    if steps <= 0:
        raise ValueError("steps must be positive")

    if temporary_impact <= 0:
        raise ValueError("temporary_impact must be positive")

    if horizon <= 0:
        raise ValueError("horizon must be positive")

    dt = horizon / steps

    kappa = np.sqrt(
        max(risk_aversion, 0.0)
        * volatility ** 2
        / temporary_impact
    )

    times = np.linspace(0.0, horizon, steps + 1)

    if kappa < 1e-10:
        holdings = total_quantity * (
            1.0 - times / horizon
        )
    else:
        denominator = np.sinh(kappa * horizon)

        holdings = total_quantity * np.sinh(
            kappa * (horizon - times)
        ) / denominator

    quantities = -np.diff(holdings)

    # Numerical normalization
    quantities *= total_quantity / quantities.sum()

    return quantities
