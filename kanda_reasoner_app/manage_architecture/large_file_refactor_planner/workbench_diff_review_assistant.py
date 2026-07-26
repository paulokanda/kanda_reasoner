"""Assisted review services for Workbench Semantic Diff and Text Diff."""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from kanda_reasoner_app.reasoner_engine.local_ai_chat_service import (
    LocalAIChatError,
    chat_with_local_model,
)

from .planner_local_ai_json_response import parse_local_ai_json_object

__all__ = [
    "DiffReviewAssistantResult",
    "WEB_AI_DIFF_REVIEW_BEGIN",
    "WEB_AI_DIFF_REVIEW_END",
    "build_heuristic_diff_review",
    "build_local_ai_diff_review",
    "build_web_ai_diff_review_prompt",
    "format_assistant_panel_appendix",
    "parse_web_ai_diff_review_response",
]

WEB_AI_DIFF_REVIEW_BEGIN = "KANDA_WORKBENCH_DIFF_REVIEW_BEGIN"
WEB_AI_DIFF_REVIEW_END = "KANDA_WORKBENCH_DIFF_REVIEW_END"
_RESPONSE_SCHEMA_VERSION = "1.0"
_MAX_CONTEXT_DIFF_ROWS = 1600


@dataclass(frozen=True)
class DiffReviewAssistantResult:
    """One bounded review result for both Workbench diff panels."""

    route: str
    status: str
    verdict: str
    semantic_review: str
    text_review: str
    correction_plan: tuple[str, ...]
    warnings: tuple[str, ...]
    model_name: str = ""


def build_heuristic_diff_review(evidence: Any) -> DiffReviewAssistantResult:
    """Build deterministic review observations from immutable completion evidence."""

    semantic = evidence.semantic_review
    text_diff = evidence.text_diff
    blockers = tuple(str(item) for item in getattr(semantic, "blockers", ()) or ())
    warnings = tuple(str(item) for item in getattr(semantic, "warnings", ()) or ())
    public_before = tuple(getattr(semantic, "public_api_before", ()) or ())
    public_after = tuple(getattr(semantic, "public_api_after", ()) or ())
    size_after = tuple(getattr(semantic, "size_after", ()) or ())
    oversize = tuple(
        (str(path), int(lines))
        for path, lines in size_after
        if int(lines) > 500
    )
    movements = tuple(getattr(semantic, "symbol_movements", ()) or ())
    counts = dict(getattr(text_diff, "counts", {}) or {})
    file_count = int(getattr(text_diff, "file_count", 1) or 0)
    file_summaries = tuple(getattr(text_diff, "file_summaries", ()) or ())
    sealed_payload = getattr(evidence, "sealed_payload", None)
    expected_file_count = (
        len(tuple(getattr(sealed_payload, "files", ()) or ()))
        if sealed_payload is not None
        else file_count
    )
    dependency_warnings = tuple(
        item
        for item in warnings
        if "BACK_REFERENCE" in item or "CYCLE" in item or "TOPOLOGY" in item
    )

    semantic_lines = [
        "Deterministic review of immutable Completion Evidence.",
        "Symbol movements: " + str(len(movements)),
        "Public API preserved: " + ("YES" if public_before == public_after else "NO"),
        "Modules above 500 physical lines after split: " + str(len(oversize)),
        "Semantic blockers: " + str(len(blockers)),
        "Semantic warnings: " + str(len(warnings)),
        "Dependency/topology warnings: " + str(len(dependency_warnings)),
        "Text Diff files covered: " + str(file_count) + "/" + str(expected_file_count),
    ]
    if oversize:
        semantic_lines.append(
            "Oversize modules: "
            + ", ".join(path + "=" + str(lines) for path, lines in oversize)
        )
    if blockers:
        semantic_lines.append("Blockers: " + ", ".join(blockers))
    if dependency_warnings:
        semantic_lines.append("Dependency warnings: " + ", ".join(dependency_warnings))

    text_lines = [
        "Deterministic text-diff summary.",
        "Added lines: " + str(int(counts.get("add", 0))),
        "Removed lines: " + str(int(counts.get("remove", 0))),
        "Diff hunks: " + str(int(counts.get("hunk", 0))),
        "Diff status: " + str(getattr(text_diff, "status", "unknown")),
        "Files covered: " + str(file_count),
    ]
    if file_summaries:
        text_lines.append(
            "Covered targets: "
            + ", ".join(str(item.get("target_label", "")) for item in file_summaries)
        )

    correction_plan: list[str] = []
    if public_before != public_after:
        correction_plan.append("Restore public API parity before transaction authorization.")
    if oversize:
        correction_plan.append("Revise split boundaries so every touched code module is <=500 lines.")
    if blockers:
        correction_plan.append("Resolve all deterministic semantic blockers before human review confirmation.")
    if file_count != expected_file_count:
        correction_plan.append("Regenerate Text Diff so every sealed payload file is covered before human review.")
    if dependency_warnings:
        correction_plan.append(
            "Review exact dependency warnings and distinguish runtime import cycles from deferred or TYPE_CHECKING-only back-references."
        )
    if not correction_plan:
        correction_plan.append(
            "No deterministic correction is required by the bounded checks; human semantic review remains mandatory."
        )

    verdict = (
        "needs_correction"
        if blockers or oversize or public_before != public_after or file_count != expected_file_count
        else "review_ready"
    )
    return DiffReviewAssistantResult(
        route="Heuristic",
        status="completed",
        verdict=verdict,
        semantic_review="\n".join(semantic_lines),
        text_review="\n".join(text_lines),
        correction_plan=tuple(correction_plan),
        warnings=warnings,
    )


def build_local_ai_diff_review(
    evidence: Any,
    *,
    model_selection: str = "",
) -> DiffReviewAssistantResult:
    """Ask the shared Local AI service for one schema-bounded diff review."""

    prompt = _review_prompt(_review_context(evidence), external=False)
    messages = [
        {
            "role": "system",
            "content": (
                "You are reviewing immutable KANDA Large File Refactor Workbench evidence. "
                "Do not claim source mutation. Return one JSON object only."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    try:
        raw, model_name = chat_with_local_model(
            messages,
            model_selection=model_selection,
            temperature=0.05,
            max_tokens=3500,
        )
    except LocalAIChatError as exc:
        return DiffReviewAssistantResult(
            route="Local AI",
            status="blocked",
            verdict="unavailable",
            semantic_review="Local AI review could not run: " + str(exc),
            text_review="No Local AI text-diff review was produced.",
            correction_plan=(),
            warnings=("LOCAL_AI_REVIEW_UNAVAILABLE",),
        )

    payload = parse_local_ai_json_object(raw, context="Local AI Workbench diff review")
    result = _result_from_payload(payload, route="Local AI", model_name=model_name)
    return result


def build_web_ai_diff_review_prompt(evidence: Any, active_project_root: str) -> str:
    """Build a clipboard package for external Web AI review and correction advice."""

    context = _review_context(evidence)
    contract = {
        "schema_version": _RESPONSE_SCHEMA_VERSION,
        "verdict": "review_ready_or_needs_correction",
        "semantic_review": "Detailed semantic assessment tied to supplied evidence.",
        "text_review": "Detailed text-diff assessment tied to supplied evidence.",
        "correction_plan": ["Concrete bounded correction step, or no-change justification."],
        "warnings": ["Optional warning code or concern."],
    }
    return "\n".join(
        [
            "KANDA LARGE FILE REFACTOR WORKBENCH DIFF REVIEW PACKAGE",
            "",
            "Active project root: " + str(active_project_root),
            "",
            "Task:",
            "Review the supplied Semantic Diff and Text Diff evidence together.",
            "Find concrete semantic, API, dependency, size, import, or text-level risks.",
            "Do not invent source state and do not claim that project source was changed.",
            "If a correction is needed, describe the smallest bounded correction plan.",
            "If the defect is in KANDA Tool code rather than the selected project refactor, you may additionally provide a governed patch ZIP/install/validate answer separately.",
            "For import into the Workbench Receive From Web AI dialog, return exactly one marker-wrapped JSON object using the contract below.",
            "",
            WEB_AI_DIFF_REVIEW_BEGIN,
            json.dumps(contract, indent=2, ensure_ascii=True),
            WEB_AI_DIFF_REVIEW_END,
            "",
            "REVIEW CONTEXT JSON",
            json.dumps(context, indent=2, ensure_ascii=True),
        ]
    )


def parse_web_ai_diff_review_response(text: str) -> DiffReviewAssistantResult:
    """Parse one exact marker-wrapped Web AI review response."""

    raw = str(text or "")
    if raw.count(WEB_AI_DIFF_REVIEW_BEGIN) != 1 or raw.count(WEB_AI_DIFF_REVIEW_END) != 1:
        raise ValueError("Web AI response must contain exactly one begin marker and one end marker.")
    start = raw.index(WEB_AI_DIFF_REVIEW_BEGIN) + len(WEB_AI_DIFF_REVIEW_BEGIN)
    end = raw.index(WEB_AI_DIFF_REVIEW_END, start)
    payload_text = raw[start:end].strip()
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Web AI diff review JSON is invalid: " + str(exc)) from exc
    if not isinstance(payload, dict):
        raise ValueError("Web AI diff review payload must be a JSON object.")
    return _result_from_payload(payload, route="Web AI", model_name="external")


def format_assistant_panel_appendix(
    result: DiffReviewAssistantResult,
    *,
    panel: str,
) -> str:
    """Format one assistant result for append-only insertion into a review panel."""

    if panel not in {"semantic", "text"}:
        raise ValueError("panel must be semantic or text")
    body = result.semantic_review if panel == "semantic" else result.text_review
    lines = [
        "",
        "--- ASSISTED REVIEW: " + result.route.upper() + " ---",
        "status: " + result.status,
        "verdict: " + result.verdict,
    ]
    if result.model_name:
        lines.append("model: " + result.model_name)
    lines.extend(["", body])
    if result.correction_plan:
        lines.extend(["", "Correction plan:"])
        lines.extend("- " + item for item in result.correction_plan)
    if result.warnings:
        lines.extend(["", "Assistant warnings:"])
        lines.extend("- " + item for item in result.warnings)
    lines.append(
        "Assistant review is advisory. Human review checkboxes and transaction gates remain manual."
    )
    return "\n".join(lines)


def _review_context(evidence: Any) -> dict[str, Any]:
    semantic = evidence.semantic_review
    text_diff = evidence.text_diff
    rows = list(getattr(text_diff, "rows", ()) or ())[:_MAX_CONTEXT_DIFF_ROWS]
    return {
        "contract_id": str(getattr(evidence.contract, "contract_id", "")),
        "contract_hash": str(getattr(semantic, "contract_hash", "")),
        "payload_hash": str(getattr(semantic, "payload_hash", "")),
        "semantic_review": semantic.to_dict(),
        "text_diff": {
            "status": str(getattr(text_diff, "status", "")),
            "source_label": str(getattr(text_diff, "source_label", "")),
            "target_label": str(getattr(text_diff, "target_label", "")),
            "counts": dict(getattr(text_diff, "counts", {}) or {}),
            "file_count": int(getattr(text_diff, "file_count", 1) or 0),
            "file_summaries": list(getattr(text_diff, "file_summaries", ()) or ()),
            "warnings": list(getattr(text_diff, "warnings", ()) or ()),
            "blockers": list(getattr(text_diff, "blockers", ()) or ()),
            "rows": [
                {
                    "kind": str(getattr(row, "kind", "")),
                    "old_lineno": getattr(row, "old_lineno", None),
                    "new_lineno": getattr(row, "new_lineno", None),
                    "text": str(getattr(row, "text", "")),
                }
                for row in rows
            ],
        },
        "dynamic_risks": {
            "status": str(getattr(evidence.dynamic_risks, "status", "")),
            "warnings": list(getattr(evidence.dynamic_risks, "warnings", ()) or ()),
            "blockers": list(getattr(evidence.dynamic_risks, "blockers", ()) or ()),
        },
        "shadow_validation": {
            "status": str(getattr(evidence.shadow_validation, "status", "")),
            "warnings": list(getattr(evidence.shadow_validation, "warnings", ()) or ()),
            "blockers": list(getattr(evidence.shadow_validation, "blockers", ()) or ()),
        },
    }


def _review_prompt(context: dict[str, Any], *, external: bool) -> str:
    schema = {
        "schema_version": _RESPONSE_SCHEMA_VERSION,
        "verdict": "review_ready_or_needs_correction",
        "semantic_review": "string",
        "text_review": "string",
        "correction_plan": ["string"],
        "warnings": ["string"],
    }
    return "\n".join(
        [
            "Review the immutable Workbench Semantic Diff and Text Diff together.",
            "Check API preservation, symbol movement, module sizes, dependency direction, imports, warnings, dynamic risks, and suspicious textual changes.",
            "Return concrete findings. Do not auto-confirm human review and do not claim source mutation.",
            "Return one JSON object matching this schema:",
            json.dumps(schema, indent=2, ensure_ascii=True),
            "Context:",
            json.dumps(context, ensure_ascii=True),
            "External mode: " + ("yes" if external else "no"),
        ]
    )


def _result_from_payload(
    payload: dict[str, Any],
    *,
    route: str,
    model_name: str,
) -> DiffReviewAssistantResult:
    schema_version = str(payload.get("schema_version", ""))
    if schema_version != _RESPONSE_SCHEMA_VERSION:
        raise ValueError("Diff review schema_version must be " + _RESPONSE_SCHEMA_VERSION)
    verdict = str(payload.get("verdict", "")).strip()
    semantic_review = str(payload.get("semantic_review", "")).strip()
    text_review = str(payload.get("text_review", "")).strip()
    correction_plan = payload.get("correction_plan", [])
    warnings = payload.get("warnings", [])
    if not verdict or not semantic_review or not text_review:
        raise ValueError("Diff review response is missing verdict or review text.")
    if not isinstance(correction_plan, list) or not all(isinstance(item, str) for item in correction_plan):
        raise ValueError("correction_plan must be a list of strings.")
    if not isinstance(warnings, list) or not all(isinstance(item, str) for item in warnings):
        raise ValueError("warnings must be a list of strings.")
    return DiffReviewAssistantResult(
        route=route,
        status="completed",
        verdict=verdict,
        semantic_review=semantic_review,
        text_review=text_review,
        correction_plan=tuple(item.strip() for item in correction_plan if item.strip()),
        warnings=tuple(item.strip() for item in warnings if item.strip()),
        model_name=model_name,
    )
