# Optimal Execution & Market Impact Simulator

A quantitative research framework for studying large-order execution, market impact, transaction costs, execution risk, and optimal trading trajectories.

The project implements an Almgren-Chriss-inspired optimal execution framework and compares it against standard execution benchmarks such as TWAP and front-loaded execution.

---

## Overview

Executing a large order is fundamentally different from deciding whether to trade.

A trader who needs to execute a large position faces a trade-off:

- Trading too quickly increases market impact.
- Trading too slowly increases exposure to price uncertainty.
- Aggressive execution can reduce timing risk but increase transaction costs.
- Passive execution can reduce immediate impact but increase uncertainty.

This project builds a simulation environment for studying this trade-off.

The simulator generates stochastic price paths, applies temporary and permanent market impact, executes different trading schedules, and evaluates their execution quality.

The main research objective is:

\[
\min_{\{q_t\}}
E[C] + \lambda Var(C)
\]

where:

- \(C\) = implementation shortfall / execution cost
- \(E[C]\) = expected execution cost
- \(Var(C)\) = execution risk
- \(\lambda\) = risk-aversion parameter
- \(q_t\) = quantity executed at time \(t\)

---

## Research Goals

The project investigates:

1. How market impact changes with execution speed.
2. How volatility affects execution risk.
3. How risk aversion changes the optimal trading schedule.
4. Whether optimal execution improves the cost-risk trade-off.
5. How TWAP compares with model-based execution.
6. How temporary and permanent impact contribute to total cost.
7. How execution quality changes across Monte Carlo simulations.

---

## Key Features

### Optimal Execution

Implements an Almgren-Chriss-inspired closed-form execution trajectory.

### Market Impact

Models:

- Temporary market impact
- Permanent market impact
- Participation-dependent impact

### Stochastic Price Simulation

Generates Monte Carlo price paths using a geometric Brownian motion process.

### Execution Strategies

Includes:

- TWAP
- Front-loaded execution
- Optimal execution

### Transaction Cost Analysis

Calculates:

- Implementation shortfall
- Average execution price
- Slippage
- Temporary impact cost
- Permanent impact cost
- Execution cost variance
- Execution cost standard deviation
- Cost per share
- Cost in basis points

### Risk-Cost Analysis

Produces a cost-risk frontier showing the effect of different risk-aversion parameters.

### Reproducibility

All experiments use deterministic random seeds by default.

---

# Mathematical Framework

## 1. Price Dynamics

The unaffected market price follows:

\[
dS_t = \sigma S_t dW_t
\]

where:

- \(S_t\) = unaffected price
- \(\sigma\) = volatility
- \(W_t\) = Brownian motion

For simulation:

\[
S_{t+\Delta t}
=
S_t
\exp
\left[
-\frac{1}{2}\sigma^2\Delta t
+
\sigma\sqrt{\Delta t}Z_t
\right]
\]

where:

\[
Z_t \sim N(0,1)
\]

---

# 2. Temporary Market Impact

Temporary impact is modeled as a nonlinear function of trading rate:

\[
I_{temp}(q_t)
=
\eta
\left|
\frac{q_t}{V_t}
\right|^\alpha
S_t
\]

where:

- \(\eta\) = temporary impact coefficient
- \(q_t\) = shares executed
- \(V_t\) = available market volume
- \(\alpha\) = impact exponent

---

# 3. Permanent Market Impact

Permanent impact changes the future reference price:

\[
I_{perm}(q_t)
=
\gamma q_t
\]

where:

- \(\gamma\) = permanent impact coefficient

The permanent impact accumulates over the execution process.

---

# 4. Execution Price

For a sell order:

\[
P_{exec,t}
=
S_t
-
I_{temp,t}
-
I_{perm,t}
\]

For a buy order:

\[
P_{exec,t}
=
S_t
+
I_{temp,t}
+
I_{perm,t}
\]

The implementation is sign-aware so the same framework can simulate both buy and sell execution.

---

# 5. Implementation Shortfall

For a sell order:

\[
IS
=
Q P_0
-
\sum_t q_tP_{exec,t}
\]

For a buy order:

\[
IS
=
\sum_t q_tP_{exec,t}
-
Q P_0
\]

A positive value represents an execution cost.

---

# 6. Optimal Execution

The execution schedule is based on the classic optimal-execution trade-off.

A simplified continuous-time trajectory is:

\[
x(t)
=
X
\frac{
\sinh(\kappa(T-t))
}{
\sinh(\kappa T)
}
\]

where:

- \(X\) = initial inventory
- \(T\) = execution horizon
- \(t\) = current time
- \(\kappa\) = execution aggressiveness parameter

The implementation derives:

\[
\kappa
=
\sqrt{
\frac{\lambda\sigma^2}{\eta}
}
\]

where:

- \(\lambda\) = risk aversion
- \(\sigma\) = volatility
- \(\eta\) = temporary impact parameter

Higher risk aversion produces a more aggressive execution schedule.

---

# Experiments

The default experiment compares:

### Strategy A — TWAP

Equal quantity is executed during every interval.

### Strategy B — Front Loaded

A larger quantity is executed earlier to reduce exposure to future price movements.

### Strategy C — Optimal Execution

The execution trajectory is adjusted according to volatility, impact, execution horizon, and risk aversion.

---

# Example Configuration
```python
total_quantity = 100000
initial_price = 100.0
volatility = 0.02
temporary_impact = 0.01
permanent_impact = 0.0001
risk_aversion = 1.0
horizon = 1.0
steps = 20
simulation_paths = 5000
git clone https://github.com/YOUR_USERNAME/Optimal-Execution-And-Market-Impact-Simulator.git
cd Optimal-Execution-And-Market-Impact-Simulator
Create a virtual environment
python -m venv .venv
Windows
.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run the simulator
python main.py
============================================================
OPTIMAL EXECUTION & MARKET IMPACT SIMULATOR
============================================================

Initial Price      : 100.00
Order Quantity     : 100,000
Execution Horizon  : 1.00
Time Steps         : 20
Monte Carlo Paths  : 5000

Strategy Results
------------------------------------------------------------

TWAP
Mean Cost                : 52496075.82
Cost Std                 : 625606.63
Cost / Share             : 524.960758
Implementation Shortfall : 52496075.82
Cost (bps)               : 52496.0758

Front-Loaded
Mean Cost                : 53289934.99
Cost Std                 : 496477.54
Cost / Share             : 532.899350
Implementation Shortfall : 53289934.99
Cost (bps)               : 53289.9350

Optimal
Mean Cost                : 52502326.07
Cost Std                 : 619602.76
Cost / Share             : 525.023261
Implementation Shortfall : 52502326.07
Cost (bps)               : 52502.3261

============================================================
Experiment completed successfully.
============================================================
Initial price: $100
Order: 100,000 shares
Horizon: 1.0
Time steps: 20
Monte Carlo paths: 5,000
Volatility: 2%
Temporary impact: 0.01
Permanent impact: 0.0001
Seed: 42
Research Interpretation
The simulator is designed to demonstrate an important execution principle:
There is generally no single execution schedule that simultaneously minimizes market impact and timing risk.
Aggressive execution:
reduces exposure to price uncertainty
increases temporary market impact
can reduce execution variance
Slow execution:
reduces instantaneous market impact
increases exposure to price movements
can increase execution variance
The optimal schedule therefore depends on the trader's risk preference and market conditions.
Metrics
The framework reports:
Implementation Shortfall
Difference between the decision/reference price and realized execution value.
Monte Carlo Analysis
The simulator evaluates each execution strategy over thousands of stochastic market paths.
For each path:
Generate an unaffected price process.
Generate the execution schedule.
Calculate temporary market impact.
Calculate permanent market impact.
Compute execution prices.
Calculate implementation shortfall.
Store execution statistics.
The resulting distribution allows the trader to study both expected cost and execution risk.
Cost-Risk Frontier
The project sweeps across multiple values of the risk-aversion parameter:
lambda
  |
  |\
  | \
  |  \
  |   \
  |    \
  |     \
  +---------------- risk
Each point represents a different execution preference.
Low risk aversion:
slower execution
lower expected impact
higher timing risk
High risk aversion:
faster execution
higher expected impact
lower timing risk
Project Architecture
                    +----------------+
                    | Configuration  |
                    +-------+--------+
                            |
                            v
                 +----------------------+
                 | Execution Strategies |
                 +----------+-----------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
            TWAP       Front Loaded     Optimal
              |             |             |
              +-------------+-------------+
                            |
                            v
                 +----------------------+
                 | Market Impact Model  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Monte Carlo Simulator|
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Execution Metrics    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Visualization/Report |
                 +----------------------+

Repository Structure
Optimal-Execution-And-Market-Impact-Simulator/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── main.py
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── execution.py
│   ├── impact.py
│   ├── simulator.py
│   ├── metrics.py
│   ├── strategies.py
│   └── visualization.py
│
├── tests/
│   └── test_project.py
│
├── data/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
Validation
The project contains unit tests for:
execution schedule conservation
TWAP inventory
optimal trajectory
market impact
implementation shortfall
Monte Carlo output dimensions
metric calculations
Run:
pytest
Possible Extensions
Future research could add:
real limit-order-book data
L2/L3 market replay
volume curves
VWAP execution
POV execution
adaptive participation
nonlinear impact calibration
Kyle's lambda
transient impact
stochastic volatility
regime switching
reinforcement-learning execution
queue-position modeling
latency
adverse selection
multi-asset execution
cross-impact
transaction fees
real market data calibration
Research References
Almgren, R. & Chriss, N.
"Optimal Execution of Portfolio Transactions."
The Journal of Risk.
The core research problem is the classical trade-off between market impact and price risk.
Disclaimer
This project is for educational and quantitative research purposes only.
It does not constitute financial advice and should not be used as a production trading system without additional validation.

Author
Thirupathi Kannan K
GitHub:
https://github.com/thirupathikannan-ai?
