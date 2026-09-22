# ------------------------------------------------------------
# Unified Output Composer — MDL Benchmark v1.0.0
# Produces deterministic unified MDL output block
# ------------------------------------------------------------

import hashlib

# ------------------------------------------------------------
# Utility: deterministic hash prefix
# ------------------------------------------------------------
def prefix_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------
# Unified Composer
# ------------------------------------------------------------
def compose_unified_output(
    text,
    drift_analysis,
    alignment_verdict,
    harmonized_response,
    stability_envelope,
    mdl_score
):
    """
    Produce a deterministic unified MDL output block.
    """

    unified = {
        "input_text": text[:200],
        "drift": drift_analysis,
        "alignment": alignment_verdict,
        "harmonized": harmonized_response,
        "stability_envelope": stability_envelope,
        "mdl_score": mdl_score,
    }

    # deterministic unified hash
    unified["unified_hash"] = prefix_hash(
        harmonized_response["core_sig_prefix"]
        + harmonized_response["residue_prefix"]
        + str(mdl_score["mdl_score"])
    )

    return unified


# ------------------------------------------------------------
# Full Unified Wrapper
# ------------------------------------------------------------
def run_unified(
    text,
    drift_fn,
    harmonizer_fn,
    audit_fn,
    envelope_fn,
    score_fn,
    pipeline_fn=None,
    pipeline_output=None,
    second_pipeline_output=None,
):
    """
    Execute the full MDL pipeline and produce unified output.
    """

    if pipeline_output is None:
        if pipeline_fn is None:
            raise ValueError("pipeline_fn is required when pipeline_output is not provided")
        pipeline_output = pipeline_fn(text)
    if second_pipeline_output is None:
        if pipeline_fn is None:
            raise ValueError(
                "second_pipeline_output is required when pipeline_fn is not provided"
            )
        second_pipeline_output = pipeline_fn(text)

    drift_analysis = drift_fn(pipeline_output, second_pipeline_output)
    harmonized = harmonizer_fn(pipeline_output)
    alignment_verdict = audit_fn(pipeline_output)
    stability_envelope = envelope_fn(
        drift_analysis,
        alignment_verdict,
        harmonized
    )
    mdl_score = score_fn(
        stability_envelope,
        drift_analysis,
        alignment_verdict
    )

    return compose_unified_output(
        text,
        drift_analysis,
        alignment_verdict,
        harmonized,
        stability_envelope,
        mdl_score
    )
