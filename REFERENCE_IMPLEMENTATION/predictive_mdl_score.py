# ------------------------------------------------------------
# Predictive MDL Score Generator — MDL Benchmark v1.0.0
# Produces deterministic MDL score from stability envelope
# ------------------------------------------------------------

import hashlib

# ------------------------------------------------------------
# Utility: deterministic hash prefix
# ------------------------------------------------------------
def prefix_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------
# MDL Score Computation
# ------------------------------------------------------------
def compute_mdl_score(stability_envelope, drift_analysis, alignment_verdict):
    """
    Deterministic MDL score:
    - base score from stability envelope
    - penalties from drift magnitude
    - penalties from misalignment
    """

    base = stability_envelope["stability_score"]

    drift_penalty = 0.0
    if drift_analysis["drift_magnitude"] > 0:
        drift_penalty = 0.5

    alignment_penalty = 0.0
    if not alignment_verdict["aligned"]:
        alignment_penalty = 0.5

    mdl_score = max(0.0, base - drift_penalty - alignment_penalty)

    score_block = {
        "mdl_score": mdl_score,
        "base": base,
        "drift_penalty": drift_penalty,
        "alignment_penalty": alignment_penalty,
        "core_prefix": stability_envelope["core_prefix"],
        "residue_prefix": stability_envelope["residue_prefix"],
    }

    score_block["score_hash"] = prefix_hash(
        str(mdl_score)
        + stability_envelope["core_prefix"]
        + stability_envelope["residue_prefix"]
    )

    return score_block


# ------------------------------------------------------------
# Full MDL Score Wrapper
# ------------------------------------------------------------
def run_mdl_score(stability_envelope, drift_analysis, alignment_verdict):
    """
    Wrap stability envelope + drift + alignment into MDL score.
    """
    return compute_mdl_score(stability_envelope, drift_analysis, alignment_verdict)
