import numpy as np


def execution_metrics(
    costs: np.ndarray,
    total_quantity: float,
    initial_price: float,
) -> dict:

    mean_cost = float(np.mean(costs))
    std_cost = float(np.std(costs, ddof=1))

    cost_per_share = mean_cost / total_quantity

    cost_bps = (
        mean_cost
        / (total_quantity * initial_price)
        * 10000
    )

    return {
        "mean_cost": mean_cost,
        "std_cost": std_cost,
        "median_cost": float(np.median(costs)),
        "cost_per_share": cost_per_share,
        "cost_bps": cost_bps,
        "min_cost": float(np.min(costs)),
        "max_cost": float(np.max(costs)),
    }


def cost_risk_point(
    costs: np.ndarray
) -> tuple[float, float]:

    return (
        float(np.mean(costs)),
        float(np.std(costs, ddof=1)),
    )
