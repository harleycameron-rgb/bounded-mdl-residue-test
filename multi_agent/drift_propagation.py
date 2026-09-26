from __future__ import annotations

import json
from typing import Dict, List

from .agent import AgentSnapshot, StateVector
from .network import AgentNetwork


def _stable(value: object) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def normalize_drift_gap(gap: float) -> float:
    return gap / (1.0 + gap)


def state_vector_distance(left: StateVector, right: StateVector) -> Dict[str, object]:
    drift_gap = abs(float(left["drift_magnitude"]) - float(right["drift_magnitude"]))
    components = {
        "core_signature": 0.0 if left["core_signature"] == right["core_signature"] else 1.0,
        "residue_signature": 0.0 if _stable(left["residue_signature"]) == _stable(right["residue_signature"]) else 1.0,
        "alignment_verdict": 0.0 if _stable(left["alignment_verdict"]) == _stable(right["alignment_verdict"]) else 1.0,
        "harmonized_response": 0.0 if _stable(left["harmonized_response"]) == _stable(right["harmonized_response"]) else 1.0,
        "stability_envelope": 0.0 if _stable(left["stability_envelope"]) == _stable(right["stability_envelope"]) else 1.0,
        "mdl_score": 0.0 if _stable(left["mdl_score"]) == _stable(right["mdl_score"]) else 1.0,
        "drift_magnitude": normalize_drift_gap(drift_gap),
    }
    normalized = sum(components.values()) / len(components)
    return {"component_distances": components, "distance": normalized}


def amplification_delta(left: StateVector, right: StateVector) -> float:
    return float(right["drift_magnitude"]) - float(left["drift_magnitude"])


def classify_amplification(delta: float) -> str:
    if delta > 0:
        return "amplified"
    if delta < 0:
        return "dampened"
    return "stable"


def measure_pair(source: AgentSnapshot, target: AgentSnapshot) -> Dict[str, object]:
    distance = state_vector_distance(source.state_vector, target.state_vector)
    delta = amplification_delta(source.state_vector, target.state_vector)
    return {
        "source": source.agent_name,
        "target": target.agent_name,
        "source_round": source.round_index,
        "target_round": target.round_index,
        "delivery_round": target.round_index,
        "distance": distance["distance"],
        "component_distances": distance["component_distances"],
        "drift_delta": delta,
        "propagation_effect": classify_amplification(delta),
    }


def analyze_network(network: AgentNetwork) -> List[Dict[str, object]]:
    analysis = []
    for round_index in range(1, len(network.round_history)):
        current_round = network.round_history[round_index]
        previous_round = network.round_history[round_index - 1]
        for target, snapshot in current_round.items():
            for source in network.predecessors(target):
                if source in previous_round:
                    analysis.append(measure_pair(previous_round[source], snapshot))
    return analysis
