from dataclasses import dataclass


@dataclass
class MarketParameters:
    initial_price: float = 100.0
    volatility: float = 0.02
    temporary_impact: float = 0.01
    permanent_impact: float = 0.0001
    impact_exponent: float = 1.0
    volume_per_period: float = 500000.0


@dataclass
class ExecutionParameters:
    total_quantity: float = 100000.0
    horizon: float = 1.0
    steps: int = 20
    risk_aversion: float = 1.0


@dataclass
class SimulationParameters:
    paths: int = 5000
    seed: int = 42
