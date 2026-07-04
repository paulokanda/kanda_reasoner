# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py
"""Build the Project Reasoner tab-7 main window layout.

This helper belongs only to the V10 GUI / Reader box used by:

Seventh step: Ask AI about project

The layout is intentionally redesigned as a horizontal, two-zone interface so
tab 7 can use available horizontal screen space and reduce vertical compression.
No backend behavior is implemented here.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

__all__ = ["build_main_window_ui"]


def _make_widget_from_layout(layout: QHBoxLayout | QVBoxLayout) -> QWidget:
    """Return a QWidget containing a prepared layout."""
    widget = QWidget()
    widget.setLayout(layout)
    return widget


def _build_project_json_group(window: Any) -> QGroupBox:
    """Build the project JSON/profile control group."""
    group = QGroupBox("Project JSON / Profile")
    layout = QGridLayout(group)

    if not hasattr(window, "json_track_value_label"):
        window.json_track_value_label = QLabel("Not loaded")
    if not hasattr(window, "ensure_local_ai_json_button"):
        window.ensure_local_ai_json_button = QPushButton("Create Local-AI Copy")
    if not hasattr(window, "refresh_local_ai_json_button"):
        window.refresh_local_ai_json_button = QPushButton("Refresh Local-AI Copy")

    if not hasattr(window, "project_root_label"):
        window.project_root_label = QLabel("Project root:")
    window.project_root_label.setStyleSheet("color: #0B3D91; font-weight: bold;")

    layout.addWidget(window.project_root_label, 0, 0)
    layout.addWidget(window.project_root_edit, 0, 1, 1, 3)
    layout.addWidget(window.pick_project_root_button, 0, 4)
    layout.addWidget(window.run_analysis_button, 0, 5)

    layout.addWidget(QLabel("JSON file:"), 1, 0)
    layout.addWidget(window.json_path_edit, 1, 1, 1, 3)
    layout.addWidget(window.load_button, 1, 4)
    layout.addWidget(window.static_context_button, 1, 5)

    layout.addWidget(QLabel("Status:"), 2, 0)
    layout.addWidget(window.analysis_status_value_label, 2, 1)
    layout.addWidget(QLabel("Generated:"), 2, 2)
    layout.addWidget(window.analysis_output_json_value_label, 2, 3, 1, 3)

    layout.addWidget(QLabel("JSON track:"), 3, 0)
    layout.addWidget(window.json_track_value_label, 3, 1)
    layout.addWidget(QLabel("Local-AI JSON:"), 3, 2)
    layout.addWidget(window.ensure_local_ai_json_button, 3, 3)
    layout.addWidget(window.refresh_local_ai_json_button, 3, 4, 1, 2)

    layout.addWidget(QLabel("Detected:"), 4, 0)
    layout.addWidget(window.detected_profile_value_label, 4, 1)
    layout.addWidget(QLabel("Active:"), 4, 2)
    layout.addWidget(window.active_profile_value_label, 4, 3, 1, 3)

    layout.addWidget(QLabel("Override:"), 5, 0)
    layout.addWidget(window.profile_override_combo, 5, 1, 1, 4)
    layout.addWidget(window.reset_profile_override_button, 5, 5)

    layout.addWidget(QLabel("Static:"), 6, 0)
    layout.addWidget(window.static_context_summary_value_label, 6, 1)
    layout.addWidget(QLabel("Packaging:"), 6, 2)
    layout.addWidget(window.static_context_packaging_value_label, 6, 3)
    layout.addWidget(QLabel("Docs:"), 6, 4)
    layout.addWidget(window.static_context_docs_value_label, 6, 5)

    layout.addWidget(window.analysis_auto_load_checkbox, 7, 1, 1, 5)

    layout.setColumnStretch(1, 1)
    layout.setColumnStretch(3, 1)
    layout.setColumnStretch(5, 1)
    return group


def _build_runtime_group(window: Any) -> QGroupBox:
    """Build the local AI runtime control group."""
    group = QGroupBox("Local AI Runtime")
    layout = QGridLayout(group)

    layout.addWidget(QLabel("Cache dir:"), 0, 0)
    layout.addWidget(window.cache_dir_edit, 0, 1)
    layout.addWidget(window.pick_cache_dir_button, 0, 2)

    layout.addWidget(QLabel("Governance:"), 1, 0)
    layout.addWidget(window.governance_path_edit, 1, 1)
    layout.addWidget(window.pick_governance_button, 1, 2)

    if not hasattr(window, "local_ai_model_label"):
        window.local_ai_model_label = QLabel("Model:")

    layout.addWidget(window.local_ai_model_label, 2, 0)
    layout.addWidget(window.model_combo, 2, 1)
    layout.addWidget(window.refresh_models_button, 2, 2)

    layout.setColumnStretch(1, 1)
    return group


def _build_ask_group(window: Any) -> QGroupBox:
    """Build the question and answer-style control group."""
    group = QGroupBox("Ask Complex Architecture Questions")
    layout = QGridLayout(group)

    layout.addWidget(QLabel("Question:"), 0, 0)
    layout.addWidget(window.question_edit, 0, 1, 1, 5)
    layout.addWidget(window.ask_ai_button, 0, 6)
    layout.addWidget(window.clear_button, 0, 7)
    layout.addWidget(window.clear_memory_button, 0, 8)

    style_row = QHBoxLayout()
    style_row.addWidget(QLabel("Answer style:"))
    style_row.addWidget(window.prefer_code_radio)
    style_row.addWidget(window.prefer_prose_radio)
    style_row.addSpacing(16)
    style_row.addWidget(QLabel("Verbosity:"))
    style_row.addWidget(window.verbosity_combo)
    style_row.addSpacing(16)
    style_row.addWidget(window.debug_checkbox)
    style_row.addStretch()
    layout.addWidget(_make_widget_from_layout(style_row), 1, 1, 1, 8)

    quick_row = QHBoxLayout()
    quick_row.addWidget(window.help_button)
    quick_row.addSpacing(10)
    quick_row.addWidget(window.quick_startup_button)
    quick_row.addWidget(window.quick_topomap_button)
    quick_row.addWidget(window.quick_timeline_button)
    quick_row.addWidget(window.quick_responsibility_button)
    quick_row.addWidget(window.quick_uncertainty_button)
    quick_row.addStretch()
    layout.addWidget(_make_widget_from_layout(quick_row), 2, 1, 1, 8)

    layout.setColumnStretch(1, 1)
    layout.setColumnStretch(2, 1)
    layout.setColumnStretch(3, 1)
    return group


def _build_top_controls(window: Any) -> QSplitter:
    """Build the wide top control area for tab 7."""
    project_panel = QWidget()
    project_layout = QVBoxLayout(project_panel)
    project_layout.setContentsMargins(0, 0, 0, 0)
    project_layout.addWidget(_build_project_json_group(window))

    runtime_ask_panel = QWidget()
    runtime_ask_layout = QVBoxLayout(runtime_ask_panel)
    runtime_ask_layout.setContentsMargins(0, 0, 0, 0)
    runtime_ask_layout.addWidget(_build_runtime_group(window))
    runtime_ask_layout.addWidget(_build_ask_group(window))

    top_splitter = QSplitter(Qt.Horizontal)
    top_splitter.addWidget(project_panel)
    top_splitter.addWidget(runtime_ask_panel)
    top_splitter.setSizes([950, 820])
    return top_splitter


def _build_evidence_panel(window: Any) -> QWidget:
    """Build the left evidence/history panel."""
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.addWidget(QLabel("Conversation History"))
    layout.addWidget(window.history_list)
    layout.addWidget(QLabel("File Evidence"))
    layout.addWidget(window.file_evidence_list)
    layout.addWidget(QLabel("Symbol Evidence"))
    layout.addWidget(window.symbol_evidence_list)
    layout.addWidget(QLabel("Selected Detail"))
    layout.addWidget(window.detail_box)
    return panel


def _build_answer_panel(window: Any) -> QWidget:
    """Build the right answer/prompt/log panel."""
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.addWidget(QLabel("Local AI Answer"))
    layout.addWidget(window.answer_box, stretch=3)
    layout.addWidget(QLabel("Prompt / Evidence Pack"))
    layout.addWidget(window.prompt_preview, stretch=2)

    log_group = QGroupBox("Log")
    log_layout = QVBoxLayout(log_group)
    log_layout.addWidget(window.log_box)
    layout.addWidget(log_group, stretch=1)

    return panel


def _build_content_splitter(window: Any) -> QSplitter:
    """Build the lower evidence/answer splitter."""
    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(_build_evidence_panel(window))
    splitter.addWidget(_build_answer_panel(window))
    splitter.setSizes([700, 1100])
    return splitter


def build_main_window_ui(window: Any) -> None:
    """Build and attach the full Qt layout for tab 7."""
    central = QWidget()
    window.setCentralWidget(central)

    main_layout = QVBoxLayout(central)
    main_layout.addWidget(_build_top_controls(window), stretch=0)
    main_layout.addWidget(_build_content_splitter(window), stretch=1)
