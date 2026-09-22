
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

3. Execution

Python (CLI):
python REFERENCE_IMPLEMENTATION/run_benchmark.py “your text here”

Python (Module Import):
from REFERENCE_IMPLEMENTATION.run_benchmark import run_benchmark
output = run_benchmark(“your text here”)
print(output)

---

4. Pipeline Architecture

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

5. Determinism Guarantees

• Stable SHA-256 hashing
• Prefix-based signatures
• Bounded text windows
• No stochastic components
• Reproducible across runs
• Identical outputs for identical inputs

---

6. Vendor Integration

Vendors integrate by calling:

run_benchmark(text)

The returned unified output block is submitted as the benchmark result.

---

7. Versioning

Current version: v1.0.0
All modules in the reference layer are locked and deterministic.

---

8. Contact

For MDL benchmark integration, specification details, or vendor onboarding, refer to the MDL documentation or your integration channel.


