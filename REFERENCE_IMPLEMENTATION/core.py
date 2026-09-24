# ------------------------------------------------------------
# Core MDL Logic — Bounded Predictive‑MDL Residue Test v1.0.0
# Deterministic compression, residue extraction, and alignment
# ------------------------------------------------------------

import hashlib
import json
import zlib

# ------------------------------------------------------------
# Utility: stable JSON hash
# ------------------------------------------------------------
def stable_hash(obj):
    encoded = json.dumps(obj, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ------------------------------------------------------------
# Compression Core
# ------------------------------------------------------------
def compress_text(text):
    """
    Deterministic compression using zlib + SHA-256 signature.
    """
    raw = text.encode("utf-8")
    compressed = zlib.compress(raw)
    signature = hashlib.sha256(compressed).hexdigest()

    return {
        "compressed_bytes": compressed,
        "signature": signature
    }


# ------------------------------------------------------------
# Residue Extraction
# ------------------------------------------------------------
def extract_residue(text, core=None):
    """
    Extract residue as a simple deterministic placeholder:
    - length
    - punctuation count
    - hash prefix
    """
    punctuation = sum(1 for c in text if c in ".,;:!?")
    length = len(text)
    prefix = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

    return {
        "length": length,
        "punctuation": punctuation,
        "hash_prefix": prefix
    }


# ------------------------------------------------------------
# Alignment Report
# ------------------------------------------------------------
def alignment_report(core_sig, residue_sig):
    """
    Deterministic alignment report:
    - compare hash prefixes
    - compare lengths
    """
    aligned = core_sig[:8] == residue_sig["hash_prefix"][:8]

    return {
        "aligned": aligned,
        "core_prefix": core_sig[:8],
        "residue_prefix": residue_sig["hash_prefix"][:8]
    }


def compress(text):
    """
    Backwards-compatible alias for deterministic compression.
    """
    return compress_text(text)


def check_alignment(core, residue):
    """
    Backwards-compatible alignment helper for callers that pass the full core.
    """
    core_sig = core["signature"] if isinstance(core, dict) else core
    return alignment_report(core_sig, residue)


# ------------------------------------------------------------
# Full Pipeline
# ------------------------------------------------------------
def run_pipeline(text):
    """
    Execute the full MDL pipeline:
    - compression
    - residue extraction
    - alignment
    - bounded response (placeholder)
    """
    compressed = compress_text(text)
    residue = extract_residue(text)
    alignment = alignment_report(compressed["signature"], residue)

    bounded_response = {
        "echo": text[:200],
        "core_sig": compressed["signature"],
        "residue_prefix": residue["hash_prefix"]
    }

    return {
        "compressed_core": compressed,
        "residue_signature": residue,
        "alignment_report": alignment,
        "bounded_response": bounded_response
    }


def run_full_pipeline(text):
    """
    Backwards-compatible alias for the benchmark pipeline.
    """
    return run_pipeline(text)
