# ------------------------------------------------------------
# MDL Benchmark Runner — v1.0.0
# Unified execution harness for full MDL pipeline
# ------------------------------------------------------------

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
    drift_analysis = analyze_drift(pipeline_output, pipeline_output)
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
        text,
        drift_analysis,
        alignment_verdict,
        harmonized,
        stability_envelope,
        mdl_score,
    )
    return {**pipeline_output, **unified}


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
