# ------------------------------------------------------------
# Bounded Response Harmonizer — MDL Benchmark v1.0.0
# Ensures deterministic, length‑bounded, drift‑safe output
# ------------------------------------------------------------

import hashlib

# ------------------------------------------------------------
# Utility: deterministic hash prefix
# ------------------------------------------------------------
def prefix_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------
# Harmonizer
# ------------------------------------------------------------
def harmonize_response(pipeline_output):
    """
    Produce a deterministic harmonized response block.
    - bounds the echo
    - injects stable hash prefixes
    - ensures residue/core alignment metadata is preserved
    """

    bounded_echo = pipeline_output["bounded_response"]["echo"][:200]
    core_sig = pipeline_output["compressed_core"]["signature"]
    residue_prefix = pipeline_output["residue_signature"]["hash_prefix"]

    harmonized = {
        "bounded_echo": bounded_echo,
        "core_sig_prefix": core_sig[:12],
        "residue_prefix": residue_prefix,
        "alignment_status": pipeline_output["alignment_report"]["aligned"],
        "harmonized_hash": prefix_hash(bounded_echo + core_sig)
    }

    return harmonized


# ------------------------------------------------------------
# Full Harmonized Pipeline Wrapper
# ------------------------------------------------------------
def run_harmonized(pipeline_output):
    """
    Wrap pipeline output with harmonization.
    """
    return harmonize_response(pipeline_output)
