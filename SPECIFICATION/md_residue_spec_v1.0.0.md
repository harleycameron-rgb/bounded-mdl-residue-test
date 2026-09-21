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

## 3. Residue Definition & Classification

Residue is the irreducible remainder left after the model attempts optimal 
compression under the MDL bounds. It represents the part of the input that 
cannot be reduced, predicted, or encoded within the allowed complexity budget.

Residue is the primary diagnostic signal of this benchmark.

### 3.1 Formal Definition
Residue R is defined as:

    R = Input − Compressed_Core

where the Compressed_Core is the minimal description produced by the model 
within the MDL constraints. Residue is measured structurally, not semantically.

### 3.2 Residue Types
Residue is classified into the following categories:

#### 3.2.1 Structural Residue
Irreducible syntactic or formal structure that cannot be compressed further 
without violating the complexity ceiling.

#### 3.2.2 Semantic Residue
Meaning-bearing content that remains unpredictable or uncompressible within 
the model’s predictive horizon.

#### 3.2.3 Epistemic Residue
Information the model cannot integrate due to limitations in its internal 
representation or knowledge boundary.

#### 3.2.4 Drift Residue
Patterns indicating deviation from stable predictive behaviour, often caused 
by overextension beyond the inference depth limit.

#### 3.2.5 Contamination Residue
Artifacts introduced by the model that do not originate from the input and 
signal instability or hallucination.

### 3.3 Residue Signature
Each evaluation produces a residue signature consisting of:

- residue magnitude  
- residue type distribution  
- structural trace  
- predictive alignment score  
- drift vector (if present)

Residue signatures are used for cross‑model comparison and stability analysis.
