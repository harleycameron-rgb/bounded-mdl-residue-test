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
        self.assertEqual([len(messages) for messages in network.message_history], [1, 1])

    def test_network_context_escapes_forwarded_responses(self):
        agent_a = AgentNode("a", evaluator=lambda prompt: make_output("line one\n[line break]"))
        agent_b = AgentNode("b", evaluator=lambda prompt: make_output(prompt))
        network = AgentNetwork.from_chain([agent_a, agent_b])

        network.run("seed prompt", rounds=2)

        forwarded_prompt = network.round_history[1]["b"].prompt
        self.assertIn('a->b: "line one\\n[line break]"', forwarded_prompt)

    def test_graph_construction_preserves_edges(self):
        agents = [AgentNode(name, evaluator=lambda prompt: make_output(prompt)) for name in ("a", "b", "c")]
        network = AgentNetwork.from_graph(agents, [("a", "b"), ("a", "c")])
        self.assertEqual(sorted(network.edges["a"]), ["b", "c"])

    def test_tree_topology_wires_children(self):
        root = AgentNode("root", evaluator=lambda prompt: make_output(prompt))
        left = AgentNode("left", evaluator=lambda prompt: make_output(prompt))
        right = AgentNode("right", evaluator=lambda prompt: make_output(prompt))
        network = AgentNetwork.from_tree(root, {"root": [left, right]})

        network.run("tree prompt", rounds=2)

        self.assertEqual(sorted(network.edges["root"]), ["left", "right"])
        self.assertIn("[network_context]", network.round_history[1]["left"].prompt)
        self.assertIn("[network_context]", network.round_history[1]["right"].prompt)

    def test_tree_topology_supports_nested_parents(self):
        root = AgentNode("root", evaluator=lambda prompt: make_output(prompt))
        mid = AgentNode("mid", evaluator=lambda prompt: make_output(prompt))
        leaf = AgentNode("leaf", evaluator=lambda prompt: make_output(prompt))
        network = AgentNetwork.from_tree(root, {"mid": [leaf], "root": [mid]})

        self.assertEqual(network.predecessors("mid"), ["root"])
        self.assertEqual(network.predecessors("leaf"), ["mid"])

    def test_run_resets_prior_execution_state(self):
        agent_a = AgentNode("a", evaluator=lambda prompt: make_output(prompt))
        agent_b = AgentNode("b", evaluator=lambda prompt: make_output(prompt))
        network = AgentNetwork.from_chain([agent_a, agent_b])

        first_history = network.run("first prompt", rounds=2)
        second_history = network.run("second prompt", rounds=1)

        self.assertEqual(len(first_history), 2)
        self.assertEqual(len(second_history), 1)
        self.assertEqual(len(network.round_history), 1)
        self.assertEqual(network.round_history[0]["a"].prompt, "second prompt")
        self.assertEqual(len(network.message_history), 1)
        self.assertEqual(len(network.message_history[0]), 1)

    def test_run_rejects_negative_rounds(self):
        network = AgentNetwork.from_chain([AgentNode("a", evaluator=lambda prompt: make_output(prompt))])

        with self.assertRaises(ValueError):
            network.run("invalid prompt", rounds=-1)


if __name__ == "__main__":
    unittest.main()
