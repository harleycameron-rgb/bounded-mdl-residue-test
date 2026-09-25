import unittest

from multi_agent.agent import AgentNode, state_vector_from_output
from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark
from tests.helpers import make_output


class AgentTests(unittest.TestCase):
    def test_reference_benchmark_exposes_required_state_components(self):
        output = run_benchmark("multi-agent baseline")
        state = state_vector_from_output(output)
        self.assertEqual(state["drift_magnitude"], 0)
        self.assertIn("core_signature", state)
        self.assertIn("residue_signature", state)
        self.assertIn("alignment_verdict", state)
        self.assertIn("harmonized_response", state)
        self.assertIn("stability_envelope", state)
        self.assertIn("mdl_score", state)

    def test_agent_tracks_history(self):
        agent = AgentNode("alpha", evaluator=lambda prompt: make_output(prompt))
        snapshot = agent.process("hello world", round_index=0)
        self.assertEqual(snapshot.agent_name, "alpha")
        self.assertEqual(snapshot.response, "hello world")
        self.assertEqual(len(agent.history), 1)

    def test_agent_prefers_bounded_response_echo(self):
        agent = AgentNode(
            "alpha",
            evaluator=lambda prompt: {
                **make_output(prompt),
                "bounded_response": {
                    "echo": "bounded",
                    "core_sig": "core",
                    "residue_prefix": "residue",
                },
                "harmonized": {
                    **make_output(prompt)["harmonized"],
                    "bounded_echo": "harmonized",
                },
            },
        )

        snapshot = agent.process("hello world", round_index=0)

        self.assertEqual(snapshot.response, "bounded")


if __name__ == "__main__":
    unittest.main()
