from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .agent import AgentSnapshot, StateVector


@dataclass(frozen=True)
class MessageEnvelope:
    source: str
    target: str
    round_index: int
    prompt: str
    response: str
    state_vector: StateVector


def build_prompt(base_prompt: str, inbound_messages: Iterable[MessageEnvelope]) -> str:
    messages = sorted(inbound_messages, key=lambda message: (message.source, message.target))
    if not messages:
        return base_prompt

    context = "\n".join(
        f"{message.source}->{message.target}: {message.response[:120]}"
        for message in messages
    )
    return f"{base_prompt}\n\n[network_context]\n{context}"


def emit_messages(
    snapshot: AgentSnapshot,
    targets: Iterable[str],
) -> List[MessageEnvelope]:
    return [
        MessageEnvelope(
            source=snapshot.agent_name,
            target=target,
            round_index=snapshot.round_index,
            prompt=snapshot.prompt,
            response=snapshot.response,
            state_vector=snapshot.state_vector,
        )
        for target in targets
    ]
