r"""Advanced context, runtime-heavy, and uncertainty scoring for file retrieval."""
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_context import (
    CandidateFileContext,
    RetrievalQueryContext,
)

__all__ = [
    'apply_advanced_and_runtime_scoring',
]



def apply_advanced_and_runtime_scoring(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    score += retriever._score_advanced_file_context(
        query.q,
        candidate.path,
        query.tokens,
        reasons,
    )

    runtime_signal_score, runtime_signal_paths = retriever._score_runtime_signal_matches(
        query.q,
        reasons,
    )
    if candidate.path in runtime_signal_paths:
        score += runtime_signal_score
        reasons.append("runtime-signal-path-boost")

    if query.is_runtime_question:
        score = _score_runtime_question(retriever, query, candidate, score, reasons)

    if query.intents.get("uncertainty", False):
        hotspot_count = len(retriever.idx.hotspots_by_file.get(candidate.path, []))
        if hotspot_count:
            hotspot_boost = min(120, hotspot_count * 12)
            score += hotspot_boost
            reasons.append(f"uncertainty-hotspot-boost:{hotspot_boost}")

    return score


def _score_runtime_question(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    runtime_blob = candidate.advanced_ctx["runtime"]

    if runtime_blob:
        score += 80
        reasons.append("runtime-heavy-question-runtime-boost")

    if (
        "runtime_runner_probe_apply_button" in query.q
        and "runtime_runner_probe_apply_button" in runtime_blob
    ):
        score += 220
        reasons.append("exact-runtime-probe-apply-button-boost")

    if "apply button" in query.q and (
        "probe apply button clicked" in runtime_blob
        or "on_apply_clicked" in runtime_blob
    ):
        score += 180
        reasons.append("apply-click-runtime-boost")

    if "signal connections" in query.q and retriever.idx.runtime_events_by_file.get(
        candidate.path
    ):
        score += 120
        reasons.append("runtime-signal-connections-file-boost")

    if "check_runtime_trace_schema.py" in candidate.normalized_path:
        score -= 120
        reasons.append("runtime-schema-validator-penalty")

    if "/tooltips/" in candidate.normalized_path or "tooltip" in candidate.normalized_path:
        score -= 80
        reasons.append("runtime-tooltip-noise-penalty")

    if (
        candidate.normalized_path.endswith("/runtime_runner.py")
        or candidate.normalized_path == "runtime_runner.py"
        or "/project_reasoner_v10_runtime_collector/" in candidate.normalized_path
        or "/runtime_collector/" in candidate.normalized_path
    ):
        score += 220
        reasons.append("runtime-collector-path-boost")

    if "runtime probe signal connections" in query.q and "signal_connection" in runtime_blob:
        score += 180
        reasons.append("runtime-probe-signal-connections-boost")

    if (
        "probe button signal-slot connections" in query.q
        and "runtime_runner_probe_apply_button" in runtime_blob
    ):
        score += 240
        reasons.append("probe-button-signal-slot-runtime-boost")

    if "on_apply_clicked" in query.q and "on_apply_clicked" in runtime_blob:
        score += 260
        reasons.append("exact-on-apply-clicked-runtime-boost")

    qt_signal_map = getattr(retriever.idx, "qt_signal_map", [])
    if isinstance(qt_signal_map, list):
        best_signal_score = 0
        for sig_record in qt_signal_map:
            if not isinstance(sig_record, dict):
                continue
            sig_file = str(sig_record.get("source_file", "")).strip()
            if sig_file != candidate.path:
                continue
            sig_name = str(sig_record.get("signal_name", "")).lower()
            target = str(sig_record.get("target", "")).lower()
            src_sym = str(sig_record.get("source_symbol", "")).lower()
            combined = sig_name + " " + target + " " + src_sym
            matched_tokens = [tok for tok in query.tokens if tok in combined]
            if not matched_tokens:
                continue
            record_score = 120 + (80 if len(matched_tokens) >= 2 else 0)
            if record_score > best_signal_score:
                best_signal_score = record_score
        if best_signal_score > 0:
            score += best_signal_score
            reasons.append("qt-signal-map-boost")

    return score
