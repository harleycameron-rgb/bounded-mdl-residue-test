# Vendor Integration Guide

Bounded Predictive‑MDL Residue Test — v1.0.0

## Contents

- [Overview](#overview)
- [Integration Modes](#integration-modes)
- [Determinism Requirements](#determinism-requirements)
- [Reference Benchmark Contract](#reference-benchmark-contract)
- [Multi-Agent Contract](#multi-agent-contract)
- [Validation](#validation)

## Overview

The repository supports deterministic MDL benchmarking for a single input and deterministic analysis for a bounded multi-agent network built from the same benchmark outputs.

## Integration Modes

Vendors can integrate at either level:

1. **Reference benchmark** — produce a deterministic MDL output for `run_benchmark(text)`.
2. **Multi-agent framework** — execute a fixed `AgentNetwork` and inspect round-scoped drift, residue, alignment, and compatibility reports.

## Determinism Requirements

All integrations must remain deterministic:

- identical inputs produce identical outputs
- no randomness
- no adaptive tuning during execution
- no hidden state carried between runs
- fixed topology and message ordering inside a network run

## Reference Benchmark Contract

The reference layer must provide deterministic equivalents of:

- `compress()`
- `extract_residue()`
- `check_alignment()`
- harmonized bounded-response generation
- drift analysis
- stability-envelope generation
- MDL scoring
- `run_full_pipeline()`
- `run_benchmark()`

The unified benchmark output should expose:

- `compressed_core`
- `residue_signature`
- `alignment_report`
- `bounded_response`
- `drift`
- `alignment`
- `harmonized`
- `stability_envelope`
- `mdl_score`
- `unified_hash`

## Multi-Agent Contract

The network layer should preserve these invariants:

- each agent derives its state vector from benchmark output
- each round only consumes messages emitted in the previous round
- message history is grouped by emission round
- residue transfer is measurable per edge
- drift propagation is measurable per edge

This keeps the framework reproducible for vendors while leaving the deeper network behaviour visible in the analysis itself rather than in special-case integration logic.

## Validation

Run the existing validation entrypoints:

```bash
python VALIDATION_SUITE/run_tests.py
python -m unittest discover -s tests -v
```
