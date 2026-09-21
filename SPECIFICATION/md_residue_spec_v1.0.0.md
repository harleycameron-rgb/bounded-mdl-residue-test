## Bounded Predictive‑MDL Residue Test — Specification v1.0.0

## 1. Purpose
The Bounded Predictive‑MDL Residue Test is a preregistered evaluation protocol designed to measure how predictive models behave under strict Minimum Description Length (MDL) constraints. It identifies the residue — the irreducible structure left after optimal compression — and uses this residue as a diagnostic signal for drift, hallucination, epistemic contamination, and compression instability.

This specification defines the formal rules, bounds, and procedures required to run the benchmark reproducibly.

## 2. MDL Bounds

The benchmark operates under a fixed Minimum Description Length (MDL) budget. 
All evaluations must respect the following constraints:

### 2.1 Complexity Ceiling
The model must compress the input into a representation whose description length 
does not exceed the predefined complexity ceiling. This ceiling is fixed for the 
entire benchmark and cannot be altered during evaluation.

### 2.2 Entropy Budget
Each evaluation run is assigned a finite entropy budget. The model’s predictive 
operations must remain within this budget, ensuring that no step introduces 
unbounded randomness or drift.

### 2.3 Predictive Horizon
The predictive horizon defines how far the model may extend its inference beyond 
the compressed core. This horizon is intentionally short to prevent runaway 
speculation and to maintain reproducibility.

### 2.4 Inference Depth Limit
The model may not exceed the maximum inference depth specified in the protocol. 
This prevents recursive elaboration that would violate MDL constraints.

### 2.5 Bound Invariance
All bounds remain invariant throughout the evaluation. No adaptive tuning, 
dynamic resizing, or post‑hoc adjustment is permitted.
