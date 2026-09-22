# bounded-mdl-residue-test

Deterministic MDL benchmark primitives plus a bounded multi-agent analysis framework for measuring how drift, residue, alignment, and stability move through a fixed communication network.

## Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Deterministic Reference Benchmark](#deterministic-reference-benchmark)
- [Multi-Agent Framework](#multi-agent-framework)
  - [State Vector](#state-vector)
  - [Round-Scoped Execution](#round-scoped-execution)
  - [Network Analysis](#network-analysis)
- [Execution](#execution)
- [Documentation](#documentation)
- [Determinism Guarantees](#determinism-guarantees)
- [Vendor Integration](#vendor-integration)

## Overview

The repository exposes two coherent layers:

1. `REFERENCE_IMPLEMENTATION/` — deterministic MDL benchmark execution for a single text input.
2. `multi_agent/` + `analysis/` — deterministic network execution and reporting built on top of MDL-derived state vectors.

The multi-agent layer keeps the surface contract technical and reproducible:

- deterministic benchmark outputs
- bounded, non-recursive network rounds
- full state-vector analysis per agent
- drift propagation measurement across edges
- residue transfer analysis across edges
- alignment and compatibility summaries for each round

## Repository Structure

```text
bounded-mdl-residue-test/
├── REFERENCE_IMPLEMENTATION/
├── VALIDATION_SUITE/
├── analysis/
├── docs/
├── multi_agent/
├── support/
└── tests/
```

## Deterministic Reference Benchmark

`run_benchmark(text)` composes the existing MDL pipeline into a single deterministic output block.

```python
from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark

output = run_benchmark("Measure a deterministic baseline.")
print(output["drift"]["drift_magnitude"])
print(output["stability_envelope"]["stability_score"])
```

The benchmark output remains importable and validation-friendly for vendors that only need the single-input reference layer.

## Multi-Agent Framework

### State Vector

Each `AgentNode` reduces benchmark output into a stable state vector containing:

- core signature
- residue signature
- drift magnitude
- alignment verdict
- harmonized response
- stability envelope
- MDL score

### Round-Scoped Execution

`AgentNetwork` executes agents in bounded rounds. Each round consumes only messages emitted in the previous round, so network context travels forward without same-round recursion.

```python
from analysis.reporter import generate_report
from multi_agent.agent import AgentNode
from multi_agent.network import AgentNetwork

network = AgentNetwork.from_chain([
    AgentNode("alpha", model_name="model-a"),
    AgentNode("beta", model_name="model-b"),
    AgentNode("gamma", model_name="model-c"),
])

network.run("Track drift propagation without recursion.", rounds=2)
report = generate_report(network, round_index=1)
print(report["drift"])
print(report["residue"])
```

`run()` starts a fresh simulation and clears prior execution history. Use `run_round()` when continuing an existing network execution on the same object.

`message_history` is grouped by emission round, while `emitted_messages` preserves a flat compatibility view for aggregate counting.

### Network Analysis

The analysis layer measures:

- pairwise and network drift propagation
- residue transfer and residue change across edges
- alignment divergence between agents
- coherence and compatibility metrics
- round-scoped reporting and lightweight visualization

## Execution

Reference validation:

```bash
python VALIDATION_SUITE/run_tests.py
```

Focused multi-agent tests:

```bash
python -m unittest discover -s tests -v
```

## Documentation

- `docs/overview.md` — project overview and architecture map
- `docs/vendor_integration.md` — deterministic integration guidance for adopters
- `README.md` — unified quick start and navigation entrypoint

## Determinism Guarantees

- stable SHA-256 hashing
- bounded text windows
- no stochastic components
- reproducible outputs for identical inputs
- fixed network topology per run
- one-round-delayed message delivery semantics

## Vendor Integration

Vendors can adopt either layer:

1. call `run_benchmark(text)` for the single-input MDL benchmark
2. construct an `AgentNetwork` to analyze bounded multi-agent execution on top of the same state schema

Both layers use deterministic data structures and reproducible control flow so adoption does not depend on hidden runtime behaviour.
