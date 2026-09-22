from __future__ import annotations

from typing import Dict

from multi_agent.alignment_analyzer import detect_divergence, snapshots_to_states
from multi_agent.drift_propagation import analyze_network as analyze_drift_network
from multi_agent.metrics import summarize
from multi_agent.network import AgentNetwork
from multi_agent.residue_transfer import analyze_network as analyze_residue_network


def generate_report(network: AgentNetwork, round_index: int = -1) -> Dict[str, object]:
    if not network.round_history:
        return {
            "agent_count": 0,
            "rounds": 0,
            "metrics": summarize({}),
            "alignment": detect_divergence({}),
            "drift": [],
            "residue": [],
        }

    snapshots = network.round_history[round_index]
    states = snapshots_to_states(snapshots)
    return {
        "agent_count": len(network.agents),
        "rounds": len(network.round_history),
        "metrics": summarize(states),
        "alignment": detect_divergence(states),
        "drift": analyze_drift_network(network),
        "residue": analyze_residue_network(network),
    }
