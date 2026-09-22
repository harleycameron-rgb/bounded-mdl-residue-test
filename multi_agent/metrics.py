from __future__ import annotations

from itertools import combinations
from typing import Dict

from .agent import StateVector


def compatibility_score(left: StateVector, right: StateVector) -> float:
    left_alignment = 1.0 if left["alignment_verdict"]["aligned"] else 0.0
    right_alignment = 1.0 if right["alignment_verdict"]["aligned"] else 0.0
    left_stability = float(left["stability_envelope"].get("stability_score", 0.0))
    right_stability = float(right["stability_envelope"].get("stability_score", 0.0))
    left_mdl = float(left["mdl_score"].get("mdl_score", 0.0))
    right_mdl = float(right["mdl_score"].get("mdl_score", 0.0))
    drift_gap = abs(float(left["drift_magnitude"]) - float(right["drift_magnitude"]))

    raw_score = (
        left_alignment
        + right_alignment
        + ((left_stability + right_stability) / 2.0)
        + (1.0 - min(1.0, abs(left_mdl - right_mdl)))
        + (1.0 - min(1.0, drift_gap))
    ) / 5.0
    return round(raw_score, 4)


def coherence_score(states: Dict[str, StateVector]) -> float:
    if not states:
        return 0.0
    harmonized_hashes = [
        state["harmonized_response"].get("harmonized_hash")
        for state in states.values()
    ]
    most_common = max(harmonized_hashes.count(value) for value in set(harmonized_hashes))
    return round(most_common / len(harmonized_hashes), 4)


def summarize(states: Dict[str, StateVector]) -> Dict[str, object]:
    pair_scores = {}
    for (left_name, left_state), (right_name, right_state) in combinations(states.items(), 2):
        pair_scores[f"{left_name}->{right_name}"] = compatibility_score(left_state, right_state)

    average_compatibility = (
        round(sum(pair_scores.values()) / len(pair_scores), 4) if pair_scores else 1.0
    )
    return {
        "coherence": coherence_score(states),
        "average_compatibility": average_compatibility,
        "pair_compatibility": pair_scores,
    }
