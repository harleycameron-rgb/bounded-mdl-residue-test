import unittest

from analysis.reporter import generate_report
from analysis.visualizer import render_network_text
from multi_agent.agent import AgentNode
from multi_agent.network import AgentNetwork
from tests.helpers import make_output


class ScenarioTests(unittest.TestCase):
    def test_aligned_agents_report_consensus(self):
        agents = [
            AgentNode("alpha", evaluator=lambda prompt: make_output(prompt, aligned=True, drift_magnitude=0)),
            AgentNode("beta", evaluator=lambda prompt: make_output(prompt, aligned=True, drift_magnitude=0)),
        ]
        network = AgentNetwork.from_chain(agents)
        network.run("stable prompt", rounds=1)
        report = generate_report(network)
        self.assertTrue(report["alignment"]["consensus"])
        self.assertEqual(report["metrics"]["coherence"], 1.0)

    def test_diverging_agents_raise_divergence_score(self):
        alpha = AgentNode("alpha", evaluator=lambda prompt: make_output(prompt, aligned=True, drift_magnitude=0))
        beta = AgentNode("beta", evaluator=lambda prompt: make_output(prompt, aligned=False, drift_magnitude=2))
        network = AgentNetwork.from_chain([alpha, beta])
        network.run("divergent prompt", rounds=2)
        report = generate_report(network)
        self.assertGreater(report["alignment"]["divergence_score"], 0.0)
        self.assertEqual(
            report["alignment"]["disagreements"],
            [
                {
                    "left": "alpha",
                    "right": "beta",
                    "left_aligned": True,
                    "right_aligned": False,
                }
            ],
        )
        self.assertIn("alpha -> beta", render_network_text(network))

    def test_report_can_scope_to_explicit_round(self):
        alpha = AgentNode("alpha", evaluator=lambda prompt: make_output(prompt, aligned=True, drift_magnitude=0))
        beta = AgentNode("beta", evaluator=lambda prompt: make_output(prompt, aligned=False, drift_magnitude=2))
        network = AgentNetwork.from_chain([alpha, beta])
        network.run("divergent prompt", rounds=2)

        report = generate_report(network, round_index=1)

        self.assertEqual(len(report["drift"]), 1)
        self.assertEqual(len(report["residue"]), 1)
        self.assertEqual(report["drift"][0]["delivery_round"], 1)
        self.assertEqual(report["residue"][0]["delivery_round"], 1)

    def test_report_rejects_out_of_range_negative_round(self):
        alpha = AgentNode("alpha", evaluator=lambda prompt: make_output(prompt))
        beta = AgentNode("beta", evaluator=lambda prompt: make_output(prompt))
        network = AgentNetwork.from_chain([alpha, beta])
        network.run("bounded prompt", rounds=1)

        with self.assertRaises(IndexError):
            generate_report(network, round_index=-2)

    def test_report_first_round_has_no_cross_round_records(self):
        alpha = AgentNode("alpha", evaluator=lambda prompt: make_output(prompt, drift_magnitude=0))
        beta = AgentNode("beta", evaluator=lambda prompt: make_output(prompt, drift_magnitude=2))
        network = AgentNetwork.from_chain([alpha, beta])
        network.run("scoped prompt", rounds=2)

        report = generate_report(network, round_index=0)

        self.assertEqual(report["drift"], [])
        self.assertEqual(report["residue"], [])


if __name__ == "__main__":
    unittest.main()
