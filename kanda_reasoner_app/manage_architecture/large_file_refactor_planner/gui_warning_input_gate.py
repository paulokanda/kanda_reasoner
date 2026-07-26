# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_warning_input_gate.py
"""Audit-warning input gate widgets for the Large File Refactor Planner."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from kanda_reasoner_app.manage_architecture.architecture_review_card_lifecycle import (
    handle_planner_target_selection,
)

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from kanda_reasoner_app.manage_architecture.large_module_target_queue import (
    LargeModuleTarget,
    normalize_target_text,
    parse_module_too_large_findings,
)

from .candidate_discovery import discover_candidates
from .models import MAX_PHYSICAL_LINES, PlannerState

__all__ = [
    "build_warning_input_gate_section",
    "browse_warning_input_target",
    "refresh_warning_input_gate",
    "sync_warning_input_selection",
]

_QUEUE_COLUMNS = (
    "#",
    "Module",
    "Size",
    "Lines",
    "Missing docstrings",
    "Action",
)


def build_warning_input_gate_section(window: object) -> QGroupBox:
    """Build the gated audit-warning target selector."""
    box = QGroupBox("1. Large-file input from WARNING MODULE_TOO_LARGE")
    layout = QVBoxLayout(box)
    row = QHBoxLayout()
    window._large_file_refactor_gate_label = QLabel(
        "Large File Refactor Planner - inactive"
    )
    window._large_file_refactor_gate_label.setStyleSheet(
        "color: #6A1B9A; font-weight: bold; padding: 4px 8px;"
    )
    row.addWidget(window._large_file_refactor_gate_label)
    row.addWidget(QLabel("Target .py:"))
    window._large_file_refactor_target_edit = QLineEdit("")
    window._large_file_refactor_target_edit.setPlaceholderText(
        "Run Selected Mode with Validate to load MODULE_TOO_LARGE warnings"
    )
    window._large_file_refactor_target_edit.setMinimumWidth(360)
    row.addWidget(window._large_file_refactor_target_edit, 1)
    window._large_file_refactor_target_count_label = QLabel("0 large files")
    row.addWidget(window._large_file_refactor_target_count_label)
    layout.addLayout(row)
    layout.addLayout(_build_warning_button_row(window))
    window._large_file_refactor_metrics_label = QLabel(
        "0 files | 0 bytes | 0 lines | 0 missing docstrings"
    )
    layout.addWidget(window._large_file_refactor_metrics_label)
    window._large_file_refactor_numbered_targets = QPlainTextEdit()
    window._large_file_refactor_numbered_targets.setReadOnly(True)
    window._large_file_refactor_numbered_targets.setMaximumHeight(88)
    window._large_file_refactor_numbered_targets.setPlainText(
        "Inactive. Run Selected Mode with Validate first."
    )
    layout.addWidget(window._large_file_refactor_numbered_targets)
    table = QTableWidget(0, len(_QUEUE_COLUMNS))
    table.setHorizontalHeaderLabels(list(_QUEUE_COLUMNS))
    table.itemSelectionChanged.connect(lambda: sync_warning_input_selection(window))
    window._large_file_refactor_candidate_table = table
    layout.addWidget(table, 1)
    return box


def _build_warning_button_row(window: object) -> QHBoxLayout:
    """Build queue buttons similar to the Large Module AST Split Audit subtab."""
    row = QHBoxLayout()
    refresh_btn = QPushButton("Refresh from Run Selected Mode")
    refresh_btn.setToolTip("Load only WARNING MODULE_TOO_LARGE findings from latest Validate output.")
    refresh_btn.clicked.connect(lambda: refresh_warning_input_gate(window))
    window._large_file_refactor_refresh_warning_btn = refresh_btn
    row.addWidget(refresh_btn)
    copy_btn = QPushButton("Copy Path")
    copy_btn.clicked.connect(lambda: _copy_target_path(window))
    window._large_file_refactor_copy_target_path_btn = copy_btn
    row.addWidget(copy_btn)
    prev_btn = QPushButton("<-")
    prev_btn.clicked.connect(lambda: _move_warning_target(window, -1))
    window._large_file_refactor_prev_target_btn = prev_btn
    row.addWidget(prev_btn)
    next_btn = QPushButton("->")
    next_btn.clicked.connect(lambda: _move_warning_target(window, 1))
    window._large_file_refactor_next_target_btn = next_btn
    row.addWidget(next_btn)
    browse_btn = QPushButton("Browse Target...")
    browse_btn.setToolTip("Select an existing MODULE_TOO_LARGE warning target; non-warning files are blocked.")
    browse_btn.clicked.connect(lambda: browse_warning_input_target(window))
    window._large_file_refactor_browse_target_btn = browse_btn
    row.addWidget(browse_btn)
    row.addStretch(1)
    return row


def refresh_warning_input_gate(window: object) -> None:
    """Refresh candidates from the latest Run Selected Mode Validate output."""
    output_text = _output_text(window)
    run_ready = _selected_validate_has_run(window, output_text)
    targets = parse_module_too_large_findings(output_text) if run_ready else []
    candidates = []
    if targets:
        root_text = _root_text(window)
        candidates = discover_candidates(
            root_text,
            threshold=MAX_PHYSICAL_LINES,
            audit_targets=targets,
            scan_fallback=False,
        )
    window._large_file_refactor_planner_candidates = candidates
    window._large_file_refactor_warning_targets = list(targets)
    window._large_file_refactor_warning_input_gate_open = bool(candidates)
    _populate_warning_candidate_table(window, candidates)
    _sync_warning_controls(window)


def sync_warning_input_selection(window: object) -> None:
    """Sync selected warning-derived planner candidate."""
    table = getattr(window, "_large_file_refactor_candidate_table", None)
    if table is None:
        return
    row = table.currentRow()
    candidates = getattr(window, "_large_file_refactor_planner_candidates", [])
    if row < 0 or row >= len(candidates):
        window._large_file_refactor_planner_selected_path = ""
        _sync_warning_controls(window)
        return
    candidate = candidates[row]
    if not handle_planner_target_selection(window, candidate.path):
        _sync_warning_controls(window)
        return
    window._large_file_refactor_planner_selected_path = candidate.path
    window._large_file_refactor_planner_state = PlannerState.CANDIDATE_SELECTED.value
    if hasattr(window, "_large_file_refactor_target_edit"):
        window._large_file_refactor_target_edit.setText(candidate.relative_path)
    _sync_warning_controls(window)


def browse_warning_input_target(window: object) -> None:
    """Select an existing warning-derived target via file dialog."""
    if not getattr(window, "_large_file_refactor_warning_input_gate_open", False):
        _set_numbered_text(window, "Blocked. Run Selected Mode with Validate first.")
        return
    root_text = _root_text(window)
    start = str(Path(root_text)) if Path(root_text).exists() else str(Path.cwd())
    path, _ = QFileDialog.getOpenFileName(
        None,
        "Select existing MODULE_TOO_LARGE target",
        start,
        "Python files (*.py)",
    )
    if not path:
        return
    selected = normalize_target_text(root_text, path)
    row = _row_for_relative_target(window, selected)
    if row < 0:
        _set_numbered_text(
            window,
            "Blocked. Browse Target accepts only modules already listed by "
            "WARNING MODULE_TOO_LARGE from Run Selected Mode.",
        )
        return
    window._large_file_refactor_candidate_table.selectRow(row)
    sync_warning_input_selection(window)


def _populate_warning_candidate_table(window: object, candidates: Sequence[object]) -> None:
    """Populate table and numbered summary from largest module first."""
    table = window._large_file_refactor_candidate_table
    table.setRowCount(len(candidates))
    numbered_lines: list[str] = []
    total_size = 0
    total_lines = 0
    total_missing = 0
    for index, candidate in enumerate(candidates, start=1):
        size = _safe_size(candidate.path)
        total_size += size
        total_lines += int(candidate.line_count_physical)
        total_missing += int(candidate.missing_docstring_count)
        row_values = (
            str(index),
            candidate.relative_path,
            str(size),
            str(candidate.line_count_physical),
            str(candidate.missing_docstring_count),
            candidate.suggested_action,
        )
        for column, value in enumerate(row_values):
            table.setItem(index - 1, column, QTableWidgetItem(value))
        numbered_lines.append(
            f"{index}. {candidate.relative_path} | size={size} bytes | "
            f"lines={candidate.line_count_physical} | "
            f"missing_docstrings={candidate.missing_docstring_count}"
        )
    metrics = f"{len(candidates)} file(s) | {total_size} bytes | {total_lines} lines | {total_missing} missing docstrings"
    window._large_file_refactor_metrics_label.setText(metrics)
    _set_numbered_text(
        window,
        "\n".join(numbered_lines) if numbered_lines else _inactive_message(window),
    )
    if candidates:
        table.selectRow(0)
        sync_warning_input_selection(window)
    else:
        window._large_file_refactor_planner_selected_path = ""
        window._large_file_refactor_planner_state = PlannerState.IDLE.value


def _sync_warning_controls(window: object) -> None:
    """Enable controls only after Run Selected Mode produced warning targets."""
    candidates = getattr(window, "_large_file_refactor_planner_candidates", [])
    gate_open = bool(getattr(window, "_large_file_refactor_warning_input_gate_open", False))
    selected = bool(getattr(window, "_large_file_refactor_planner_selected_path", ""))
    if hasattr(window, "_large_file_refactor_gate_label"):
        if gate_open:
            window._large_file_refactor_gate_label.setText("Large File Refactor Planner")
            window._large_file_refactor_gate_label.setToolTip("Active after Run Selected Mode produced MODULE_TOO_LARGE warnings.")
        else:
            window._large_file_refactor_gate_label.setText("Large File Refactor Planner - inactive")
            window._large_file_refactor_gate_label.setToolTip("Run Selected Mode with Validate before using this planner.")
    _set_enabled(window, "_large_file_refactor_analyze_button", gate_open and selected)
    _set_enabled(window, "_large_file_refactor_copy_target_path_btn", selected)
    _set_enabled(window, "_large_file_refactor_browse_target_btn", gate_open)
    navigation = gate_open and len(candidates) > 1
    _set_enabled(window, "_large_file_refactor_prev_target_btn", navigation)
    _set_enabled(window, "_large_file_refactor_next_target_btn", navigation)
    counter = format_warning_target_counter(candidates, _current_row(window))
    if hasattr(window, "_large_file_refactor_target_count_label"):
        window._large_file_refactor_target_count_label.setText(counter)


def format_warning_target_counter(candidates: Sequence[object], index: int) -> str:
    """Format a warning-derived candidate counter."""
    if not candidates:
        return "0 large files"
    safe_index = max(0, min(index, len(candidates) - 1))
    candidate = candidates[safe_index]
    return f"{safe_index + 1}/{len(candidates)} | {candidate.line_count_physical} lines"


def _move_warning_target(window: object, step: int) -> None:
    """Move through warning-derived planner candidates."""
    candidates = getattr(window, "_large_file_refactor_planner_candidates", [])
    if not candidates:
        return
    next_row = (_current_row(window) + step) % len(candidates)
    window._large_file_refactor_candidate_table.selectRow(next_row)
    sync_warning_input_selection(window)


def _selected_validate_has_run(window: object, output_text: str) -> bool:
    """Return whether the Run Selected Mode validation output is available."""
    last_mode = str(getattr(window, "_last_mode_run", "") or "")
    finished_validate = "[finished] mode=validate" in output_text
    return last_mode == "validate" and finished_validate


def _row_for_relative_target(window: object, selected: str) -> int:
    """Find a candidate row by relative or absolute selected target."""
    selected_norm = selected.replace("\\", "/")
    for index, candidate in enumerate(getattr(window, "_large_file_refactor_planner_candidates", [])):
        if candidate.relative_path == selected_norm:
            return index
        if str(Path(candidate.path)).replace("\\", "/") == selected_norm:
            return index
    return -1


def _copy_target_path(window: object) -> None:
    """Copy selected target path to clipboard."""
    path = getattr(window, "_large_file_refactor_planner_selected_path", "")
    if not path:
        return
    QApplication.clipboard().setText(str(path))


def _inactive_message(window: object) -> str:
    """Return the inactive state message for the numbered target list."""
    if str(getattr(window, "_last_mode_run", "") or "") != "validate":
        return "Inactive. Run Selected Mode with Validate first."
    return "No WARNING MODULE_TOO_LARGE modules found in latest Validate output."


def _output_text(window: object) -> str:
    """Return Project Audit Results text."""
    output = getattr(window, "_output", None)
    return output.toPlainText() if output is not None else ""


def _root_text(window: object) -> str:
    """Return active project root text."""
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return str(Path.cwd())
    return edit.text().strip() or str(Path.cwd())


def _safe_size(path_text: str) -> int:
    """Return file size or zero when unavailable."""
    try:
        return Path(path_text).stat().st_size
    except OSError:
        return 0


def _current_row(window: object) -> int:
    """Return current table row safely."""
    table = getattr(window, "_large_file_refactor_candidate_table", None)
    if table is None:
        return 0
    return max(0, table.currentRow())


def _set_enabled(window: object, attr_name: str, enabled: bool) -> None:
    """Set enabled state on an optional widget."""
    widget = getattr(window, attr_name, None)
    if widget is not None:
        widget.setEnabled(enabled)


def _set_numbered_text(window: object, text: str) -> None:
    """Write the numbered target list when the widget exists."""
    output = getattr(window, "_large_file_refactor_numbered_targets", None)
    if output is not None:
        output.setPlainText(text)
