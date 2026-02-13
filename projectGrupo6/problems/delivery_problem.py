#Definido conforme a modelagem formal do problema
from aima3.search import Problem

class DeliveryProblem(Problem):

    # Inicialização do problema
    def __init__(self, initial, grid_size):
        self.grid_size = grid_size
        super().__init__(initial)

    #Ações possíveis
    def actions(self, state):
        (x, y), deliveries = state
        actions = []

        if x > 0:
            actions.append("UP")
        if x < self.grid_size - 1:
            actions.append("DOWN")
        if y > 0:
            actions.append("LEFT")
        if y < self.grid_size - 1:
            actions.append("RIGHT")

        return actions

    # Modelo de transição
    def result(self, state, action):
        (x, y), deliveries = state
        deliveries = set(deliveries)

        if action == "UP":
            x -= 1
        elif action == "DOWN":
            x += 1
        elif action == "LEFT":
            y -= 1
        elif action == "RIGHT":
            y += 1

        # Remove entrega se chegou na posição
        if (x, y) in deliveries:
            deliveries.remove((x, y))

        return ((x, y), frozenset(deliveries))

    # Teste de objetivo
    def goal_test(self, state):
        _, deliveries = state
        return len(deliveries) == 0

    #Custo de caminho
    def path_cost(self, c, state1, action, state2):
        return c + 1

    # Heurística
    def h(self, node):
        (x, y), deliveries = node.state

        if not deliveries:
            return 0

        distances = [
            abs(x - dx) + abs(y - dy)
            for dx, dy in deliveries
        ]

        return min(distances)
