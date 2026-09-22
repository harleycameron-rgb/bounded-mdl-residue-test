
# bounded-mdl-residue-test

Deterministic MDL benchmark primitives plus a multi-agent communication analysis framework for studying how drift, residue, alignment, and stability propagate between LLM-like agents during live interaction.

## Project vision

The repository now supports two layers:

1. **Reference MDL benchmark modules** in `REFERENCE_IMPLEMENTATION/`
2. **Multi-agent communication analysis** in `multi_agent/` and `analysis/`

The multi-agent layer treats each model as a node with a state vector derived from the MDL output:

- core signature
- residue signature
- drift magnitude
- alignment verdict
- harmonized response
- stability envelope
- MDL score

This enables research into:

- cross-model drift propagation
- residue transfer dynamics
- alignment divergence across agents
- stability envelope compatibility
- harmonized response coherence
- drift amplification or dampening in a network

## Repository structure

```text
bounded-mdl-residue-test/
├── REFERENCE_IMPLEMENTATION/
├── VALIDATION_SUITE/
├── analysis/
├── examples/
├── multi_agent/
├── tests/
├── README.md
├── requirements.txt
└── setup.py
```

## Reference benchmark usage

```python
from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark

output = run_benchmark("Measure a deterministic baseline.")
print(output["drift"]["drift_magnitude"])  # 0 for identical baseline comparison
```

The reference benchmark remains deterministic:

- stable SHA-256 hashing
- bounded text windows
- no stochastic components
- reproducible output for identical input

## Multi-agent framework

### Core components

- `multi_agent.agent` — agent node with per-round state tracking
- `multi_agent.communication` — prompt composition and message envelopes
- `multi_agent.network` — chain, tree, and graph topologies with non-recursive rounds
- `multi_agent.drift_propagation` — pairwise and network drift spread analysis
- `multi_agent.residue_transfer` — residue change and amplification/dampening tracking
- `multi_agent.alignment_analyzer` — disagreement and divergence detection
- `multi_agent.metrics` — coherence and compatibility scoring
- `analysis.reporter` — aggregate report generation
- `analysis.visualizer` — lightweight text visualization

### Non-recursive design

The communication framework is intentionally bounded: each round only consumes messages emitted in the **previous** round. That prevents same-round feedback loops while still allowing drift propagation analysis over time.

## Quick start

### Validation suite

```bash
python VALIDATION_SUITE/run_tests.py
```

### Focused test suite

```bash
python -m unittest discover -s tests -v
```

### Example scenario

```bash
python -m examples.basic_multi_agent
```

## Example workflow

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
report = generate_report(network)
print(report["metrics"])
print(report["alignment"])
```

## Research methodology guide

1. Build a network topology with `AgentNetwork`
2. Inject a shared prompt or scenario
3. Execute bounded rounds of communication
4. Compare state vectors across edges and rounds
5. Inspect compatibility, coherence, drift, residue, and divergence reports

Suggested scenarios:

- aligned peers with matching prompts
- diverging agents with mismatched alignment outputs
- cascading drift along a chain
- tree fan-out for stability envelope compatibility

## Development notes

- The project currently uses only the Python standard library.
- `setup.py` is included for lightweight packaging.
- Example scripts are deterministic demonstrations rather than live API integrations.
