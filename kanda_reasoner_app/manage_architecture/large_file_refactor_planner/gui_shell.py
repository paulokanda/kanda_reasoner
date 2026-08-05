# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py
"""Qt shell for the Architecture Review Large File Refactor Planner sub-tab."""
from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from .analysis_formatting import format_analysis_report
from .planner_analysis_feedback import format_planner_analysis_completion
from .docstring_formatting import format_docstring_proposals
from .ast_analysis import analyze_python_file
from .gui_warning_input_gate import (
    build_warning_input_gate_section,
    refresh_warning_input_gate,
    sync_warning_input_selection,
)
from .docstring_planner import build_docstring_proposals
from .split_formatting import format_split_plan
from .models import FEATURE_ID, PlannerSettings, PlannerState
from .planner_background_cancel import cancel_planner_background_work
from .planner_bounded_refinement import (
    attach_docstring_proposals_to_plan,
    plan_allows_ai_architecture_correction,
)
from .planner_local_ai_review_gui import (
    start_comprehensive_local_ai_review_for_window,
)
from .planner_split_plan_gui import start_split_plan_generation_for_window
from .planner_inner_tabs_layout import build_planner_inner_tabs
from .planner_web_ai_plan_panel import PlannerWebAIPlanOutput
from .planner_settings_panel_presentation import apply_settings_panel_presentation
from .planner_version_selector_gui import (
    build_planner_version_selector,
    refresh_planner_version_selector,
    render_selected_planner_version,
)
from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_WEB_AI,
    get_planner_version_bundle,
    initialize_planner_version_state,
    selected_planner_version,
    store_heuristic_version,
)
from .planner_preimplementation_summary import build_planning_summary
from .main_workbench_refactoring_folder_button import build_main_workbench_controls
from .planner_status_projection import refresh_planner_status as _update_status
from .planner_versioned_generation import planner_generation_route
from .planner_web_ai_exchange_gui import (
    copy_comprehensive_planning_for_web_ai,
    copy_web_ai_refactor_version_how_to,
    copy_web_ai_split_file_wrapper,
    open_pasted_planning_from_web_ai,
    open_receive_planning_from_web_ai,
    open_view_web_ai_proposal,
)
__all__ = ["build_large_file_refactor_planner_page", "refresh_large_file_refactor_planner_status"]
def build_large_file_refactor_planner_page(window: object) -> QWidget:
    """Build the first train-car shell for the large-file planner."""
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    _initialize_planner_state(window)
    candidate_section = _build_candidate_section(window)
    settings_section = _build_settings_section(window)
    evidence_section = _build_evidence_section(window)
    plan_section = _build_plan_section(window)
    preview_section = _build_preview_section(window)
    inner_tabs = build_planner_inner_tabs(
        [candidate_section, settings_section, evidence_section],
        [plan_section, preview_section],
        send_web_ai_split_callback=lambda: copy_web_ai_split_file_wrapper(window),
    )
    window._large_file_refactor_planner_inner_tab_stack = inner_tabs.stack
    window._large_file_refactor_planner_inner_tab_buttons = inner_tabs.buttons
    window._large_file_refactor_send_web_ai_split_button = inner_tabs.send_web_ai_split_button
    layout.addWidget(inner_tabs.root, 1)
    _refresh_candidate_table(window)
    return page
def _initialize_planner_state(window: object) -> None:
    """Install minimal planner state on the existing Architecture window."""
    window._large_file_refactor_planner_state = PlannerState.IDLE.value
    window._large_file_refactor_planner_settings = PlannerSettings()
    window._large_file_refactor_planner_candidates = []
    window._large_file_refactor_planner_selected_path = ""
    initialize_planner_version_state(window)
def _build_candidate_section(window: object) -> QGroupBox:
    """Create warning-derived candidate controls and table."""
    return build_warning_input_gate_section(window)
def _build_settings_section(window: object) -> QGroupBox:
    """Create the settings row with safe v1 defaults."""
    settings = PlannerSettings()
    box = QGroupBox("2. Settings panel")
    row = QHBoxLayout(box)
    window._large_file_refactor_ideal_spin = QSpinBox()
    window._large_file_refactor_ideal_spin.setRange(100, 500)
    window._large_file_refactor_ideal_spin.setValue(settings.ideal_physical_lines)
    window._large_file_refactor_max_spin = QSpinBox()
    window._large_file_refactor_max_spin.setRange(100, 500)
    window._large_file_refactor_max_spin.setValue(settings.maximum_physical_lines)
    window._large_file_refactor_min_helper_spin = QSpinBox()
    window._large_file_refactor_min_helper_spin.setRange(100, 500)
    window._large_file_refactor_min_helper_spin.setValue(settings.minimum_helper_physical_lines)
    row.addWidget(QLabel("Ideal"))
    row.addWidget(window._large_file_refactor_ideal_spin)
    row.addWidget(QLabel("Max"))
    row.addWidget(window._large_file_refactor_max_spin)
    row.addWidget(QLabel("Min helper"))
    row.addWidget(window._large_file_refactor_min_helper_spin)
    _add_checked_box(row, "Preserve public facade", settings.preserve_public_facade)
    _add_checked_box(row, "Generate missing docstrings", settings.generate_missing_docstrings)
    _add_checked_box(row, "Import migration preview", settings.import_migration_preview)
    _add_checked_box(row, "Preview only", settings.preview_only)
    apply_settings_panel_presentation(box, row)
    row.addStretch(1)
    return box
def _build_evidence_section(window: object) -> QGroupBox:
    """Create the analysis evidence panel."""
    box = QGroupBox("3. Analysis evidence panel")
    layout = QVBoxLayout(box)
    window._large_file_refactor_evidence_output = QPlainTextEdit()
    window._large_file_refactor_evidence_output.setReadOnly(True)
    window._large_file_refactor_evidence_output.setPlainText(
        "Analysis not run. Select a candidate and click Analyze File to run "
        "read-only AST evidence extraction. Implementation continues in Large "
        "File Refactor Workbench only after a valid plan is reviewed."
    )
    layout.addWidget(window._large_file_refactor_evidence_output, 1)
    return box
def _build_plan_section(window: object) -> QGroupBox:
    """Create the proposed split plan placeholder panel."""
    box = QGroupBox("4. Proposed split plan panel")
    layout = QVBoxLayout(box)
    window._large_file_refactor_plan_output = PlannerWebAIPlanOutput(
        paste_callback=lambda text: open_pasted_planning_from_web_ai(
            window, text, refresh_callback=_update_status),
        load_installed_callback=lambda: open_receive_planning_from_web_ai(
            window, refresh_callback=_update_status),
    )
    window._large_file_refactor_plan_output.setPlainText(
        "Plan not generated. Generate Split Plan first. ZIP path: install the "
        "Web AI package and select Imported Web AI Version. Paste path: copy the "
        "complete marker-wrapped response from chat, focus this Panel 4, and "
        "press Ctrl+V. Both paths validate before review and loading."
    )
    layout.addWidget(window._large_file_refactor_plan_output, 1)
    return box
def _build_preview_section(window: object) -> QGroupBox:
    """Create the explicit pre-implementation planning pipeline."""
    box = QGroupBox("5. Planning pipeline and AI exchange")
    layout = QVBoxLayout(box)
    window._large_file_refactor_status_label = QLabel(
        "Analysis: not run | Plan: not generated | Docstrings: not generated | "
        "Local AI: not run | Imported Web AI: none | Workbench handoff: not ready"
    )
    layout.addWidget(window._large_file_refactor_status_label)
    selector = build_planner_version_selector(
        window,
        refresh_callback=_update_status,
        web_ai_import_callback=lambda target: open_receive_planning_from_web_ai(
            target, refresh_callback=_update_status
        ),
        cancel_callback=lambda target: cancel_planner_background_work(
            target,
            refresh_callback=_update_status,
            user_visible=True,
        ),
    )
    layout.addWidget(selector)
    pipeline_row = QHBoxLayout()
    analyze_btn = QPushButton("Analyze File")
    analyze_btn.clicked.connect(lambda: _show_selected_candidate_summary(window))
    analyze_btn.setEnabled(False)
    window._large_file_refactor_analyze_button = analyze_btn
    pipeline_row.addWidget(analyze_btn)
    plan_btn = QPushButton("Generate Split Plan")
    plan_btn.clicked.connect(lambda: _generate_split_plan(window))
    plan_btn.setEnabled(False)
    window._large_file_refactor_plan_button = plan_btn
    pipeline_row.addWidget(plan_btn)
    docstring_btn = QPushButton("Generate Docstring Plan")
    docstring_btn.clicked.connect(lambda: _generate_docstring_plan(window))
    docstring_btn.setEnabled(False)
    window._large_file_refactor_docstring_button = docstring_btn
    pipeline_row.addWidget(docstring_btn)
    local_ai_btn = QPushButton("Review & Refine Plan with Local AI")
    local_ai_btn.clicked.connect(lambda: _review_refine_with_local_ai(window))
    local_ai_btn.setEnabled(False)
    window._large_file_refactor_llm_button = local_ai_btn
    pipeline_row.addWidget(local_ai_btn)
    howto_btn = QPushButton("Open External AI Refactor How To")
    
    howto_btn.setStyleSheet("background-color: #f28c28; font-weight: bold;")
    howto_btn.setStyleSheet(
        """
        QPushButton {
            background-color: #d9d9d9;
            color: #ff8c00;
            font-weight: bold;
        }
        """
    )
    howto_btn.setToolTip("Copy the canonical protocol and open the selected external AI.")
    howto_btn.clicked.connect(lambda: copy_web_ai_refactor_version_how_to(window))
    window._large_file_refactor_web_ai_howto_button = howto_btn
    pipeline_row.addWidget(howto_btn)
    pipeline_row.addStretch(1)
    layout.addLayout(pipeline_row)
    web_row = QHBoxLayout()
    copy_web_btn = QPushButton("Send Planning to External AI")
    copy_web_btn.clicked.connect(lambda: copy_comprehensive_planning_for_web_ai(window))
    copy_web_btn.setEnabled(False)
    window._large_file_refactor_copy_web_ai_button = copy_web_btn
    web_row.addWidget(copy_web_btn)
    view_web_btn = QPushButton("Review Imported Web AI Version")
    view_web_btn.clicked.connect(lambda: open_view_web_ai_proposal(window))
    view_web_btn.setEnabled(False)
    window._large_file_refactor_view_web_ai_button = view_web_btn
    web_row.addWidget(view_web_btn)
    show_summary_btn = QPushButton("Show Planning Summary")
    show_summary_btn.clicked.connect(lambda: _show_planning_summary(window))
    web_row.addWidget(show_summary_btn)
    web_row.addStretch(1)
    layout.addLayout(web_row)
    layout.addWidget(build_main_workbench_controls(window))
    return box
def _add_checked_box(row: QHBoxLayout, text: str, checked: bool) -> QCheckBox:
    """Create one settings checkbox."""
    box = QCheckBox(text)
    box.setChecked(checked)
    row.addWidget(box)
    return box
def _refresh_candidate_table(window: object) -> None:
    """Refresh candidates only from latest MODULE_TOO_LARGE warnings."""
    refresh_warning_input_gate(window)
    _update_status(window)
def _sync_selected_candidate(window: object) -> None:
    """Store the selected warning-derived candidate path."""
    sync_warning_input_selection(window)
    _update_status(window)
def _show_selected_candidate_summary(window: object) -> None:
    """Run read-only AST analysis and populate the evidence panel."""
    path = getattr(window, "_large_file_refactor_planner_selected_path", "")
    if not path:
        window._large_file_refactor_evidence_output.setPlainText(
            "No candidate selected. Run Selected Mode with Validate, then select "
            "a WARNING MODULE_TOO_LARGE module."
        )
        return
    try:
        window._large_file_refactor_planner_state = PlannerState.ANALYZING.value
        window._large_file_refactor_plan_output.setPlainText(
            "ANALYZING FILE\n" + str(path) + "\n\nRead-only AST evidence extraction is running."
        )
        _update_status(window)
        report = analyze_python_file(path)
    except OSError as exc:
        window._large_file_refactor_planner_state = PlannerState.BLOCKED.value
        window._large_file_refactor_evidence_output.setPlainText(
            f"Analysis blocked. Could not read source file: {exc}"
        )
        _update_status(window)
        return
    window._large_file_refactor_planner_state = PlannerState.ANALYZED.value
    window._large_file_refactor_last_analysis = report
    initialize_planner_version_state(window, preserve_selection=True)
    refresh_planner_version_selector(window)
    window._large_file_refactor_plan_ai_review_result = None
    window._large_file_refactor_web_ai_proposal = None
    window._large_file_refactor_web_ai_proposal_applied = False
    window._large_file_refactor_evidence_output.setPlainText(format_analysis_report(report))
    window._large_file_refactor_plan_output.setPlainText(
        format_planner_analysis_completion(
            report,
            selected_planner_version(window),
        )
    )
    _update_status(window)
def _generate_split_plan(window: object) -> None:
    """Generate a deterministic split plan with visible sonar activity."""
    report = getattr(window, "_large_file_refactor_last_analysis", None)
    if report is None:
        window._large_file_refactor_plan_output.setPlainText(
            "Run Analyze File before generating a split plan."
        )
        return
    selected_version = selected_planner_version(window)
    if selected_version == PLANNER_VERSION_WEB_AI:
        window._large_file_refactor_plan_output.setPlainText(
            "Imported Web AI Version is not generated locally. Select Heuristic or "
            "Local AI to generate a native plan, then export it to external Web AI."
        )
        return
    settings = PlannerSettings(
        ideal_physical_lines=int(window._large_file_refactor_ideal_spin.value()),
        maximum_physical_lines=int(window._large_file_refactor_max_spin.value()),
        minimum_helper_physical_lines=int(window._large_file_refactor_min_helper_spin.value()),
    )
    start_split_plan_generation_for_window(
        window,
        report,
        settings,
        refresh_callback=_update_status,
        completion_callback=lambda active_window, plan: _complete_versioned_split_generation(
            active_window,
            report,
            plan,
            selected_version,
        ),
    )
def _complete_versioned_split_generation(
    window: object,
    report: object,
    plan: object,
    version_name: str,
) -> None:
    """Continue generation according to the version selected before the split."""
    route = planner_generation_route(version_name)
    if not route.generate_docstrings_automatically:
        _update_status(window)
        return
    proposals = build_docstring_proposals(report, plan)
    plan_with_docs = attach_docstring_proposals_to_plan(plan, proposals)
    store_heuristic_version(window, plan_with_docs, proposals)
    refresh_planner_version_selector(window)
    if route.start_local_ai_review:
        window._large_file_refactor_plan_output.setPlainText(
            format_split_plan(plan_with_docs)
            + "\n\n"
            + format_docstring_proposals(proposals)
            + "\n\nLOCAL AI VERSION GENERATION STARTED"
        )
        start_comprehensive_local_ai_review_for_window(
            window, report, plan_with_docs, proposals, refresh_callback=_update_status
        )
        return
    window._large_file_refactor_planner_state = (
        PlannerState.BLOCKED.value
        if plan_with_docs.status == "blocked"
        else PlannerState.DOCSTRING_READY.value
    )
    render_selected_planner_version(window)
    _update_status(window)
def _generate_docstring_plan(window: object) -> None:
    """Generate deterministic docstrings for the isolated heuristic version."""
    report = getattr(window, "_large_file_refactor_last_analysis", None)
    bundle = get_planner_version_bundle(window, PLANNER_VERSION_HEURISTIC)
    plan = bundle.plan if bundle is not None else None
    if report is None or plan is None:
        window._large_file_refactor_plan_output.setPlainText(
            "Run Analyze File and Generate Split Plan before generating docstrings."
        )
        return
    proposals = build_docstring_proposals(report, plan)
    plan = attach_docstring_proposals_to_plan(plan, proposals)
    store_heuristic_version(window, plan, proposals)
    refresh_planner_version_selector(window)
    window._large_file_refactor_plan_ai_review_result = None
    window._large_file_refactor_web_ai_proposal = None
    window._large_file_refactor_web_ai_proposal_applied = False
    window._large_file_refactor_plan_output.setPlainText(
        format_split_plan(plan) + "\n\n" + format_docstring_proposals(proposals)
    )
    window._large_file_refactor_planner_state = (
        PlannerState.DOCSTRING_READY.value
        if plan_allows_ai_architecture_correction(plan)
        else PlannerState.BLOCKED.value
    )
    _update_status(window)
def _review_refine_with_local_ai(window: object) -> None:
    """Run question-driven architecture and docstring review on heuristic state."""
    report = getattr(window, "_large_file_refactor_last_analysis", None)
    bundle = get_planner_version_bundle(window, PLANNER_VERSION_HEURISTIC)
    plan = bundle.plan if bundle is not None else None
    proposals = list(bundle.docstring_proposals) if bundle is not None else []
    if report is None or plan is None:
        window._large_file_refactor_plan_output.setPlainText(
            "Complete Analyze File and Generate Split Plan before local AI review."
        )
        return
    start_comprehensive_local_ai_review_for_window(
        window, report, plan, proposals, refresh_callback=_update_status
    )
def _show_planning_summary(window: object) -> None:
    """Render a Planner-only pre-implementation summary."""
    window._large_file_refactor_plan_output.setPlainText(
        build_planning_summary(window)
    )
def refresh_large_file_refactor_planner_status(window: object) -> None:
    """Refresh Planner status text and stage-button enablement."""
    _update_status(window)
def _root_text(window: object) -> str:
    """Return the active project root from the Architecture Review window."""
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return str(Path.cwd())
    text = edit.text().strip()
    return text or str(Path.cwd())
