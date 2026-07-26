"""Shared compute/apply adapters for manual and automatic Workbench stages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .advanced_quality_review_gui import (
    invalidate_advanced_quality_review_gui,
    mark_advanced_quality_review_ready_for_run,
)
from .cst_real_preview_writer import build_and_write_real_preview
from .real_preview_structural_validator import validate_real_preview_structure
from .workbench_dependency_formatting import format_workbench_dependency_readiness
from .workbench_dependency_readiness import build_workbench_dependency_readiness
from .workbench_gui_progression import preview_validation_guidance
from .workbench_real_preview_formatting import format_real_preview_result
from .workbench_snapshot_bridge import materialize_workbench_owned_plan
from .workbench_structural_validation_formatting import (
    format_real_preview_structural_validation,
)
from .workbench_preflight_backup_formatting import format_preflight_gate_reason

__all__ = [
    "DependencyStageRequest",
    "PreviewStageRequest",
    "StructuralStageRequest",
    "apply_dependency_stage_result",
    "apply_preview_stage_result",
    "apply_structural_stage_result",
    "capture_dependency_stage_request",
    "capture_preview_stage_request",
    "capture_structural_stage_request",
    "execute_dependency_stage",
    "execute_preview_stage",
    "execute_structural_stage",
]

SyncCallback = Callable[[object], None]
RootCallback = Callable[[object], str]


@dataclass(frozen=True)
class DependencyStageRequest:
    """Immutable input for read-only dependency readiness computation."""

    intake: Any


@dataclass(frozen=True)
class PreviewStageRequest:
    """Immutable input for Project-support Real Preview generation."""

    plan: Any
    intake: Any
    dependency_readiness: Any
    active_project_root: str


@dataclass(frozen=True)
class StructuralStageRequest:
    """Immutable input for structural validation of one Real Preview."""

    plan: Any
    preview_result: Any
    active_project_root: str


def capture_dependency_stage_request(window: object) -> DependencyStageRequest:
    """Capture current Workbench-owned intake on the GUI thread."""
    intake = getattr(window, "_large_file_refactor_workbench_intake", None)
    if intake is None:
        raise ValueError("MAIN_WORKBENCH_PLAN_INTAKE_MISSING")
    return DependencyStageRequest(intake=intake)


def execute_dependency_stage(request: DependencyStageRequest) -> Any:
    """Compute dependency readiness without touching Qt widgets."""
    return build_workbench_dependency_readiness(request.intake)


def apply_dependency_stage_result(
    window: object,
    result: Any,
    sync_callback: SyncCallback,
) -> None:
    """Apply dependency evidence to the shared Workbench state on the GUI thread."""
    window._large_file_refactor_workbench_dependency_readiness = result
    output = getattr(window, "_large_file_refactor_workbench_dependency_output", None)
    if output is not None:
        output.setPlainText(format_workbench_dependency_readiness(result))
    if bool(getattr(result, "ready_for_real_preview_writer", False)):
        window._large_file_refactor_workbench_state = "DEPENDENCY_READY"
    elif str(getattr(result, "status", "")) == "blocked":
        window._large_file_refactor_workbench_state = "BLOCKED"
    sync_callback(window)


def capture_preview_stage_request(
    window: object,
    root_callback: RootCallback,
) -> PreviewStageRequest:
    """Capture plan, intake, readiness, and Project root before worker execution."""
    invalidate_advanced_quality_review_gui(window, "REAL_PREVIEW_REGENERATED")
    return PreviewStageRequest(
        plan=materialize_workbench_owned_plan(window),
        intake=getattr(window, "_large_file_refactor_workbench_intake", None),
        dependency_readiness=getattr(
            window,
            "_large_file_refactor_workbench_dependency_readiness",
            None,
        ),
        active_project_root=str(root_callback(window)),
    )


def execute_preview_stage(request: PreviewStageRequest) -> Any:
    """Generate Real Preview files under Project Support off the GUI thread."""
    return build_and_write_real_preview(
        plan=request.plan,
        intake=request.intake,
        dependency_readiness=request.dependency_readiness,
        active_project_root=request.active_project_root,
    )


def apply_preview_stage_result(
    window: object,
    result: Any,
    sync_callback: SyncCallback,
) -> None:
    """Apply one Preview result to shared Workbench GUI state."""
    window._large_file_refactor_workbench_real_preview = result
    output = getattr(window, "_large_file_refactor_workbench_real_preview_output", None)
    if output is not None:
        output.setPlainText(format_real_preview_result(result))
    status = str(getattr(result, "status", ""))
    if status == "real_preview_written":
        window._large_file_refactor_workbench_state = "REAL_PREVIEW_READY"
    elif status == "blocked":
        window._large_file_refactor_workbench_state = "BLOCKED"
    validation_output = getattr(
        window,
        "_large_file_refactor_workbench_validation_output",
        None,
    )
    if validation_output is not None:
        validation_output.setPlainText(preview_validation_guidance(result))
    sync_callback(window)


def capture_structural_stage_request(
    window: object,
    root_callback: RootCallback,
) -> StructuralStageRequest:
    """Capture one immutable structural-validation request on the GUI thread."""
    invalidate_advanced_quality_review_gui(window, "STRUCTURAL_VALIDATION_RERUN")
    return StructuralStageRequest(
        plan=materialize_workbench_owned_plan(window),
        preview_result=getattr(
            window,
            "_large_file_refactor_workbench_real_preview",
            None,
        ),
        active_project_root=str(root_callback(window)),
    )


def execute_structural_stage(request: StructuralStageRequest) -> Any:
    """Run structural validation off the GUI thread."""
    return validate_real_preview_structure(
        plan=request.plan,
        preview_result=request.preview_result,
        active_project_root=request.active_project_root,
    )


def apply_structural_stage_result(
    window: object,
    result: Any,
    sync_callback: SyncCallback,
) -> None:
    """Apply structural evidence to shared Workbench state on the GUI thread."""
    window._large_file_refactor_workbench_structural_validation = result
    output = getattr(window, "_large_file_refactor_workbench_validation_output", None)
    if output is not None:
        output.setPlainText(format_real_preview_structural_validation(result))
    preflight_output = getattr(
        window,
        "_large_file_refactor_workbench_preflight_output",
        None,
    )
    status = str(getattr(result, "status", ""))
    if preflight_output is not None:
        preflight_output.setPlainText(format_preflight_gate_reason(status))
    if status.startswith("passed"):
        mark_advanced_quality_review_ready_for_run(window, status)
        window._large_file_refactor_workbench_state = "STRUCTURAL_PREVIEW_VALIDATED"
    elif status == "blocked":
        window._large_file_refactor_workbench_state = "BLOCKED"
    sync_callback(window)
