"""Tests for the water jug breadth-first search.
"""
import json
from pathlib import Path

from jug_search import WaterJugProblem, breadth_first_search

DATA = Path(__file__).parent / "data"        # the tests/data folder


def test_assignment_problem():
    # 12/8/3 jugs, measure 1 gallon -> shortest solution is 3 steps
    problem = WaterJugProblem(capacities=(12, 8, 3), goal_amount=1)
    result = breadth_first_search(problem)
    assert result.path_cost == 3
    assert 1 in result.state


def test_transition_model():
    # Fill, empty, and pour (pouring stops when the other jug is full)
    problem = WaterJugProblem(capacities=(12, 8, 3))
    assert problem.result((0, 0, 0), ("fill", 0)) == (12, 0, 0)
    assert problem.result((12, 0, 0), ("empty", 0)) == (0, 0, 0)
    assert problem.result((12, 0, 0), ("pour", 0, 1)) == (4, 8, 0)


def test_goal_test():
    # Goal: any jug holds exactly 1 gallon
    problem = WaterJugProblem(capacities=(12, 8, 3), goal_amount=1)
    assert problem.is_goal((1, 8, 3))
    assert not problem.is_goal((4, 8, 0))

def test_actions():
    # Only fills are possible when all jugs are empty
    problem = WaterJugProblem(capacities=(12, 8, 3))
    assert problem.actions((0, 0, 0)) == [("fill", 0), ("fill", 1), ("fill", 2)]

def test_cases_from_test_data():
    # Every problem in tests/data/cases.json gives the expected number of steps
    cases = json.loads((DATA / "cases.json").read_text())
    for case in cases:
        problem = WaterJugProblem(tuple(case["capacities"]), case["goal"])
        result = breadth_first_search(problem)
        if case["expected_steps"] is None:
            assert result is None, case["name"]             # no solution
        else:
            assert result.path_cost == case["expected_steps"], case["name"]