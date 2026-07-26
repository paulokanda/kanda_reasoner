# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_status_projection.py
"""Planner status and normal-mode action projection.

This module keeps GUI enablement projection separate from Planner construction and
analysis logic. It reads existing Planner state, updates existing controls, and
then refreshes the Main Workbench controls through their public GUI contract.
"""

from __future__ import annotations

from .main_workbench_gui import sync_main_workbench_controls
from .planner_action_enablement import build_planner_action_enablement
from .planner_bounded_refinement import plan_allows_ai_architecture_correction
from .planner_version_selector_gui import refresh_planner_version_selector
from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    get_planner_exchange_base_bundle,
    get_planner_version_bundle,
    get_selected_planner_version_bundle,
    selected_planner_version,
)

__all__ = ["refresh_planner_status"]


def refresh_planner_status(window: object) -> None:
    """Synchronize Planner labels, buttons, handoff state, and Main Workbench."""
    analysis = getattr(window, "_large_file_refactor_last_analysis", None)
    heuristic = get_planner_version_bundle(window, PLANNER_VERSION_HEURISTIC)
    selected = get_selected_planner_version_bundle(window)
    exchange_base = get_planner_exchange_base_bundle(window)
    heuristic_plan = heuristic.plan if heuristic is not None else None
    active_plan = selected.plan if selected is not None else None
    heuristic_docs = (
        list(heuristic.docstring_proposals) if heuristic is not None else []
    )
    split_running = bool(
        getattr(window, "_large_file_refactor_split_plan_running", False)
    )
    ai_running = bool(
        getattr(window, "_large_file_refactor_ai_review_running", False)
    )
    ai_result = getattr(window, "_large_file_refactor_plan_ai_review_result", None)
    web_proposal = getattr(window, "_large_file_refactor_web_ai_proposal", None)
    web_applied = bool(
        getattr(window, "_large_file_refactor_web_ai_proposal_applied", False)
    )
    heuristic_status = str(getattr(heuristic_plan, "status", ""))
    active_status = str(getattr(active_plan, "status", ""))
    plan_text = _plan_status_text(
        split_running=split_running,
        plan=heuristic_plan,
        plan_status=heuristic_status,
    )
    llm_text = _local_ai_status_text(
        ai_running=ai_running,
        ai_result=ai_result,
    )
    handoff_text = _handoff_status_text(
        active_plan=active_plan,
        active_status=active_status,
        ai_running=ai_running,
    )
    actions = build_planner_action_enablement(
        has_analysis=analysis is not None,
        has_plan=heuristic_plan is not None,
        plan_status=heuristic_status,
        has_preview=False,
        validation_passed=False,
        payload_status="",
        ai_review_running=(ai_running or split_running),
        has_docstring_plan=bool(heuristic_docs),
        ai_correctable_plan=bool(
            heuristic_plan
            and plan_allows_ai_architecture_correction(heuristic_plan)
        ),
    )
    _set_button_enabled(
        window,
        "_large_file_refactor_plan_button",
        actions.generate_split_plan,
    )
    _set_button_enabled(
        window,
        "_large_file_refactor_docstring_button",
        actions.generate_docstring_plan,
    )
    _set_button_enabled(
        window,
        "_large_file_refactor_llm_button",
        actions.run_llm_arbitration,
    )
    web_ready = bool(
        analysis is not None
        and exchange_base is not None
        and not split_running
        and not ai_running
    )
    _set_button_enabled(
        window,
        "_large_file_refactor_copy_web_ai_button",
        web_ready,
    )
    _set_button_enabled(
        window,
        "_large_file_refactor_view_web_ai_button",
        web_proposal is not None,
    )
    refresh_planner_version_selector(window)
    _render_status_label(
        window=window,
        analysis=analysis,
        plan_text=plan_text,
        heuristic_docs=heuristic_docs,
        llm_text=llm_text,
        selected=selected,
        web_proposal=web_proposal,
        web_applied=web_applied,
        handoff_text=handoff_text,
    )
    sync_main_workbench_controls(window)


def _plan_status_text(*, split_running: bool, plan: object, plan_status: str) -> str:
    if split_running:
        return "generating"
    if plan_status == "blocked":
        return "needs architecture correction"
    if plan is not None:
        return "ok"
    return "not generated"


def _local_ai_status_text(*, ai_running: bool, ai_result: object | None) -> str:
    if ai_running:
        return "reviewing"
    if ai_result is not None:
        return str(getattr(ai_result, "status", "reviewed"))
    return "pending"


def _handoff_status_text(
    *,
    active_plan: object | None,
    active_status: str,
    ai_running: bool,
) -> str:
    if active_plan is not None and active_status != "blocked" and not ai_running:
        return "ready"
    if active_status == "blocked":
        return "blocked"
    return "not ready"


def _render_status_label(
    *,
    window: object,
    analysis: object | None,
    plan_text: str,
    heuristic_docs: list[object],
    llm_text: str,
    selected: object | None,
    web_proposal: object | None,
    web_applied: bool,
    handoff_text: str,
) -> None:
    label = getattr(window, "_large_file_refactor_status_label", None)
    if label is None:
        return
    version_name = selected_planner_version(window).replace("_", " ")
    version_state = "ready" if selected is not None else "unavailable"
    web_text = (
        "none"
        if web_proposal is None
        else "accepted"
        if web_applied
        else "proposal ready"
    )
    label.setText(
        "Analysis: " + ("ok" if analysis is not None else "not run")
        + " | Plan: " + plan_text
        + " | Docstrings: " + ("ok" if heuristic_docs else "not generated")
        + " | Local AI: " + llm_text
        + " | Imported Web AI: " + web_text
        + " | Use version: " + version_name + " (" + version_state + ")"
        + " | Workbench handoff: " + handoff_text
    )


def _set_button_enabled(window: object, attr_name: str, enabled: bool) -> None:
    button = getattr(window, attr_name, None)
    if button is not None:
        button.setEnabled(bool(enabled))
