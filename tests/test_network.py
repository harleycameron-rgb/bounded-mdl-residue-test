import unittest

from multi_agent.agent import AgentNode
from multi_agent.network import AgentNetwork
from tests.helpers import make_output


class NetworkTests(unittest.TestCase):
    def test_chain_network_delays_context_by_one_round(self):
        agent_a = AgentNode("a", evaluator=lambda prompt: make_output(prompt))
        agent_b = AgentNode("b", evaluator=lambda prompt: make_output(prompt))
        network = AgentNetwork.from_chain([agent_a, agent_b])

        network.run("seed prompt", rounds=2)

        self.assertEqual(len(network.round_history), 2)
        self.assertNotIn("[network_context]", network.round_history[0]["b"].prompt)
        self.assertIn("[network_context]", network.round_history[1]["b"].prompt)
        self.assertEqual(len(network.message_history), 2)

    def test_graph_construction_preserves_edges(self):
        agents = [AgentNode(name, evaluator=lambda prompt: make_output(prompt)) for name in ("a", "b", "c")]
        network = AgentNetwork.from_graph(agents, [("a", "b"), ("a", "c")])
        self.assertEqual(sorted(network.edges["a"]), ["b", "c"])


if __name__ == "__main__":
    unittest.main()
