from __future__ import annotations

from typing import List

from multi_agent.network import AgentNetwork


def render_network_text(network: AgentNetwork) -> str:
    lines: List[str] = ["Multi-Agent Drift Network"]
    for source, targets in network.edges.items():
        if not targets:
            lines.append(f"- {source}")
            continue
        for target in targets:
            lines.append(f"- {source} -> {target}")
    lines.append(f"Rounds executed: {len(network.round_history)}")
    lines.append(f"Messages emitted: {sum(len(messages) for messages in network.message_history)}")
    return "\n".join(lines)
