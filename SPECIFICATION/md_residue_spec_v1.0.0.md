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
## 4. Predictive Alignment Rules

Predictive alignment ensures that the model’s output remains consistent with the 
compressed core and does not introduce drift, contamination, or unbounded 
inference. All responses generated during evaluation must satisfy the following 
constraints.

### 4.1 Core Alignment
The model’s response must align strictly with the Compressed_Core produced during 
the MDL compression step. No new structural or semantic elements may be introduced 
that exceed the predictive horizon.

### 4.2 Residue Preservation
The model must not attempt to reinterpret, erase, or overwrite residue. Residue is 
a diagnostic signal and must remain intact for analysis.

### 4.3 Drift Prevention
The model must avoid generating content that:
- extends beyond the inference depth limit  
- increases entropy beyond the allowed budget  
- introduces new, unanchored semantic structures  
- contradicts the compressed core  

Any such behaviour is classified as drift.

### 4.4 Entropy-Constrained Prediction
All predictive behaviour must remain within the entropy budget. The model may not 
use randomness, stochastic elaboration, or speculative inference that violates the 
budget.

### 4.5 No Retroactive Reinterpretation
The model may not reinterpret or modify previous turns, compressed cores, or 
residue signatures. All prior states are locked once produced.

### 4.6 Stability Requirement
The model’s response must be stable under repeated evaluation. Identical inputs 
under identical bounds must produce identical compressed cores and residue 
signatures.
## 5. Evaluation Procedure

This section defines the step‑by‑step process required to run the Bounded 
Predictive‑MDL Residue Test. All evaluations must follow this procedure exactly 
to ensure reproducibility and comparability across models and systems.

### 5.1 Input Acquisition
The model receives a preregistered input sample. Inputs may not be altered, 
expanded, filtered, or preprocessed beyond the minimal normalization specified 
in the reference implementation.

### 5.2 MDL Compression Step
The model attempts to compress the input under the fixed MDL bounds. The output 
of this step is the Compressed_Core, which must satisfy:

- complexity ceiling  
- entropy budget  
- predictive horizon  
- inference depth limit  

The Compressed_Core is locked once produced.

### 5.3 Residue Extraction
Residue is computed as:

    Residue = Input − Compressed_Core

The model must classify the residue according to the taxonomy defined in 
Section 3. Residue signatures must include:

- residue magnitude  
- residue type distribution  
- structural trace  
- predictive alignment score  
- drift vector (if present)

### 5.4 Predictive Alignment Check
The model evaluates whether its intended response aligns with the Compressed_Core 
and respects all MDL constraints. If misalignment is detected, the model must 
correct its response before proceeding.

### 5.5 Response Generation
The model generates a bounded response that:

- aligns with the Compressed_Core  
- preserves residue  
- avoids drift  
- respects entropy constraints  
- remains within the predictive horizon  

The response is locked once produced.

### 5.6 State Update
The evaluation state is updated with:

- compressed core  
- residue signature  
- alignment score  
- drift vector  
- stability indicators  

No retroactive modification of previous states is permitted.

### 5.7 Output Packaging
The final output for each evaluation consists of:

- Compressed_Core  
- Residue signature  
- MDL trace  
- Predictive alignment report  
- Drift analysis  
- Final bounded response  

This output must conform to the locked result format defined in Section 7.
