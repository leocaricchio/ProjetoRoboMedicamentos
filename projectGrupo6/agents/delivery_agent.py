# projectGrupo6/agents/delivery_agent.py

from aima3.search import astar_search
from aima3.agents import Agent
from problems.delivery_problem import DeliveryProblem


class DeliveryAgentProgram:
    """
    Programa de agente baseado no modelo SimpleProblemSolvingAgentProgram do AIMA.
    """

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.plan = []  # sequência de ações
        self.initial_state = None

    def __call__(self, percept):
        """
        percept deve ser o estado atual:
        ((x, y), frozenset(entregas))
        """

        state = percept

        # Se não há plano, formular problema e buscar solução
        if not self.plan:
            problem = DeliveryProblem(state, self.grid_size)
            solution = astar_search(problem)

            if solution:
                self.plan = solution.solution()
            else:
                return None

        # Executa uma ação por vez
        if self.plan:
            return self.plan.pop(0)
        else:
            return None


class DeliveryAgent(Agent):
    """
    Agente que encapsula o programa de decisão.
    """

    def __init__(self, grid_size):
        super().__init__(program=DeliveryAgentProgram(grid_size))
