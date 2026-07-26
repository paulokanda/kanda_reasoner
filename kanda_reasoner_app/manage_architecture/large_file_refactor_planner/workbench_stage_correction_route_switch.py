# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_route_switch.py
"""Coordinate safe switching among reusable Workbench correction routes."""

from __future__ import annotations

from collections.abc import Callable

from .workbench_heuristic_correction_qt_controller import (
    cancel_heuristic_correction,
    heuristic_execution_state,
)
from .workbench_local_ai_correction_qt_controller import (
    cancel_local_ai_correction,
    local_ai_execution_state,
)

__all__ = [
    "abandon_heuristic_before_local_ai",
    "abandon_local_ai_before_heuristic",
    "abandon_workers_before_web_receive",
]

RenderResult = Callable[[object, str, str], None]
SyncCallback = Callable[[object], None]


def abandon_local_ai_before_heuristic(
    window: object,
    render_result: RenderResult,
    sync_callback: SyncCallback,
) -> bool:
    """Abandon an active Local AI result before Heuristic takes ownership."""
    state = local_ai_execution_state(window)
    if not state.waiting:
        return False
    cancel_local_ai_correction(
        window,
        state.active_stage,
        render_result,
        sync_callback,
    )
    return True


def abandon_heuristic_before_local_ai(
    window: object,
    render_result: RenderResult,
    sync_callback: SyncCallback,
) -> bool:
    """Abandon an active Heuristic result before Local AI takes ownership."""
    state = heuristic_execution_state(window)
    if not state.waiting:
        return False
    cancel_heuristic_correction(
        window,
        state.active_stage,
        render_result,
        sync_callback,
    )
    return True


def abandon_workers_before_web_receive(
    window: object,
    render_result: RenderResult,
    sync_callback: SyncCallback,
) -> tuple[bool, bool]:
    """Abandon worker-route authority before imported Web AI replacement intake."""
    heuristic_abandoned = abandon_heuristic_before_local_ai(
        window,
        render_result,
        sync_callback,
    )
    local_abandoned = abandon_local_ai_before_heuristic(
        window,
        render_result,
        sync_callback,
    )
    return heuristic_abandoned, local_abandoned


def _route_switch_contract() -> tuple[str, ...]:
    """Expose stable safety statements for architecture review and documentation."""
    return (
        "CORRECTION_ALTERNATIVES_REUSABLE_WHILE_BLOCKER_CURRENT",
        "ACTIVE_WORKER_RESULT_ABANDONED_BEFORE_ROUTE_SWITCH",
        "LATE_RESULT_DISCARDED_BY_GENERATION_AUTHORITY",
        "WEB_COPY_READ_ONLY_AND_NON_MUTATING",
        "WEB_RECEIVE_ABANDONS_ACTIVE_WORKER_AUTHORITY",
        "NO_DIRECT_GATE_ENABLE_FROM_ROUTE_SWITCH",
        "NO_SOURCE_MUTATION_FROM_ROUTE_SWITCH",
        "ATOMIC_PUBLIC_HANDOFF_REMAINS_REQUIRED",
    )


def route_switch_contract_summary() -> str:
    """Return a compact human-readable statement of route-switch invariants."""
    return " | ".join(_route_switch_contract())


def route_switch_allows_retry_after_timeout() -> bool:
    """Document that timeout does not permanently consume a correction route."""
    return True


def route_switch_allows_retry_after_cancel() -> bool:
    """Document that cancellation does not permanently consume a correction route."""
    return True


def route_switch_requires_current_blocker() -> bool:
    """Document that reusable alternatives still require current correctable evidence."""
    return True
