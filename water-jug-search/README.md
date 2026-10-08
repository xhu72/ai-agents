# Water Jug Search

Breadth-first search for the three-jug problem: with jugs of 12, 8 and 3 gallons and a faucet, measure out exactly 1 gallon.

## Requirements

Python 3.10+ and pytest. The search itself uses only the Python standard library.

## Running the search

```bash
python jug_search.py
```

Output:

```
Jugs (12, 8, 3), goal: exactly 1 gallon

Start:                 (0, 0, 0)
Step 1: Fill 12         (12, 0, 0)
Step 2: Pour 12 -> 8    (4, 8, 0)
Step 3: Pour 12 -> 3    (1, 8, 3)

Solved in 3 steps.
```


## Running the tests

```bash
python -m pytest -v
```

There are four tests: 
- the assignment's problem (3 steps), 
- the transition model (fill, empty, pour), 
- the goal test, 
- the actions test,
- and the problems in the test data file `tests/data/cases.json`. Each case there gives jug sizes, a goal and the expected number of steps (`null` means no solution exists).

The tests also run automatically on every push through GitHub Actions (`.github/workflows/water-jug-search.yml` at the repository root).

## Design

| Book | Code |
|---|---|
| Problem: `INITIAL`, `ACTIONS`, `RESULT`, `IS-GOAL`, `ACTION-COST` | `WaterJugProblem`: `initial`, `actions()`, `result()`, `is_goal()`, `action_cost()` |
| `NODE` with `STATE`, `PARENT`, `ACTION`, `PATH-COST` | `Node` |
| `EXPAND` (Figure 3.7) | `expand()` |
| `BREADTH-FIRST-SEARCH` (Figure 3.9) | `breadth_first_search()` |


- **State:** a tuple with the gallons in each jug, e.g. `(4, 8, 0)`. Initial state: `(0, 0, 0)`.
- **Goal:** any jug holds exactly 1 gallon.
- **Actions:** `('fill', i)`, `('empty', i)`, `('pour', i, j)`, where `i` and `j` are jug positions: 0 = 12-gallon, 1 = 8-gallon, 2 = 3-gallon. Only actions that change the state are generated.
- **Transition model:** fill sets a jug to its capacity, empty sets it to 0, and pour moves `min(amount in i, room left in j)`.
- **Cost:** every action costs 1, so BFS returns the solution with the fewest steps.
