"""Mock semantic evidence contract for future routing_signal_scorer v3 ML work.

This module is intentionally standard-library-only and does not implement
embeddings, vector search, model loading, corpus generation, prompt loading, or
routing authority. It exists so future semantic providers must fit an
advisory-only evidence shape before any real ML dependency is introduced.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

FEATURE_ID = "routing_signal_scorer_v3_mock_semantic_evidence_contract_v1"
SCHEMA_VERSION = "3.1-mock"
AUTHORITY = "advisory_only"
DEFAULT_PROVIDER_ID = "disabled_null_provider"
DEFAULT_AMBIGUITY_DELTA = 0.05
CURRENT_ALLOWED_USE = "advisory_routing_hint"

SEMANTIC_STATES = (
    "NO_SEMANTIC_PROVIDER",
    "NO_MATCH",
    "WEAK_SEMANTIC_MATCH",
    "STRONG_SEMANTIC_ADVISORY",
    "HIGH_SIGNAL_ADVISORY",
    "AMBIGUOUS_SEMANTIC_MATCH",
    "STALE_CORPUS_FALLBACK",
    "INDEX_MISSING_FALLBACK",
    "INDEX_CORRUPT_FALLBACK",
    "PROVIDER_UNAVAILABLE_FALLBACK",
    "ERROR_STATE_FALLBACK",
)

FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {
        "final_route",
        "required_prompts",
        "may_proceed_now",
        "route_override",
        "auto_load_prompts",
        "write_freeze_memory",
        "modify_startup",
        "modify_prompt_library",
        "self_update_corpus",
        "router_override",
        "required_prompt_files",
        "load_prompts_now",
        "freeze_write",
        "startup_mutation",
        "prompt_library_mutation",
    }
)

APPROVED_CANDIDATE_FIELDS = frozenset(
    {
        "candidate_id",
        "candidate_label",
        "route_family_hint",
        "score",
        "confidence_band",
        "ambiguity_status",
        "evidence_summary",
        "source_context_id",
        "source_context_version",
        "source_structural_hash",
        "corpus_hash",
        "embedding_model_id",
        "embedding_model_version",
        "embedding_dimensions",
        "lifecycle_status",
        "isolation_domain",
        "allowed_use",
        "forbidden_use",
        "source_hash_status",
        "corpus_hash_status",
        "stale_status",
        "metadata_eligible",
        "metadata_eligibility_reasons",
        "candidate_promotion_allowed",
        "advisory_only_reason",
    }
)

REQUIRED_INPUT_CANDIDATE_FIELDS = frozenset(
    {
        "candidate_id",
        "candidate_label",
        "score",
        "lifecycle_status",
        "allowed_use",
        "source_structural_hash",
        "corpus_hash",
        "embedding_model_id",
    }
)


@dataclass(frozen=True)
class CandidateValidation:
    """Validation result for one mock semantic candidate."""

    is_valid: bool
    errors: tuple[str, ...]


def build_disabled_semantic_evidence_report(text: object = "") -> dict[str, object]:
    """Return the disabled semantic-provider evidence shape.

    The raw input text is never persisted in the returned report. This is a
    contract guard for the future no-query-persistence policy.
    """

    source_text = "" if text is None else str(text)
    return {
        "schema_version": SCHEMA_VERSION,
        "feature_id": FEATURE_ID,
        "authority": AUTHORITY,
        "semantic_enabled": False,
        "provider_id": DEFAULT_PROVIDER_ID,
        "semantic_state": "NO_SEMANTIC_PROVIDER",
        "semantic_candidates": [],
        "rejected_candidates": [],
        "metadata_eligibility_gate_applied": True,
        "ambiguity_gate_applied": True,
        "advisory_only_guard_applied": True,
        "lexical_fallback_required": True,
        "lexical_fallback_reason": "semantic provider disabled; lexical scorer remains primary",
        "canon_decides_final_route": True,
        "does_not_override_router": True,
        "automatic_prompt_loading": False,
        "self_learning_enabled": False,
        "external_dependencies": [],
        "input_text_persisted": False,
        "input_length": len(source_text),
        "advisory_only_reason": "semantic evidence is an untrusted witness and never routing authority",
    }


def build_mock_semantic_evidence_report(
    candidates: Iterable[Mapping[str, Any]] | None,
    *,
    provider_id: str = "mock_semantic_provider",
    ambiguity_delta: float = DEFAULT_AMBIGUITY_DELTA,
) -> dict[str, object]:
    """Build an advisory-only semantic evidence report from mock candidates.

    This function accepts prebuilt mock candidate dictionaries. It does not
    embed text, load a model, read a vector index, generate a corpus, scan the
    filesystem, persist user queries, or decide routing. It only proves the
    future evidence contract and guards.
    """

    normalized_candidates: list[dict[str, object]] = []
    rejected: list[dict[str, object]] = []

    for index, candidate in enumerate(list(candidates or [])):
        if not isinstance(candidate, Mapping):
            rejected.append({"candidate_index": index, "errors": ["candidate is not a mapping"]})
            continue
        validation = validate_semantic_candidate(candidate)
        if not validation.is_valid:
            rejected.append(
                {
                    "candidate_index": index,
                    "candidate_id": str(candidate.get("candidate_id", "unknown")),
                    "errors": list(validation.errors),
                }
            )
            continue
        prepared = _prepare_candidate(candidate)
        if bool(prepared["metadata_eligible"]):
            normalized_candidates.append(prepared)
        else:
            rejected.append(
                {
                    "candidate_index": index,
                    "candidate_id": str(candidate.get("candidate_id", "unknown")),
                    "errors": list(prepared["metadata_eligibility_reasons"]),
                }
            )

    normalized_candidates.sort(key=lambda item: float(item.get("score", 0.0)), reverse=True)
    ambiguous = _is_ambiguous(normalized_candidates, ambiguity_delta=ambiguity_delta)
    semantic_state = _semantic_state(normalized_candidates, rejected, ambiguous)

    if ambiguous:
        for candidate in normalized_candidates:
            candidate["ambiguity_status"] = True
            candidate["candidate_promotion_allowed"] = False
            candidate["advisory_only_reason"] = (
                "semantic candidates are close; ambiguity increases caution and cannot increase authority"
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "feature_id": FEATURE_ID,
        "authority": AUTHORITY,
        "semantic_enabled": True,
        "provider_id": str(provider_id or "mock_semantic_provider"),
        "semantic_state": semantic_state,
        "semantic_candidates": normalized_candidates,
        "rejected_candidates": rejected,
        "metadata_eligibility_gate_applied": True,
        "ambiguity_gate_applied": True,
        "ambiguity_delta": round(float(ambiguity_delta), 6),
        "advisory_only_guard_applied": True,
        "lexical_fallback_required": semantic_state in {
            "NO_MATCH",
            "AMBIGUOUS_SEMANTIC_MATCH",
            "ERROR_STATE_FALLBACK",
        },
        "lexical_fallback_reason": _fallback_reason(semantic_state),
        "canon_decides_final_route": True,
        "does_not_override_router": True,
        "automatic_prompt_loading": False,
        "self_learning_enabled": False,
        "external_dependencies": [],
        "input_text_persisted": False,
        "advisory_only_reason": "semantic evidence is an untrusted witness and never routing authority",
    }


def validate_semantic_candidate(candidate: Mapping[str, Any]) -> CandidateValidation:
    """Validate a mock semantic candidate against the approved evidence shape."""

    errors: list[str] = []
    keys = set(candidate.keys())
    forbidden = sorted(keys & FORBIDDEN_AUTHORITY_FIELDS)
    unexpected = sorted(keys - APPROVED_CANDIDATE_FIELDS)
    missing = sorted(REQUIRED_INPUT_CANDIDATE_FIELDS - keys)

    if forbidden:
        errors.append("forbidden authority fields present: " + ", ".join(forbidden))
    if unexpected:
        errors.append("unexpected fields present: " + ", ".join(unexpected))
    if missing:
        errors.append("required fields missing: " + ", ".join(missing))

    try:
        score = float(candidate.get("score", 0.0))
    except (TypeError, ValueError):
        errors.append("score is not numeric")
    else:
        if score < 0.0 or score > 1.0:
            errors.append("score must be between 0.0 and 1.0")

    return CandidateValidation(is_valid=not errors, errors=tuple(errors))


def render_mock_semantic_evidence_report_text(report: Mapping[str, Any]) -> str:
    """Render a compact, non-imperative semantic evidence report."""

    candidates = report.get("semantic_candidates", [])
    if not isinstance(candidates, list):
        candidates = []

    labels: list[str] = []
    for item in candidates[:3]:
        if not isinstance(item, Mapping):
            continue
        labels.append(str(item.get("candidate_label", "unknown")))

    lines = [
        "Routing signal scorer v3 mock semantic evidence report",
        "authority=advisory_only",
        "semantic_state=" + str(report.get("semantic_state", "unknown")),
        "provider_id=" + str(report.get("provider_id", "unknown")),
        "metadata_eligibility_gate_applied=" + str(bool(report.get("metadata_eligibility_gate_applied"))),
        "ambiguity_gate_applied=" + str(bool(report.get("ambiguity_gate_applied"))),
        "lexical_fallback_required=" + str(bool(report.get("lexical_fallback_required"))),
        "canon_decides_final_route=" + str(bool(report.get("canon_decides_final_route"))),
        "automatic_prompt_loading=False",
        "semantic_candidates=" + (", ".join(labels) if labels else "none"),
        "advisory_note=semantic evidence is not routing authority",
    ]
    return "\n".join(lines)


def _prepare_candidate(candidate: Mapping[str, Any]) -> dict[str, object]:
    score = round(float(candidate.get("score", 0.0)), 6)
    eligible, reasons = _metadata_eligibility(candidate)
    return {
        "candidate_id": str(candidate.get("candidate_id", "")),
        "candidate_label": str(candidate.get("candidate_label", "")),
        "route_family_hint": str(candidate.get("route_family_hint", "semantic_candidate")),
        "score": score,
        "confidence_band": _confidence_band(score),
        "ambiguity_status": False,
        "evidence_summary": str(candidate.get("evidence_summary", "mock semantic evidence candidate")),
        "source_context_id": str(candidate.get("source_context_id", candidate.get("candidate_id", ""))),
        "source_context_version": str(candidate.get("source_context_version", "mock-v1")),
        "source_structural_hash": str(candidate.get("source_structural_hash", "")),
        "corpus_hash": str(candidate.get("corpus_hash", "")),
        "embedding_model_id": str(candidate.get("embedding_model_id", "mock-model")),
        "embedding_model_version": str(candidate.get("embedding_model_version", "mock-version")),
        "embedding_dimensions": int(candidate.get("embedding_dimensions", 0) or 0),
        "lifecycle_status": str(candidate.get("lifecycle_status", "")),
        "isolation_domain": str(candidate.get("isolation_domain", "routing_signal_scorer")),
        "allowed_use": _as_list(candidate.get("allowed_use", [])),
        "forbidden_use": _as_list(candidate.get("forbidden_use", [])),
        "source_hash_status": str(candidate.get("source_hash_status", "valid")),
        "corpus_hash_status": str(candidate.get("corpus_hash_status", "valid")),
        "stale_status": str(candidate.get("stale_status", "fresh")),
        "metadata_eligible": eligible,
        "metadata_eligibility_reasons": reasons,
        "candidate_promotion_allowed": False,
        "advisory_only_reason": "semantic evidence is not routing authority",
    }


def _metadata_eligibility(candidate: Mapping[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    lifecycle_status = str(candidate.get("lifecycle_status", "")).lower()
    allowed_use = set(_as_list(candidate.get("allowed_use", [])))
    forbidden_use = set(_as_list(candidate.get("forbidden_use", [])))
    source_hash_status = str(candidate.get("source_hash_status", "valid")).lower()
    corpus_hash_status = str(candidate.get("corpus_hash_status", "valid")).lower()
    stale_status = str(candidate.get("stale_status", "fresh")).lower()

    if lifecycle_status != "active":
        reasons.append("lifecycle_status is not active")
    if CURRENT_ALLOWED_USE not in allowed_use:
        reasons.append("allowed_use does not include advisory_routing_hint")
    if CURRENT_ALLOWED_USE in forbidden_use:
        reasons.append("forbidden_use blocks advisory_routing_hint")
    if source_hash_status != "valid":
        reasons.append("source_structural_hash is not valid")
    if corpus_hash_status != "valid":
        reasons.append("corpus_hash is not valid")
    if stale_status not in {"fresh", "current", "valid"}:
        reasons.append("candidate is stale")
    return (not reasons, reasons or ["metadata eligible"])


def _is_ambiguous(candidates: list[Mapping[str, Any]], *, ambiguity_delta: float) -> bool:
    if len(candidates) < 2:
        return False
    first = float(candidates[0].get("score", 0.0))
    second = float(candidates[1].get("score", 0.0))
    return abs(first - second) <= float(ambiguity_delta)


def _semantic_state(candidates: list[Mapping[str, Any]], rejected: list[Mapping[str, Any]], ambiguous: bool) -> str:
    if ambiguous:
        return "AMBIGUOUS_SEMANTIC_MATCH"
    if not candidates:
        return "ERROR_STATE_FALLBACK" if rejected else "NO_MATCH"
    top_score = float(candidates[0].get("score", 0.0))
    return _confidence_band(top_score)


def _confidence_band(score: float) -> str:
    if score >= 0.80:
        return "HIGH_SIGNAL_ADVISORY"
    if score >= 0.65:
        return "STRONG_SEMANTIC_ADVISORY"
    if score > 0.0:
        return "WEAK_SEMANTIC_MATCH"
    return "NO_MATCH"


def _fallback_reason(state: str) -> str:
    if state == "AMBIGUOUS_SEMANTIC_MATCH":
        return "semantic candidates are ambiguous; lexical scorer remains primary"
    if state == "ERROR_STATE_FALLBACK":
        return "mock semantic candidate contract rejected one or more candidates; lexical scorer remains primary"
    if state == "NO_MATCH":
        return "no eligible semantic candidates; lexical scorer remains primary"
    return "lexical scorer remains deterministic fallback even when semantic evidence is present"


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value]
    return [str(value)]
