# ------------------------------------------------------------
# MDL Benchmark Runner — v1.0.0
# Unified execution harness for full MDL pipeline
# ------------------------------------------------------------

import json

try:
    from .core import run_pipeline
    from .drift import analyze_drift
    from .bounded_response import harmonize_response
    from .alignment_auditor import run_alignment_audit
    from .stability_envelope import run_stability_envelope
    from .predictive_mdl_score import run_mdl_score
    from .unified_output import compose_unified_output
except ImportError:  # pragma: no cover - script execution fallback
    from core import run_pipeline
    from drift import analyze_drift
    from bounded_response import harmonize_response
    from alignment_auditor import run_alignment_audit
    from stability_envelope import run_stability_envelope
    from predictive_mdl_score import run_mdl_score
    from unified_output import compose_unified_output


# ------------------------------------------------------------
# Unified Benchmark Runner
# ------------------------------------------------------------
def run_benchmark(text):
    """
    Execute the full MDL benchmark pipeline and return unified output.
    """
    pipeline_output = run_pipeline(text)
    repeated_pipeline_output = run_pipeline(text)
    drift_analysis = analyze_drift(pipeline_output, repeated_pipeline_output)
    harmonized = harmonize_response(pipeline_output)
    alignment_verdict = run_alignment_audit(pipeline_output)
    stability_envelope = run_stability_envelope(
        drift_analysis,
        alignment_verdict,
        harmonized,
    )
    mdl_score = run_mdl_score(
        stability_envelope,
        drift_analysis,
        alignment_verdict,
    )
    unified = compose_unified_output(
        pipeline_output,
        drift_analysis,
        alignment_verdict,
        harmonized,
        stability_envelope,
        mdl_score,
    )
    return {**pipeline_output, **unified}


# ------------------------------------------------------------
# CLI Entry Point
# ------------------------------------------------------------
def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Run the MDL residue benchmark.")
    parser.add_argument("text", help="Input text to evaluate")
    args = parser.parse_args(argv)
    print(json.dumps(run_benchmark(args.text), indent=2))


if __name__ == "__main__":
    main()
