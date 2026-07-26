# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_staged_protocol.py
"""Staged bounded local-AI architecture correction with targeted retries."""
from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

from kanda_reasoner_app.reasoner_engine.local_ai_chat_service import (
    LocalAIChatError,
    chat_with_local_model,
    get_local_ai_model_candidates,
)

from .models import MIN_HELPER_PHYSICAL_LINES, ModuleAnalysisReport, RefactorPlan
from .planner_ai_architecture_questions import ARCHITECTURE_REVIEW_QUESTIONS
from .planner_bounded_refinement import (
    apply_bounded_architecture_refinement,
    plan_allows_ai_architecture_correction,
)
from .planner_local_ai_json_response import parse_local_ai_json_object
from .planner_local_ai_review_models import PlanAIReviewResult
from .planner_local_ai_staged_prompts import (
    audit_messages,
    naming_messages,
    repair_messages,
    responsibility_messages,
)

__all__ = ["review_plan_with_staged_local_ai"]
_MAX_REPAIR_ATTEMPTS = 4
_MAX_AUDIT_ATTEMPTS = 3
_NAMING_FENCE_PATTERN = re.compile(r"```(?:json)?\s*(.*?)```", flags=re.IGNORECASE | re.DOTALL)


def review_plan_with_staged_local_ai(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    *,
    enabled: bool = True,
    model_selection: str = "",
    max_rounds: int = _MAX_REPAIR_ATTEMPTS,
    candidate_strategy: str = "",
    strategy_instruction: str = "",
    force_exploration: bool = False,
    progress_callback: Callable[[str], None] | None = None,
    interruption_check: Callable[[], None] | None = None,
    include_naming_review: bool = True,
    include_final_audit: bool = True,
    chat_callback: Callable[[list[str], list[dict[str, str]]], tuple[str, str]] | None = None,
) -> PlanAIReviewResult:
    """Run responsibility, repair, naming, and final-audit stages separately."""
    if not enabled:
        return _fallback("skipped_disabled", plan, "Local AI review is disabled.")
    if not plan_allows_ai_architecture_correction(plan):
        return _fallback(
            "blocked_non_correctable",
            plan,
            "Plan contains blockers outside the bounded AI architecture correction contract.",
        )
    try:
        candidates = get_local_ai_model_candidates(model_selection)
    except Exception as exc:
        return _fallback("skipped_unavailable", plan, "Local AI model lookup failed: " + str(exc))
    if not candidates:
        return _fallback("skipped_unavailable", plan, "No local AI model is available.")

    chat_fn = chat_callback or _chat
    progress = progress_callback or (lambda _phase: None)
    interrupt = interruption_check or (lambda: None)

    notes: list[str] = []
    stages: list[tuple[str, str]] = []
    used_model = ""
    current = plan
    action_count = 0
    responsibilities: dict[str, Any] = {}

    try:
        interrupt()
        progress("RESPONSIBILITY_ANALYSIS")
        raw, used_model = chat_fn(candidates, responsibility_messages(report, current))
        responsibilities = _parse_responsibilities(raw, current)
        stages.append(("responsibility_analysis", "validated"))
    except (LocalAIChatError, ValueError, RuntimeError) as exc:
        notes.append("Responsibility analysis failed; deterministic labels preserved: " + str(exc))
        stages.append(("responsibility_analysis", "fallback_deterministic"))
        responsibilities = _deterministic_responsibilities(current)

    attempts = max(1, min(int(max_rounds), _MAX_REPAIR_ATTEMPTS))
    rejection = ""
    repair_calls = 0
    for attempt in range(1, attempts + 1):
        if (
            current.status == "planned"
            and _all_helpers_within_size_gate(current)
            and not rejection
            and not (force_exploration and repair_calls == 0)
        ):
            break
        repair_calls += 1
        try:
            interrupt()
            progress("TARGETED_REPAIR_ATTEMPT_" + str(attempt))
            raw, used_model = chat_fn(
                candidates,
                repair_messages(
                    report,
                    current,
                    responsibilities,
                    rejection,
                    candidate_strategy=candidate_strategy,
                    strategy_instruction=strategy_instruction,
                ),
            )
            repair = _parse_repair_actions(raw)
        except (LocalAIChatError, ValueError, RuntimeError) as exc:
            rejection = "Transport/schema rejection: " + str(exc)
            notes.append("Repair attempt " + str(attempt) + " failed: " + str(exc))
            continue
        if repair["verdict"] == "valid" and current.status == "planned":
            rejection = ""
            break
        actions = len(repair["module_merges"]) + len(repair["reassignments"])
        if actions == 0:
            rejection = "needs_correction returned without any merge or reassignment action"
            notes.append("Repair attempt " + str(attempt) + " returned no bounded action.")
            continue
        try:
            candidate = apply_bounded_architecture_refinement(
                report,
                current,
                reassignments=repair["reassignments"],
                module_merges=repair["module_merges"],
                module_renames=[],
            )
        except ValueError as exc:
            rejection = str(exc)
            notes.append("Targeted repair rejection: " + rejection)
            continue
        current = candidate
        action_count += actions
        rejection = ""
        notes.append(
            "Accepted " + str(actions) + " repair action(s); deterministic status=" + current.status + "."
        )
    stages.append(("targeted_architecture_repair", "validated" if current.status == "planned" else "incomplete"))

    if current.status == "planned" and include_naming_review:
        try:
            interrupt()
            progress("SEMANTIC_NAMING_REVIEW")
            raw, used_model = chat_fn(candidates, naming_messages(report, current, responsibilities))
            renames = _parse_naming_actions(raw)
            if renames:
                current = apply_bounded_architecture_refinement(
                    report,
                    current,
                    reassignments=[],
                    module_merges=[],
                    module_renames=renames,
                )
                action_count += len(renames)
            stages.append(("semantic_naming_review", "validated"))
        except (LocalAIChatError, ValueError, RuntimeError) as exc:
            notes.append("Semantic naming review kept deterministic names: " + str(exc))
            stages.append(("semantic_naming_review", "fallback_deterministic"))
    elif current.status != "planned":
        stages.append(("semantic_naming_review", "skipped_blocked_plan"))
    else:
        stages.append(("semantic_naming_review", "skipped_bounded_correction_lane"))

    answers: dict[str, str] = {}
    audit_rationale = ""
    audit_warnings: list[str] = []
    required_audit_ids = [key for key, _question in ARCHITECTURE_REVIEW_QUESTIONS]
    if include_final_audit:
        for audit_attempt in range(1, _MAX_AUDIT_ATTEMPTS + 1):
            missing = [key for key in required_audit_ids if key not in answers]
            if not missing:
                break
            try:
                interrupt()
                progress("FINAL_ARCHITECTURE_AUDIT_" + str(audit_attempt))
                raw, used_model = chat_fn(
                    candidates,
                    audit_messages(
                        report,
                        current,
                        responsibilities,
                        required_question_ids=missing,
                        accepted_answers=answers,
                    ),
                )
                partial_answers, partial_rationale, partial_warnings = _parse_audit_partial(
                    raw,
                    current,
                    requested_ids=set(missing),
                )
                answers.update(partial_answers)
                if partial_rationale:
                    audit_rationale = partial_rationale
                audit_warnings.extend(partial_warnings)
                remaining = [key for key in required_audit_ids if key not in answers]
                if remaining:
                    notes.append(
                        "Final architecture audit retry requested only missing fields: "
                        + ", ".join(remaining)
                    )
            except (LocalAIChatError, ValueError, RuntimeError) as exc:
                notes.append(
                    "Final architecture audit attempt " + str(audit_attempt) + " incomplete: " + str(exc)
                )
        missing_audit = [key for key in required_audit_ids if key not in answers]
        if missing_audit:
            notes.append(
                "Final architecture audit incomplete after targeted retries. Missing: "
                + ", ".join(missing_audit)
            )
            stages.append(("final_architecture_audit", "incomplete"))
        else:
            stages.append(("final_architecture_audit", "validated"))
    else:
        stages.append(("final_architecture_audit", "skipped_bounded_correction_lane"))

    valid = current.status == "planned" and _all_helpers_within_size_gate(current)
    status = "corrected" if valid and action_count else "validated" if valid else "review_incomplete"
    truthful_rationale = (
        audit_rationale
        if valid and audit_rationale
        else "Local AI corrections were accepted and deterministically revalidated."
        if valid and action_count
        else "No complete Local AI architecture correction passed all deterministic gates."
    )
    return PlanAIReviewResult(
        status=status,
        plan=current,
        model_name=used_model,
        rounds=repair_calls,
        rationale=truthful_rationale,
        warnings=tuple(notes + audit_warnings),
        fallback_used=not valid,
        architecture_answers=tuple(sorted(answers.items())),
        corrections_applied=action_count,
        stage_evidence=tuple(stages),
    )


def _chat(candidates: list[str], messages: list[dict[str, str]]) -> tuple[str, str]:
    errors: list[str] = []
    for model in candidates:
        try:
            return chat_with_local_model(messages, model_selection=model, temperature=0.02, max_tokens=2600)
        except Exception as exc:
            errors.append(model + ": " + str(exc))
    raise LocalAIChatError("No local model completed stage. " + " | ".join(errors))


def _parse_responsibilities(raw: str, plan: RefactorPlan) -> dict[str, Any]:
    payload = parse_local_ai_json_object(raw, context="Local AI responsibility response")
    mapping = payload.get("module_responsibilities", {}) if isinstance(payload, dict) else {}
    if not isinstance(mapping, dict):
        raise ValueError("module_responsibilities must be an object")
    helpers = {m.filename: set(m.symbols) for m in plan.proposed_modules if m.role != "public_facade"}
    result: dict[str, Any] = {}
    for module, value in mapping.items():
        if module not in helpers or not isinstance(value, dict):
            raise ValueError("Responsibility analysis used unknown helper: " + str(module))
        outliers = [str(item) for item in value.get("outliers", [])]
        if any(item not in helpers[module] for item in outliers):
            raise ValueError("Responsibility outlier is outside its helper: " + module)
        primary = str(value.get("primary", "")).strip()
        if not primary:
            raise ValueError("Responsibility primary label cannot be empty: " + module)
        result[module] = {
            "primary": primary,
            "secondary": [str(item) for item in value.get("secondary", [])],
            "outliers": outliers,
        }
    if set(result) != set(helpers):
        raise ValueError("Responsibility analysis must cover every helper")
    return result


def _parse_repair_actions(raw: str) -> dict[str, Any]:
    payload = parse_local_ai_json_object(raw, context="Local AI repair response")
    if not isinstance(payload, dict):
        raise ValueError("Repair response must be an object")
    verdict = str(payload.get("verdict", "")).strip()
    if verdict not in {"valid", "needs_correction"}:
        raise ValueError("Unsupported repair verdict: " + verdict)
    return {
        "verdict": verdict,
        "module_merges": _action_list(payload.get("module_merges", []), "source_module", "target_module"),
        "reassignments": _action_list(payload.get("reassignments", []), "symbol", "target_module"),
    }


def _parse_naming_actions(raw: str) -> list[dict[str, str]]:
    try:
        payload = parse_local_ai_json_object(raw, context="Local AI naming response")
    except ValueError:
        if _is_empty_naming_array(raw):
            return []
        raise
    if not isinstance(payload, dict):
        raise ValueError("Naming response must be an object")
    return _action_list(payload.get("module_renames", []), "module", "new_filename")


def _is_empty_naming_array(raw: Any) -> bool:
    """Accept only an empty JSON array as a stage-specific naming no-op."""
    if isinstance(raw, list):
        return raw == []
    text = str(raw or "").strip()
    candidates = [text]
    candidates.extend(match.strip() for match in _NAMING_FENCE_PATTERN.findall(text))
    for candidate in candidates:
        if not candidate:
            continue
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if parsed == []:
            return True
    return False


def _parse_audit_partial(
    raw: str,
    plan: RefactorPlan,
    *,
    requested_ids: set[str],
) -> tuple[dict[str, str], str, list[str]]:
    payload = parse_local_ai_json_object(raw, context="Local AI audit response")
    if not isinstance(payload, dict):
        raise ValueError("Audit response must be an object")
    answers = payload.get("architecture_answers", {})
    if not isinstance(answers, dict):
        raise ValueError("architecture_answers must be an object")
    normalized = {
        str(k).strip(): str(v).strip()
        for k, v in answers.items()
        if str(k).strip() and str(v).strip() and str(k).strip() in requested_ids
    }
    if not normalized:
        raise ValueError(
            "Audit response answered none of the requested fields: " + ", ".join(sorted(requested_ids))
        )
    final_gate = normalized.get("final_gate", "").lower()
    if plan.status == "blocked" and any(token in final_gate for token in ("pass", "satisf", "valid")):
        raise ValueError("final_gate answer contradicts blocked deterministic plan")
    warnings = payload.get("warnings", [])
    return normalized, str(payload.get("rationale", "")).strip(), [str(item) for item in warnings] if isinstance(warnings, list) else []


def _action_list(value: Any, first: str, second: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError(first + " actions must be a list")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Each action must be an object")
        normalized = {first: str(item.get(first, "")).strip(), second: str(item.get(second, "")).strip()}
        if not normalized[first] or not normalized[second]:
            raise ValueError("Action fields cannot be empty")
        if normalized[first] in seen:
            raise ValueError("Duplicate action identity: " + normalized[first])
        seen.add(normalized[first])
        result.append(normalized)
    return result


def _deterministic_responsibilities(plan: RefactorPlan) -> dict[str, Any]:
    evidence = plan.import_migration if isinstance(plan.import_migration, dict) else {}
    labels = evidence.get("responsibility_labeling", {})
    result: dict[str, Any] = {}
    helpers = [m for m in plan.proposed_modules if m.role != "public_facade"]
    for module in helpers:
        found = next((value for value in labels.values() if isinstance(value, dict) and set(value.get("evidence_tokens", [])) & set(module.symbols)), None)
        result[module.filename] = found or {"primary": module.role, "secondary": [], "outliers": []}
    return result


def _all_helpers_within_size_gate(plan: RefactorPlan) -> bool:
    minimum = max(MIN_HELPER_PHYSICAL_LINES, int(plan.settings.get("minimum_helper_physical_lines", 100)))
    maximum = int(plan.settings.get("maximum_physical_lines", 500))
    return all(minimum <= m.estimated_lines <= maximum for m in plan.proposed_modules if m.role != "public_facade")


def _fallback(status: str, plan: RefactorPlan, rationale: str) -> PlanAIReviewResult:
    return PlanAIReviewResult(status=status, plan=plan, rationale=rationale, warnings=(rationale,), fallback_used=True)
