# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_preimplementation_summary.py
"""Planner-only pre-implementation summary formatting."""

from __future__ import annotations

from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
    get_planner_version_bundle,
    get_selected_planner_version_bundle,
    selected_planner_version,
)

__all__ = ["build_planning_summary"]


def build_planning_summary(window: object) -> str:
    """Return pipeline status plus isolated Heuristic, Local AI, and Imported Web AI versions."""

    analysis = getattr(window, "_large_file_refactor_last_analysis", None)
    selected = get_selected_planner_version_bundle(window)
    ai_running = bool(
        getattr(window, "_large_file_refactor_ai_review_running", False)
    )
    ai_result = getattr(window, "_large_file_refactor_plan_ai_review_result", None)
    web_proposal = getattr(window, "_large_file_refactor_web_ai_proposal", None)
    web_applied = bool(
        getattr(window, "_large_file_refactor_web_ai_proposal_applied", False)
    )
    selected_name = selected_planner_version(window)
    selected_plan = selected.plan if selected is not None else None
    lines = [
        "LARGE FILE REFACTOR PLANNER - PRE-IMPLEMENTATION SUMMARY",
        "Selected target: "
        + str(
            getattr(window, "_large_file_refactor_planner_selected_path", "")
            or "<none>"
        ),
        "Planner state: "
        + str(getattr(window, "_large_file_refactor_planner_state", "IDLE")),
        "Selected version: " + selected_name,
        "Selected version availability: "
        + ("ready" if selected is not None else "unavailable"),
        "",
        "Pipeline:",
        "1. Analysis: " + ("ready" if analysis is not None else "not run"),
        "2. Deterministic split plan: " + _version_status(window, PLANNER_VERSION_HEURISTIC),
        "3. Deterministic docstring plan: " + _docstring_status(window),
        "4. Local AI architecture review: " + _local_status(ai_running, ai_result),
        "5. Imported Web AI version: " + _web_status(web_proposal, web_applied),
        "6. Workbench handoff: "
        + _handoff_status(analysis, selected_plan, ai_running),
        "",
        "Available versions:",
        "- Heuristic: " + _version_status(window, PLANNER_VERSION_HEURISTIC),
        "- Local AI: " + _version_status(window, PLANNER_VERSION_LOCAL_AI),
        "- Imported Web AI Version: " + _version_status(window, PLANNER_VERSION_WEB_AI),
    ]
    if analysis is not None:
        lines.extend(_analysis_lines(analysis))
    if selected_plan is not None:
        lines.extend(_plan_lines(selected_plan))
    lines.extend(
        [
            "",
            "Planner boundary:",
            "- Helpers below 100 lines are hard blockers for the default policy.",
            "- Local AI and imported Web AI versions may contain only bounded architecture corrections.",
            "- AI may merge known helpers, reassign known movable symbols, and rename surviving helpers safely.",
            "- Every AI architecture action is deterministically revalidated for size, atomic clusters, and helper dependency cycles.",
            "- Analysis is deterministic evidence and is never overwritten by AI.",
            "- Version selection never destroys or mutates the other stored versions.",
            "- Workbench receives only the selected active Planner version through its explicit immutable handoff.",
        ]
    )
    return "\n".join(lines)


def _version_status(window: object, version_name: str) -> str:
    bundle = get_planner_version_bundle(window, version_name)
    if bundle is None:
        return "unavailable"
    return str(bundle.plan.status)


def _docstring_status(window: object) -> str:
    bundle = get_planner_version_bundle(window, PLANNER_VERSION_HEURISTIC)
    if bundle is None or not bundle.docstring_proposals:
        return "not generated"
    return str(len(bundle.docstring_proposals)) + " proposals"


def _analysis_lines(analysis: object) -> list[str]:
    symbols = list(getattr(analysis, "symbols", []))
    risks = list(getattr(analysis, "risk_flags", []))
    errors = list(getattr(analysis, "analysis_errors", []))
    return [
        "",
        "Analysis evidence:",
        "- Physical lines: " + str(getattr(analysis, "line_count_physical", 0)),
        "- Top-level symbols: " + str(len(symbols)),
        "- Missing docstrings: "
        + str(getattr(analysis, "missing_docstring_count", 0)),
        "- Risk flags: " + str(len(risks)),
        "- Analysis errors: " + str(len(errors)),
    ]


def _plan_lines(plan: object) -> list[str]:
    modules = list(getattr(plan, "proposed_modules", []))
    blockers = list(getattr(plan, "validation_blockers", []))
    lines = [
        "",
        "Selected version architecture:",
        "- Proposed modules: " + str(len(modules)),
        "- Validation blockers: " + str(len(blockers)),
    ]
    for module in modules:
        lines.append(
            "- "
            + str(getattr(module, "filename", "<unnamed>"))
            + ": "
            + str(getattr(module, "role", "unspecified"))
            + "; "
            + str(len(list(getattr(module, "symbols", []))))
            + " symbols; estimated "
            + str(int(getattr(module, "estimated_lines", 0)))
            + " lines"
        )
    if blockers:
        lines.append("- Blockers: " + ", ".join(str(item) for item in blockers))
    return lines


def _local_status(ai_running: bool, ai_result: object | None) -> str:
    if ai_running:
        return "reviewing"
    if ai_result is None:
        return "not run"
    return str(getattr(ai_result, "status", "reviewed"))


def _web_status(proposal: object | None, applied: bool) -> str:
    if proposal is None:
        return "none"
    status = str(getattr(proposal, "status", "validated"))
    return status + ("; accepted" if applied else "; awaiting acceptance")


def _handoff_status(
    analysis: object | None,
    plan: object | None,
    ai_running: bool,
) -> str:
    if analysis is None or plan is None:
        return "not ready"
    if str(getattr(plan, "status", "")) == "blocked":
        return "blocked"
    if ai_running:
        return "waiting for local AI review"
    return "ready for Workbench intake checks"
