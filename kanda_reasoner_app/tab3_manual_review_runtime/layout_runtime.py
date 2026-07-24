# project-path: kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py
"""Runtime implementation for the Tab 3 review layout."""

from __future__ import annotations

from importlib import import_module
from typing import Any


def _build_ui(window: object) -> None:
    """Build the Tab 3 window around widgets created by window_state."""
    QHBoxLayout, QSizePolicy, QSplitter, QVBoxLayout, QWidget = _qt_widgets(
        "QHBoxLayout", "QSizePolicy", "QSplitter", "QVBoxLayout", "QWidget"
    )

    central = QWidget()
    _relieve_horizontal_size_pressure(central, QSizePolicy)
    root_layout = QHBoxLayout(central)

    left_column = QWidget()
    _relieve_horizontal_size_pressure(left_column, QSizePolicy)
    left_layout = QVBoxLayout(left_column)
    left_layout.addWidget(_build_ai_group(window))
    left_layout.addWidget(_build_options_group(window))
    left_layout.addWidget(window._progress)
    left_layout.addWidget(_build_output_panel(window), 1)
    left_layout.addWidget(_build_report_group(window))

    right_column = QWidget()
    _relieve_horizontal_size_pressure(right_column, QSizePolicy)
    right_layout = QVBoxLayout(right_column)
    right_layout.addWidget(_build_review_panel(window), 1)

    column_splitter = QSplitter()
    _relieve_horizontal_size_pressure(column_splitter, QSizePolicy)
    column_splitter.addWidget(left_column)
    column_splitter.addWidget(right_column)
    column_splitter.setStretchFactor(0, 1)
    column_splitter.setStretchFactor(1, 1)
    column_splitter.setSizes([1, 1])
    column_splitter.setChildrenCollapsible(False)
    root_layout.addWidget(column_splitter, 1)

    window.setCentralWidget(central)


def _relieve_horizontal_size_pressure(widget: object, size_policy_cls: Any) -> None:
    """Allow a widget to shrink without forcing the main window wider."""
    set_minimum_width = getattr(widget, "setMinimumWidth", None)
    if callable(set_minimum_width):
        set_minimum_width(0)

    set_size_policy = getattr(widget, "setSizePolicy", None)
    if callable(set_size_policy):
        set_size_policy(size_policy_cls.Ignored, size_policy_cls.Expanding)

def _wire_events(window: object) -> None:
    """Connect Tab 3 widgets to their owner-window methods."""
    _connect(window._run_button, "clicked", window.run_selected_mode)
    _connect(window._stop_button, "clicked", _stop_running_selected_mode_slot(window))
    _connect(
        window._mode_combo,
        "currentTextChanged",
        lambda mode: _scan_only_runtime().refresh_selected_mode_controls(window, mode),
    )
    _connect(window._browse_root_button, "clicked", window.browse_root)
    _connect(window._browse_target_button, "clicked", window.browse_target_path)
    _connect(window._clear_target_button, "clicked", _clear_target_path(window))
    _connect(window._browse_report_button, "clicked", window.browse_report_path)
    _connect(window._save_report_button, "clicked", _report_io_slot(window, "save_report"))
    _connect(window._load_report_button, "clicked", _report_io_slot(window, "load_report"))
    _connect(window._copy_report_button, "clicked", _report_io_slot(window, "copy_report"))
    _connect(window._refresh_models_button, "clicked", window.refresh_models)
    _connect(window._load_config_button, "clicked", window.load_config_from_file)
    _connect(window._save_config_button, "clicked", window.save_config_to_file)
    _connect(window._ai_enabled_checkbox, "toggled", window._set_ai_controls_enabled)
    _connect(window._scope_combo, "currentTextChanged", window._update_scope_controls)
    _ai_controls_runtime().wire_events(window)
    _connect(window._review_filter_combo, "currentTextChanged", window._populate_review_list)
    _connect(window._review_list, "currentItemChanged", window._show_review_item_details)
    _connect(window._review_list, "itemDoubleClicked", _open_review_window_slot(window))
    _connect(window._review_generate_visible_drafts_button, "clicked", _bulk_draft_slot(window, "visible"))
    _connect(window._review_generate_all_drafts_button, "clicked", _bulk_draft_slot(window, "all"))
    _connect(window._review_undo_bulk_drafts_button, "clicked", _bulk_draft_undo_slot(window))
    _inline_corrector_runtime().wire_inline_corrector_events(window)

def _set_ai_controls_enabled(window: object, enabled: bool) -> None:
    """Enable or disable provider-specific AI controls."""
    _ai_controls_runtime().apply_control_state(window, enabled)


def _build_project_group(window: object) -> Any:
    """Return a hidden compatibility placeholder for the retired body Project group."""
    QWidget = _qt_widgets("QWidget")[0]

    group = QWidget()
    group.setVisible(False)
    return group

def _build_options_group(window: object) -> Any:
    """Return the scan scope and run options group."""
    QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout = _qt_widgets(
        "QGroupBox", "QHBoxLayout", "QLabel", "QPushButton", "QVBoxLayout"
    )

    _scan_only_runtime().configure_scan_diff_write_controls(window)

    group = QGroupBox("Run Options")
    layout = QVBoxLayout(group)

    mode_row = QHBoxLayout()
    mode_row.addWidget(QLabel("Mode"))
    mode_row.addWidget(window._mode_combo)
    mode_row.addWidget(window._tab1_audit_docstring_radio)
    mode_row.addSpacing(16)
    mode_row.addWidget(QLabel("Scope"))
    mode_row.addWidget(window._scope_combo)
    mode_row.addWidget(window._target_path_edit, 1)
    mode_row.addWidget(window._browse_target_button)
    mode_row.addWidget(window._clear_target_button)
    layout.addLayout(mode_row)

    include_row = QHBoxLayout()
    include_row.addWidget(window._module_checkbox)
    include_row.addWidget(window._class_checkbox)
    include_row.addWidget(window._function_checkbox)
    include_row.addWidget(window._file_address_checkbox)
    include_row.addWidget(window._confirm_write_checkbox)
    include_row.addStretch(1)
    layout.addLayout(include_row)

    workers_row = QHBoxLayout()
    workers_row.addWidget(QLabel("Workers"))
    workers_row.addWidget(window._workers_spin)
    workers_row.addSpacing(16)
    window._run_button = QPushButton("Run selected mode")
    window._stop_button = QPushButton("Stop Running Selected Mode")
    window._stop_button.setEnabled(False)
    workers_row.addWidget(window._run_button)
    workers_row.addWidget(window._stop_button)
    workers_row.addStretch(1)
    layout.addLayout(workers_row)
    _scan_only_runtime().refresh_selected_mode_controls(window)

    return group

def _build_ai_group(window: object) -> Any:
    """Return the shared AI Assistant configuration group."""
    return _ai_controls_runtime().build_ai_group(window)


def _ensure_ai_docstring_verbosity_combo(window: object, combo_cls: Any) -> None:
    """Ensure the Local AI group has a docstring verbosity combo."""
    combo = getattr(window, "_ai_docstring_verbosity_combo", None)
    if combo is not None:
        return
    combo = combo_cls()
    add_items = getattr(combo, "addItems", None)
    if callable(add_items):
        add_items(["Concise", "Balanced", "Detailed"])
    set_current = getattr(combo, "setCurrentText", None)
    if callable(set_current):
        set_current("Concise")
    window._ai_docstring_verbosity_combo = combo

def _build_report_group(window: object) -> Any:
    """Return the report import, export, copy, and path controls group."""
    QGroupBox, QHBoxLayout, QLabel, QPushButton = _qt_widgets(
        "QGroupBox", "QHBoxLayout", "QLabel", "QPushButton"
    )

    group = QGroupBox("Report")
    layout = QHBoxLayout(group)
    layout.addWidget(QLabel("Report path"))
    layout.addWidget(window._report_path_edit, 1)
    layout.addWidget(window._browse_report_button)

    window._save_report_button = QPushButton("Save report")
    window._load_report_button = QPushButton("Load report")
    window._copy_report_button = QPushButton("Copy report")
    layout.addWidget(window._save_report_button)
    layout.addWidget(window._load_report_button)
    layout.addWidget(window._copy_report_button)
    return group

def _build_output_panel(window: object) -> Any:
    """Return the run output panel."""
    QGroupBox, QVBoxLayout = _qt_widgets("QGroupBox", "QVBoxLayout")

    group = QGroupBox("Output")
    layout = QVBoxLayout(group)
    layout.addWidget(window._output)
    return group

def _build_review_panel(window: object) -> Any:
    """Return the report review and inline correction tab panel."""
    (
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QPlainTextEdit,
        QSizePolicy,
        QPushButton,
        QSplitter,
        QTabWidget,
        QVBoxLayout,
        QWidget,
    ) = _qt_widgets(
        "QGroupBox",
        "QHBoxLayout",
        "QLabel",
        "QPlainTextEdit",
        "QSizePolicy",
        "QPushButton",
        "QSplitter",
        "QTabWidget",
        "QVBoxLayout",
        "QWidget",
    )

    tabs = QTabWidget()
    _relieve_horizontal_size_pressure(tabs, QSizePolicy)
    review_tab = QWidget()
    _relieve_horizontal_size_pressure(review_tab, QSizePolicy)
    review_layout = QVBoxLayout(review_tab)

    window._review_previous_button = QPushButton("Previous")
    window._review_next_button = QPushButton("Next")
    window._review_reset_button = QPushButton("Reset")
    window._review_original_snippet = QPlainTextEdit()
    window._review_original_snippet.setReadOnly(True)
    _relieve_horizontal_size_pressure(window._review_original_snippet, QSizePolicy)
    window._review_original_snippet.setLineWrapMode(QPlainTextEdit.WidgetWidth)

    before_group = QGroupBox("Before Correction")
    _relieve_horizontal_size_pressure(before_group, QSizePolicy)
    before_layout = QVBoxLayout(before_group)
    before_layout.addWidget(window._review_summary)

    filter_row = QHBoxLayout()
    filter_row.addWidget(QLabel("Filter"))
    filter_row.addWidget(window._review_filter_combo)
    filter_row.addStretch(1)
    before_layout.addLayout(filter_row)

    navigation_row = QHBoxLayout()
    navigation_row.addWidget(window._review_previous_button)
    navigation_row.addWidget(window._review_next_button)
    navigation_row.addWidget(window._review_reset_button)
    navigation_row.addStretch(1)
    before_layout.addLayout(navigation_row)
    before_layout.addWidget(window._review_list, 2)
    before_layout.addWidget(window._review_original_snippet, 3)

    window._review_engine_status_label = QLabel("HEURISTIC CORRECTION")
    window._review_engine_status_label.setStyleSheet(
        "font-weight: bold; color: green;"
    )

    window._review_draft_status_label = QLabel("NO DRAFT GENERATED")
    window._review_draft_status_label.setStyleSheet(
        "font-weight: bold; color: green;"
    )

    window._review_generate_draft_button = QPushButton("Generate Draft")
    window._review_generate_visible_drafts_button = QPushButton("Generate Visible Drafts")
    window._review_generate_all_drafts_button = QPushButton("Generate All Drafts")
    window._review_stop_ai_drafts_button = QPushButton("Stop AI Drafts")
    window._review_stop_ai_drafts_button.setEnabled(False)
    window._review_undo_bulk_drafts_button = QPushButton("Undo Last Bulk Drafts")
    window._review_save_change_button = QPushButton("Save Review Decision")
    window._review_approve_row_button = QPushButton("Approve Row")
    window._review_reject_row_button = QPushButton("Reject Row")
    window._review_undo_button = QPushButton("Undo Row Change")
    window._review_save_all_button = QPushButton("Approve Visible Rows")
    window._review_corrected_snippet = QPlainTextEdit()
    window._review_corrected_snippet.setReadOnly(True)
    _relieve_horizontal_size_pressure(window._review_corrected_snippet, QSizePolicy)
    window._review_corrected_snippet.setLineWrapMode(QPlainTextEdit.WidgetWidth)
    window._review_details = QPlainTextEdit()
    _relieve_horizontal_size_pressure(window._review_details, QSizePolicy)
    window._review_details.setReadOnly(True)
    window._review_details.hide()
    after_group = QGroupBox("After Correction")
    _relieve_horizontal_size_pressure(after_group, QSizePolicy)
    after_layout = QVBoxLayout(after_group)
    draft_action_row = QHBoxLayout()
    draft_action_row.addWidget(window._review_engine_status_label)
    draft_action_row.addSpacing(16)
    draft_action_row.addWidget(window._review_generate_draft_button)
    draft_action_row.addWidget(window._review_generate_visible_drafts_button)
    draft_action_row.addWidget(window._review_generate_all_drafts_button)
    draft_action_row.addWidget(window._review_stop_ai_drafts_button)
    draft_action_row.addWidget(window._review_undo_bulk_drafts_button)
    draft_action_row.addStretch(1)
    after_layout.addLayout(draft_action_row)
    review_decision_row = QHBoxLayout()
    review_decision_row.addWidget(window._review_save_change_button)
    review_decision_row.addWidget(window._review_approve_row_button)
    review_decision_row.addWidget(window._review_reject_row_button)
    review_decision_row.addWidget(window._review_undo_button)
    review_decision_row.addWidget(window._review_save_all_button)
    review_decision_row.addStretch(1)
    after_layout.addLayout(review_decision_row)
    after_layout.addWidget(window._review_draft_status_label)
    after_layout.addWidget(window._review_corrected_snippet, 1)

    review_splitter = QSplitter()
    _relieve_horizontal_size_pressure(review_splitter, QSizePolicy)
    review_splitter.addWidget(before_group)
    review_splitter.addWidget(after_group)
    review_splitter.setStretchFactor(0, 1)
    review_splitter.setStretchFactor(1, 1)
    review_splitter.setSizes([1, 1])
    review_layout.addWidget(review_splitter, 1)

    tabs.addTab(review_tab, "Review and Correct Missing Docstrings")
    return tabs

def _bulk_draft_slot(window: object, scope: str) -> Any:
    """Return a slot that generates drafts for one bulk review scope."""
    def _run() -> None:
        module = import_module(
            "kanda_reasoner_app.tab3_manual_review_runtime.review_bulk_drafts_runtime"
        )
        module.generate_bulk_drafts(window, scope)

    return _run


def _bulk_draft_undo_slot(window: object) -> Any:
    """Return a slot that undoes the last bulk draft-generation run."""
    def _run() -> None:
        module = import_module(
            "kanda_reasoner_app.tab3_manual_review_runtime.review_bulk_drafts_runtime"
        )
        module.undo_last_bulk_draft_generation(window)

    return _run


def _inline_corrector_runtime() -> Any:
    """Load the Tab 3 inline corrector runtime lazily."""
    module_name = (
        "kanda_reasoner_app.tab3_manual_review_runtime"
        + ".inline_corrector_runtime"
    )
    return import_module(module_name)


def _scan_only_runtime() -> Any:
    """Load the Tab 3 scan-only workflow runtime lazily."""
    module_name = (
        "kanda_reasoner_app.tab3_manual_review_runtime"
        + ".scan_only_workflow"
    )
    return import_module(module_name)


def _report_io_slot(window: object, action_name: str) -> Any:
    """Return a slot that executes one Tab 3 report IO action."""
    def _run() -> None:
        module = import_module(
            "kanda_reasoner_app.tab3_manual_review_runtime.report_io_runtime"
        )
        action = getattr(module, action_name)
        action(window)

    return _run


def _stop_running_selected_mode_slot(window: object) -> Any:
    """Return a slot that requests cancellation of the active Tab 3 run."""
    def _stop() -> None:
        package = (
            "kanda_reasoner_app."
            + "insert_missing_docstrings"
            + "_"
            + "gui.insert_missing_docstrings"
            + "_"
            + "gui_help.run_controls"
        )
        module = import_module(package)
        module.stop_running_selected_mode(window)

    return _stop


def _clear_target_path(window: object) -> Any:
    """Return a slot that clears the target path and saves preferences."""
    def _clear() -> None:
        window._target_path_edit.clear()
        window._save_prefs()

    return _clear


def _open_review_window_slot(window: object) -> Any:
    """Return a slot that opens one manual-review dialog."""
    def _open(item: Any = None) -> None:
        package = (
            "kanda_reasoner_app."
            + "insert_missing_docstrings"
            + "_"
            + "gui.insert_missing_docstrings"
            + "_"
            + "gui_help.report_review_panel"
        )
        module = import_module(package)
        module.open_docstring_review_window(window, item)

    return _open


def _connect(widget: object, signal_name: str, slot: Any) -> None:
    """Connect a Qt signal when the signal is present."""
    signal = getattr(widget, signal_name, None)
    connect = getattr(signal, "connect", None)
    if callable(connect):
        connect(slot)




def _ai_controls_runtime() -> Any:
    """Return the shared Docstring Assistant AI controls owner."""
    return import_module(
        "kanda_reasoner_app.tab3_manual_review_runtime.ai_web_controls_runtime"
    )

def _qt_widgets(*names: str) -> tuple[Any, ...]:
    """Return Qt widget classes lazily."""
    module = import_module("PySide" + "6.QtWidgets")
    return tuple(getattr(module, name) for name in names)
