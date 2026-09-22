from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.demo_support import make_output
from analysis.reporter import generate_report
from multi_agent.agent import AgentNode
from multi_agent.network import AgentNetwork


def main():
    agents = [
        AgentNode("aligned", evaluator=lambda prompt: make_output(prompt, aligned=True)),
        AgentNode("misaligned", evaluator=lambda prompt: make_output(prompt, aligned=False, drift_magnitude=2)),
    ]
    network = AgentNetwork.from_chain(agents)
    network.run("Observe when coordinated agents start disagreeing.", rounds=2)
    print(generate_report(network)["alignment"])


if __name__ == "__main__":
    main()
