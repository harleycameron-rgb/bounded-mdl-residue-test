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
## 9. Reference Implementation Requirements

The reference implementation provides a minimal, transparent, and reproducible 
baseline for running the Bounded Predictive‑MDL Residue Test. It is not intended 
to be optimized; instead, it defines the canonical behaviour that all compliant 
implementations must match.

Two reference implementations are required:

- Python module: REFERENCE_IMPLEMENTATION/core.py  
- JavaScript module: REFERENCE_IMPLEMENTATION/core.js  

Both must follow the rules defined in this section.

### 9.1 Purpose
The reference implementation serves four functions:

1. Demonstrate correct handling of MDL bounds  
2. Provide a canonical method for extracting residue  
3. Define the structure of the compressed core  
4. Provide a baseline for drift detection and stability analysis  

All third‑party implementations must match the behaviour of the reference 
implementation on all test vectors.

### 9.2 Required Functions
Both the Python and JavaScript modules must implement the following functions:

#### 9.2.1 `compress(input_text)`
Produces the Compressed_Core under fixed MDL constraints. Must return:

- `core_structure`  
- `core_length`  
- `entropy_usage`  
- `horizon`  
- `depth`  

#### 9.2.2 `extract_residue(input_text, compressed_core)`
Computes the irreducible remainder. Must return:

- `residue_magnitude`  
- `residue_types`  
- `structural_trace`  
- `alignment_score`  
- `drift_vector`  

#### 9.2.3 `check_alignment(compressed_core, residue)`
Evaluates predictive alignment and returns:

- `alignment_score`  
- `violations`  
- `entropy_deviation`  
- `horizon_overrun`  
- `depth_limit_check`  

#### 9.2.4 `generate_bounded_response(compressed_core, residue)`
Produces the final bounded response under MDL constraints.

### 9.3 Determinism Requirement
Both reference implementations must be fully deterministic. Identical inputs 
must produce identical outputs across all environments. No randomness, 
stochastic behaviour, or adaptive tuning is permitted.

### 9.4 Bound Enforcement
The reference implementation must enforce:

- complexity ceiling  
- entropy budget  
- predictive horizon  
- inference depth limit  

Any violation must raise a standardized error.

### 9.5 Output Format
All functions must return JSON‑serializable objects matching the locked result 
format defined in Section 7.

### 9.6 Cross‑Language Consistency
The Python and JavaScript implementations must produce identical outputs for 
all test vectors. Differences in formatting, whitespace, or ordering are not 
permitted.

### 9.7 Minimal Dependencies
Reference implementations must use minimal external dependencies to ensure 
portability and reproducibility. Only standard library modules may be used.

### 9.8 Versioning
Reference implementations are versioned independently from the specification. 
Any change requires:

- a new version tag  
- updated documentation  
- updated test vector metadata  
- a new release  

Retroactive modification is not permitted.
## 10. Validation Suite Requirements

The validation suite ensures that any implementation of the Bounded 
Predictive‑MDL Residue Test behaves correctly on all test vectors and 
produces outputs that conform to the locked result format. The suite is 
implemented in:

    VALIDATION_SUITE/run_tests.py

This section defines the required behaviour of the validation suite.

### 10.1 Purpose
The validation suite serves four critical functions:

1. Verify correct MDL compression behaviour  
2. Confirm accurate residue extraction and classification  
3. Detect drift, contamination, and instability  
4. Ensure strict adherence to the locked result format  

Any implementation that fails validation is considered non‑compliant.

### 10.2 Required Test Categories
The validation suite must include tests for:

#### 10.2.1 Structural Tests
Verify correct handling of syntactic patterns and structural residue.

#### 10.2.2 Semantic Tests
Verify correct extraction of meaning‑bearing residue and alignment behaviour.

#### 10.2.3 Drift Tests
Detect instability across repeated runs using drift‑sensitive inputs.

#### 10.2.4 Format Tests
Ensure that all outputs match the locked result format defined in Section 7.

### 10.3 Required Functions in run_tests.py
The validation suite must implement the following functions:

#### 10.3.1 `load_test_vectors()`
Loads all test vectors and associated metadata from:

    TEST_VECTORS/inputs/
    TEST_VECTORS/metadata.json

#### 10.3.2 `run_compression_tests(impl)`
Validates that `impl.compress()` produces a correct Compressed_Core.

#### 10.3.3 `run_residue_tests(impl)`
Validates that `impl.extract_residue()` produces correct residue signatures.

#### 10.3.4 `run_alignment_tests(impl)`
Validates predictive alignment behaviour and checks for violations.

#### 10.3.5 `run_drift_tests(impl)`
Runs repeated evaluations to detect drift, contamination, or instability.

#### 10.3.6 `run_format_tests(impl)`
Ensures that all outputs conform to the locked result format.

#### 10.3.7 `run_all_tests(impl)`
Runs the full validation suite and produces a compliance report.

### 10.4 Determinism Requirement
The validation suite must enforce determinism. Any non‑deterministic behaviour 
is classified as drift and results in failure.

### 10.5 Error Handling
The suite must raise standardized errors for:

- MDL bound violations  
- entropy budget overruns  
- horizon or depth limit violations  
- format mismatches  
- drift or contamination detection  

Errors must be descriptive and reproducible.

### 10.6 Compliance Report
The validation suite must produce a final compliance report containing:

- pass/fail status for each test category  
- detailed error messages  
- drift vectors and severity levels  
- alignment scores  
- format compliance results  
- overall compliance classification  

This report must be JSON‑serializable and included in the release artifacts.

### 10.7 Versioning
The validation suite is versioned independently. Any change requires:

- a new version tag  
- updated documentation  
- updated test vector metadata  
- a new release  

Retroactive modification is not permitted.
## 11. Versioning & Release Rules

The Bounded Predictive‑MDL Residue Test follows strict versioning and release 
rules to ensure reproducibility, transparency, and long‑term stability. All 
changes to the specification, reference implementations, test vectors, or 
validation suite must follow the procedures defined in this section.

### 11.1 Semantic Versioning
The benchmark uses semantic versioning:

    MAJOR.MINOR.PATCH

- MAJOR: breaking changes to the specification or locked result format  
- MINOR: new features, new test vectors, or new validation rules  
- PATCH: corrections, clarifications, or non‑breaking updates  

Version numbers must be incremented consistently across all components.

### 11.2 Release Artifacts
Each release must include:

- the full specification  
- reference implementations (Python + JavaScript)  
- test vectors and metadata  
- validation suite  
- compliance report template  
- changelog  

All artifacts must be included in the GitHub release.

### 11.3 Changelog Requirements
Every release must include a changelog entry describing:

- what changed  
- why it changed  
- which components were affected  
- whether the change is breaking or non‑breaking  

Changelog entries must be clear, concise, and complete.

### 11.4 Retroactive Modification Prohibited
No component of the benchmark may be modified retroactively. This includes:

- specification text  
- test vectors  
- reference implementations  
- validation suite  
- locked results  
- metadata  

Any change requires a new version and a new release.

### 11.5 Zenodo Archival Requirement
All releases must be archived in Zenodo to ensure long‑term preservation. Each 
release must include:

- DOI  
- release artifacts  
- metadata  
- license information  

Zenodo DOIs must be referenced in the README.

### 11.6 Locked Results
Locked results must never be stored in the repository. They must be uploaded 
separately to Zenodo as sealed artifacts. Locked results are immutable and 
cannot be altered once published.

### 11.7 Cross‑Version Compatibility
Implementations must specify which version of the benchmark they target. 
Compatibility across versions is not guaranteed. Validation must be performed 
against the exact version declared.

### 11.8 Deprecation Policy
Components may be deprecated only in MINOR or MAJOR releases. Deprecation 
requires:

- clear documentation  
- migration guidance  
- updated validation rules  
- updated test vector metadata  

Deprecated components must remain available for at least one full version cycle.

### 11.9 Release Governance
All releases must be approved by the benchmark maintainers. Approval requires:

- complete artifacts  
- passing validation suite  
- updated documentation  
- updated changelog  
- Zenodo archival  

Unapproved releases must not be published.
