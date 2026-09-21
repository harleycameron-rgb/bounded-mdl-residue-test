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
## 6. Drift Detection & Stability Analysis

Drift refers to any deviation from stable, bounded predictive behaviour. The 
Bounded Predictive‑MDL Residue Test includes a formal drift‑detection mechanism 
to identify instability, contamination, or divergence across repeated runs.

### 6.1 Definition of Drift
Drift occurs when the model’s output changes in ways that cannot be explained by 
the MDL bounds, entropy budget, or predictive horizon. Drift is detected when:

- residue magnitude changes unexpectedly  
- residue type distribution shifts without cause  
- structural traces diverge across identical inputs  
- predictive alignment scores degrade  
- new semantic structures appear that were not present in the compressed core  

### 6.2 Drift Vector
Each evaluation produces a drift vector representing the direction and magnitude 
of deviation. The drift vector includes:

- Δ residue magnitude  
- Δ structural trace  
- Δ semantic alignment  
- Δ entropy usage  
- Δ predictive horizon stability  

A non‑zero drift vector indicates instability.

### 6.3 Stability Threshold
The benchmark defines a stability threshold. If the drift vector exceeds this 
threshold, the model is classified as unstable for that evaluation. Thresholds 
are fixed and cannot be tuned per model.

### 6.4 Repeated Evaluation Requirement
Models must undergo repeated evaluation using identical inputs and MDL bounds. 
Stable models produce:

- identical compressed cores  
- identical residue signatures  
- identical drift vectors (zero or near‑zero)  
- identical alignment scores  

Any divergence across runs is recorded as drift.

### 6.5 Contamination Detection
Contamination occurs when the model introduces artifacts not present in the 
input or compressed core. Contamination is detected when:

- new semantic elements appear  
- hallucinated structures emerge  
- entropy usage spikes  
- residue signatures contain foreign patterns  

Contamination is treated as a severe form of drift.

### 6.6 Drift Severity Levels
Drift is classified into three severity levels:

#### Level 1 — Minor Drift
Small deviations within acceptable tolerance. Model remains usable.

#### Level 2 — Moderate Drift
Significant deviations indicating instability. Model requires further analysis.

#### Level 3 — Severe Drift
Major deviations, contamination, or hallucination. Model fails the benchmark.

### 6.7 Stability Report
Each evaluation produces a stability report containing:

- drift vector  
- severity level  
- contamination indicators  
- entropy usage summary  
- predictive alignment score  
- stability classification  

This report is included in the final locked output.
## 7. Locked Result Format

All benchmark outputs must conform to a strict locked format to ensure 
reproducibility, comparability, and auditability. The locked result format 
prevents post‑hoc modification, adaptive tuning, or selective reporting.

Each evaluation produces a single result package containing the following 
components.

### 7.1 Compressed Core
A JSON object representing the minimal MDL‑constrained representation of the 
input. It must include:

- `core_structure`: structural representation  
- `core_length`: description length  
- `entropy_usage`: entropy consumed during compression  
- `horizon`: predictive horizon used  
- `depth`: inference depth reached  

The compressed core is immutable once produced.

### 7.2 Residue Signature
A structured record describing the irreducible remainder. It must include:

- `residue_magnitude`  
- `residue_types`: list of structural, semantic, epistemic, drift, contamination  
- `structural_trace`: irreducible syntactic patterns  
- `alignment_score`: predictive alignment with the compressed core  
- `drift_vector`: if present  

Residue signatures must follow the taxonomy defined in Section 3.

### 7.3 MDL Trace
A chronological record of the compression process, including:

- step‑by‑step description length changes  
- entropy usage at each step  
- horizon and depth transitions  
- bound checks and constraint validations  

The MDL trace must be complete and unaltered.

### 7.4 Predictive Alignment Report
A formal report evaluating whether the model’s response aligns with the 
compressed core. It must include:

- alignment score  
- violations detected  
- entropy deviations  
- horizon overruns  
- depth limit checks  

Any misalignment must be explicitly recorded.

### 7.5 Drift Analysis
A structured analysis of drift behaviour, including:

- drift vector  
- severity level  
- contamination indicators  
- stability threshold comparison  
- repeated‑run divergence  

Drift analysis must follow the rules defined in Section 6.

### 7.6 Final Bounded Response
The model’s final response, generated under MDL constraints. It must:

- align with the compressed core  
- preserve residue  
- avoid drift  
- respect entropy limits  
- remain within the predictive horizon  

The final response is locked and cannot be modified.

### 7.7 Packaging Requirements
All components must be packaged into a single JSON or JSONL file with the 
following top‑level keys:

- `compressed_core`  
- `residue_signature`  
- `mdl_trace`  
- `alignment_report`  
- `drift_analysis`  
- `bounded_response`  

This file constitutes the official locked result for the evaluation.
## 8. Test Vector Requirements

Test vectors are the public, preregistered input samples used to validate 
implementations of the Bounded Predictive‑MDL Residue Test. They ensure that 
all models are evaluated using identical, reproducible inputs.

### 8.1 Purpose of Test Vectors
Test vectors serve three functions:

1. Provide standardized inputs for cross‑model comparison  
2. Enable independent verification of benchmark behaviour  
3. Ensure that residue extraction and drift detection operate consistently  

Test vectors must be publicly accessible and included in the repository.

### 8.2 Structure of Test Vectors
Each test vector consists of:

- `input_id`: unique identifier  
- `input_text`: the raw input sample  
- `expected_core_properties`: high‑level expectations for the compressed core  
- `expected_residue_properties`: high‑level expectations for residue  
- `notes`: optional clarifications  

These expectations do not include locked results; they only define the 
structural behaviour the model should exhibit.

### 8.3 Types of Test Vectors
The benchmark requires at least three categories of test vectors:

#### 8.3.1 Structural Inputs
Inputs with strong syntactic patterns designed to test structural residue 
extraction.

#### 8.3.2 Semantic Inputs
Meaning‑bearing inputs designed to test semantic residue and predictive 
alignment.

#### 8.3.3 Drift‑Sensitive Inputs
Inputs engineered to reveal drift, contamination, or instability across 
repeated runs.

### 8.4 Format Requirements
Test vectors must be stored as plain text files in:

    TEST_VECTORS/inputs/

Metadata for each test vector must be stored in:

    TEST_VECTORS/metadata.json

Metadata must include:

- `input_id`  
- `category`  
- `description`  
- `expected_core_properties`  
- `expected_residue_properties`  

### 8.5 Versioning
Test vectors are versioned independently from the benchmark specification. 
Changes to test vectors require:

- a new version tag  
- updated metadata  
- a changelog entry  
- a new release  

Test vectors must never be altered retroactively.

### 8.6 Public Availability
All test vectors must remain publicly accessible to ensure transparency and 
independent verification. Locked results, however, must not be included in the 
repository.

### 8.7 Compliance Requirement
Any implementation of the benchmark must demonstrate correct behaviour on all 
test vectors to be considered compliant.
