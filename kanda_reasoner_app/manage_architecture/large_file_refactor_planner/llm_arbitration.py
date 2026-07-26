# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/llm_arbitration.py
"""Optional JSON-only local LLM arbitration contracts for the planner."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    LLMArbitrationRequest,
    LLMArbitrationResult,
    ModuleAnalysisReport,
    RefactorPlan,
    RefactorSymbol,
)

__all__ = [
    "build_llm_arbitration_request",
    "arbitrate_symbol_assignment",
    "parse_llm_arbitration_response",
]

PROMPT_VERSION = "large-file-refactor-planner-llm-arbitration-v1"
_ALLOWED_PURPOSES = {
    "assign_ambiguous_symbol",
    "suggest_semantic_helper_filename",
    "draft_missing_docstring",
    "explain_cycle_cause",
    "suggest_merge_or_shared_helper",
}
_FORBIDDEN_ACTIONS = {
    "rewrite_module",
    "create_patch",
    "write_file",
    "bypass_validation",
    "bypass_no_leak",
    "decide_ownership_without_source_inspection",
}


def build_llm_arbitration_request(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    symbol: RefactorSymbol | None = None,
    *,
    purpose: str = "assign_ambiguous_symbol",
    model_name: str = "",
    temperature: float = 0.0,
    settings_hash: str = "",
    local_llm_enabled: bool = False,
) -> LLMArbitrationRequest:
    """Build a bounded request without calling an LLM."""
    if purpose not in _ALLOWED_PURPOSES:
        raise ValueError("Unsupported LLM arbitration purpose: " + purpose)
    chosen = symbol or _first_symbol(report)
    modules = [module.filename for module in plan.proposed_modules]
    line_span = (chosen.start_line, chosen.end_line) if chosen else (0, 0)
    symbol_name = chosen.name if chosen else ""
    symbol_hash = chosen.content_hash if chosen else ""
    modules_hash = _hash_text("\n".join(sorted(modules)))
    cache_key = _cache_key(
        report.source_content_hash,
        symbol_name,
        line_span,
        symbol_hash,
        modules_hash,
        model_name,
        temperature,
        settings_hash,
        PROMPT_VERSION,
    )
    return LLMArbitrationRequest(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=report.target_file,
        purpose=purpose,
        symbol_name=symbol_name,
        symbol_line_span=line_span,
        candidate_modules=modules,
        model_name=model_name,
        temperature=temperature,
        settings_hash=settings_hash,
        prompt_version=PROMPT_VERSION,
        file_content_hash=report.source_content_hash,
        symbol_body_hash=symbol_hash,
        candidate_module_list_hash=modules_hash,
        cache_key=cache_key,
        local_llm_enabled=local_llm_enabled,
    )


def arbitrate_symbol_assignment(
    request: LLMArbitrationRequest,
    raw_response: str | None = None,
) -> LLMArbitrationResult:
    """Return a validated result or safe deterministic fallback."""
    if not request.local_llm_enabled:
        return _fallback("LLM_DISABLED", "Local LLM is disabled by settings.")
    if raw_response is None or not raw_response.strip():
        return _fallback("LLM_UNAVAILABLE", "No local LLM response was provided.")
    try:
        return parse_llm_arbitration_response(request, raw_response)
    except ValueError as exc:
        return _fallback("LLM_INVALID_RESPONSE", str(exc))


def parse_llm_arbitration_response(
    request: LLMArbitrationRequest,
    raw_response: str,
) -> LLMArbitrationResult:
    """Parse and validate a JSON-only LLM arbitration response."""
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response must be JSON only: " + str(exc)) from exc
    if not isinstance(payload, dict):
        raise ValueError("LLM response must be a JSON object.")
    forbidden = set(payload.get("actions", [])) & _FORBIDDEN_ACTIONS
    if forbidden:
        raise ValueError("Forbidden LLM action requested: " + sorted(forbidden)[0])
    selected = str(payload.get("selected_module", ""))
    if selected and selected not in request.candidate_modules:
        raise ValueError("Selected module is not in the candidate module list.")
    confidence = str(payload.get("confidence", "low"))
    if confidence not in {"low", "medium", "high"}:
        raise ValueError("Unsupported LLM confidence value: " + confidence)
    rationale = str(payload.get("rationale", "")).strip()
    warnings = _string_list(payload.get("warnings", []))
    return LLMArbitrationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status="ok",
        selected_module=selected,
        confidence=confidence,
        rationale=rationale,
        warnings=warnings,
        raw_response_used=True,
        fallback_used=False,
    )


def _fallback(status: str, message: str) -> LLMArbitrationResult:
    """Return a safe no-write fallback result."""
    return LLMArbitrationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        confidence="none",
        rationale=message,
        warnings=[message],
        raw_response_used=False,
        fallback_used=True,
    )


def _first_symbol(report: ModuleAnalysisReport) -> RefactorSymbol | None:
    """Return a stable representative symbol for advisory review."""
    return report.symbols[0] if report.symbols else None


def _cache_key(
    file_hash: str,
    symbol_name: str,
    line_span: tuple[int, int],
    symbol_hash: str,
    modules_hash: str,
    model_name: str,
    temperature: float,
    settings_hash: str,
    prompt_version: str,
) -> str:
    """Return the required cache-key hash for bounded LLM arbitration."""
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "file_content_hash": file_hash,
        "symbol_name": symbol_name,
        "symbol_line_span": list(line_span),
        "symbol_body_hash": symbol_hash,
        "candidate_module_list_hash": modules_hash,
        "model_name": model_name,
        "temperature": temperature,
        "llm_settings_hash": settings_hash,
        "prompt_version": prompt_version,
    }
    text = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return _hash_text(text)


def _hash_text(text: str) -> str:
    """Return a SHA-256 hash for text data."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _string_list(value: object) -> list[str]:
    """Return a list of strings from a JSON value."""
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]
