# ------------------------------------------------------------
# MDL Benchmark Runner — v1.0.0
# Unified execution harness for full MDL pipeline
# ------------------------------------------------------------

try:
    from .core import run_pipeline
    from .drift import analyze_drift
    from .bounded_response import run_harmonized
    from .alignment_auditor import run_alignment_audit
    from .stability_envelope import run_stability_envelope
    from .predictive_mdl_score import run_mdl_score
    from .unified_output import run_unified
except ImportError:
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


# ------------------------------------------------------------
# Optional CLI Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run_benchmark.py \"your text here\"")
        sys.exit(1)

    text = sys.argv[1]
    output = run_benchmark(text)
    print(output)
