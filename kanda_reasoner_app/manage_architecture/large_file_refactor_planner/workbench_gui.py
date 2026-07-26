"""Qt shell for the Architecture Review Large File Refactor Workbench."""
from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from .advanced_quality_review_gui import (
    build_advanced_quality_review_section,
    invalidate_advanced_quality_review_gui,
    sync_advanced_quality_review_controls,
)
from .workbench_formatting import format_workbench_intake
from .workbench_preflight_backup_formatting import format_preflight_backup_readiness
from .workbench_preflight_backup_readiness import build_and_write_preflight_backup_readiness
from .workbench_source_payload_builder import build_and_write_source_apply_payload
from .workbench_source_payload_formatting import format_source_apply_payload_readiness
from .workbench_completion_gui import build_workbench_completion_section
from .main_workbench_stage_adapters import (
    apply_dependency_stage_result,
    apply_preview_stage_result,
    apply_structural_stage_result,
    capture_dependency_stage_request,
    capture_preview_stage_request,
    capture_structural_stage_request,
    execute_dependency_stage,
    execute_preview_stage,
    execute_structural_stage,
)
from .workbench_external_source_stale_gui import (
    sync_completion_external_source_stale_state,
)
from .workbench_diff_review_assistant_gui import sync_diff_review_assistant_controls
from .workbench_gui_progression import build_workbench_gui_progression
from .workbench_stage_correction_gui import (
    build_workbench_stage_correction_row,
    sync_workbench_stage_correction_controls,
)
from .workbench_gui_layout import (
    build_scrollable_workbench_content,
    compact_workbench_text_outputs,
)
from .workbench_page_code_gui import build_workbench_page_code_button
from .workbench_plan_intake import WorkbenchPlanIntakeResult
from .workbench_snapshot_bridge import (
    load_latest_snapshot_into_workbench,
    materialize_workbench_owned_plan,
    recheck_owned_snapshot_intake,
)
__all__ = [
    "build_large_file_refactor_workbench_page",
    "recheck_workbench_pipeline_source",
    "run_workbench_dependency_stage",
    "run_workbench_plan_intake_stage",
    "run_workbench_preview_stage",
    "run_workbench_structural_stage",
    "sync_workbench_controls",
]
def build_large_file_refactor_workbench_page(window: object) -> QWidget:
    """Build the guarded Workbench shell that consumes Planner output."""
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    _initialize_workbench_state(window)
    layout.addWidget(build_workbench_page_code_button(window))
    scroll_area, content, content_layout = build_scrollable_workbench_content()
    content_layout.addWidget(_build_intake_section(window))
    content_layout.addWidget(_build_dependency_section(window))
    content_layout.addWidget(_build_preview_section(window))
    content_layout.addWidget(_build_validation_section(window))
    content_layout.addWidget(
        build_advanced_quality_review_section(
            window,
            root_text_callback=_root_text,
            sync_callback=_sync_workbench_buttons,
        )
    )
    content_layout.addWidget(_build_apply_section(window))
    content_layout.addWidget(build_workbench_completion_section(window, _root_text))
    content_layout.addStretch(1)
    compact_workbench_text_outputs(content)
    window._large_file_refactor_workbench_scroll_area = scroll_area
    window._large_file_refactor_workbench_content_widget = content
    layout.addWidget(scroll_area, 1)
    return page
def _initialize_workbench_state(window: object) -> None:
    """Install Workbench state without touching Planner state."""
    window._large_file_refactor_workbench_state = "IDLE"
    window._large_file_refactor_workbench_plan_snapshot = None
    window._large_file_refactor_workbench_intake = None
    window._large_file_refactor_workbench_dependency_readiness = None
    window._large_file_refactor_workbench_real_preview = None
    window._large_file_refactor_workbench_structural_validation = None
    window._large_file_refactor_workbench_advanced_quality_review = None
    window._large_file_refactor_workbench_aqr_identity_hash = ""
    window._large_file_refactor_workbench_aqr_context = None
    window._large_file_refactor_workbench_preflight_backup = None
    window._large_file_refactor_workbench_source_payload = None
    window._large_file_refactor_workbench_guarded_apply = None
    window._large_file_refactor_workbench_post_apply_validation = None
    window._large_file_refactor_workbench_rollback = None
def _build_intake_section(window: object) -> QGroupBox:
    """Create Plan Intake controls."""
    box = QGroupBox("1. Plan Intake from Large File Refactor Planner")
    layout = QVBoxLayout(box)
    row = QHBoxLayout()
    load_btn = QPushButton("Load Latest Planner Plan")
    load_btn.clicked.connect(lambda: _load_latest_planner_plan(window))
    row.addWidget(load_btn)
    recheck_btn = QPushButton("Recheck Source Hash")
    recheck_btn.clicked.connect(lambda: _recheck_source_hash(window))
    row.addWidget(recheck_btn)
    row.addStretch(1)
    layout.addLayout(row)
    window._large_file_refactor_workbench_intake_output = QPlainTextEdit()
    window._large_file_refactor_workbench_intake_output.setReadOnly(True)
    window._large_file_refactor_workbench_intake_output.setPlainText(
        "No Planner plan loaded. Generate a split plan in Large File "
        "Refactor Planner, then load it here. This Workbench train is "
        "intake-only and cannot write source files."
    )
    layout.addWidget(window._large_file_refactor_workbench_intake_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "PLAN_INTAKE", _root_text, _sync_workbench_buttons))
    return box
def _build_dependency_section(window: object) -> QGroupBox:
    """Create read-only dependency readiness controls."""
    box = QGroupBox("2. Dependency and Scope Readiness")
    layout = QVBoxLayout(box)
    row = QHBoxLayout()
    analyze_btn = QPushButton("Analyze Dependency Readiness")
    analyze_btn.setEnabled(False)
    analyze_btn.clicked.connect(lambda: _analyze_dependency_readiness(window))
    window._large_file_refactor_workbench_dependency_button = analyze_btn
    row.addWidget(analyze_btn)
    row.addStretch(1)
    layout.addLayout(row)
    window._large_file_refactor_workbench_dependency_output = QPlainTextEdit()
    window._large_file_refactor_workbench_dependency_output.setReadOnly(True)
    window._large_file_refactor_workbench_dependency_output.setPlainText(
        "Load a Planner plan first. Dependency readiness is read-only and "
        "will not move code or write source files."
    )
    layout.addWidget(window._large_file_refactor_workbench_dependency_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "DEPENDENCY_READINESS", _root_text, _sync_workbench_buttons))
    return box
def _build_preview_section(window: object) -> QGroupBox:
    """Create real preview generation controls."""
    box = QGroupBox("3. Real Moved-Code Preview Generation")
    layout = QVBoxLayout(box)
    label = QLabel(
        "Generate real facade/helper preview files under selected project support only. "
        "This does not write project source and does not enable apply."
    )
    layout.addWidget(label)
    preview_btn = QPushButton("Generate Real Preview")
    preview_btn.setEnabled(False)
    preview_btn.clicked.connect(lambda: _generate_real_preview(window))
    window._large_file_refactor_workbench_real_preview_button = preview_btn
    layout.addWidget(preview_btn)
    window._large_file_refactor_workbench_real_preview_output = QPlainTextEdit()
    window._large_file_refactor_workbench_real_preview_output.setReadOnly(True)
    window._large_file_refactor_workbench_real_preview_output.setPlainText(
        "Run Dependency Readiness first. Real preview writes only governed "
        "project-support artifacts and never writes active project source."
    )
    layout.addWidget(window._large_file_refactor_workbench_real_preview_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "REAL_PREVIEW", _root_text, _sync_workbench_buttons))
    return box
def _build_validation_section(window: object) -> QGroupBox:
    """Create structural validation placeholder controls."""
    box = QGroupBox("4. Structural Validation")
    layout = QVBoxLayout(box)
    label = QLabel(
        "Validation will distinguish STRUCTURAL PASS from "
        "BEHAVIOR-VALIDATED PASS. No behavior equivalence claim is made here."
    )
    layout.addWidget(label)
    validate_btn = QPushButton("Validate Real Preview")
    validate_btn.setEnabled(False)
    validate_btn.clicked.connect(lambda: _validate_real_preview(window))
    window._large_file_refactor_workbench_validate_button = validate_btn
    layout.addWidget(validate_btn)
    window._large_file_refactor_workbench_validation_output = QPlainTextEdit()
    window._large_file_refactor_workbench_validation_output.setReadOnly(True)
    window._large_file_refactor_workbench_validation_output.setPlainText(
        "Generate Real Preview first. Validation writes only daily-work "
        "validation reports and import migration preview evidence."
    )
    layout.addWidget(window._large_file_refactor_workbench_validation_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "STRUCTURAL_VALIDATION", _root_text, _sync_workbench_buttons))
    return box
def _build_apply_section(window: object) -> QGroupBox:
    """Create preflight backup and guarded apply placeholder controls."""
    box = QGroupBox("6. Preflight Backup and Source Payload")
    layout = QVBoxLayout(box)
    label = QLabel(
        "Validate Preview, prepare durable backup readiness, then build the exact "
        "source payload used by Completion Evidence and the journaled transaction path."
    )
    layout.addWidget(label)
    preflight_btn = QPushButton("Prepare Preflight Backup Readiness")
    preflight_btn.setEnabled(False)
    preflight_btn.clicked.connect(lambda: _prepare_preflight_backup(window))
    window._large_file_refactor_workbench_preflight_button = preflight_btn
    layout.addWidget(preflight_btn)
    window._large_file_refactor_workbench_preflight_output = QPlainTextEdit()
    window._large_file_refactor_workbench_preflight_output.setReadOnly(True)
    window._large_file_refactor_workbench_preflight_output.setPlainText(
        "Run Advanced Quality Review after Structural Validation first. Preflight backup readiness writes only "
        "project-support recovery evidence and never applies source changes."
    )
    layout.addWidget(window._large_file_refactor_workbench_preflight_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "PREFLIGHT_BACKUP", _root_text, _sync_workbench_buttons))
    payload_btn = QPushButton("Build Source Apply Payload")
    payload_btn.setEnabled(False)
    payload_btn.clicked.connect(lambda: _build_source_apply_payload(window))
    window._large_file_refactor_workbench_source_payload_button = payload_btn
    layout.addWidget(payload_btn)
    window._large_file_refactor_workbench_source_payload_output = QPlainTextEdit()
    window._large_file_refactor_workbench_source_payload_output.setReadOnly(True)
    window._large_file_refactor_workbench_source_payload_output.setPlainText(
        "Prepare Preflight Backup Readiness first. This builds source-ready "
        "project-support payload files but still does not apply source changes."
    )
    layout.addWidget(window._large_file_refactor_workbench_source_payload_output, 1)
    layout.addWidget(build_workbench_stage_correction_row(window, "SOURCE_PAYLOAD", _root_text, _sync_workbench_buttons))
    layout.addWidget(
        QLabel(
            "Next governed stage: Completion Review and Refactor Authorization. "
            "Legacy direct apply and rollback controls are not part of this workflow."
        )
    )
    return box
def _load_latest_planner_plan(window: object) -> None:
    """Capture once through public handoff and transfer Workbench ownership."""
    result, message = load_latest_snapshot_into_workbench(
        window, _root_text(window)
    )
    if result is not None:
        _store_and_render_intake(window, result)
    if message:
        window._large_file_refactor_workbench_intake_output.setPlainText(message)
def _recheck_source_hash(window: object) -> None:
    """Recheck owned snapshot freshness without auto-loading Planner."""
    result = recheck_owned_snapshot_intake(window)
    if result is None:
        window._large_file_refactor_workbench_intake_output.setPlainText(
            "Load Latest Planner Plan first. Recheck does not auto-load Planner."
        )
        return
    _store_and_render_intake(window, result)
def _analyze_dependency_readiness(window: object) -> None:
    """Run shared dependency computation and apply its result on the GUI thread."""
    try:
        request = capture_dependency_stage_request(window)
    except ValueError:
        window._large_file_refactor_workbench_dependency_output.setPlainText(
            "Load Latest Planner Plan first. No automatic Planner reach-back."
        )
        return
    result = execute_dependency_stage(request)
    apply_dependency_stage_result(window, result, _sync_workbench_buttons)
def _generate_real_preview(window: object) -> None:
    """Run shared Preview compute/apply behavior for the detailed Workbench."""
    request = capture_preview_stage_request(window, _root_text)
    result = execute_preview_stage(request)
    apply_preview_stage_result(window, result, _sync_workbench_buttons)
def _validate_real_preview(window: object) -> None:
    """Run shared structural compute/apply behavior for the detailed Workbench."""
    request = capture_structural_stage_request(window, _root_text)
    result = execute_structural_stage(request)
    apply_structural_stage_result(window, result, _sync_workbench_buttons)
def _prepare_preflight_backup(window: object) -> None:
    """Create preflight backup readiness evidence under selected project support only."""
    plan = materialize_workbench_owned_plan(window)
    preview = getattr(window, "_large_file_refactor_workbench_real_preview", None)
    structural = getattr(window, "_large_file_refactor_workbench_structural_validation", None)
    result = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=_root_text(window),
    )
    window._large_file_refactor_workbench_preflight_backup = result
    if hasattr(window, "_large_file_refactor_workbench_preflight_output"):
        window._large_file_refactor_workbench_preflight_output.setPlainText(
            format_preflight_backup_readiness(result)
        )
    if result.status == "preflight_backup_ready":
        window._large_file_refactor_workbench_state = "PREFLIGHT_BACKUP_READY"
    elif result.status == "blocked":
        window._large_file_refactor_workbench_state = "BLOCKED"
    _sync_workbench_buttons(window)
def _build_source_apply_payload(window: object) -> None:
    """Build source-ready payload files under selected project support without applying them."""
    plan = materialize_workbench_owned_plan(window)
    preview = getattr(window, "_large_file_refactor_workbench_real_preview", None)
    structural = getattr(window, "_large_file_refactor_workbench_structural_validation", None)
    preflight = getattr(window, "_large_file_refactor_workbench_preflight_backup", None)
    result = build_and_write_source_apply_payload(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        preflight_backup=preflight,
        active_project_root=_root_text(window),
    )
    window._large_file_refactor_workbench_source_payload = result
    if hasattr(window, "_large_file_refactor_workbench_source_payload_output"):
        window._large_file_refactor_workbench_source_payload_output.setPlainText(
            format_source_apply_payload_readiness(result)
        )
    if result.status == "source_apply_payload_ready":
        window._large_file_refactor_workbench_state = "SOURCE_APPLY_PAYLOAD_READY"
    elif result.status == "blocked":
        window._large_file_refactor_workbench_state = "BLOCKED"
    _sync_workbench_buttons(window)
def _store_and_render_intake(
    window: object,
    result: WorkbenchPlanIntakeResult,
) -> None:
    """Store Workbench intake result and refresh controls."""
    invalidate_advanced_quality_review_gui(window, "PROJECT_CARD_OR_INTAKE_CHANGED")
    window._large_file_refactor_workbench_intake = result
    window._large_file_refactor_workbench_state = (
        "READY_FOR_REAL_PREVIEW" if result.ready_for_real_preview else "BLOCKED"
    )
    window._large_file_refactor_workbench_intake_output.setPlainText(
        format_workbench_intake(result)
    )
    _sync_workbench_buttons(window)
def _sync_workbench_buttons(window: object) -> None:
    """Project all sequential button states from one fail-closed progression model."""
    progression = build_workbench_gui_progression(
        intake=getattr(window, "_large_file_refactor_workbench_intake", None),
        dependency_readiness=getattr(window, "_large_file_refactor_workbench_dependency_readiness", None),
        preview=getattr(window, "_large_file_refactor_workbench_real_preview", None),
        structural_validation=getattr(window, "_large_file_refactor_workbench_structural_validation", None),
        advanced_quality_review=getattr(window, "_large_file_refactor_workbench_advanced_quality_review", None),
        preflight=getattr(window, "_large_file_refactor_workbench_preflight_backup", None),
        source_payload=getattr(window, "_large_file_refactor_workbench_source_payload", None),
        completion_evidence=getattr(window, "_large_file_refactor_workbench_completion_evidence", None),
        completion_transaction=getattr(window, "_large_file_refactor_workbench_completion_transaction", None),
        completion_outcome=getattr(window, "_large_file_refactor_workbench_completion_apply_outcome", None),
    )
    controls = (
        ("_large_file_refactor_workbench_dependency_button", progression.dependency_analysis_enabled),
        ("_large_file_refactor_workbench_real_preview_button", progression.real_preview_enabled),
        ("_large_file_refactor_workbench_validate_button", progression.structural_validation_enabled),
        ("_large_file_refactor_workbench_preflight_button", progression.preflight_enabled),
        ("_large_file_refactor_workbench_source_payload_button", progression.source_payload_enabled),
        ("_large_file_refactor_workbench_completion_prepare_button", progression.completion_evidence_enabled),
    )
    for attribute, enabled in controls:
        widget = getattr(window, attribute, None)
        if widget is not None:
            widget.setEnabled(enabled)
    sync_advanced_quality_review_controls(window, progression)
    sync_diff_review_assistant_controls(window)
    sync_workbench_stage_correction_controls(window, _root_text)
    sync_completion_external_source_stale_state(window)


def run_workbench_plan_intake_stage(window: object):
    """Run the existing explicit Planner handoff and return owned intake state."""
    _load_latest_planner_plan(window)
    return getattr(window, "_large_file_refactor_workbench_intake", None)


def recheck_workbench_pipeline_source(window: object):
    """Recheck current Workbench-owned card freshness without Planner reach-back."""
    _recheck_source_hash(window)
    return getattr(window, "_large_file_refactor_workbench_intake", None)


def run_workbench_dependency_stage(window: object):
    """Run existing dependency readiness and return its stored result."""
    _analyze_dependency_readiness(window)
    return getattr(window, "_large_file_refactor_workbench_dependency_readiness", None)


def run_workbench_preview_stage(window: object):
    """Run existing Real Preview generation and return its stored result."""
    _generate_real_preview(window)
    return getattr(window, "_large_file_refactor_workbench_real_preview", None)


def run_workbench_structural_stage(window: object):
    """Run existing structural validation and return its stored result."""
    _validate_real_preview(window)
    return getattr(window, "_large_file_refactor_workbench_structural_validation", None)


def sync_workbench_controls(window: object) -> None:
    """Refresh the detailed Workbench projection after normal-mode orchestration."""
    _sync_workbench_buttons(window)

def _root_text(window: object) -> str:
    """Return the active project root from the Architecture Review window."""
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return str(Path.cwd())
    text = edit.text().strip()
    return text or str(Path.cwd())
