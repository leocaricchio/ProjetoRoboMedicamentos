import pytest
from problems.hospital_problem import HospitalDeliveryProblem
from aima3.search import astar_search


def test_goal_test():
    state = ((0, 0), frozenset())
    problem = HospitalDeliveryProblem(state)
    assert problem.goal_test(state) is True


def test_result_updates_state():
    state = ((0, 0), frozenset({(1, 0)}))
    problem = HospitalDeliveryProblem(state)

    new_state = problem.result(state, "DOWN")

    assert new_state[0] == (1, 0)


def test_heuristic_non_negative():
    state = ((0, 0), frozenset({(2, 2)}))
    problem = HospitalDeliveryProblem(state)

    h_value = problem.h(state)
    assert h_value >= 0


def test_astar_finds_solution():
    state = ((0, 0), frozenset({(1, 0)}))
    problem = HospitalDeliveryProblem(state)

    solution = astar_search(problem)

    assert solution is not None
