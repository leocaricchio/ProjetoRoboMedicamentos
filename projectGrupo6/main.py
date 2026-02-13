from aima3.search import astar_search
from problems.delivery_problem import DeliveryProblem

#Teste inicial(sem o ambiente construido)

def main():
    # Estado inicial
    initial_position = (0, 0)
    deliveries = frozenset({(2, 2), (3, 1)})

    initial_state = (initial_position, deliveries)

    problem = DeliveryProblem(initial_state, grid_size=5)

    #execução do algoritmo A*
    solution = astar_search(problem)

    if solution:
        print("Plano encontrado:")
        print(solution.solution())
        print("Custo:", solution.path_cost)
    else:
        print("Nenhuma solução encontrada")

if __name__ == "__main__":
    main()
