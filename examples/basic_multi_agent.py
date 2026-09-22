from analysis.reporter import generate_report
from analysis.visualizer import render_network_text
from multi_agent.agent import AgentNode
from multi_agent.network import AgentNetwork


def main():
    network = AgentNetwork.from_chain(
        [
            AgentNode("alpha", model_name="baseline"),
            AgentNode("beta", model_name="peer"),
        ]
    )
    network.run("Summarize the same prompt without recursion.", rounds=2)
    print(render_network_text(network))
    print(generate_report(network))


if __name__ == "__main__":
    main()
