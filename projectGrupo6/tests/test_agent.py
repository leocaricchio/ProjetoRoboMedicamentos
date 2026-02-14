from agents.delivery_agent import DeliveryAgent


def test_agent_returns_action():
    agent = DeliveryAgent()

    state = ((0, 0), frozenset({(1, 0)}))

    action = agent.program(state)

    assert action is not None
