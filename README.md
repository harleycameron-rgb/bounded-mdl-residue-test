
README.md

MDL Benchmark — Reference Implementation v1.0.0
Deterministic multi-layer MDL evaluation pipeline for LLM stability, drift, and residue analysis.

---

1. Overview

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

2. Repository Structure

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

3. Installation

From a checkout:

pip install .

From PyPI (after publication):

pip install mdl-residue-llm

---

4. Execution

Python (CLI):
python REFERENCE_IMPLEMENTATION/run_benchmark.py “your text here”

Installed CLI:
mdl-residue-llm "your text here"

Python (Module Import):
from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark
output = run_benchmark(“your text here”)
print(output)

Stable package import:
from mdl_residue_llm import run_benchmark
output = run_benchmark("your text here")
print(output)

---

5. Pipeline Architecture

4.1 Core Pipeline
Deterministic compression, residue extraction, and alignment report.

4.2 Drift Analysis
Magnitude-only drift vector derived from text features.

4.3 Harmonizer
Produces bounded echo, stable prefixes, and harmonized hash.

4.4 Alignment Auditor
Generates alignment verdict, confidence score, and audit hash.

4.5 Stability Envelope
Combines drift + alignment + harmonized response into a stability score.

4.6 Predictive MDL Score
Applies base score, drift penalty, alignment penalty, and score hash.

4.7 Unified Output
Final composed MDL output block with unified hash.

---

6. Determinism Guarantees

• Stable SHA-256 hashing
• Prefix-based signatures
• Bounded text windows
• No stochastic components
• Reproducible across runs
• Identical outputs for identical inputs

---

7. Vendor Integration

Vendors integrate by calling:

run_benchmark(text)

The returned unified output block is submitted as the benchmark result.

---

8. Publishing

This repository includes Python packaging metadata in `pyproject.toml` and a
GitHub Actions workflow at `.github/workflows/publish.yml`.

Release flow:

• build locally with `python -m build`
• verify the `dist/` artifacts
• push a version tag like `v1.0.0`
• publish through the GitHub Actions workflow using PyPI trusted publishing

---

9. Versioning

Current version: v1.0.0
All modules in the reference layer are locked and deterministic.

---

10. Contact

For MDL benchmark integration, specification details, or vendor onboarding, refer to the MDL documentation or your integration channel.

