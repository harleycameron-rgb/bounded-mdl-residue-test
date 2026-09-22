import unittest

from multi_agent.agent import AgentNode
from multi_agent.drift_propagation import analyze_network, measure_pair, state_vector_distance
from multi_agent.network import AgentNetwork
from multi_agent.residue_transfer import track_pair
from tests.helpers import make_output


class DriftPropagationTests(unittest.TestCase):
    def test_state_distance_detects_component_changes(self):
        left = make_output("left", drift_magnitude=0)
        right = make_output("right", drift_magnitude=2, aligned=False)
        distance = state_vector_distance(
            {
                "core_signature": left["compressed_core"]["signature"],
                "residue_signature": left["residue_signature"],
                "drift_magnitude": left["drift"]["drift_magnitude"],
                "alignment_verdict": left["alignment"],
                "harmonized_response": left["harmonized"],
                "stability_envelope": left["stability_envelope"],
                "mdl_score": left["mdl_score"],
            },
            {
                "core_signature": right["compressed_core"]["signature"],
                "residue_signature": right["residue_signature"],
                "drift_magnitude": right["drift"]["drift_magnitude"],
                "alignment_verdict": right["alignment"],
                "harmonized_response": right["harmonized"],
                "stability_envelope": right["stability_envelope"],
                "mdl_score": right["mdl_score"],
            },
        )
        self.assertGreater(distance["distance"], 0)
        self.assertEqual(distance["component_distances"]["drift_magnitude"], 2.0)

    def test_pair_analysis_classifies_amplification(self):
        agent_a = AgentNode("a", evaluator=lambda prompt: make_output(prompt, drift_magnitude=0))
        agent_b = AgentNode("b", evaluator=lambda prompt: make_output(prompt, drift_magnitude=2))
        source = agent_a.process("prompt-a", round_index=0)
        target = agent_b.process("prompt-b", round_index=1)
        pair = measure_pair(source, target)
        transfer = track_pair(source, target)
        self.assertEqual(pair["propagation_effect"], "amplified")
        self.assertEqual(transfer["transfer_effect"], "amplified")

    def test_network_analysis_uses_previous_round_edges(self):
        agent_a = AgentNode("a", evaluator=lambda prompt: make_output(prompt, drift_magnitude=1))
        agent_b = AgentNode("b", evaluator=lambda prompt: make_output(prompt, drift_magnitude=3))
        network = AgentNetwork.from_chain([agent_a, agent_b])
        network.run("seed", rounds=2)
        analysis = analyze_network(network)
        self.assertEqual(len(analysis), 1)
        self.assertEqual(analysis[0]["source"], "a")
        self.assertEqual(analysis[0]["target"], "b")


if __name__ == "__main__":
    unittest.main()
