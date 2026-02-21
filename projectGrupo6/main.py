import time
import collections
import collections.abc
collections.Callable = collections.abc.Callable

from env.hospital_env import HospitalEnvironment
from agents.delivery_agent import DeliveryAgent

def run_environment_demo():
    """
    Demo oficial: cria ambiente, adiciona agente, executa passo a passo com render().
    Usa DeliveryProblem via DeliveryAgentProgram (A*).
    """

    grid_size = 5

    walls = set()

    # Entregas (mesmas do benchmark antigo)
    deliveries = {(2, 2), (3, 1)}
    start = (0, 0)

    env = HospitalEnvironment(
        grid_size=grid_size,
        walls=walls,
        deliveries=deliveries,
        start=start,
    )

    agent = DeliveryAgent(grid_size=grid_size)
    env.add_thing(agent)

    max_steps = 200

    print("\n=== SIMULACAO NO AMBIENTE (passo a passo) ===")
    for step in range(max_steps):
        print(f"\n--- step {step} ---")
        env.render()

        percept_state = env.percept_state()  # ((x,y), frozenset(deliveries))
        action = agent.program(percept_state)

        if action is None:
            print("Agente retornou None (sem plano/sem solução). Encerrando.")
            break

        env.execute_action(agent, action)

        if len(env.deliveries) == 0:
            print("\nTodas as entregas concluídas!")
            env.render()
            break

        time.sleep(0.2)


def main():
    run_environment_demo()


if __name__ == "__main__":
    main()
