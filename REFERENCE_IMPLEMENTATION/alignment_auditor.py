# ------------------------------------------------------------
# Alignment Auditor — MDL Benchmark v1.0.0
# Deterministic alignment verification and verdict generation
# ------------------------------------------------------------

import hashlib

# ------------------------------------------------------------
# Utility: deterministic hash prefix
# ------------------------------------------------------------
def prefix_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------
# Alignment Verdict
# ------------------------------------------------------------
def audit_alignment(alignment_report):
    """
    Produce a deterministic alignment verdict block.
    - aligned: boolean
    - confidence: simple deterministic score
    - audit_hash: stable hash of the verdict
    """

    aligned = alignment_report["aligned"]

    # deterministic confidence score
    confidence = 1.0 if aligned else 0.0

    verdict = {
        "aligned": aligned,
        "confidence": confidence,
        "core_prefix": alignment_report["core_prefix"],
        "residue_prefix": alignment_report["residue_prefix"],
    }

    verdict["audit_hash"] = prefix_hash(
        verdict["core_prefix"] + verdict["residue_prefix"]
    )

    return verdict


# ------------------------------------------------------------
# Full Auditor Wrapper
# ------------------------------------------------------------
def run_alignment_audit(pipeline_output):
    """
    Wrap the pipeline output with an alignment audit.
    """
    return audit_alignment(pipeline_output["alignment_report"])
