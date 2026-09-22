
# MDL Benchmark — Reference Implementation v1.0.0

Deterministic multi-layer MDL evaluation pipeline for LLM stability, drift, and residue analysis.

## Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Execution](#execution)
- [Pipeline Architecture](#pipeline-architecture)
  - [Core Pipeline](#core-pipeline)
  - [Drift Analysis](#drift-analysis)
  - [Harmonizer](#harmonizer)
  - [Alignment Auditor](#alignment-auditor)
  - [Stability Envelope](#stability-envelope)
  - [Predictive MDL Score](#predictive-mdl-score)
  - [Unified Output](#unified-output)
- [Determinism Guarantees](#determinism-guarantees)
- [Vendor Integration](#vendor-integration)
- [Versioning](#versioning)
- [Contact](#contact)

---

## Overview

This benchmark evaluates:

• compression signature stability
• residue extraction consistency
• drift magnitude
• alignment integrity
• harmonized bounded response behavior
• stability envelope formation
• predictive MDL scoring
• unified output composition


All modules are deterministic and language-agnostic.

---

## Repository Structure

REFERENCE_IMPLEMENTATION/
• core.py
• core.js
• drift.py
• residue.py
• bounded_response.py
• alignment_auditor.py
• stability_envelope.py
• predictive_mdl_score.py
• unified_output.py
• run_benchmark.py

VALIDATION_SUITE/
• run_tests.py

---

## Execution

Python (CLI):
python REFERENCE_IMPLEMENTATION/run_benchmark.py “your text here”

Python (Module Import):
from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark
output = run_benchmark(“your text here”)
print(output)

---

## Pipeline Architecture

### Core Pipeline
Deterministic compression, residue extraction, and alignment report.

### Drift Analysis
Magnitude-only drift vector derived from text features.

### Harmonizer
Produces bounded echo, stable prefixes, and harmonized hash.

### Alignment Auditor
Generates alignment verdict, confidence score, and audit hash.

### Stability Envelope
Combines drift + alignment + harmonized response into a stability score.

### Predictive MDL Score
Applies base score, drift penalty, alignment penalty, and score hash.

### Unified Output
Final composed MDL output block with unified hash.

---

## Determinism Guarantees

• Stable SHA-256 hashing
• Prefix-based signatures
• Bounded text windows
• No stochastic components
• Reproducible across runs
• Identical outputs for identical inputs

---

## Vendor Integration

Vendors integrate by calling:

run_benchmark(text)

The returned unified output block is submitted as the benchmark result.

---

## Versioning

Current version: v1.0.0
All modules in the reference layer are locked and deterministic.

---

## Contact

For MDL benchmark integration, specification details, or vendor onboarding, refer to the MDL documentation or your integration channel.

