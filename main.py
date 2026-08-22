from pathlib import Path

import numpy as np
import pandas as pd

from src.models import (
    MarketParameters,
    ExecutionParameters,
    SimulationParameters,
)

from src.strategies import (
    twap_schedule,
    front_loaded_schedule,
    optimal_execution_schedule,
)

from src.simulator import monte_carlo_execution

from src.metrics import execution_metrics

from src.visualization import (
    plot_execution_trajectories,
    plot_cost_distributions,
    plot_cost_risk_frontier,
)


OUTPUT_DIR = Path("outputs")


def run_strategy(
    name,
    schedule,
    market,
    execution,
    simulation,
):

    simulation_result = monte_carlo_execution(
        schedule=schedule,
        market_parameters=market,
        execution_parameters=execution,
        simulation_parameters=simulation,
        side="sell",
    )

    metrics = execution_metrics(
        costs=simulation_result["costs"],
        total_quantity=execution.total_quantity,
        initial_price=market.initial_price,
    )

    return {
        "name": name,
        "schedule": schedule,
        **simulation_result,
        **metrics,
    }


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    market = MarketParameters(
        initial_price=100.0,
        volatility=0.02,
        temporary_impact=0.01,
        permanent_impact=0.0001,
        impact_exponent=1.0,
        volume_per_period=500000.0,
    )

    execution = ExecutionParameters(
        total_quantity=100000.0,
        horizon=1.0,
        steps=20,
        risk_aversion=1.0,
    )

    simulation = SimulationParameters(
        paths=5000,
        seed=42,
    )

    schedules = {

        "TWAP": twap_schedule(
            execution.total_quantity,
            execution.steps,
        ),

        "Front-Loaded": front_loaded_schedule(
            execution.total_quantity,
            execution.steps,
            strength=2.0,
        ),

        "Optimal": optimal_execution_schedule(
            total_quantity=execution.total_quantity,
            volatility=market.volatility,
            temporary_impact=market.temporary_impact,
            risk_aversion=execution.risk_aversion,
            horizon=execution.horizon,
            steps=execution.steps,
        ),
    }

    results = {}

    print("=" * 60)
    print("OPTIMAL EXECUTION & MARKET IMPACT SIMULATOR")
    print("=" * 60)

    print(
        f"\nInitial Price      : {market.initial_price:.2f}"
    )

    print(
        f"Order Quantity     : "
        f"{execution.total_quantity:,.0f}"
    )

    print(
        f"Execution Horizon  : "
        f"{execution.horizon:.2f}"
    )

    print(
        f"Time Steps         : "
        f"{execution.steps}"
    )

    print(
        f"Monte Carlo Paths   : "
        f"{simulation.paths}"
    )

    print("\nStrategy Results")
    print("-" * 60)

    rows = []

    for name, schedule in schedules.items():

        result = run_strategy(
            name,
            schedule,
            market,
            execution,
            simulation,
        )

        results[name] = result

        rows.append({
            "strategy": name,
            "mean_cost": result["mean_cost"],
            "std_cost": result["std_cost"],
            "median_cost": result["median_cost"],
            "cost_per_share": result["cost_per_share"],
            "cost_bps": result["cost_bps"],
        })

        print(f"\n{name}")

        print(
            f"Mean Cost                : "
            f"{result['mean_cost']:.4f}"
        )

        print(
            f"Cost Std                 : "
            f"{result['std_cost']:.4f}"
        )

        print(
            f"Cost / Share             : "
            f"{result['cost_per_share']:.6f}"
        )

        print(
            f"Implementation Shortfall : "
            f"{result['mean_cost']:.4f}"
        )

        print(
            f"Cost (bps)               : "
            f"{result['cost_bps']:.4f}"
        )

    summary = pd.DataFrame(rows)

    summary.to_csv(
        OUTPUT_DIR / "execution_summary.csv",
        index=False,
    )

    plot_execution_trajectories(
        schedules=schedules,
        output_path=OUTPUT_DIR
        / "execution_trajectories.png",
    )

    plot_cost_distributions(
        results=results,
        output_path=OUTPUT_DIR
        / "cost_distribution.png",
    )

    risk_aversions = np.array([
        0.0,
        0.1,
        0.25,
        0.5,
        1.0,
        2.0,
        5.0,
    ])

    frontier_rows = []

    for risk in risk_aversions:

        schedule = optimal_execution_schedule(
            total_quantity=execution.total_quantity,
            volatility=market.volatility,
            temporary_impact=market.temporary_impact,
            risk_aversion=risk,
            horizon=execution.horizon,
            steps=execution.steps,
        )

        simulation_result = monte_carlo_execution(
            schedule=schedule,
            market_parameters=market,
            execution_parameters=execution,
            simulation_parameters=simulation,
        )

        frontier_rows.append({
            "risk_aversion": risk,
            "mean_cost": simulation_result["mean_cost"],
            "risk": simulation_result["std_cost"],
        })

    frontier = pd.DataFrame(frontier_rows)

    frontier.to_csv(
        OUTPUT_DIR / "cost_risk_frontier.csv",
        index=False,
    )

    plot_cost_risk_frontier(
        frontier=frontier,
        output_path=OUTPUT_DIR
        / "cost_risk_frontier.png",
    )

    print("\n" + "=" * 60)
    print("Experiment completed successfully.")
    print("=" * 60)

    print("\nGenerated files:")

    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(f"  - {file}")


if __name__ == "__main__":
    main()
