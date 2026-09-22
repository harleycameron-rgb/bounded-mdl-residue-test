import json
import sys
from pathlib import Path

# ------------------------------------------------------------
# Validation Suite — Bounded Predictive‑MDL Residue Test v1.0.0
# Deterministic scaffold
# ------------------------------------------------------------

# Import reference implementation
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import REFERENCE_IMPLEMENTATION.core as impl


def resolve_test_vector_paths():
    base = ROOT / "TEST_VECTORS"
    candidate_layouts = (
        (base / "inputs", base / "metadata.json"),
        (base / "inputs", base / "TEST_VECTORS" / "metadata.json"),
    )

    for inputs_dir, metadata_file in candidate_layouts:
        if inputs_dir.is_dir() and metadata_file.exists():
            return inputs_dir, metadata_file

    raise FileNotFoundError("Unable to locate test vector inputs and metadata")


def make_json_safe(value):
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [make_json_safe(item) for item in value]
    return value


# ------------------------------------------------------------
# Load Test Vectors
# ------------------------------------------------------------
def load_test_vectors():
    inputs_dir, metadata_file = resolve_test_vector_paths()

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
        core = impl.compress_text(v["text"])
        results.append({
            "id": v["id"],
            "compressed_core": {
                "signature": core["signature"],
                "compressed_size": len(core["compressed_bytes"]),
            }
        })

    return results


# ------------------------------------------------------------
# Residue Tests
# ------------------------------------------------------------
def run_residue_tests():
    results = []
    vectors = load_test_vectors()

    for v in vectors:
        residue = impl.extract_residue(v["text"])
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
        core = impl.compress_text(v["text"])
        residue = impl.extract_residue(v["text"])
        alignment = impl.alignment_report(core["signature"], residue)
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
        first = impl.run_pipeline(v["text"])
        second = impl.run_pipeline(v["text"])

        drift_detected = first != second

        results.append({
            "id": v["id"],
            "drift_detected": drift_detected,
            "first_run": make_json_safe(first),
            "second_run": make_json_safe(second)
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
        output = make_json_safe(impl.run_pipeline(v["text"]))
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
