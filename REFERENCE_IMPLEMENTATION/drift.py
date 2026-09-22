# ------------------------------------------------------------
# Drift Math Module — Bounded Predictive‑MDL Residue Test v1.0.0
# Deterministic drift vector computation and stability checks
# ------------------------------------------------------------

import hashlib
import json

# ------------------------------------------------------------
# Utility: stable hash for drift detection
# ------------------------------------------------------------
def stable_hash(obj):
    """Compute a deterministic hash for any JSON‑serializable object."""
    encoded = json.dumps(obj, sort_keys=True, default=_json_default).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _json_default(value):
    if isinstance(value, bytes):
        return value.hex()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


# ------------------------------------------------------------
# Drift Vector Computation
# ------------------------------------------------------------
def compute_drift_vector(first_output, second_output):
    """
    Compute a drift vector representing differences between two pipeline runs.
    Drift vector is a simple structural placeholder for v1.0.0.
    """
    drift = {
        "core_hash_change": stable_hash(first_output["compressed_core"]) != stable_hash(second_output["compressed_core"]),
        "residue_hash_change": stable_hash(first_output["residue_signature"]) != stable_hash(second_output["residue_signature"]),
        "alignment_hash_change": stable_hash(first_output["alignment_report"]) != stable_hash(second_output["alignment_report"]),
        "response_hash_change": stable_hash(first_output["bounded_response"]) != stable_hash(second_output["bounded_response"])
    }

    return drift


# ------------------------------------------------------------
# Drift Magnitude
# ------------------------------------------------------------
def drift_magnitude(drift_vector):
    """
    Count how many components changed.
    Deterministic placeholder for v1.0.0.
    """
    return sum(1 for k, v in drift_vector.items() if v)


# ------------------------------------------------------------
# Drift Stability Check
# ------------------------------------------------------------
def is_stable(drift_vector):
    """
    A model is stable if drift magnitude is zero.
    """
    return drift_magnitude(drift_vector) == 0


# ------------------------------------------------------------
# Full Drift Analysis
# ------------------------------------------------------------
def analyze_pipeline_drift(first_output, second_output):
    """
    Produce a full drift analysis block.
    """
    vector = compute_drift_vector(first_output, second_output)
    magnitude = drift_magnitude(vector)
    stable = is_stable(vector)

    return {
        "drift_vector": vector,
        "drift_magnitude": magnitude,
        "stable": stable
    }


def analyze_drift(text, pipeline_fn):
    """
    Produce a full drift analysis block from repeated pipeline execution.
    """
    return analyze_pipeline_drift(pipeline_fn(text), pipeline_fn(text))
