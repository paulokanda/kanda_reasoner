# project-path: kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py
"""PySide6 Engineering Diagnostics panel over the frozen public backend."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from threading import Event
import traceback
from typing import Callable
from kanda_reasoner_app.engineering_diagnostics import (
    ARCHITECTURE_PRODUCER_ID,
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    SHADOW_PRODUCER_ID,
)

from .controller import EngineeringDiagnosticsController
from .diagnostic_table_model import create_finding_table_model_class
from .engineering_diagnostics_sonar import create_engineering_diagnostics_sonar
from .grouping_ui import (
    bind_grouping_actions,
    create_group_filter,
    create_grouping_buttons,
)
from .lifecycle_ui import bind_lifecycle_actions, create_lifecycle_controls
from ._navigation_ui import _bind_engineering_diagnostics_navigation
from .history_async import bind_async_history
from .engineering_diagnostics_lifecycle import (
    EngineeringDiagnosticsPanelLifecycle,
    future_is_active,
    mark_future_settled,
)
from .models import EngineeringDiagnosticsGuiCancelled
from .owner_ui import build_finding_detail_lines
from .patch_preview_ui import bind_patch_preview_action, create_patch_preview_button
from .table_columns import ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS

__all__ = ["create_engineering_diagnostics_panel"]

def _tool_root() -> Path:
    return Path(__file__).resolve().parents[2]
def create_engineering_diagnostics_panel(
    project_root_provider: Callable[[], object] | None = None,
    *,
    controller: EngineeringDiagnosticsController | None = None,
    defer_initial_refresh: bool = False,
):
    """Create the Engineering Diagnostics child tab using public contracts only."""
    from PySide6.QtCore import QAbstractTableModel, QModelIndex
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QComboBox,
        QHBoxLayout,
        QInputDialog,
        QLabel,
        QLineEdit,
        QMessageBox,
        QPlainTextEdit,
        QPushButton,
        QSplitter,
        QTableView,
        QVBoxLayout,
        QWidget,
    )
    active_controller = controller or EngineeringDiagnosticsController(
        tool_root=_tool_root()
    )
    FindingTableModel = create_finding_table_model_class(
        QAbstractTableModel,
        QModelIndex,
        Qt,
        ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS,
    )
    panel = QWidget()
    panel.setObjectName("engineering_diagnostics_page")
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    toolbar = QHBoxLayout()
    producer_combo = QComboBox()
    producer_combo.addItem("BOM", BOM_PRODUCER_ID)
    producer_combo.addItem("Ruff", RUFF_PRODUCER_ID)
    producer_combo.addItem("Architecture", ARCHITECTURE_PRODUCER_ID)
    producer_combo.addItem("Shadow", SHADOW_PRODUCER_ID)
    run_button = QPushButton("Run Engineering Diagnostics")
    run_button.setObjectName("engineering_diagnostics_run_button")
    cancel_button = QPushButton("Cancel Diagnostics")
    cancel_button.setObjectName("engineering_diagnostics_cancel_button")
    refresh_button = QPushButton("Refresh History")
    baseline_button = QPushButton("Activate as Baseline")
    cancel_button.setEnabled(False)
    toolbar.addWidget(QLabel("Collector"))
    toolbar.addWidget(producer_combo)
    toolbar.addWidget(run_button)
    toolbar.addWidget(cancel_button)
    toolbar.addWidget(refresh_button)
    toolbar.addWidget(baseline_button)
    group_buttons = create_grouping_buttons(toolbar, QPushButton)
    lifecycle_controls = create_lifecycle_controls(
        toolbar, QComboBox, QPushButton, QLabel
    )
    patch_preview_button = create_patch_preview_button(toolbar, QPushButton)
    toolbar.addStretch(1)
    layout.addLayout(toolbar)
    selection_row = QHBoxLayout()
    run_combo = QComboBox()
    severity_combo = QComboBox()
    severity_combo.addItems(("all", "error", "warning", "info"))
    lifecycle_combo = QComboBox()
    lifecycle_combo.addItems(("all", "new", "persistent", "current"))
    decision_combo = QComboBox()
    decision_combo.addItems(("all", "open", "investigating", "confirmed",
        "fix_planned", "patch_prepared", "validating", "resolution_candidate",
        "resolved", "accepted_risk", "false_positive", "suppressed", "deferred",
        "reopened"))
    scope_combo = QComboBox()
    scope_combo.addItems(("all", "active", "test", "fixture", "prototype",
        "generated", "reference", "deprecated", "workbench", "snippet",
        "temporary", "unknown"))
    frozen_combo = QComboBox()
    frozen_combo.addItems(("all", "frozen", "touches_frozen",
                           "historical_frozen", "unfrozen", "unknown"))
    owner_combo = QComboBox()
    owner_combo.addItems(("all", "ready", "needs_review", "no_owner",
                          "degraded", "not_evaluated"))
    search_edit = QLineEdit()
    search_edit.setPlaceholderText(
        "Filter code, path, message, owner, scope, or Freeze ID"
    )
    selection_row.addWidget(QLabel("Run"))
    selection_row.addWidget(run_combo, 2)
    selection_row.addWidget(QLabel("Severity"))
    selection_row.addWidget(severity_combo)
    selection_row.addWidget(QLabel("Baseline"))
    selection_row.addWidget(lifecycle_combo)
    selection_row.addWidget(QLabel("Decision"))
    selection_row.addWidget(decision_combo)
    selection_row.addWidget(QLabel("Scope"))
    selection_row.addWidget(scope_combo)
    selection_row.addWidget(QLabel("Frozen"))
    selection_row.addWidget(frozen_combo)
    selection_row.addWidget(QLabel("Owner"))
    selection_row.addWidget(owner_combo)
    group_combo = create_group_filter(selection_row, QComboBox, QLabel)
    selection_row.addWidget(search_edit, 2)
    layout.addLayout(selection_row)
    summary_label = QLabel("No diagnostic run selected.")
    status_label = QLabel("Ready")
    sonar = create_engineering_diagnostics_sonar(panel)
    layout.addWidget(summary_label)
    layout.addWidget(status_label)
    splitter = QSplitter()
    table = QTableView(splitter)
    detail = QPlainTextEdit(splitter)
    detail.setReadOnly(True)
    detail.setPlainText("Select a diagnostic finding to inspect its evidence.")
    splitter.addWidget(table)
    splitter.addWidget(detail)
    splitter.setStretchFactor(0, 3)
    splitter.setStretchFactor(1, 2)
    layout.addWidget(splitter, 1)
    model = FindingTableModel()
    table.setModel(model)
    header = table.horizontalHeader()
    header.setSectionsClickable(True)
    header.setSortIndicatorShown(False)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    executor = ThreadPoolExecutor(max_workers=1)
    state = {
        "generation": 0,
        "future": None,
        "cancel": None,
        "project_root": "",
        "closing": False,
        "discard_reason": "",
    }
    def current_project_root() -> str:
        if project_root_provider is not None:
            value = str(project_root_provider() or "").strip()
            if value:
                return value
        return str(Path.cwd())
    def selected_producer_id() -> str:
        return str(producer_combo.currentData() or BOM_PRODUCER_ID)
    def producer_label() -> str:
        producer_id = selected_producer_id()
        if producer_id == RUFF_PRODUCER_ID:
            return "Ruff"
        if producer_id == ARCHITECTURE_PRODUCER_ID:
            return "Architecture"
        if producer_id == SHADOW_PRODUCER_ID:
            return "Shadow"
        return "BOM"
    def update_run_button() -> None:
        run_button.setToolTip("Run read-only " + producer_label() + " diagnostics")
    def set_busy(busy: bool) -> None:
        producer_combo.setEnabled(not busy)
        run_button.setEnabled(not busy)
        cancel_button.setEnabled(busy)
        refresh_button.setEnabled(not busy)
        baseline_button.setEnabled(not busy)
        grouping_actions.set_enabled(not busy)
        lifecycle_actions.set_enabled(not busy)
        patch_preview_actions.set_enabled(not busy)
    def show_error(prefix: str, exc: BaseException) -> None:
        status_label.setText(prefix + ": " + str(exc))
        detail.setPlainText(traceback.format_exc())
    def apply_filters() -> None:
        model.set_filters(
            severity_combo.currentText(),
            lifecycle_combo.currentText(),
            scope_combo.currentText(),
            frozen_combo.currentText(),
            owner_combo.currentText(),
            group_combo.currentText(),
            decision_combo.currentText(),
            search_edit.text(),
        )
    history_actions = bind_async_history(
        controller=active_controller,
        current_project_root=current_project_root,
        selected_producer_id=selected_producer_id,
        run_combo=run_combo,
        model=model,
        summary_label=summary_label,
        status_label=status_label,
        detail=detail,
        apply_filters=apply_filters,
    )
    render_run = history_actions.render_run
    refresh_history = history_actions.refresh_history
    def finish_scan(generation: int, future: Future) -> None:
        owns_slot = state.get("future") is future
        if bool(state.get("closing", False)):
            mark_future_settled(state, "future", future)
            return
        if generation != state["generation"]:
            mark_future_settled(state, "future", future)
            if owns_slot:
                state["cancel"] = None
                sonar.stop()
                set_busy(False)
                status_label.setText(
                    "Diagnostic run cancelled after settlement."
                    if state.get("discard_reason") == "user_cancel"
                    else "Previous Project diagnostic result discarded after settlement."
                )
            return
        mark_future_settled(state, "future", future)
        state["cancel"] = None
        sonar.stop()
        set_busy(False)
        try:
            candidate = future.result()
            run = active_controller.commit_candidate(
                current_project_root(),
                candidate,
                current_generation=generation,
            )
        except EngineeringDiagnosticsGuiCancelled:
            status_label.setText("Diagnostic run cancelled.")
            return
        except Exception as exc:  # noqa: BLE001
            show_error("Diagnostic run failed", exc)
            return
        status_label.setText("Diagnostic run stored: " + run.run_id[:12])
        refresh_history(run.run_id)
    def poll_scan(generation: int, future: Future) -> None:
        if bool(state.get("closing", False)):
            return
        if future.done():
            finish_scan(generation, future)
            return
        QTimer.singleShot(100, lambda: poll_scan(generation, future))
    def start_scan() -> None:
        if future_is_active(state, "future"):
            return
        root = current_project_root()
        state["generation"] += 1
        generation = state["generation"]
        cancellation = Event()
        state["cancel"] = cancellation
        state["project_root"] = root
        state["discard_reason"] = ""
        set_busy(True)
        producer_id = selected_producer_id()
        status_label.setText(
            "Running read-only " + producer_label() + " diagnostics..."
        )
        sonar.start(producer_label())
        collector = active_controller.collect_bom_candidate
        if producer_id == RUFF_PRODUCER_ID:
            collector = active_controller.collect_ruff_candidate
        if producer_id == ARCHITECTURE_PRODUCER_ID:
            collector = active_controller.collect_architecture_candidate
        if producer_id == SHADOW_PRODUCER_ID:
            collector = active_controller.collect_shadow_candidate
        future = executor.submit(
            collector,
            root,
            generation,
            cancellation,
        )
        state["future"] = future
        QTimer.singleShot(100, lambda: poll_scan(generation, future))
    def cancel_scan() -> None:
        cancellation = state.get("cancel")
        if cancellation is None or state.get("future") is None:
            status_label.setText("No Engineering Diagnostics run is active.")
            return
        if cancellation.is_set():
            return
        lifecycle.request_user_cancellation()
        sonar.stop()
        cancel_button.setEnabled(False)
        status_label.setText(
            "Cancellation requested; late results will be discarded after settlement."
        )
    def activate_baseline() -> None:
        run_id = str(run_combo.currentData() or "")
        if not run_id:
            status_label.setText("Select a completed run first.")
            return
        label, accepted = QInputDialog.getText(
            panel,
            "Baseline label",
            "Label for this immutable baseline:",
        )
        if not accepted or not str(label).strip():
            return
        confirmation = QMessageBox.question(
            panel,
            "Activate baseline",
            "Activate the selected completed run as the current baseline?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirmation != QMessageBox.Yes:
            return
        try:
            baseline = active_controller.activate_run_as_baseline(
                current_project_root(),
                run_id,
                label=str(label).strip(),
            )
        except Exception as exc:  # noqa: BLE001
            show_error("Baseline activation failed", exc)
            return
        status_label.setText(
            "Baseline activated: " + baseline.baseline_id[:12]
        )
        render_run(run_id)
    def show_selected_detail() -> None:
        indexes = table.selectionModel().selectedRows()
        if not indexes:
            return
        view = model.row_view(indexes[0].row())
        if view is None:
            return
        record = view.record
        try:
            excerpt = active_controller.source_excerpt(
                current_project_root(),
                record,
            )
        except Exception as exc:  # noqa: BLE001
            excerpt = "Source excerpt unavailable: " + str(exc)
        rendered = build_finding_detail_lines(view, excerpt)
        detail.setPlainText("\n".join(rendered))
    grouping_actions = bind_grouping_actions(
        panel=panel,
        controller=active_controller,
        buttons=group_buttons,
        input_dialog=QInputDialog,
        message_box=QMessageBox,
        current_project_root=current_project_root,
        current_run_id=lambda: str(run_combo.currentData() or ""),
        table=table,
        model=model,
        render_run=render_run,
        show_error=show_error,
        status_label=status_label,
    )
    lifecycle_actions = bind_lifecycle_actions(
        panel=panel,
        controller=active_controller,
        controls=lifecycle_controls,
        input_dialog=QInputDialog,
        message_box=QMessageBox,
        current_project_root=current_project_root,
        current_run_id=lambda: str(run_combo.currentData() or ""),
        table=table,
        model=model,
        render_run=render_run,
        show_error=show_error,
        status_label=status_label,
    )
    patch_preview_actions = bind_patch_preview_action(
        panel=panel, button=patch_preview_button, table=table, model=model,
        detail=detail, status_label=status_label, controller=active_controller,
        current_project_root=current_project_root,
        current_run_id=lambda: str(run_combo.currentData() or ""),
        input_dialog=QInputDialog, message_box=QMessageBox,
    )
    _bind_engineering_diagnostics_navigation(
        panel, active_controller, current_project_root, producer_combo, run_combo,
        severity_combo, lifecycle_combo, search_edit, refresh_history,
        update_run_button, apply_filters, status_label,
    )
    lifecycle = EngineeringDiagnosticsPanelLifecycle(
        state=state,
        executors=(executor,),
        future_keys=("future",),
        active_reason="Engineering Diagnostics scan is still running",
        auxiliary=history_actions,
    )
    def set_project_root(_value: object = None) -> None:
        lifecycle.request_project_scope_settlement()
        model.set_rows(())
        run_combo.clear()
        detail.setPlainText("Project selection changed. Refreshing diagnostics...")
        refresh_history()
    producer_combo.currentIndexChanged.connect(
        lambda _index: (update_run_button(), refresh_history())
    )
    run_button.clicked.connect(start_scan)
    cancel_button.clicked.connect(cancel_scan)
    refresh_button.clicked.connect(lambda: refresh_history())
    baseline_button.clicked.connect(activate_baseline)
    run_combo.currentIndexChanged.connect(
        lambda _index: render_run(str(run_combo.currentData() or ""))
    )
    severity_combo.currentTextChanged.connect(lambda _value: apply_filters())
    lifecycle_combo.currentTextChanged.connect(lambda _value: apply_filters())
    decision_combo.currentTextChanged.connect(lambda _value: apply_filters())
    scope_combo.currentTextChanged.connect(lambda _value: apply_filters())
    frozen_combo.currentTextChanged.connect(lambda _value: apply_filters())
    owner_combo.currentTextChanged.connect(lambda _value: apply_filters())
    group_combo.currentTextChanged.connect(lambda _value: apply_filters())
    search_edit.textChanged.connect(lambda _value: apply_filters())
    header.sectionClicked.connect(
        lambda section: (
            model.sort(
                section,
                Qt.DescendingOrder
                if model._sort_column == section and not model._sort_descending
                else Qt.AscendingOrder,
            ),
            header.setSortIndicatorShown(True),
            header.setSortIndicator(
                section,
                Qt.DescendingOrder if model._sort_descending else Qt.AscendingOrder,
            ),
        )
    )
    table.selectionModel().selectionChanged.connect(
        lambda _selected, _deselected: show_selected_detail()
    )
    panel.destroyed.connect(lambda _obj=None: lifecycle.begin_shutdown())
    panel.set_project_root = set_project_root
    panel.refresh_engineering_diagnostics = refresh_history
    panel.start_engineering_diagnostics = start_scan
    panel.cancel_engineering_diagnostics = cancel_scan
    panel.project_scope_switch_block_reason = lifecycle.project_scope_switch_block_reason
    panel.request_project_scope_settlement = lifecycle.request_project_scope_settlement
    panel.begin_shutdown = lifecycle.begin_shutdown
    panel.shutdown_ready = lifecycle.shutdown_ready
    panel.engineering_diagnostics_controller = active_controller
    panel.engineering_diagnostics_history_actions = history_actions
    panel.engineering_diagnostics_table = table
    panel.engineering_diagnostics_producer_combo = producer_combo
    panel.engineering_diagnostics_status_label = status_label
    panel.engineering_diagnostics_run_button = run_button
    panel.engineering_diagnostics_cancel_button = cancel_button
    panel.engineering_diagnostics_sonar = sonar
    panel.engineering_diagnostics_sonar_widget = sonar.widget()
    panel.engineering_diagnostics_scope_combo = scope_combo
    panel.engineering_diagnostics_frozen_combo = frozen_combo
    panel.engineering_diagnostics_owner_combo = owner_combo
    panel.engineering_diagnostics_group_combo = group_combo
    panel.engineering_diagnostics_grouping_buttons = group_buttons
    panel.engineering_diagnostics_decision_combo = decision_combo
    panel.engineering_diagnostics_lifecycle_controls = lifecycle_controls
    update_run_button()
    if not defer_initial_refresh:
        QTimer.singleShot(0, refresh_history)
    return panel
