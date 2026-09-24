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
        self.message_history: List[List[MessageEnvelope]] = []
        self.emitted_messages: List[MessageEnvelope] = []
        self.messages_by_delivery_round: Dict[int, List[MessageEnvelope]] = defaultdict(list)

    def add_agent(self, agent: AgentNode) -> None:
        self.agents[agent.name] = agent
        self.edges.setdefault(agent.name, [])

    def reset(self) -> None:
        self.round_history.clear()
        self.message_history.clear()
        self.emitted_messages.clear()
        self.messages_by_delivery_round.clear()
        for agent in self.agents.values():
            agent.history.clear()

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

        round_messages: List[MessageEnvelope] = []
        for source, targets in self.edges.items():
            outbound = emit_messages(snapshots[source], targets, delivery_round=round_index + 1)
            round_messages.extend(outbound)
            self.emitted_messages.extend(outbound)
            self.messages_by_delivery_round[round_index + 1].extend(outbound)

        self.message_history.append(round_messages)
        self.round_history.append(snapshots)
        return snapshots

    def run(self, prompt: str, rounds: int = 1) -> List[Dict[str, AgentSnapshot]]:
        """
        Start a fresh bounded simulation for the requested number of rounds.
        Use run_round() directly to continue an existing execution without reset.
        """
        if rounds < 0:
            raise ValueError("rounds must be non-negative")
        self.reset()
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
        for child_agents in children.values():
            for child in child_agents:
                all_agents[child.name] = child

        edges = []
        for parent, child_agents in children.items():
            if parent not in all_agents:
                raise KeyError(f"Parent {parent!r} must be provided as the root or as a child agent")
            for child in child_agents:
                edges.append((parent, child.name))
        return cls.from_graph(all_agents.values(), edges)
