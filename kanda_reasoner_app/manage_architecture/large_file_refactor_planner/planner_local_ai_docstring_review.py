# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_docstring_review.py
"""Bounded local-AI review for low-confidence deterministic docstring proposals."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from kanda_reasoner_app.reasoner_engine.local_ai_chat_service import (
    LocalAIChatError,
    chat_with_local_model,
    get_local_ai_model_candidates,
)

from .models import DocstringProposal, ModuleAnalysisReport
from .planner_bounded_refinement import apply_bounded_docstring_updates
from .planner_local_ai_json_response import parse_local_ai_json_object

__all__ = [
    "DocstringAIReviewResult",
    "review_docstring_proposals_with_local_ai",
]

_MAX_TARGETS = 24


@dataclass(frozen=True)
class DocstringAIReviewResult:
    """Outcome of bounded local-AI review for deterministic docstring proposals."""

    status: str
    proposals: tuple[DocstringProposal, ...]
    model_name: str = ""
    reviewed_count: int = 0
    updated_count: int = 0
    rationale: str = ""
    warnings: tuple[str, ...] = ()
    fallback_used: bool = False


def review_docstring_proposals_with_local_ai(
    report: ModuleAnalysisReport,
    proposals: list[DocstringProposal],
    *,
    model_selection: str = "",
) -> DocstringAIReviewResult:
    """Review only low-confidence or review-required proposals with local AI."""

    pending = [
        proposal
        for proposal in proposals
        if proposal.confidence == "low"
        or proposal.status == "review_required"
        or proposal.provenance in {
            "low_confidence_needs_review",
            "manual_required",
        }
    ]
    if not pending:
        return DocstringAIReviewResult(
            status="validated_no_changes",
            proposals=tuple(proposals),
            rationale="No low-confidence docstring proposals required AI review.",
        )
    try:
        candidates = get_local_ai_model_candidates(model_selection)
    except Exception as exc:
        return _fallback(proposals, "Model lookup failed: " + str(exc))
    if not candidates:
        return _fallback(proposals, "No local AI model is available.")

    selected = pending[:_MAX_TARGETS]
    try:
        raw, model_name = _chat_first_available(
            candidates,
            _build_messages(report, selected),
        )
        payload = _parse_response(raw, selected)
        refined = apply_bounded_docstring_updates(
            proposals,
            payload["updates"],
            provenance="llm_drafted",
        )
    except (LocalAIChatError, ValueError, RuntimeError) as exc:
        return _fallback(proposals, "Docstring review failed: " + str(exc))

    partial = len(pending) > len(selected)
    warnings = list(payload["warnings"])
    if partial:
        warnings.append(
            "Review target limit reached; remaining low-confidence proposals need human review."
        )
    return DocstringAIReviewResult(
        status="review_partial" if partial else "refined",
        proposals=tuple(refined),
        model_name=model_name,
        reviewed_count=len(selected),
        updated_count=len(payload["updates"]),
        rationale=payload["rationale"],
        warnings=tuple(warnings),
        fallback_used=False,
    )


def _chat_first_available(
    candidates: list[str],
    messages: list[dict[str, str]],
) -> tuple[str, str]:
    errors: list[str] = []
    for model_name in candidates:
        try:
            return chat_with_local_model(
                messages,
                model_selection=model_name,
                temperature=0.02,
                max_tokens=3200,
            )
        except Exception as exc:
            errors.append(model_name + ": " + str(exc))
    raise LocalAIChatError(
        "No local model completed docstring review. " + " | ".join(errors)
    )


def _build_messages(
    report: ModuleAnalysisReport,
    proposals: list[DocstringProposal],
) -> list[dict[str, str]]:
    symbols = {
        symbol.name: {
            "kind": symbol.kind,
            "signature": symbol.signature,
            "return_annotation": symbol.return_annotation,
            "risk_flags": symbol.risk_flags,
        }
        for symbol in report.symbols
    }
    payload = {
        "target_file": report.target_file,
        "source_content_hash": report.source_content_hash,
        "targets": [proposal.to_dict() for proposal in proposals],
        "symbol_context": symbols,
    }
    system = (
        "Review only the provided docstring proposal targets. Return JSON only. "
        "Do not add targets, change code, infer unsupported behavior, or use Markdown. "
        "Allowed schema: {\"updates\":[{\"target_kind\":\"kind\","
        "\"target_name\":\"name\",\"proposed_docstring\":\"triple-quoted text\"}],"
        "\"rationale\":\"text\",\"warnings\":[\"text\"]}. "
        "Every proposed_docstring must be wrapped in triple double quotes. "
        "Return an empty updates list when the deterministic wording should remain."
    )
    return [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": json.dumps(payload, sort_keys=True, ensure_ascii=True),
        },
    ]


def _parse_response(
    raw: str,
    allowed: list[DocstringProposal],
) -> dict[str, Any]:
    payload = parse_local_ai_json_object(
        raw,
        context="Local AI docstring response",
    )
    if not isinstance(payload, dict):
        raise ValueError("Docstring review response must be a JSON object.")
    updates = payload.get("updates", [])
    if not isinstance(updates, list):
        raise ValueError("updates must be a list.")
    allowed_keys = {
        (item.target_kind, item.target_name) for item in allowed
    }
    normalized: list[dict[str, str]] = []
    for item in updates:
        if not isinstance(item, dict):
            raise ValueError("Each docstring update must be an object.")
        update = {
            "target_kind": str(item.get("target_kind", "")).strip(),
            "target_name": str(item.get("target_name", "")).strip(),
            "proposed_docstring": str(
                item.get("proposed_docstring", "")
            ).strip(),
        }
        if (update["target_kind"], update["target_name"]) not in allowed_keys:
            raise ValueError("Local AI returned an unknown docstring target.")
        normalized.append(update)
    warnings = payload.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
    return {
        "updates": normalized,
        "rationale": str(payload.get("rationale", "")).strip(),
        "warnings": [str(item) for item in warnings],
    }


def _fallback(
    proposals: list[DocstringProposal],
    rationale: str,
) -> DocstringAIReviewResult:
    return DocstringAIReviewResult(
        status="skipped_unavailable",
        proposals=tuple(proposals),
        rationale=rationale,
        warnings=(rationale,),
        fallback_used=True,
    )
