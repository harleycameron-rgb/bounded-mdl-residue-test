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
        AgentNode("source", evaluator=lambda prompt: make_output(prompt, drift_magnitude=0)),
        AgentNode("relay", evaluator=lambda prompt: make_output(prompt, drift_magnitude=1)),
        AgentNode("sink", evaluator=lambda prompt: make_output(prompt, drift_magnitude=3)),
    ]
    network = AgentNetwork.from_chain(agents)
    network.run("Track how drift compounds across the chain.", rounds=2)
    print(generate_report(network)["drift"])


if __name__ == "__main__":
    main()
