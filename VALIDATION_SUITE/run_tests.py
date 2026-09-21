#import json
import os
from pathlib import Path

# ------------------------------------------------------------
# Validation Suite — Bounded Predictive‑MDL Residue Test v1.0.0
# Deterministic scaffold
# ------------------------------------------------------------

# Import reference implementation
import REFERENCE_IMPLEMENTATION.core as impl


# ------------------------------------------------------------
# Load Test Vectors
# ------------------------------------------------------------
def load_test_vectors():
    base = Path("TEST_VECTORS")
    inputs_dir = base / "inputs"
    metadata_file = base / "metadata.json"

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    vectors = []
    for entry in metadata["test_vectors"]:
        input_path = inputs_dir / f"{entry['input_id']}.txt"
        with open(input_path, "r") as f:
            text = f.read().strip()

        vectors.append({
            "id": entry["input_id"],
            "category": entry["category"],
            "text": text,
            "meta": entry
        })

    return vectors


# ------------------------------------------------------------
# Compression Tests
# ------------------------------------------------------------
def run_compression_tests():
    results = []
    vectors = load_test_vectors()

    for v in vectors:
        core = impl.compress(v["text"])
        results.append({
            "id": v["id"],
            "compressed_core": core
        })

    return results


# ------------------------------------------------------------
# Residue Tests
# ------------------------------------------------------------
def run_residue_tests():
    results = []
    vectors = load_test_vectors()

    for v in vectors:
        core = impl.compress(v["text"])
        residue = impl.extract_residue(v["text"], core)
        results.append({
            "id": v["id"],
            "residue_signature": residue
        })

    return results


# ------------------------------------------------------------
# Alignment Tests
# ------------------------------------------------------------
def run_alignment_tests():
    results = []
    vectors = load_test_vectors()

    for v in vectors:
        core = impl.compress(v["text"])
        residue = impl.extract_residue(v["text"], core)
        alignment = impl.check_alignment(core, residue)
        results.append({
            "id": v["id"],
            "alignment_report": alignment
        })

    return results


# ------------------------------------------------------------
# Drift Tests (Repeated Evaluation)
# ------------------------------------------------------------
def run_drift_tests():
    results = []
    vectors = load_test_vectors()

    for v in vectors:
        first = impl.run_full_pipeline(v["text"])
        second = impl.run_full_pipeline(v["text"])

        drift_detected = first != second

        results.append({
            "id": v["id"],
            "drift_detected": drift_detected,
            "first_run": first,
            "second_run": second
        })

    return results


# ------------------------------------------------------------
# Format Tests
# ------------------------------------------------------------
def run_format_tests():
    results = []
    vectors = load_test_vectors()

    required_keys = {
        "compressed_core",
        "residue_signature",
        "alignment_report",
        "bounded_response"
    }

    for v in vectors:
        output = impl.run_full_pipeline(v["text"])
        missing = required_keys - set(output.keys())

        results.append({
            "id": v["id"],
            "missing_keys": list(missing),
            "format_valid": len(missing) == 0
        })

    return results


# ------------------------------------------------------------
# Run All Tests
# ------------------------------------------------------------
def run_all_tests():
    return {
        "compression": run_compression_tests(),
        "residue": run_residue_tests(),
        "alignment": run_alignment_tests(),
        "drift": run_drift_tests(),
        "format": run_format_tests()
    }


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    report = run_all_tests()
    print(json.dumps(report, indent=2))

