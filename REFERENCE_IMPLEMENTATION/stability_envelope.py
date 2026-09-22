# ------------------------------------------------------------
# Stability Envelope Generator — MDL Benchmark v1.0.0
# Produces deterministic stability envelope from drift + audit
# ------------------------------------------------------------

import hashlib

# ------------------------------------------------------------
# Utility: deterministic hash prefix
# ------------------------------------------------------------
def prefix_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------
# Stability Envelope
# ------------------------------------------------------------
def generate_stability_envelope(drift_analysis, alignment_verdict, harmonized_response):
    """
    Produce a deterministic stability envelope block.
    - stability_score: combines drift + alignment
    - envelope_hash: stable hash of envelope contents
    - metadata: core + residue prefixes
    """

    drift_mag = drift_analysis["drift_magnitude"]
    aligned = alignment_verdict["aligned"]

    # deterministic stability score
    stability_score = 1.0 if (drift_mag == 0 and aligned) else 0.0

    core_prefix = harmonized_response["core_sig_prefix"]
    residue_prefix = harmonized_response["residue_prefix"]

    envelope = {
        "stability_score": stability_score,
        "drift_magnitude": drift_mag,
        "aligned": aligned,
        "core_prefix": core_prefix,
        "residue_prefix": residue_prefix,
    }

    envelope["envelope_hash"] = prefix_hash(
        core_prefix + residue_prefix + str(stability_score)
    )

    return envelope


# ------------------------------------------------------------
# Full Envelope Wrapper
# ------------------------------------------------------------
def run_stability_envelope(drift_analysis, alignment_verdict, harmonized_response):
    """
    Wrap drift + alignment + harmonized response into a stability envelope.
    """
    return generate_stability_envelope(drift_analysis, alignment_verdict, harmonized_response)
