from __future__ import annotations

from typing import Dict

from multi_agent.alignment_analyzer import detect_divergence, snapshots_to_states
from multi_agent.drift_propagation import analyze_network as analyze_drift_network
from multi_agent.metrics import summarize
from multi_agent.network import AgentNetwork
from multi_agent.residue_transfer import analyze_network as analyze_residue_network


def _resolve_round_index(round_index: int, total_rounds: int) -> int:
    resolved = round_index if round_index >= 0 else total_rounds + round_index
    if not 0 <= resolved < total_rounds:
        raise IndexError(f"round_index {round_index} is out of range for {total_rounds} rounds")
    return resolved


def _scope_records(records, resolved_round: int):
    return [record for record in records if record.get("delivery_round") == resolved_round]


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

    resolved_round = _resolve_round_index(round_index, len(network.round_history))
    snapshots = network.round_history[resolved_round]
    states = snapshots_to_states(snapshots)
    drift_records = analyze_drift_network(network)
    residue_records = analyze_residue_network(network)
    return {
        "agent_count": len(network.agents),
        "rounds": len(network.round_history),
        "metrics": summarize(states),
        "alignment": detect_divergence(states),
        "drift": _scope_records(drift_records, resolved_round),
        "residue": _scope_records(residue_records, resolved_round),
    }
