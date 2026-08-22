# project-path: kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py
"""Nested tab layout helpers for Audit Project and Architecture Review."""
from __future__ import annotations

from importlib import import_module
from typing import Callable

from .architecture_review_mode_ui import bind_mode_action_button
from .architecture_finding_review_gui import (
    build_dismissed_findings_page,
    install_architecture_findings_review,
)
from .audit_project_sibling_tabs import (
    _build_audit_project_sibling_tabs,
)

from kanda_reasoner_app.manage_architecture.architecture_audit_external_ai import (
    handoff_audit_results_to_external_ai,
)
from kanda_reasoner_app.manage_architecture.architecture_review_card_lifecycle import (
    bind_architecture_review_card_lifecycle,
)
from kanda_reasoner_app.manage_architecture.ast_split_web_ai_gui import (
    add_ast_split_web_ai_risk_repair_button,
    bind_ast_split_web_ai_single_output,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_audit_planner_sync import (
    sync_planner_from_ast_audit_target,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.gui_shell import (
    build_large_file_refactor_planner_page,
    refresh_large_file_refactor_planner_status,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui import (
    build_large_file_refactor_workbench_page,
)
from kanda_reasoner_app.manage_architecture.warning_resolver_cancel_gui import (
    cancel_warning_resolver,
)
from kanda_reasoner_app.manage_architecture.warning_resolver_split_control import (
    build_warning_resolver_split_control,
)

__all__ = ["build_architecture_review_ui"]

_AUDIT_PROJECT_ARCHITECTURE_TAB_LABEL = "Architecture Review"
_ARCHITECTURE_REVIEW_CHILD_TAB_LABELS = (
    "Check Update Architecture",
    "Dismissed Findings",
    "Large Module AST Split Audit",
    "Large File Refactor Planner",
    "Large File Refactor WorkBench",
)


def _qt_widgets() -> object:
    """Load Qt widgets only when the Architecture GUI is being built."""
    return import_module("PySide6.QtWidgets")


def _contain_subtab_horizontal_size_pressure(window: object) -> None:
    """Prevent hidden nested pages from widening the host GUI."""
    QSizePolicy = _qt_widgets().QSizePolicy
    containers = (
        window._audit_project_subtab_widget,
        window._architecture_review_page,
        window._architecture_review_subtab_stack,
        window._architecture_review_general_page,
        window._architecture_review_dismissed_findings_page,
        window._architecture_review_split_page,
        window._architecture_review_refactor_planner_page,
        window._architecture_review_refactor_workbench_page,
        window._engineering_safety_page,
        window._engineering_safety_page.engineering_safety_audit_tabs,
        window._engineering_safety_page.engineering_safety_full_audit_page,
        window._engineering_safety_page.engineering_safety_pontual_audit_page,
        window._engineering_diagnostics_page,
        window._workflow_review_page,
        window._workflow_review_page.centralWidget(),
    )
    for container in containers:
        container.setMinimumSize(0, 0)
        container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)


def build_architecture_review_ui(
    window: object,
    install_ai_controls: Callable[[object, object], None],
) -> None:
    """Build Audit Project with an Architecture Review child-tab hierarchy."""
    QtWidgets = _qt_widgets()
    QStatusBar = QtWidgets.QStatusBar
    QTabWidget = QtWidgets.QTabWidget
    QVBoxLayout = QtWidgets.QVBoxLayout
    QWidget = QtWidgets.QWidget

    central = QWidget(window)
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(8)

    window._audit_project_subtab_widget = QTabWidget(central)
    window._audit_project_subtab_widget.setObjectName(
        "audit_project_subtab_widget"
    )
    window._architecture_review_page = QWidget(
        window._audit_project_subtab_widget
    )
    architecture_layout = QVBoxLayout(window._architecture_review_page)
    architecture_layout.setContentsMargins(0, 0, 0, 0)
    architecture_layout.setSpacing(8)

    window._architecture_review_subtab_stack = QTabWidget(
        window._architecture_review_page
    )
    window._architecture_review_subtab_stack.setObjectName(
        "architecture_review_child_tab_widget"
    )
    window._architecture_review_general_page = _build_general_audit_page(
        window,
        install_ai_controls,
    )
    window._architecture_review_dismissed_findings_page = (
        build_dismissed_findings_page(window)
    )
    window._architecture_review_split_page = _build_split_audit_page(window)
    window._architecture_review_refactor_planner_page = (
        build_large_file_refactor_planner_page(window)
    )
    window._architecture_review_refactor_workbench_page = (
        build_large_file_refactor_workbench_page(window)
    )

    child_pages = (
        window._architecture_review_general_page,
        window._architecture_review_dismissed_findings_page,
        window._architecture_review_split_page,
        window._architecture_review_refactor_planner_page,
        window._architecture_review_refactor_workbench_page,
    )
    for page, label in zip(
        child_pages,
        _ARCHITECTURE_REVIEW_CHILD_TAB_LABELS,
        strict=True,
    ):
        window._architecture_review_subtab_stack.addTab(page, label)

    architecture_layout.addWidget(
        window._architecture_review_subtab_stack,
        1,
    )
    window._audit_project_subtab_widget.addTab(
        window._architecture_review_page,
        _AUDIT_PROJECT_ARCHITECTURE_TAB_LABEL,
    )
    _build_audit_project_sibling_tabs(window)
    layout.addWidget(window._audit_project_subtab_widget, 1)
    _contain_subtab_horizontal_size_pressure(window)

    window._architecture_review_subtab_stack.currentChanged.connect(
        lambda index: _activate_subtab(window, index)
    )
    _activate_subtab(window, 0)
    bind_architecture_review_card_lifecycle(window)

    window.setStatusBar(QStatusBar(window))
    window.statusBar().showMessage("Ready")


def _build_general_audit_page(
    window: object,
    install_ai_controls: Callable[[object, object], None],
) -> object:
    """Build the check-and-update and project-audit page."""
    QtWidgets = _qt_widgets()
    QCheckBox = QtWidgets.QCheckBox
    QComboBox = QtWidgets.QComboBox
    QHBoxLayout = QtWidgets.QHBoxLayout
    QLabel = QtWidgets.QLabel
    QPlainTextEdit = QtWidgets.QPlainTextEdit
    QPushButton = QtWidgets.QPushButton
    QSizePolicy = QtWidgets.QSizePolicy
    QVBoxLayout = QtWidgets.QVBoxLayout
    QWidget = QtWidgets.QWidget

    page = QWidget()
    page_layout = QVBoxLayout(page)
    page_layout.setContentsMargins(0, 0, 0, 0)
    page_layout.setSpacing(8)

    window._mode_quick_buttons = {}
    controls_row = QHBoxLayout()
    controls_row.setContentsMargins(0, 0, 0, 0)
    controls_row.setSpacing(6)
    window._run_options_toolbar_widget = QWidget(page)
    window._run_options_toolbar_widget.setObjectName(
        "architecture_review_run_options_toolbar_widget"
    )
    run_options_layout = QHBoxLayout(window._run_options_toolbar_widget)
    run_options_layout.setContentsMargins(0, 0, 0, 0)
    run_options_layout.setSpacing(6)

    window._run_button = QPushButton("Validate Project")
    window._run_button.setStyleSheet(
        "color: #008000; font-weight: bold; border: 1px solid #008000; "
        "padding: 2px 6px;"
    )
    window._run_button.clicked.connect(window.run_selected_mode)
    window._cancel_operation_button = QPushButton("Cancel")
    window._cancel_operation_button.setObjectName(
        "architecture_review_cancel_operation_button"
    )
    window._cancel_operation_button.setToolTip(
        "Cancel the currently running Architecture operation. Hard cancellation "
        "may stop a worker thread mid-run."
    )
    window._cancel_operation_button.setStyleSheet(
        "QPushButton { color: #C2185B; font-weight: bold; } "
        "QPushButton:disabled { color: #9A9A9A; }"
    )
    window._cancel_operation_button.setEnabled(False)
    window._cancel_operation_button.clicked.connect(window.cancel_running_operation)
    window._run_options_toolbar_label = QLabel("Run options")
    window._mode_toolbar_label = QLabel("Mode")
    window._mode_combo = QComboBox()
    window._mode_combo.setMinimumWidth(105)
    window._mode_combo.setMaximumWidth(130)
    window._mode_combo.addItems(["validate", "diff", "scan", "write"])
    window._mode_combo.setCurrentText("validate")
    bind_mode_action_button(window._mode_combo, window._run_button)
    window._run_mode_selector_widget = QWidget(window._run_options_toolbar_widget)
    window._run_mode_selector_widget.setObjectName(
        "architecture_review_run_mode_selector_group"
    )
    window._run_mode_selector_widget.setStyleSheet(
        "QWidget#architecture_review_run_mode_selector_group {"
        " border: 1px solid #B7BCC5; border-radius: 4px; }"
    )
    run_mode_selector_layout = QHBoxLayout(window._run_mode_selector_widget)
    run_mode_selector_layout.setContentsMargins(6, 0, 6, 0)
    run_mode_selector_layout.setSpacing(4)
    run_mode_selector_layout.addWidget(window._run_options_toolbar_label)
    run_mode_selector_layout.addWidget(window._mode_toolbar_label)
    run_mode_selector_layout.addWidget(window._mode_combo)
    window._strict_write_checkbox = QCheckBox("Require confirm before write")
    window._strict_write_checkbox.setChecked(True)

    run_options_layout.addWidget(window._run_button)
    run_options_layout.addWidget(window._cancel_operation_button)
    run_options_layout.addWidget(window._run_mode_selector_widget)
    run_options_layout.addWidget(window._strict_write_checkbox)
    install_ai_controls(window, run_options_layout)
    controls_row.addWidget(window._run_options_toolbar_widget, 1)

    window._output = QPlainTextEdit()
    window._output.setReadOnly(True)
    window._output.setLineWrapMode(QPlainTextEdit.NoWrap)
    window._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    clear_button = QPushButton("Clear Audit Results")
    clear_button.clicked.connect(window._output.clear)
    controls_row.addWidget(clear_button, 0)
    save_button = QPushButton("Save Audit Results")
    save_button.clicked.connect(window.save_output)
    controls_row.addWidget(save_button, 0)
    help_button = QPushButton("Mode Help")
    help_button.clicked.connect(window.show_mode_help)
    controls_row.addWidget(help_button, 0)
    page_layout.addLayout(controls_row)

    audit_header = QHBoxLayout()
    window._audit_results_label = QLabel("Project Audit Results")
    window._audit_results_label.setStyleSheet(
        "color: #000000; font-weight: bold;"
    )
    audit_header.addWidget(window._audit_results_label)
    window._include_refactor_report_checkbox = QCheckBox(
        "Include latest Refactor Report evidence"
    )
    window._include_refactor_report_checkbox.setChecked(True)
    window._include_refactor_report_checkbox.setToolTip(
        "Run Refactor Report before copying and append compact evidence for AI."
    )
    audit_header.addWidget(window._include_refactor_report_checkbox)
    window._copy_audit_btn = QPushButton("Copy Audit Results")
    window._copy_audit_btn.clicked.connect(window.copy_audit_to_clipboard)
    audit_header.addWidget(window._copy_audit_btn)
    window._external_audit_btn = QPushButton("Copy and Open External AI")
    window._external_audit_btn.setObjectName("audit_project_external_ai_handoff")
    window._external_audit_btn.clicked.connect(
        lambda: handoff_audit_results_to_external_ai(window)
    )
    audit_header.addWidget(window._external_audit_btn)
    resolver_control = build_warning_resolver_split_control(
        page,
        heuristic_callback=window.run_warning_heuristic_resolver,
        model_callback=window.run_warning_model_resolver,
        web_callback=window.run_warning_web_ai_resolver,
        cancel_callback=lambda: cancel_warning_resolver(window),
    )
    window._warning_heuristic_resolver_btn = resolver_control.main_button
    window._warning_resolver_cancel_btn = resolver_control.cancel_button
    window._warning_heuristic_resolver_btn.setObjectName(
        "architecture_review_warning_heuristic_resolver_button"
    )
    window._warning_heuristic_resolver_btn.setText("Warning Heuristic Resolver")
    audit_header.addWidget(resolver_control.container)
    window._copy_large_module_protocol_btn = QPushButton(
        "Large Module Creation/Refactor Protocol"
    )
    window._copy_large_module_protocol_btn.clicked.connect(
        window.copy_large_module_protocol_to_clipboard
    )
    audit_header.addWidget(window._copy_large_module_protocol_btn)
    audit_header.addStretch(1)
    page_layout.addLayout(audit_header)

    install_architecture_findings_review(window, page_layout, window._output)
    return page


def _build_split_audit_page(window: object) -> object:
    """Build the Large Module AST Split Audit page."""
    QtWidgets = _qt_widgets()
    QButtonGroup = QtWidgets.QButtonGroup
    QHBoxLayout = QtWidgets.QHBoxLayout
    QLabel = QtWidgets.QLabel
    QLineEdit = QtWidgets.QLineEdit
    QPlainTextEdit = QtWidgets.QPlainTextEdit
    QPushButton = QtWidgets.QPushButton
    QRadioButton = QtWidgets.QRadioButton
    QSizePolicy = QtWidgets.QSizePolicy
    QVBoxLayout = QtWidgets.QVBoxLayout
    QWidget = QtWidgets.QWidget

    page = QWidget()
    page_layout = QVBoxLayout(page)
    page_layout.setContentsMargins(0, 0, 0, 0)
    page_layout.setSpacing(8)

    target_row = QHBoxLayout()
    target_row.setContentsMargins(0, 0, 0, 0)
    target_row.setSpacing(6)
    window._large_module_split_label = QLabel("Large Module AST Split Audit")
    window._large_module_split_label.setStyleSheet(
        "color: #6A1B9A; font-weight: bold; padding: 4px 8px;"
    )
    target_row.addWidget(window._large_module_split_label)
    target_row.addWidget(QLabel("Target .py:"))
    window._large_module_target_edit = QLineEdit("")
    window._large_module_target_edit.setPlaceholderText(
        "Run Validate to populate oversized module targets"
    )
    window._large_module_target_edit.setMinimumWidth(260)
    window._large_module_target_edit.setMaximumWidth(720)
    target_row.addWidget(window._large_module_target_edit, stretch=1)
    window._copy_large_module_target_path_btn = QPushButton("Copy Path")
    window._copy_large_module_target_path_btn.setObjectName(
        "architecture_review_copy_large_module_target_path_button"
    )
    window._copy_large_module_target_path_btn.setToolTip(
        "Copy the selected Large Module AST Audit target .py path to clipboard"
    )
    window._copy_large_module_target_path_btn.clicked.connect(
        window.copy_large_module_target_path_to_clipboard
    )
    target_row.addWidget(window._copy_large_module_target_path_btn)
    window._browse_large_module_target_btn = QPushButton("Browse Target...")
    window._browse_large_module_target_btn.clicked.connect(
        window.browse_large_module_target
    )
    target_row.addWidget(window._browse_large_module_target_btn)
    page_layout.addLayout(target_row)

    target_actions_row = QHBoxLayout()
    target_actions_row.setContentsMargins(0, 0, 0, 0)
    target_actions_row.setSpacing(6)
    target_actions_row.addWidget(QLabel("Large modules:"))
    window._large_module_target_count_label = QLabel("0 large modules")
    window._large_module_target_count_label.setMinimumWidth(120)
    target_actions_row.addWidget(window._large_module_target_count_label)
    window._prev_large_module_target_btn = QPushButton("<-")
    window._prev_large_module_target_btn.setToolTip(
        "Previous oversized module from latest Project Audit Results"
    )
    window._prev_large_module_target_btn.clicked.connect(
        lambda: window._move_large_module_target(-1)
    )
    target_actions_row.addWidget(window._prev_large_module_target_btn)
    window._next_large_module_target_btn = QPushButton("->")
    window._next_large_module_target_btn.setToolTip(
        "Next oversized module from latest Project Audit Results"
    )
    window._next_large_module_target_btn.clicked.connect(
        lambda: window._move_large_module_target(1)
    )
    target_actions_row.addWidget(window._next_large_module_target_btn)
    window._run_large_module_split_btn = QPushButton("Run AST Split Audit")
    window._run_large_module_split_btn.clicked.connect(
        window.run_large_module_split_audit_from_gui
    )
    target_actions_row.addWidget(window._run_large_module_split_btn)
    window._copy_large_module_split_btn = QPushButton("Copy Split Handoff for AI")
    window._copy_large_module_split_btn.clicked.connect(
        window.copy_large_module_split_handoff
    )
    target_actions_row.addWidget(window._copy_large_module_split_btn)
    add_ast_split_web_ai_risk_repair_button(window, target_actions_row)
    target_actions_row.addStretch(1)
    window._large_module_target_edit.textChanged.connect(
        lambda _text="": window._sync_large_module_target_controls()
    )
    page_layout.addLayout(target_actions_row)

    classifier_row = QHBoxLayout()
    classifier_row.setContentsMargins(0, 0, 0, 0)
    classifier_row.setSpacing(8)
    classifier_row.addWidget(QLabel("Safety classifier:"))
    window._large_module_split_classifier_group = QButtonGroup(page)
    window._large_module_split_classifier_ast_radio = QRadioButton("AST heuristic")
    window._large_module_split_classifier_ast_radio.setChecked(True)
    window._large_module_split_classifier_ast_radio.setToolTip(
        "Use deterministic built-in AST evidence for safe/risk labeling."
    )
    window._large_module_split_classifier_tool_radio = QRadioButton(
        "Static Tools (AST + Ruff)"
    )
    window._large_module_split_classifier_tool_radio.setToolTip(
        "Use AST evidence plus read-only Ruff JSON lint evidence."
    )
    window._large_module_split_classifier_group.addButton(
        window._large_module_split_classifier_ast_radio
    )
    window._large_module_split_classifier_group.addButton(
        window._large_module_split_classifier_tool_radio
    )
    classifier_row.addWidget(window._large_module_split_classifier_ast_radio)
    classifier_row.addWidget(window._large_module_split_classifier_tool_radio)
    window._large_module_refactor_safety_label = QLabel(
        "Refactor safety: not audited"
    )
    window._large_module_refactor_safety_label.setStyleSheet(
        "color: #555555; font-weight: bold; padding: 4px 8px;"
    )
    classifier_row.addWidget(window._large_module_refactor_safety_label)
    classifier_row.addStretch(1)
    page_layout.addLayout(classifier_row)

    window._large_module_split_output = QPlainTextEdit()
    window._large_module_split_output.setReadOnly(False)
    window._large_module_split_output.setLineWrapMode(QPlainTextEdit.NoWrap)
    window._large_module_split_output.setSizePolicy(
        QSizePolicy.Expanding,
        QSizePolicy.Expanding,
    )
    page_layout.addWidget(window._large_module_split_output, 1)
    bind_ast_split_web_ai_single_output(window)
    window._sync_large_module_target_controls()
    return page


def _activate_subtab(window: object, index: int) -> None:
    """Activate one Architecture Review child tab and refresh its context."""
    stack = getattr(window, "_architecture_review_subtab_stack", None)
    if index == 1:
        sync_ast_target = getattr(
            window,
            "_sync_largest_module_target_from_latest_run_results",
            None,
        )
        if callable(sync_ast_target):
            sync_ast_target()
    if index == 2:
        sync_planner_from_ast_audit_target(window)
        refresh_large_file_refactor_planner_status(window)
    if stack is not None and stack.currentIndex() != index:
        stack.setCurrentIndex(index)

