# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py
"""Build the Local AI tab as a professional sidebar-and-chat surface.

This module owns presentation only. Existing controls, callbacks, local-model
runtime, retrieval, memory, analysis, and project-JSON behavior remain owned by
their current controllers.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStyle,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_theme import (
    LOCAL_AI_THEME,
)

__all__ = ["build_main_window_ui"]


def _muted_label(text: str) -> QLabel:
    """Return one consistently styled secondary label."""
    label = QLabel(text)
    label.setObjectName("localAIMuted")
    label.setWordWrap(True)
    return label


def _section(title: str) -> tuple[QFrame, QVBoxLayout]:
    """Return one low-noise sidebar section."""
    frame = QFrame()
    frame.setObjectName("localAISection")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)
    heading = QLabel(title)
    heading.setObjectName("localAISectionTitle")
    layout.addWidget(heading)
    return frame, layout


def _force_opaque_combo(combo: QComboBox) -> None:
    """Force opaque popup and viewport surfaces across native Qt styles."""
    popup = combo.view()
    viewport = popup.viewport()
    popup.setStyleSheet(
        "QAbstractItemView {"
        "background-color: #1d2128;"
        "color: #f4f6f8;"
        "border: 1px solid #3d4552;"
        "outline: 0;"
        "selection-background-color: #2f4f48;"
        "selection-color: #ffffff;"
        "}"
    )
    viewport.setStyleSheet("background-color: #1d2128;")
    for surface in (popup, viewport):
        surface.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        surface.setAutoFillBackground(True)
        palette = surface.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#1d2128"))
        palette.setColor(QPalette.ColorRole.Window, QColor("#1d2128"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#f4f6f8"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#2f4f48"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        surface.setPalette(palette)


def _configure_controls(window: Any) -> None:
    """Apply presentation metadata without changing controller contracts."""
    if not hasattr(window, "json_track_value_label"):
        window.json_track_value_label = QLabel("Not loaded")
    if not hasattr(window, "ensure_local_ai_json_button"):
        window.ensure_local_ai_json_button = QPushButton("Create Local-AI Copy")
    if not hasattr(window, "refresh_local_ai_json_button"):
        window.refresh_local_ai_json_button = QPushButton("Refresh Local-AI Copy")
    if not hasattr(window, "project_root_label"):
        window.project_root_label = QLabel("Project root")
    if not hasattr(window, "local_ai_model_label"):
        window.local_ai_model_label = QLabel("Model")

    window.question_edit.setObjectName("localAIComposer")
    window.question_edit.setPlaceholderText("Message Local AI about this project")
    window.answer_box.setObjectName("localAIConversation")
    for edit in (
        window.detail_box,
        window.prompt_preview,
        window.log_box,
    ):
        edit.setObjectName("localAISideText")

    window.ask_ai_button.setObjectName("localAISendButton")
    window.ask_ai_button.setText("")
    window.ask_ai_button.setIcon(
        window.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
    )
    window.ask_ai_button.setIconSize(QSize(21, 21))
    window.ask_ai_button.setAccessibleName("Ask Local AI")
    window.ask_ai_button.setToolTip("Ask Local AI")
    window.ask_ai_button.setFixedSize(44, 44)

    window.clear_button.setText("+  New session")
    window.clear_button.setObjectName("localAINewSessionButton")
    window.clear_memory_button.setText("Clear memory")

    for combo in (
        window.model_combo,
        window.profile_override_combo,
        window.verbosity_combo,
    ):
        _force_opaque_combo(combo)


def _project_section(window: Any) -> QFrame:
    """Build project JSON, analysis, and profile controls."""
    frame, layout = _section("Project context")
    layout.addWidget(window.project_root_label)
    layout.addWidget(window.project_root_edit)
    root_actions = QHBoxLayout()
    root_actions.setSpacing(6)
    root_actions.addWidget(window.pick_project_root_button)
    root_actions.addWidget(window.run_analysis_button)
    layout.addLayout(root_actions)

    layout.addWidget(_muted_label("Project JSON"))
    layout.addWidget(window.json_path_edit)
    json_actions = QHBoxLayout()
    json_actions.setSpacing(6)
    json_actions.addWidget(window.load_button)
    json_actions.addWidget(window.static_context_button)
    layout.addLayout(json_actions)

    status_form = QFormLayout()
    status_form.setContentsMargins(0, 2, 0, 0)
    status_form.setHorizontalSpacing(8)
    status_form.setVerticalSpacing(6)
    status_form.addRow(_muted_label("Analysis"), window.analysis_status_value_label)
    status_form.addRow(_muted_label("Generated"), window.analysis_output_json_value_label)
    status_form.addRow(_muted_label("JSON track"), window.json_track_value_label)
    layout.addLayout(status_form)

    copy_actions = QHBoxLayout()
    copy_actions.setSpacing(6)
    copy_actions.addWidget(window.ensure_local_ai_json_button)
    copy_actions.addWidget(window.refresh_local_ai_json_button)
    layout.addLayout(copy_actions)

    profile_form = QFormLayout()
    profile_form.setContentsMargins(0, 2, 0, 0)
    profile_form.setHorizontalSpacing(8)
    profile_form.setVerticalSpacing(6)
    profile_form.addRow(_muted_label("Detected"), window.detected_profile_value_label)
    profile_form.addRow(_muted_label("Active"), window.active_profile_value_label)
    profile_form.addRow(_muted_label("Override"), window.profile_override_combo)
    layout.addLayout(profile_form)
    layout.addWidget(window.reset_profile_override_button)
    layout.addWidget(window.analysis_auto_load_checkbox)
    return frame


def _runtime_section(window: Any) -> QFrame:
    """Build local runtime and answer-style controls."""
    frame, layout = _section("Local runtime")
    layout.addWidget(_muted_label("Cache directory"))
    layout.addWidget(window.cache_dir_edit)
    layout.addWidget(window.pick_cache_dir_button)
    layout.addWidget(_muted_label("Governance state"))
    layout.addWidget(window.governance_path_edit)
    layout.addWidget(window.pick_governance_button)
    layout.addWidget(window.local_ai_model_label)
    layout.addWidget(window.model_combo)
    layout.addWidget(window.refresh_models_button)

    style_form = QFormLayout()
    style_form.setContentsMargins(0, 2, 0, 0)
    style_form.setHorizontalSpacing(8)
    style_form.setVerticalSpacing(6)
    style_form.addRow(_muted_label("Verbosity"), window.verbosity_combo)
    layout.addLayout(style_form)
    layout.addWidget(window.prefer_code_radio)
    layout.addWidget(window.prefer_prose_radio)
    layout.addWidget(window.debug_checkbox)
    return frame


def _quick_section(window: Any) -> QFrame:
    """Build quick project-question shortcuts."""
    frame, layout = _section("Quick questions")
    layout.addWidget(window.help_button)
    for button in (
        window.quick_startup_button,
        window.quick_topomap_button,
        window.quick_timeline_button,
        window.quick_responsibility_button,
        window.quick_uncertainty_button,
    ):
        layout.addWidget(button)
    return frame


def _history_panel(window: Any) -> QWidget:
    """Build session controls and memory-backed conversation history."""
    panel = QWidget()
    panel.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.addWidget(window.clear_button)

    heading_row = QHBoxLayout()
    heading = QLabel("Conversations")
    heading.setObjectName("localAISectionTitle")
    heading_row.addWidget(heading)
    heading_row.addStretch(1)
    heading_row.addWidget(_muted_label("memory only"))
    layout.addLayout(heading_row)
    layout.addWidget(window.history_list, 1)
    layout.addWidget(window.clear_memory_button)
    return panel


def _sidebar(window: Any) -> QFrame:
    """Build the professional Local AI sidebar."""
    sidebar = QFrame()
    sidebar.setObjectName("localAISidebar")
    sidebar.setMinimumWidth(320)
    sidebar.setMaximumWidth(420)

    root = QVBoxLayout(sidebar)
    root.setContentsMargins(15, 16, 15, 15)
    root.setSpacing(12)

    title_row = QHBoxLayout()
    title = QLabel("Local AI")
    title.setObjectName("localAITitle")
    title_row.addWidget(title)
    title_row.addStretch(1)
    badge = QLabel("LOCAL  PRIVATE")
    badge.setObjectName("localAIBadge")
    title_row.addWidget(badge)
    root.addLayout(title_row)

    subtitle = QLabel("Project-aware analysis using the existing local model runtime")
    subtitle.setObjectName("localAISubtitle")
    subtitle.setWordWrap(True)
    root.addWidget(subtitle)
    root.addWidget(_history_panel(window), 1)

    divider = QFrame()
    divider.setObjectName("localAIDivider")
    root.addWidget(divider)

    settings_content = QWidget()
    settings_content.setStyleSheet("background: transparent;")
    settings_layout = QVBoxLayout(settings_content)
    settings_layout.setContentsMargins(0, 0, 0, 0)
    settings_layout.setSpacing(9)
    settings_layout.addWidget(_project_section(window))
    settings_layout.addWidget(_runtime_section(window))
    settings_layout.addWidget(_quick_section(window))
    settings_layout.addStretch(1)

    settings_scroll = QScrollArea()
    settings_scroll.setWidgetResizable(True)
    settings_scroll.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    )
    settings_scroll.setMaximumHeight(470)
    settings_scroll.setWidget(settings_content)
    root.addWidget(settings_scroll)

    window.sidebar_panel = sidebar
    return sidebar


def _evidence_tab(window: Any) -> QWidget:
    """Build evidence lists and selected detail without changing ownership."""
    panel = QWidget()
    layout = QHBoxLayout(panel)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)

    lists = QWidget()
    lists_layout = QVBoxLayout(lists)
    lists_layout.setContentsMargins(0, 0, 0, 0)
    lists_layout.setSpacing(6)
    lists_layout.addWidget(_muted_label("File evidence"))
    lists_layout.addWidget(window.file_evidence_list, 1)
    lists_layout.addWidget(_muted_label("Symbol evidence"))
    lists_layout.addWidget(window.symbol_evidence_list, 1)

    detail = QWidget()
    detail_layout = QVBoxLayout(detail)
    detail_layout.setContentsMargins(0, 0, 0, 0)
    detail_layout.setSpacing(6)
    detail_layout.addWidget(_muted_label("Selected detail"))
    detail_layout.addWidget(window.detail_box, 1)

    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.addWidget(lists)
    splitter.addWidget(detail)
    splitter.setSizes([470, 720])
    layout.addWidget(splitter)
    return panel


def _plain_tab(title: str, widget: QWidget) -> QWidget:
    """Wrap one existing diagnostic control in a titled panel."""
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(6)
    layout.addWidget(_muted_label(title))
    layout.addWidget(widget, 1)
    return panel


def _inspector(window: Any) -> QTabWidget:
    """Build compact evidence, prompt, and log inspection tabs."""
    tabs = QTabWidget()
    tabs.setObjectName("localAIInspectorTabs")
    tabs.addTab(_evidence_tab(window), "Evidence")
    tabs.addTab(_plain_tab("Prompt / evidence pack", window.prompt_preview), "Prompt")
    tabs.addTab(_plain_tab("Runtime log", window.log_box), "Log")
    tabs.setMinimumHeight(190)
    return tabs


def _composer(window: Any) -> QFrame:
    """Build the message composer using existing controls."""
    frame = QFrame()
    frame.setObjectName("localAIComposerFrame")
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(11, 7, 8, 7)
    layout.setSpacing(8)
    layout.addWidget(window.question_edit, 1)
    layout.addWidget(window.ask_ai_button, 0, Qt.AlignmentFlag.AlignRight)
    return frame


def _chat_canvas(window: Any) -> QFrame:
    """Build the dominant conversation region."""
    panel = QFrame()
    panel.setObjectName("localAIChatCanvas")
    panel.setMinimumWidth(620)

    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    header = QFrame()
    header.setObjectName("localAIHeader")
    header_layout = QHBoxLayout(header)
    header_layout.setContentsMargins(30, 14, 30, 12)
    heading_stack = QVBoxLayout()
    heading_stack.setSpacing(2)
    heading = QLabel("Project-aware conversation")
    heading.setStyleSheet("font-size: 16px; font-weight: 650;")
    heading_stack.addWidget(heading)
    status = QLabel("Private local analysis - project evidence stays on this machine")
    status.setObjectName("localAIStatus")
    heading_stack.addWidget(status)
    header_layout.addLayout(heading_stack, 1)
    header_layout.addWidget(_muted_label("Local model runtime"), 0, Qt.AlignmentFlag.AlignTop)
    layout.addWidget(header)

    content_splitter = QSplitter(Qt.Orientation.Vertical)
    content_splitter.setChildrenCollapsible(False)
    content_splitter.addWidget(window.answer_box)
    content_splitter.addWidget(_inspector(window))
    content_splitter.setStretchFactor(0, 1)
    content_splitter.setStretchFactor(1, 0)
    content_splitter.setSizes([680, 260])
    layout.addWidget(content_splitter, 1)

    composer_shell = QWidget()
    composer_shell.setStyleSheet("background: #0d0d0d;")
    composer_layout = QVBoxLayout(composer_shell)
    composer_layout.setContentsMargins(48, 13, 48, 21)
    composer_layout.setSpacing(7)
    composer_layout.addWidget(_composer(window))
    note = _muted_label(
        "Answers are advisory and grounded in the currently loaded project JSON and evidence."
    )
    note.setAlignment(Qt.AlignmentFlag.AlignCenter)
    composer_layout.addWidget(note)
    layout.addWidget(composer_shell)

    window.chat_panel = panel
    return panel


def build_main_window_ui(window: Any) -> None:
    """Build Local AI inside the existing height-contained host contract."""
    window.setObjectName("localAITab")
    window.setProperty("kandaContainHostHeight", True)
    window.setMinimumHeight(0)
    window.setStyleSheet(LOCAL_AI_THEME)
    _configure_controls(window)

    central = QWidget()
    central.setMinimumHeight(0)
    central.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
    window.setCentralWidget(central)

    main_layout = QVBoxLayout(central)
    main_layout.setContentsMargins(0, 0, 0, 0)

    scroll = QScrollArea()
    scroll.setObjectName("projectQaBodyScrollArea")
    scroll.setWidgetResizable(True)
    scroll.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setMinimumHeight(0)
    scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

    body = QWidget()
    body.setObjectName("projectQaScrollableBody")
    body.setProperty("localAIProfessionalBody", True)
    body.setMinimumHeight(0)
    body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    body_layout = QVBoxLayout(body)
    body_layout.setContentsMargins(0, 0, 0, 0)
    body_layout.setSpacing(0)
    body_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.setObjectName("localAIMainSplitter")
    splitter.setChildrenCollapsible(False)
    splitter.addWidget(_sidebar(window))
    splitter.addWidget(_chat_canvas(window))
    splitter.setStretchFactor(0, 0)
    splitter.setStretchFactor(1, 1)
    splitter.setSizes([370, 1170])
    body_layout.addWidget(splitter, 1)

    scroll.setWidget(body)
    main_layout.addWidget(scroll, stretch=1)

    window.main_splitter = splitter
    window._project_qa_body_scroll_area = scroll
    window._project_qa_scrollable_body = body
