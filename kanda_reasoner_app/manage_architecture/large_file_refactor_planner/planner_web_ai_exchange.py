# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange.py
"""Strict copy/paste planning exchange contract for untrusted Web AI proposals."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import DocstringProposal, ModuleAnalysisReport, RefactorPlan
from .planner_ai_architecture_questions import (
    ARCHITECTURE_REVIEW_QUESTIONS,
    architecture_review_payload,
)
from .planner_bounded_refinement import (
    apply_bounded_architecture_refinement,
    apply_bounded_docstring_updates,
    attach_docstring_proposals_to_plan,
)

__all__ = [
    "WEB_AI_RESPONSE_BEGIN",
    "WEB_AI_RESPONSE_END",
    "WebAIPlanningProposal",
    "build_comprehensive_web_ai_planning_prompt",
    "format_web_ai_proposal",
    "parse_and_validate_web_ai_planning_response",
]

EXCHANGE_FEATURE_ID = "large-file-refactor-planner-web-ai-exchange-v2"
WEB_AI_RESPONSE_BEGIN = "KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN"
WEB_AI_RESPONSE_END = "KANDA_WEB_AI_PLANNING_RESPONSE_END"
_PACKAGE_BEGIN = "KANDA_COMPREHENSIVE_PLANNING_PACKAGE_BEGIN"
_PACKAGE_END = "KANDA_COMPREHENSIVE_PLANNING_PACKAGE_END"


@dataclass(frozen=True)
class WebAIPlanningProposal:
    """Validated but not-yet-accepted external architectural planning proposal."""

    status: str
    source_content_hash: str
    base_plan_hash: str
    response_hash: str
    proposed_plan: RefactorPlan
    proposed_docstrings: tuple[DocstringProposal, ...]
    module_merges_count: int
    reassignments_count: int
    module_renames_count: int
    docstring_updates_count: int
    architecture_answers: tuple[tuple[str, str], ...]
    analysis_observations: tuple[str, ...]
    rationale: str
    warnings: tuple[str, ...]


def build_comprehensive_web_ai_planning_prompt(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
    local_ai_summary: dict[str, Any] | None = None,
    import_contract: dict[str, Any] | None = None,
    base_version_name: str = "",
) -> str:
    """Build selected-file evidence, architecture questions, and strict response map."""

    source_path = Path(report.target_file)
    source_code = source_path.read_text(encoding="utf-8", errors="replace")
    plan_hash = _plan_hash(plan)
    package = {
        "schema_version": "2.0",
        "exchange_feature_id": EXCHANGE_FEATURE_ID,
        "target_name": source_path.name,
        "source_content_hash": report.source_content_hash,
        "base_plan_hash": plan_hash,
        "source_code": source_code,
        "analysis": _scrub_target_paths(
            report.to_dict(), report.target_file, source_path.name
        ),
        "current_plan": _scrub_target_paths(
            plan.to_dict(), report.target_file, source_path.name
        ),
        "docstring_proposals": [
            _scrub_target_paths(
                item.to_dict(), report.target_file, source_path.name
            )
            for item in proposals
        ],
        "local_ai_review": local_ai_summary or {},
        "base_version_name": base_version_name,
        "architecture_review": architecture_review_payload(plan),
        "imported_web_ai_version_install_contract": import_contract or {},
        "known_helper_modules": [
            module.filename
            for module in plan.proposed_modules
            if module.role != "public_facade"
        ],
        "known_movable_symbols": sorted(
            symbol
            for module in plan.proposed_modules
            if module.role != "public_facade"
            for symbol in module.symbols
        ),
        "improvement_objective": {
            "rule": "Do not merely reproduce the native plan; search for bounded improvement, but return no changes when no defensible improvement exists.",
            "prefer": [
                "higher responsibility cohesion",
                "lower mixed-responsibility concentration",
                "better helper size balance without micro-files",
                "lower avoidable facade back-reference pressure",
                "semantic names for surviving known helpers",
            ],
            "never_override": [
                "public facade ownership",
                "atomic clusters",
                "helper cycle blockers",
                "minimum and maximum helper size gates",
                "source_content_hash and base_plan_hash identity",
            ],
        },
    }
    response_template = {
        "schema_version": "2.0",
        "exchange_feature_id": EXCHANGE_FEATURE_ID,
        "source_content_hash": report.source_content_hash,
        "base_plan_hash": plan_hash,
        "verdict": "valid_or_refine",
        "module_merges": [
            {
                "source_module": "KNOWN_HELPER.py",
                "target_module": "KNOWN_HELPER.py",
            }
        ],
        "reassignments": [
            {"symbol": "KNOWN_SYMBOL", "target_module": "KNOWN_HELPER.py"}
        ],
        "module_renames": [
            {
                "module": "KNOWN_SURVIVING_HELPER.py",
                "new_filename": "_semantic_private_name.py",
            }
        ],
        "docstring_updates": [
            {
                "target_kind": "KNOWN_KIND",
                "target_name": "KNOWN_TARGET",
                "proposed_docstring": '\"\"\"Improved bounded proposal.\"\"\"',
            }
        ],
        "architecture_answers": {
            question_id: "Answer this question from the supplied evidence."
            for question_id, _question in ARCHITECTURE_REVIEW_QUESTIONS
        },
        "analysis_observations": [
            "Read-only observation; does not replace deterministic AST evidence."
        ],
        "rationale": "Explain why the bounded architecture is better and safer.",
        "warnings": ["Any unresolved planning concern."],
    }
    instructions = [
        "You are the architecture corrector for a pre-implementation Python large-file refactor plan.",
        "Create an installable ZIP containing INSTALL.ps1 and one payload file whose contents are exactly the required marker-wrapped JSON response block.",
        "Follow imported_web_ai_version_install_contract exactly; the installer writes only the external pending import artifact and must not patch KANDA Python source.",
        "Also provide beginner-safe PowerShell install code for the returned ZIP.",
        "After the ZIP instructions, repeat the exact complete marker-wrapped KANDA_WEB_AI_PLANNING_RESPONSE block in chat so the human can copy it and paste it directly into Panel 4: Proposed split plan as the fallback path.",
        "Do not merely reproduce the native plan. First search for a bounded, evidence-backed improvement; if none is defensible, return a truthful no-change response.",
        "Prefer small corrections such as one outlier-symbol reassignment, one compatible known-helper merge, or one semantic rename over an unnecessary full redesign.",
        "Compare the proposed result against responsibility cohesion, mixed-responsibility concentration, helper size balance, topology, facade back-reference pressure, atomic clusters, and supplied Git-history confidence.",
        "Treat sparse Git history according to its supplied confidence weight; raw co-change similarity alone is not authority.",
        "Do real architectural work when evidence shows tiny helpers, fragmentation, weak cohesion, generic helper names, mixed-responsibility concentration, or unsafe dependency structure.",
        "Answer every architecture_review question before declaring the plan valid.",
        "Helpers below minimum_helper_physical_lines are hard blockers and must be corrected, never merely justified.",
        "You may merge only known helper modules into known helper modules.",
        "You may reassign only known movable symbols to known helper modules.",
        "You may semantically rename only surviving known helpers; a rename must be one private underscore-prefixed .py basename.",
        "Do not create additional modules, invent symbols, edit imports directly, write source code, or change public-facade ownership.",
        "Do not split atomic clusters or introduce circular helper dependencies.",
        "Docstring updates may target only entries already present in docstring_proposals.",
        "Every proposed_docstring must be wrapped in triple double quotes.",
        "analysis_observations are advisory only and cannot replace deterministic AST analysis.",
        "The response will be rejected unless source_content_hash and base_plan_hash still match.",
        "The preferred governed ZIP contains INSTALL.ps1, VALIDATE.ps1, FREEZE.ps1, KANDA_FREEZE_HINT.json, bundle_manifest.json, and the payload artifact.",
        "INSTALL.ps1 writes only the external pending imported-plan artifact. VALIDATE.ps1 checks markers, JSON identity, hashes, architecture-answer completeness, and installed-copy equality. FREEZE.ps1 merges evidence only after review; canonical freeze still requires Preview and Confirm and Write.",
        "In PowerShell, never count literal markers with String.Split(markerString); use Regex.Matches with Regex.Escape for exact complete-marker counts.",
        "Use empty lists when no action of a given type is recommended.",
    ]
    return "\n".join(
        [
            "LARGE FILE REFACTOR PLANNER - COMPREHENSIVE WEB AI EXCHANGE",
            "",
            "INSTRUCTIONS TO WEB AI:",
            *["- " + item for item in instructions],
            "",
            _PACKAGE_BEGIN,
            json.dumps(package, indent=2, ensure_ascii=True),
            _PACKAGE_END,
            "",
            "REQUIRED PAYLOAD ARTIFACT CONTENT:",
            WEB_AI_RESPONSE_BEGIN,
            json.dumps(response_template, indent=2, ensure_ascii=True),
            WEB_AI_RESPONSE_END,
        ]
    )


def parse_and_validate_web_ai_planning_response(
    raw_text: str,
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> WebAIPlanningProposal:
    """Validate Web AI architecture actions and build a non-active proposal."""

    payload_text = _extract_marker_payload(raw_text)
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Web AI response JSON is invalid: " + str(exc)) from exc
    if not isinstance(payload, dict):
        raise ValueError("Web AI response must be one JSON object.")
    _validate_identity(payload, report, plan)
    module_merges = _normalize_action_list(
        payload.get("module_merges", []),
        ("source_module", "target_module"),
    )
    reassignments = _normalize_action_list(
        payload.get("reassignments", []),
        ("symbol", "target_module"),
    )
    module_renames = _normalize_action_list(
        payload.get("module_renames", []),
        ("module", "new_filename"),
    )
    doc_updates = _normalize_docstring_updates(
        payload.get("docstring_updates", [])
    )
    architecture_answers = _normalize_architecture_answers(
        payload.get("architecture_answers", {})
    )
    proposed_plan = apply_bounded_architecture_refinement(
        report,
        plan,
        reassignments=reassignments,
        module_merges=module_merges,
        module_renames=module_renames,
    )
    proposed_docs = apply_bounded_docstring_updates(
        proposals,
        doc_updates,
        provenance="web_ai_drafted",
    )
    proposed_plan = attach_docstring_proposals_to_plan(
        proposed_plan, proposed_docs
    )
    observations = _string_list(payload.get("analysis_observations", []))
    warnings = _string_list(payload.get("warnings", []))
    response_hash = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()
    action_count = (
        len(module_merges)
        + len(reassignments)
        + len(module_renames)
        + len(doc_updates)
    )
    status = "validated_no_changes" if action_count == 0 else "validated_proposal"
    return WebAIPlanningProposal(
        status=status,
        source_content_hash=report.source_content_hash,
        base_plan_hash=_plan_hash(plan),
        response_hash=response_hash,
        proposed_plan=proposed_plan,
        proposed_docstrings=tuple(proposed_docs),
        module_merges_count=len(module_merges),
        reassignments_count=len(reassignments),
        module_renames_count=len(module_renames),
        docstring_updates_count=len(doc_updates),
        architecture_answers=tuple(sorted(architecture_answers.items())),
        analysis_observations=tuple(observations),
        rationale=str(payload.get("rationale", "")).strip(),
        warnings=tuple(warnings),
    )


def format_web_ai_proposal(proposal: WebAIPlanningProposal) -> str:
    """Return a review surface for one validated external architecture proposal."""

    lines = [
        "WEB AI PLANNING PROPOSAL",
        "Status: " + proposal.status,
        "Response hash: " + proposal.response_hash,
        "Module merges: " + str(proposal.module_merges_count),
        "Symbol reassignments: " + str(proposal.reassignments_count),
        "Module renames: " + str(proposal.module_renames_count),
        "Docstring updates: " + str(proposal.docstring_updates_count),
        "Resulting plan status: " + proposal.proposed_plan.status,
        "Rationale: " + (proposal.rationale or "No rationale supplied."),
        "",
        "Architecture question answers:",
    ]
    if proposal.architecture_answers:
        lines.extend(
            "- " + key + ": " + value
            for key, value in proposal.architecture_answers
        )
    else:
        lines.append("- none")
    lines.extend(["", "Analysis observations (advisory only):"])
    if proposal.analysis_observations:
        lines.extend("- " + item for item in proposal.analysis_observations)
    else:
        lines.append("- none")
    lines.append("")
    lines.append("Warnings:")
    if proposal.warnings:
        lines.extend("- " + item for item in proposal.warnings)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Acceptance boundary:",
            "- This proposal is validated but not active until Accept is clicked.",
            "- Deterministic AST analysis is never overwritten by Web AI.",
            "- Architecture actions are bounded and deterministically revalidated.",
            "- No source or Workbench file is written by this exchange.",
        ]
    )
    return "\n".join(lines)


def _validate_identity(
    payload: dict[str, Any],
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
) -> None:
    if str(payload.get("schema_version", "")) != "2.0":
        raise ValueError("Unsupported Web AI response schema_version.")
    if str(payload.get("exchange_feature_id", "")) != EXCHANGE_FEATURE_ID:
        raise ValueError("Unsupported Web AI exchange feature_id.")
    if str(payload.get("source_content_hash", "")) != report.source_content_hash:
        raise ValueError("STALE_WEB_AI_RESPONSE_SOURCE_HASH")
    if str(payload.get("base_plan_hash", "")) != _plan_hash(plan):
        raise ValueError("STALE_WEB_AI_RESPONSE_BASE_PLAN_HASH")
    verdict = str(payload.get("verdict", "")).strip()
    if verdict not in {"valid", "refine", "valid_or_refine"}:
        raise ValueError("Unsupported Web AI verdict: " + verdict)


def _normalize_action_list(
    value: Any,
    required_keys: tuple[str, str],
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError(required_keys[0] + " actions must be a list.")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Each architecture action must be a JSON object.")
        normalized = {
            key: str(item.get(key, "")).strip() for key in required_keys
        }
        if not all(normalized.values()):
            raise ValueError("Architecture action fields cannot be empty.")
        identity = normalized[required_keys[0]]
        if identity in seen:
            raise ValueError("Duplicate architecture action: " + identity)
        seen.add(identity)
        result.append(normalized)
    return result


def _normalize_docstring_updates(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError("docstring_updates must be a list.")
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Each docstring update must be a JSON object.")
        normalized = {
            "target_kind": str(item.get("target_kind", "")).strip(),
            "target_name": str(item.get("target_name", "")).strip(),
            "proposed_docstring": str(item.get("proposed_docstring", "")).strip(),
        }
        key = (normalized["target_kind"], normalized["target_name"])
        if key in seen:
            raise ValueError("Duplicate docstring update target: " + ":".join(key))
        seen.add(key)
        result.append(normalized)
    return result


def _normalize_architecture_answers(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("architecture_answers must be a JSON object.")
    result = {
        str(key).strip(): str(answer).strip()
        for key, answer in value.items()
        if str(key).strip() and str(answer).strip()
    }
    required = {question_id for question_id, _ in ARCHITECTURE_REVIEW_QUESTIONS}
    if not required.issubset(result):
        raise ValueError(
            "Web AI must answer every architecture question: "
            + ", ".join(sorted(required - set(result)))
        )
    return result


def _extract_marker_payload(raw_text: str) -> str:
    begin_count = raw_text.count(WEB_AI_RESPONSE_BEGIN)
    end_count = raw_text.count(WEB_AI_RESPONSE_END)
    if begin_count != 1 or end_count != 1:
        raise ValueError("Web AI response must contain exactly one response block.")
    before, remainder = raw_text.split(WEB_AI_RESPONSE_BEGIN, 1)
    body, after = remainder.split(WEB_AI_RESPONSE_END, 1)
    if before.strip() or after.strip():
        raise ValueError("Return only the marker-wrapped Web AI response block.")
    return body.strip()


def _scrub_target_paths(value: Any, absolute_path: str, safe_name: str) -> Any:
    """Replace selected local absolute path strings before clipboard export."""

    if isinstance(value, dict):
        return {
            key: _scrub_target_paths(item, absolute_path, safe_name)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [
            _scrub_target_paths(item, absolute_path, safe_name)
            for item in value
        ]
    if isinstance(value, str) and value == absolute_path:
        return safe_name
    return value


def _plan_hash(plan: RefactorPlan) -> str:
    canonical = json.dumps(
        plan.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise ValueError("Expected a list of strings.")
    return [str(item).strip() for item in value if str(item).strip()]
