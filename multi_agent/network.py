from __future__ import annotations

from collections import OrderedDict, defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

from .agent import AgentNode, AgentSnapshot
from .communication import MessageEnvelope, build_prompt, emit_messages


class AgentNetwork:
    """
    Non-recursive agent network. Each round only consumes messages emitted
    in the previous round, preventing feedback loops within a round.
    """

    def __init__(self) -> None:
        self.agents: "OrderedDict[str, AgentNode]" = OrderedDict()
        self.edges: Dict[str, List[str]] = defaultdict(list)
        self.round_history: List[Dict[str, AgentSnapshot]] = []
        self.message_history: List[MessageEnvelope] = []
        self.messages_by_delivery_round: Dict[int, List[MessageEnvelope]] = defaultdict(list)

    def add_agent(self, agent: AgentNode) -> None:
        self.agents[agent.name] = agent
        self.edges.setdefault(agent.name, [])

    def connect(self, source: str, target: str) -> None:
        if source not in self.agents or target not in self.agents:
            raise KeyError("Both source and target must be registered agents")
        if target not in self.edges[source]:
            self.edges[source].append(target)

    def predecessors(self, target: str) -> List[str]:
        return [source for source, targets in self.edges.items() if target in targets]

    def messages_delivered_in_round(self, round_index: int) -> List[MessageEnvelope]:
        return list(self.messages_by_delivery_round.get(round_index, []))

    def run_round(self, prompt: str) -> Dict[str, AgentSnapshot]:
        round_index = len(self.round_history)
        previous_messages = self.messages_delivered_in_round(round_index)
        snapshots: Dict[str, AgentSnapshot] = {}

        for agent_name, agent in self.agents.items():
            inbound = [message for message in previous_messages if message.target == agent_name]
            composed_prompt = build_prompt(prompt, inbound)
            snapshots[agent_name] = agent.process(composed_prompt, round_index)

        for source, targets in self.edges.items():
            outbound = emit_messages(snapshots[source], targets, delivery_round=round_index + 1)
            self.message_history.extend(outbound)
            self.messages_by_delivery_round[round_index + 1].extend(outbound)

        self.round_history.append(snapshots)
        return snapshots

    def run(self, prompt: str, rounds: int = 1) -> List[Dict[str, AgentSnapshot]]:
        return [self.run_round(prompt) for _ in range(rounds)]

    @classmethod
    def from_graph(
        cls,
        agents: Iterable[AgentNode],
        edges: Sequence[Tuple[str, str]],
    ) -> "AgentNetwork":
        network = cls()
        for agent in agents:
            network.add_agent(agent)
        for source, target in edges:
            network.connect(source, target)
        return network

    @classmethod
    def from_chain(cls, agents: Sequence[AgentNode]) -> "AgentNetwork":
        edges = [(agents[index].name, agents[index + 1].name) for index in range(len(agents) - 1)]
        return cls.from_graph(agents, edges)

    @classmethod
    def from_tree(
        cls,
        root: AgentNode,
        children: Dict[str, Sequence[AgentNode]],
    ) -> "AgentNetwork":
        all_agents = {root.name: root}
        edges = []
        for parent, child_agents in children.items():
            for child in child_agents:
                all_agents[child.name] = child
                edges.append((parent, child.name))
        return cls.from_graph(all_agents.values(), edges)
