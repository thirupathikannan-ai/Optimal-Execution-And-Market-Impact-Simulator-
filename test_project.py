import numpy as np

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

from src.impact import (
    temporary_market_impact,
    permanent_market_impact,
)

from src.simulator import (
    simulate_price_path,
    monte_carlo_execution,
)


def test_twap_conserves_quantity():

    quantity = 100000
    steps = 20

    schedule = twap_schedule(
        quantity,
        steps,
    )

    assert len(schedule) == steps
    assert np.isclose(
        schedule.sum(),
        quantity,
    )


def test_front_loaded_conserves_quantity():

    quantity = 100000
    steps = 20

    schedule = front_loaded_schedule(
        quantity,
        steps,
    )

    assert np.isclose(
        schedule.sum(),
        quantity,
    )

    assert schedule[0] > schedule[-1]


def test_optimal_schedule_conserves_quantity():

    schedule = optimal_execution_schedule(
        total_quantity=100000,
        volatility=0.02,
        temporary_impact=0.01,
        risk_aversion=1.0,
        horizon=1.0,
        steps=20,
    )

    assert len(schedule) == 20

    assert np.isclose(
        schedule.sum(),
        100000,
    )

    assert np.all(schedule >= 0)


def test_zero_risk_optimal_schedule():

    schedule = optimal_execution_schedule(
        total_quantity=100000,
        volatility=0.02,
        temporary_impact=0.01,
        risk_aversion=0.0,
        horizon=1.0,
        steps=20,
    )

    assert np.allclose(
        schedule,
        np.full(20, 5000),
        atol=1e-6,
    )


def test_temporary_impact_positive():

    impact = temporary_market_impact(
        price=100,
        quantity=10000,
        volume=500000,
        coefficient=0.01,
    )

    assert impact > 0


def test_permanent_impact_positive():

    impact = permanent_market_impact(
        price=100,
        cumulative_quantity=10000,
        coefficient=0.0001,
    )

    assert impact > 0


def test_price_path_length():

    rng = np.random.default_rng(42)

    prices = simulate_price_path(
        initial_price=100,
        volatility=0.02,
        horizon=1.0,
        steps=20,
        rng=rng,
    )

    assert len(prices) == 20
    assert np.all(prices > 0)


def test_monte_carlo_output():

    market = MarketParameters()

    execution = ExecutionParameters(
        total_quantity=100000,
        steps=20,
    )

    simulation = SimulationParameters(
        paths=100,
        seed=42,
    )

    schedule = twap_schedule(
        execution.total_quantity,
        execution.steps,
    )

    result = monte_carlo_execution(
        schedule=schedule,
        market_parameters=market,
        execution_parameters=execution,
        simulation_parameters=simulation,
    )

    assert len(result["costs"]) == 100
    assert np.isfinite(result["mean_cost"])
    assert np.isfinite(result["std_cost"])
