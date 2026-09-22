from __future__ import annotations

from typing import Dict, List

from .agent import AgentSnapshot
from .drift_propagation import classify_amplification
from .network import AgentNetwork


def track_pair(source: AgentSnapshot, target: AgentSnapshot) -> Dict[str, object]:
    source_residue = source.state_vector["residue_signature"]["hash_prefix"]
    target_residue = target.state_vector["residue_signature"]["hash_prefix"]
    drift_delta = float(target.state_vector["drift_magnitude"]) - float(source.state_vector["drift_magnitude"])
    return {
        "source": source.agent_name,
        "target": target.agent_name,
        "source_residue": source_residue,
        "target_residue": target_residue,
        "residue_changed": source_residue != target_residue,
        "drift_delta": drift_delta,
        "transfer_effect": classify_amplification(drift_delta),
    }


def analyze_network(network: AgentNetwork) -> List[Dict[str, object]]:
    transfers = []
    for round_index in range(1, len(network.round_history)):
        current_round = network.round_history[round_index]
        previous_round = network.round_history[round_index - 1]
        for target, snapshot in current_round.items():
            for source in network.predecessors(target):
                if source in previous_round:
                    transfers.append(track_pair(previous_round[source], snapshot))
    return transfers
