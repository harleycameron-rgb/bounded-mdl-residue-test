import hashlib


def make_output(
    text,
    *,
    aligned=True,
    drift_magnitude=0,
    stability_score=1.0,
    mdl_score=1.0,
    residue_prefix=None,
):
    residue_prefix = residue_prefix or hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    core_signature = hashlib.sha256(f"core::{text}".encode("utf-8")).hexdigest()
    harmonized_hash = hashlib.sha256(f"harm::{text}".encode("utf-8")).hexdigest()[:12]
    return {
        "compressed_core": {
            "compressed_bytes": text.encode("utf-8"),
            "signature": core_signature,
        },
        "residue_signature": {
            "length": len(text),
            "punctuation": sum(1 for char in text if char in ".,;:!?"),
            "hash_prefix": residue_prefix,
        },
        "alignment_report": {
            "aligned": aligned,
            "core_prefix": core_signature[:8],
            "residue_prefix": residue_prefix[:8],
        },
        "bounded_response": {
            "echo": text[:200],
            "core_sig": core_signature,
            "residue_prefix": residue_prefix,
        },
        "drift": {
            "drift_vector": {},
            "drift_magnitude": drift_magnitude,
            "stable": drift_magnitude == 0,
        },
        "alignment": {
            "aligned": aligned,
            "confidence": 1.0 if aligned else 0.0,
            "core_prefix": core_signature[:8],
            "residue_prefix": residue_prefix[:8],
            "audit_hash": hashlib.sha256(f"audit::{text}".encode("utf-8")).hexdigest()[:12],
        },
        "harmonized": {
            "bounded_echo": text[:200],
            "core_sig_prefix": core_signature[:12],
            "residue_prefix": residue_prefix,
            "alignment_status": aligned,
            "harmonized_hash": harmonized_hash,
        },
        "stability_envelope": {
            "stability_score": stability_score,
            "drift_magnitude": drift_magnitude,
            "aligned": aligned,
            "core_prefix": core_signature[:12],
            "residue_prefix": residue_prefix,
            "envelope_hash": hashlib.sha256(f"env::{text}".encode("utf-8")).hexdigest()[:12],
        },
        "mdl_score": {
            "mdl_score": mdl_score,
            "base": stability_score,
            "drift_penalty": 0.0,
            "alignment_penalty": 0.0 if aligned else 0.5,
            "core_prefix": core_signature[:12],
            "residue_prefix": residue_prefix,
            "score_hash": hashlib.sha256(f"score::{text}".encode("utf-8")).hexdigest()[:12],
        },
        "unified_hash": hashlib.sha256(f"unified::{text}".encode("utf-8")).hexdigest()[:12],
    }
