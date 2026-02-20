[README.md](https://github.com/user-attachments/files/25447159/README.md)
# Gridworld MDP — RL Assignment 1

Implementation of a Gridworld Markov Decision Process with two methods for computing state values.

## Environment

5×5 grid with:
- **Goal** (cell 14): reward +5, terminal
- **Danger/Fire** (cells 2, 18, 21): reward -5, terminal
- **Blocked** (cells 6, 7, 11, 12): impassable
- **Actions**: up, right, down, left
- **Noise**: optional stochastic transitions (default 0.0)

## Algorithms

1. **Linear Solver** (`solve_linear_system`) — solves Ax = b exactly for the deterministic case under a uniform random policy
2. **Value Iteration** (`value_iteration`) — finds the optimal value function via repeated Bellman updates, supports both deterministic and stochastic environments

## Usage

```python
from gridworld import GridWorld, value_iteration

# Deterministic
gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
gw.solve_linear_system(discount_factor=0.95)
print(gw)

# Value Iteration
gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
value_iteration(gw, discount=0.95, tolerance=0.01)
print(gw)

# Stochastic
gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.2)
value_iteration(gw, discount=0.95, tolerance=0.01)
print(gw)
```

## Results

| Scenario | Discount | Noise | Iterations |
|----------|----------|-------|------------|
| Value Iteration | 0.95 | 0.0 | 12 |
| Value Iteration | 0.75 | 0.0 | 12 |
| Value Iteration | 0.95 | 0.2 | 20 |
| Linear Solver | 0.95 | 0.0 | 1 (exact) |
| Linear Solver | 0.75 | 0.0 | 1 (exact) |

**Value Iteration — Deterministic (discount=0.95):**
```
  3.15   2.99  -5.00   4.51   4.75
  3.32   ----   ----   4.75   5.00
  3.49   ----   ----   5.00   GOAL
  3.68   3.87   4.07  -5.00   5.00
  3.49  -5.00   4.29   4.51   4.75
```

**Value Iteration — Stochastic noise=0.2 (discount=0.95):**
```
  1.19   0.78  -5.00   3.86   4.59
  1.29   ----   ----   4.58   4.92
  1.37   ----   ----   4.43   GOAL
  1.46   1.58   2.09  -5.00   4.40
  1.03  -5.00   2.68   3.35   4.11
```

**Linear Solver — Deterministic (discount=0.95):**
```
 -2.56  -3.42  -5.00  -1.56   0.00
 -2.23   ----   ----   0.00   1.56
 -2.38   ----   ----   0.00   GOAL
 -3.03  -3.71  -3.90  -5.00  -0.54
 -3.63  -5.00  -3.79  -3.28  -1.72
```

> Note: the linear solver evaluates the uniform random policy while value iteration finds the optimal policy, so their values differ by design.

## Requirements

```
numpy
```

Install with `pip install numpy`.
