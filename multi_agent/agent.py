from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark


StateVector = Dict[str, object]
BenchmarkFn = Callable[[str], Dict[str, object]]


def state_vector_from_output(output: Dict[str, object]) -> StateVector:
    """
    Normalize a benchmark output into the multi-agent state vector schema.
    """
    harmonized = output.get("harmonized", {})
    alignment = output.get("alignment", output.get("alignment_report", {}))
    stability = output.get("stability_envelope", {})
    mdl_score = output.get("mdl_score", {})

    return {
        "core_signature": output["compressed_core"]["signature"],
        "residue_signature": output["residue_signature"],
        "drift_magnitude": output.get("drift", {}).get("drift_magnitude", 0),
        "alignment_verdict": alignment,
        "harmonized_response": harmonized,
        "stability_envelope": stability,
        "mdl_score": mdl_score,
    }


@dataclass(frozen=True)
class AgentSnapshot:
    agent_name: str
    model_name: str
    round_index: int
    prompt: str
    response: str
    state_vector: StateVector
    raw_output: Dict[str, object]


class AgentNode:
    """
    Deterministic stand-in for an LLM agent participating in a network.
    """

    def __init__(
        self,
        name: str,
        model_name: Optional[str] = None,
        evaluator: Optional[BenchmarkFn] = None,
    ) -> None:
        self.name = name
        self.model_name = model_name or name
        self.evaluator = evaluator or run_benchmark
        self.history: List[AgentSnapshot] = []

    def process(self, prompt: str, round_index: int) -> AgentSnapshot:
        output = self.evaluator(prompt)
        state_vector = state_vector_from_output(output)
        harmonized = state_vector["harmonized_response"]
        if not isinstance(harmonized, dict):
            harmonized = {}
        response = harmonized.get("bounded_echo", output.get("bounded_response", {}).get("echo", ""))
        snapshot = AgentSnapshot(
            agent_name=self.name,
            model_name=self.model_name,
            round_index=round_index,
            prompt=prompt,
            response=response,
            state_vector=state_vector,
            raw_output=output,
        )
        self.history.append(snapshot)
        return snapshot

    @property
    def latest_snapshot(self) -> Optional[AgentSnapshot]:
        return self.history[-1] if self.history else None

    @property
    def latest_state_vector(self) -> Optional[StateVector]:
        snapshot = self.latest_snapshot
        return snapshot.state_vector if snapshot else None
