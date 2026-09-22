from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, List

from .agent import AgentSnapshot, StateVector


def detect_divergence(states: Dict[str, StateVector]) -> Dict[str, object]:
    disagreements: List[Dict[str, object]] = []
    for (left_name, left_state), (right_name, right_state) in combinations(states.items(), 2):
        left_aligned = bool(left_state["alignment_verdict"]["aligned"])
        right_aligned = bool(right_state["alignment_verdict"]["aligned"])
        if left_aligned != right_aligned:
            disagreements.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "left_aligned": left_aligned,
                    "right_aligned": right_aligned,
                }
            )

    total_pairs = len(list(combinations(states.keys(), 2)))
    divergence_score = len(disagreements) / total_pairs if total_pairs else 0.0
    return {
        "divergence_score": divergence_score,
        "disagreements": disagreements,
        "consensus": divergence_score == 0.0,
    }


def snapshots_to_states(snapshots: Dict[str, AgentSnapshot]) -> Dict[str, StateVector]:
    return {name: snapshot.state_vector for name, snapshot in snapshots.items()}
