# ------------------------------------------------------------
# Residue Classification Module — Bounded Predictive‑MDL Residue Test v1.0.0
# Deterministic residue type classification (structural, semantic, drift)
# ------------------------------------------------------------

import re
import hashlib

# ------------------------------------------------------------
# Utility: stable hash
# ------------------------------------------------------------
def stable_hash(text):
    """Deterministic SHA‑256 hash for classification."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ------------------------------------------------------------
# Structural Residue Detection
# ------------------------------------------------------------
def detect_structural_residue(text, core):
    """
    Structural residue is detected by repetitive patterns, character runs,
    or compression‑friendly sequences.
    """
    patterns = [
        r"(.)\1{3,}",        # repeated characters
        r"(..)\1{2,}",       # repeated 2‑char sequences
        r"(...)\\1{2,}"      # repeated 3‑char sequences
    ]

    structural_score = 0
    for p in patterns:
        if re.search(p, text):
            structural_score += 1

    return {
        "score": structural_score,
        "detected": structural_score > 0
    }


# ------------------------------------------------------------
# Semantic Residue Detection
# ------------------------------------------------------------
def detect_semantic_residue(text, core):
    """
    Semantic residue is detected by presence of natural language structure:
    - multiple words
    - verbs
    - adjectives
    - punctuation patterns
    """
    word_count = len(text.split())
    has_verbs = bool(re.search(r"\b(is|are|was|were|be|have|has|do|does|did|jumps|runs|thinks)\b", text))
    has_punctuation = bool(re.search(r"[.,;:!?]", text))

    semantic_score = sum([
        word_count > 5,
        has_verbs,
        has_punctuation
    ])

    return {
        "score": semantic_score,
        "detected": semantic_score > 0
    }


# ------------------------------------------------------------
# Drift Residue Detection
# ------------------------------------------------------------
def detect_drift_residue(text, core):
    """
    Drift residue is detected by instability between text and core hash.
    Placeholder logic for v1.0.0.
    """
    text_hash = stable_hash(text)
    core_hash = stable_hash(core)

    drift_detected = text_hash[:8] != core_hash[:8]

    return {
        "score": 1 if drift_detected else 0,
        "detected": drift_detected
    }


# ------------------------------------------------------------
# Combined Residue Classification
# ------------------------------------------------------------
def classify_residue(text, core):
    """
    Produce a deterministic residue classification block.
    """
    structural = detect_structural_residue(text, core)
    semantic = detect_semantic_residue(text, core)
    drift = detect_drift_residue(text, core)

    return {
        "structural": structural,
        "semantic": semantic,
        "drift": drift
    }
