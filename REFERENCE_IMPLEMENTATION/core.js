/* ------------------------------------------------------------
   Core MDL Logic — Bounded Predictive‑MDL Residue Test v1.0.0
   Deterministic compression, residue extraction, and alignment
------------------------------------------------------------- */

import crypto from "crypto";

/* ------------------------------------------------------------
   Utility: stable JSON hash
------------------------------------------------------------- */
export function stableHash(obj) {
    const encoded = JSON.stringify(obj, Object.keys(obj).sort());
    return crypto.createHash("sha256").update(encoded).digest("hex");
}

/* ------------------------------------------------------------
   Compression Core
------------------------------------------------------------- */
export function compressText(text) {
    const raw = Buffer.from(text, "utf8");
    const compressed = Buffer.from(raw); // placeholder (JS zlib optional)
    const signature = crypto.createHash("sha256").update(compressed).digest("hex");

    return {
        compressed_bytes: compressed,
        signature
    };
}

/* ------------------------------------------------------------
   Residue Extraction
------------------------------------------------------------- */
export function extractResidue(text) {
    const punctuation = [...text].filter(c => ".,;:!?".includes(c)).length;
    const length = text.length;
    const prefix = crypto.createHash("sha256").update(text).digest("hex").slice(0, 12);

    return {
        length,
        punctuation,
        hash_prefix: prefix
    };
}

/* ------------------------------------------------------------
   Alignment Report
------------------------------------------------------------- */
export function alignmentReport(coreSig, residueSig) {
    const aligned = coreSig.slice(0, 8) === residueSig.hash_prefix.slice(0, 8);

    return {
        aligned,
        core_prefix: coreSig.slice(0, 8),
        residue_prefix: residueSig.hash_prefix.slice(0, 8)
    };
}

/* ------------------------------------------------------------
   Full Pipeline
------------------------------------------------------------- */
export function runPipeline(text) {
    const compressed = compressText(text);
    const residue = extractResidue(text);
    const alignment = alignmentReport(compressed.signature, residue);

    const bounded_response = {
        echo: text.slice(0, 200),
        core_sig: compressed.signature,
        residue_prefix: residue.hash_prefix
    };

    return {
        compressed_core: compressed,
        residue_signature: residue,
        alignment_report: alignment,
        bounded_response
    };
}
