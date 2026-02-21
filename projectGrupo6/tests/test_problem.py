from problems.delivery_problem import DeliveryProblem
from aima3.search import astar_search


def test_goal_test():
    state = ((0, 0), frozenset())
    problem = DeliveryProblem(state, grid_size=5)
    assert problem.goal_test(state) is True


def test_result_updates_state():
    state = ((0, 0), frozenset({(1, 0)}))
    problem = DeliveryProblem(state, grid_size=5)

    new_state = problem.result(state, "DOWN")

    assert new_state[0] == (1, 0)


def test_heuristic_non_negative():
    state = ((0, 0), frozenset({(2, 2)}))
    problem = DeliveryProblem(state, grid_size=5)

    # Criar um node simples
    class Node:
        def __init__(self, state):
            self.state = state

    node = Node(state)

    h_value = problem.h(node)
    assert h_value >= 0


def test_astar_finds_solution():
    state = ((0, 0), frozenset({(1, 0)}))
    problem = DeliveryProblem(state, grid_size=5)

    solution = astar_search(problem)

    assert solution is not None
