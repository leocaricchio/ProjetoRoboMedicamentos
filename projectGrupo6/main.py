import time
from aima3.search import astar_search, breadth_first_search, uniform_cost_search
from problems.delivery_problem import DeliveryProblem

#Teste para algoritmo sem ambiente definido

# Estado inicial
initial_position = (0, 0)
deliveries = frozenset({(2, 2), (3, 1)})
initial_state = (initial_position, deliveries)

# Criar problema
problem = DeliveryProblem(initial_state, grid_size=5)


# BFS
print("\nBFS:")
start = time.time()
solution = breadth_first_search(problem)
end = time.time()

if solution:
    print("Custo:", solution.path_cost)
    print("Passos:", len(solution.solution()))
    print("Tempo:", round(end - start, 6), "segundos")
else:
    print("Sem solução")


# UCS
print("\nUCS:")
start = time.time()
solution = uniform_cost_search(problem)
end = time.time()

if solution:
    print("Custo:", solution.path_cost)
    print("Passos:", len(solution.solution()))
    print("Tempo:", round(end - start, 6), "segundos")
else:
    print("Sem solução")


# A*
print("\nA*:")
start = time.time()
solution = astar_search(problem)
end = time.time()

if solution:
    print("Custo:", solution.path_cost)
    print("Passos:", len(solution.solution()))
    print("Tempo:", round(end - start, 6), "segundos")
else:
    print("Sem solução")
