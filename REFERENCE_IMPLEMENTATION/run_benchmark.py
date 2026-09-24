# ------------------------------------------------------------
# MDL Benchmark Runner — v1.0.0
# Unified execution harness for full MDL pipeline
# ------------------------------------------------------------

import json

try:
    from .core import run_pipeline
    from .drift import analyze_drift
    from .bounded_response import run_harmonized
    from .alignment_auditor import run_alignment_audit
    from .stability_envelope import run_stability_envelope
    from .predictive_mdl_score import run_mdl_score
    from .unified_output import run_unified
except ImportError:  # pragma: no cover - script execution fallback
    from core import run_pipeline
    from drift import analyze_drift
    from bounded_response import run_harmonized
    from alignment_auditor import run_alignment_audit
    from stability_envelope import run_stability_envelope
    from predictive_mdl_score import run_mdl_score
    from unified_output import run_unified

# ------------------------------------------------------------
# Unified Benchmark Runner
# ------------------------------------------------------------
def run_benchmark(text):
    """
    Execute the full MDL benchmark pipeline and return unified output.
    """

    return run_unified(
        text,
        drift_fn=analyze_drift,
        pipeline_fn=run_pipeline,
        harmonizer_fn=run_harmonized,
        audit_fn=run_alignment_audit,
        envelope_fn=run_stability_envelope,
        score_fn=run_mdl_score
    )


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Run the MDL residue benchmark.")
    parser.add_argument("text", help="Input text to evaluate")
    args = parser.parse_args(argv)
    print(json.dumps(run_benchmark(args.text), indent=2))


# ------------------------------------------------------------
# Optional CLI Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
