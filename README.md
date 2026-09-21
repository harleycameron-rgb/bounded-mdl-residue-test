# bounded-mdl-residue-test
-

README.md — Bounded Predictive‑MDL Residue Test (v1.0.0)

Preregistered Benchmark • Locked Results • Standards‑Ready Specification

Overview

The Bounded Predictive‑MDL Residue Test is a preregistered evaluation protocol designed to measure how predictive models behave under strict Minimum Description Length (MDL) constraints. It identifies the residue—the irreducible structure left after optimal compression—which serves as a diagnostic signal for:

• drift
• hallucination
• epistemic contamination
• compression failure
• unstable inference


This benchmark provides a stable, reproducible, audit‑friendly method for evaluating large language models and other predictive systems.

---

Key Features

• Bounded MDL Framework
Fixed complexity ceiling, entropy budget, and predictive horizon.
• Residue Extraction
Formal classification of structural, semantic, epistemic, and drift residue.
• Preregistered Protocol
The evaluation plan is locked prior to execution to prevent retroactive tuning.
• Locked Results
Reference outputs are sealed to ensure reproducibility and prevent gaming.
• Vendor‑Neutral Reference Implementation
Minimal Python and JavaScript modules for easy integration.
• Open Test Vectors
Public sample inputs and expected outputs for independent verification.


---

Why This Benchmark Exists

Modern LLMs compress and predict at massive scale, but their failure modes often hide inside the parts they cannot compress.
Residue reveals:

• where the model’s internal representation breaks
• where drift begins
• where hallucination signatures form
• where compression becomes unstable


This benchmark provides a mathematically grounded, reproducible, and auditable way to detect those failures.

---

Repository Structure

bounded-mdl-residue-test/
│
├── SPECIFICATION/              # Formal standard
├── REFERENCE_IMPLEMENTATION/   # Minimal Python + JS modules
├── TEST_VECTORS/               # Public inputs + expected outputs
├── VALIDATION_SUITE/           # Compliance tests
└── DOCS/                       # Theory, reproducibility, integration


The full dataset, locked results, and instrument contamination maps are intentionally excluded to preserve benchmark integrity.

---

Getting Started

1. Install Dependencies

The reference implementation uses only standard libraries.
No external dependencies are required.

2. Run the Reference Implementation

Example (Python):

python validate.py --input test_vectors/inputs/sample_01.txt


This produces:

• compressed core
• residue signature
• MDL trace
• drift‑check result


3. Validate Against Test Vectors

Use the validation suite:

python run_tests.py


This confirms:

• MDL bounds respected
• residue classification correct
• drift detection functioning
• outputs match expected signatures


---

Specification

The full formal specification is located in:

SPECIFICATION/md_residue_spec_v1.0.0.md


It defines:

• MDL bounds
• residue taxonomy
• predictive horizon rules
• drift‑detection logic
• locked‑result format


This document is intended for standards bodies, safety labs, and vendors.

---

Use Cases

• LLM safety evaluation
• drift‑detection pipelines
• hallucination analysis
• compression‑stability testing
• multi‑LLM cooperative inference
• regulatory compliance audits


---

Citing This Benchmark

Cameron, Harley (waxtablet). Bounded Predictive‑MDL Residue Test: Preregistered Benchmark and Locked Results (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.22882941

---

License

This project is licensed under the Apache License 2.0, enabling broad commercial and research adoption while protecting the integrity of the benchmark.

---

Contact

For questions, reproducibility reports, or integration support, please open an issue in this repository.

---
