from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_execution_trajectories(
    schedules: dict,
    output_path: str,
) -> None:

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    for name, schedule in schedules.items():

        holdings = schedule.sum() - np.cumsum(schedule)

        plt.plot(
            np.arange(len(holdings)),
            holdings,
            label=name,
        )

    plt.xlabel("Execution Period")
    plt.ylabel("Remaining Inventory")
    plt.title("Execution Trajectories")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_cost_distributions(
    results: dict,
    output_path: str,
) -> None:

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    for name, result in results.items():

        plt.hist(
            result["costs"],
            bins=50,
            alpha=0.45,
            label=name,
        )

    plt.xlabel("Implementation Shortfall")
    plt.ylabel("Frequency")
    plt.title("Execution Cost Distribution")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_cost_risk_frontier(
    frontier: pd.DataFrame,
    output_path: str,
) -> None:

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.plot(
        frontier["risk"],
        frontier["mean_cost"],
        marker="o",
    )

    for _, row in frontier.iterrows():

        plt.annotate(
            f"{row['risk_aversion']:.2g}",
            (row["risk"], row["mean_cost"]),
        )

    plt.xlabel("Execution Risk (Std. Cost)")
    plt.ylabel("Expected Cost")
    plt.title("Cost-Risk Frontier")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
