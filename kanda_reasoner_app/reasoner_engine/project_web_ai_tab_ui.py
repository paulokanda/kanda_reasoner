# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py
"""Build the Project Web AI conversation and advisory configuration subtabs."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QSplitter,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.reasoner_engine.project_web_ai_tab_theme import (
    PROJECT_WEB_AI_THEME,
)

__all__ = ["build_project_web_ai_ui", "create_project_web_ai_controls"]

# Legacy validator marker: background: #0d0d0d


def _muted_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("projectWebAIMuted")
    label.setWordWrap(True)
    return label


def _section(title: str) -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName("projectWebAISection")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(10)
    heading = QLabel(title)
    heading.setObjectName("projectWebAISectionTitle")
    layout.addWidget(heading)
    return frame, layout


def _force_opaque_combo(combo: QComboBox) -> None:
    popup = combo.view()
    viewport = popup.viewport()
    popup.setObjectName("projectWebAIComboPopup")
    viewport.setObjectName("projectWebAIComboPopupViewport")
    popup.setStyleSheet(
        "QAbstractItemView {"
        "background-color: #1d2128; color: #f4f6f8;"
        "border: 1px solid #3d4552; outline: 0;"
        "selection-background-color: #2f4f48;"
        "selection-color: #ffffff;}"
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


def create_project_web_ai_controls(owner: Any) -> None:
    owner.project_root_edit = QLineEdit()
    owner.project_root_edit.setObjectName("projectWebAIProjectRootEdit")
    owner.project_root_edit.setPlaceholderText("Select the project source root")
    owner.pick_project_button = QPushButton("Browse...")
    owner.pick_project_button.setObjectName("projectWebAIProjectBrowseButton")
    owner.pick_project_button.setToolTip("Browse for the shared active Project root")
    owner.reload_context_button = QPushButton("Reload Context")
    owner.reload_context_button.setObjectName("projectWebAIReloadContextButton")
    owner.support_root_value = _muted_label("Not resolved")
    owner.collector_status_value = QLabel("Not loaded")
    owner.snapshot_value = QLabel("Not loaded")
    owner.context_size_value = QLabel("0 bytes")
    owner.context_details = QPlainTextEdit()
    owner.context_details.setObjectName("projectWebAISideText")
    owner.context_details.setReadOnly(True)
    owner.context_details.setMinimumHeight(260)

    owner.web_access_combo = QComboBox()
    owner.web_access_combo.setObjectName("projectWebAIAccessCombo")
    owner.web_access_combo.addItem("Gateway", "gateway")
    owner.web_access_combo.addItem("Direct API", "direct")
    owner.web_provider_combo = QComboBox()
    owner.web_provider_combo.setObjectName("projectWebAIProviderCombo")
    owner.web_model_combo = QComboBox()
    owner.web_model_combo.setObjectName("projectWebAIModelCombo")
    owner.web_model_combo.setMinimumContentsLength(36)
    for combo in (
        owner.web_access_combo,
        owner.web_provider_combo,
        owner.web_model_combo,
    ):
        _force_opaque_combo(combo)
    owner.web_refresh_models_button = QPushButton("Refresh Models")
    owner.web_refresh_models_button.setObjectName("projectWebAIRefreshModelsButton")
    owner.web_config_summary_value = QLabel("Web AI is not configured")
    owner.web_config_summary_value.setWordWrap(True)
    owner.web_config_status_value = _muted_label("Not loaded")
    owner.web_config_privacy_value = _muted_label("")
    owner.open_web_config_button = QPushButton("Open Provider Configuration")

    owner.question_edit = QPlainTextEdit()
    owner.question_edit.setObjectName("projectWebAIComposer")
    owner.question_edit.setPlaceholderText("Message Web AI")
    owner.question_edit.setMinimumHeight(68)
    owner.question_edit.setMaximumHeight(150)
    owner.paste_question_button = QPushButton("Paste")
    owner.copy_question_button = QPushButton("Copy")
    for button in (owner.paste_question_button, owner.copy_question_button):
        button.setObjectName("projectWebAIClipboardAction")
        button.setFixedHeight(30)
    owner.send_button = QPushButton()
    owner.send_button.setObjectName("projectWebAISendButton")
    owner.send_button.setIcon(
        owner.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
    )
    owner.send_button.setIconSize(QSize(21, 21))
    owner.send_button.setAccessibleName("Send to Web AI")
    owner.send_button.setToolTip("Send to Web AI")
    owner.send_button.setFixedSize(44, 44)
    owner.stop_button = QPushButton("Stop")
    owner.stop_button.setObjectName("projectWebAIStopButton")
    owner.stop_button.setEnabled(False)
    owner.inspect_project_checkbox = QCheckBox("Inspect Project")
    owner.inspect_project_checkbox.setObjectName("projectWebAIInspectProjectCheckbox")
    owner.inspect_project_checkbox.setChecked(True)
    owner.inspect_project_checkbox.setToolTip(
        "Allow bounded read-only Project listing, search, and file reads."
    )
    owner.prepare_changes_button = QPushButton("Prepare Changes")
    owner.prepare_changes_button.setObjectName("projectWebAIPrepareChangesButton")
    owner.prepare_changes_button.setEnabled(False)
    owner.prepare_changes_button.setToolTip(
        "Create a Shadow Preview before any separate governed write approval."
    )

    owner.clear_button = QPushButton("+  New chat")
    owner.clear_button.setObjectName("projectWebAINewChatButton")
    owner.chat_list = QListWidget()
    owner.chat_list.setObjectName("projectWebAIChatList")
    owner.chat_list.setMinimumHeight(220)
    owner.load_chat_button = QPushButton("Load")
    owner.delete_chat_button = QPushButton("Delete")
    owner.save_chat_button = QPushButton("Save .md")
    for button in (
        owner.load_chat_button,
        owner.delete_chat_button,
        owner.save_chat_button,
    ):
        button.setObjectName("projectWebAIHistoryAction")

    owner.answer_box = QTextBrowser()
    owner.answer_box.setObjectName("projectWebAIConversation")
    owner.answer_box.setReadOnly(True)
    owner.answer_box.setOpenExternalLinks(False)
    owner.answer_box.setOpenLinks(False)
    owner.answer_box.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Expanding,
    )
    owner.provenance_box = QPlainTextEdit()
    owner.provenance_box.setObjectName("projectWebAISideText")
    owner.provenance_box.setReadOnly(True)
    owner.provenance_box.setMinimumHeight(420)
    owner.status_value = QLabel("Select a project and load context.")
    owner.status_value.setObjectName("projectWebAIStatus")
    owner.status_value.setWordWrap(True)


def _project_selector(owner: Any) -> QFrame:
    frame = QFrame()
    frame.setObjectName("projectWebAIProjectSelector")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(8)
    heading = QLabel("Active Project root")
    heading.setObjectName("projectWebAISectionTitle")
    layout.addWidget(heading)
    path_row = QHBoxLayout()
    path_row.setSpacing(8)
    path_row.addWidget(owner.project_root_edit, 1)
    path_row.addWidget(owner.pick_project_button)
    layout.addLayout(path_row)
    action_row = QHBoxLayout()
    action_row.addWidget(_muted_label("Shared across all Project tabs"), 1)
    action_row.addWidget(owner.reload_context_button)
    layout.addLayout(action_row)
    owner.project_selector_panel = frame
    return frame


def _project_context_section(owner: Any) -> QFrame:
    frame, layout = _section("Project context status")
    form = QFormLayout()
    form.setContentsMargins(0, 2, 0, 0)
    form.setHorizontalSpacing(12)
    form.setVerticalSpacing(8)
    form.addRow(_muted_label("Support"), owner.support_root_value)
    form.addRow(_muted_label("Collector"), owner.collector_status_value)
    form.addRow(_muted_label("Snapshot"), owner.snapshot_value)
    form.addRow(_muted_label("Context"), owner.context_size_value)
    layout.addLayout(form)
    layout.addWidget(owner.context_details, 1)
    return frame


def _provider_section(owner: Any) -> QFrame:
    frame, layout = _section("Web advisory configuration")
    form = QFormLayout()
    form.setContentsMargins(0, 2, 0, 0)
    form.setHorizontalSpacing(12)
    form.setVerticalSpacing(8)
    form.addRow(_muted_label("Access"), owner.web_access_combo)
    form.addRow(_muted_label("Provider"), owner.web_provider_combo)
    form.addRow(_muted_label("Python model"), owner.web_model_combo)
    layout.addLayout(form)
    actions = QHBoxLayout()
    actions.setSpacing(8)
    actions.addWidget(owner.web_refresh_models_button)
    actions.addWidget(owner.open_web_config_button)
    actions.addStretch(1)
    layout.addLayout(actions)
    layout.addWidget(owner.web_config_summary_value)
    layout.addWidget(_muted_label("Catalog"))
    layout.addWidget(owner.web_config_status_value)
    layout.addWidget(_muted_label("Privacy"))
    layout.addWidget(owner.web_config_privacy_value)
    return frame


def _details_section(owner: Any) -> QFrame:
    frame, layout = _section("Latest response details")
    layout.addWidget(owner.provenance_box, 1)
    return frame


def _chat_history_panel(owner: Any) -> QWidget:
    panel = QWidget()
    panel.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.addWidget(owner.clear_button)
    heading_row = QHBoxLayout()
    heading = QLabel("Chats")
    heading.setObjectName("projectWebAISectionTitle")
    heading_row.addWidget(heading)
    heading_row.addStretch(1)
    heading_row.addWidget(_muted_label("memory only"))
    layout.addLayout(heading_row)
    layout.addWidget(owner.chat_list, 1)
    actions = QHBoxLayout()
    actions.setSpacing(5)
    actions.addWidget(owner.load_chat_button)
    actions.addWidget(owner.delete_chat_button)
    actions.addWidget(owner.save_chat_button)
    layout.addLayout(actions)
    return panel


def _conversation_sidebar(owner: Any) -> QFrame:
    sidebar = QFrame()
    sidebar.setObjectName("projectWebAISidebar")
    sidebar.setMinimumWidth(270)
    sidebar.setMaximumWidth(360)
    root = QVBoxLayout(sidebar)
    root.setContentsMargins(15, 16, 15, 15)
    root.setSpacing(12)
    title_row = QHBoxLayout()
    title = QLabel("Web AI")
    title.setObjectName("projectWebAITitle")
    title_row.addWidget(title)
    title_row.addStretch(1)
    badge = QLabel("CONVERSATION")
    badge.setObjectName("projectWebAIBadge")
    title_row.addWidget(badge)
    root.addLayout(title_row)
    subtitle = QLabel("Project-aware chat history and conversation")
    subtitle.setObjectName("projectWebAISubtitle")
    subtitle.setWordWrap(True)
    root.addWidget(subtitle)
    root.addWidget(_chat_history_panel(owner), 1)
    owner.sidebar_panel = sidebar
    return sidebar


def _composer(owner: Any) -> QFrame:
    frame = QFrame()
    frame.setObjectName("projectWebAIComposerFrame")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(11, 7, 8, 7)
    layout.setSpacing(6)
    input_row = QHBoxLayout()
    input_row.setSpacing(8)
    input_row.addWidget(owner.question_edit, 1)
    actions = QVBoxLayout()
    actions.setContentsMargins(0, 0, 0, 0)
    actions.setSpacing(6)
    actions.addWidget(owner.send_button, 0, Qt.AlignmentFlag.AlignRight)
    actions.addWidget(owner.stop_button, 0, Qt.AlignmentFlag.AlignRight)
    input_row.addLayout(actions)
    layout.addLayout(input_row)
    clipboard_row = QHBoxLayout()
    clipboard_row.setSpacing(6)
    clipboard_row.addWidget(owner.paste_question_button)
    clipboard_row.addWidget(owner.copy_question_button)
    clipboard_row.addStretch(1)
    layout.addLayout(clipboard_row)
    return frame


def _chat_canvas(owner: Any) -> QFrame:
    panel = QFrame()
    panel.setObjectName("projectWebAIChatCanvas")
    panel.setMinimumWidth(620)
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    header = QFrame()
    header.setObjectName("projectWebAIHeader")
    header_layout = QHBoxLayout(header)
    header_layout.setContentsMargins(30, 14, 30, 12)
    title_stack = QVBoxLayout()
    title_stack.setSpacing(2)
    heading = QLabel("Project-aware conversation")
    heading.setStyleSheet("font-size: 16px; font-weight: 650;")
    title_stack.addWidget(heading)
    title_stack.addWidget(owner.status_value)
    header_layout.addLayout(title_stack, 1)
    header_layout.addWidget(
        _muted_label("Gateway or direct API"),
        0,
        Qt.AlignmentFlag.AlignTop,
    )
    layout.addWidget(header)
    layout.addWidget(owner.answer_box, 1)
    composer_shell = QWidget()
    composer_shell.setStyleSheet("background: #0d0d0d;")
    composer_layout = QVBoxLayout(composer_shell)
    composer_layout.setContentsMargins(48, 13, 48, 21)
    composer_layout.setSpacing(7)
    composer_layout.addWidget(_composer(owner))
    action_row = QHBoxLayout()
    action_row.addStretch(1)
    action_row.addWidget(owner.inspect_project_checkbox)
    owner.prepare_changes_button.setMaximumWidth(210)
    action_row.addWidget(owner.prepare_changes_button)
    action_row.addStretch(1)
    composer_layout.addLayout(action_row)
    note = _muted_label(
        "Inspect Project is read-only. Prepare Changes builds a Shadow before "
        "any separate governed write confirmation."
    )
    note.setAlignment(Qt.AlignmentFlag.AlignCenter)
    composer_layout.addWidget(note)
    layout.addWidget(composer_shell)
    owner.chat_panel = panel
    return panel


def _conversation_page(owner: Any) -> QWidget:
    page = QWidget()
    page.setObjectName("projectWebAIConversationPage")
    layout = QHBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.setObjectName("projectWebAIMainSplitter")
    splitter.setChildrenCollapsible(False)
    splitter.addWidget(_conversation_sidebar(owner))
    splitter.addWidget(_chat_canvas(owner))
    splitter.setStretchFactor(0, 0)
    splitter.setStretchFactor(1, 1)
    splitter.setSizes([320, 1200])
    owner.main_splitter = splitter
    layout.addWidget(splitter)
    owner.conversation_page = page
    return page


def _advisory_config_page(owner: Any) -> QWidget:
    page = QWidget()
    page.setObjectName("projectWebAIAdvisoryConfigPage")
    page_layout = QVBoxLayout(page)
    page_layout.setContentsMargins(0, 0, 0, 0)
    page_layout.setSpacing(0)
    scroll = QScrollArea()
    scroll.setObjectName("projectWebAISettingsScroll")
    scroll.setWidgetResizable(True)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    content = QWidget()
    content.setObjectName("projectWebAIAdvisoryContent")
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(26, 22, 26, 26)
    content_layout.setSpacing(16)
    title = QLabel("Web advisory configuration")
    title.setObjectName("projectWebAITitle")
    content_layout.addWidget(title)
    content_layout.addWidget(
        _muted_label(
            "Project context, provider selection, privacy, catalog status, and "
            "response provenance are shown here at full working width."
        )
    )
    content_layout.addWidget(_project_selector(owner))
    columns = QSplitter(Qt.Orientation.Horizontal)
    columns.setObjectName("projectWebAIAdvisorySplitter")
    columns.setChildrenCollapsible(False)
    left = QWidget()
    left_layout = QVBoxLayout(left)
    left_layout.setContentsMargins(0, 0, 8, 0)
    left_layout.setSpacing(16)
    left_layout.addWidget(_project_context_section(owner), 1)
    left_layout.addWidget(_provider_section(owner))
    right = QWidget()
    right_layout = QVBoxLayout(right)
    right_layout.setContentsMargins(8, 0, 0, 0)
    right_layout.addWidget(_details_section(owner), 1)
    columns.addWidget(left)
    columns.addWidget(right)
    columns.setStretchFactor(0, 1)
    columns.setStretchFactor(1, 1)
    columns.setSizes([720, 720])
    content_layout.addWidget(columns, 1)
    scroll.setWidget(content)
    page_layout.addWidget(scroll)
    owner.settings_scroll = scroll
    owner.advisory_config_splitter = columns
    owner.advisory_config_page = page
    return page


def build_project_web_ai_ui(owner: Any) -> None:
    owner.setObjectName("projectWebAITab")
    owner.setProperty("kandaContainHostHeight", True)
    owner.setMinimumSize(1080, 0)
    owner.setStyleSheet(PROJECT_WEB_AI_THEME)
    root = QVBoxLayout(owner)
    root.setContentsMargins(0, 0, 0, 0)
    root.setSpacing(0)
    tabs = QTabWidget()
    tabs.setObjectName("projectWebAISubtabs")
    tabs.setDocumentMode(True)
    tabs.addTab(_conversation_page(owner), "Project Conversation")
    tabs.addTab(_advisory_config_page(owner), "Web Advisory Config")
    tabs.setCurrentIndex(0)
    owner.web_ai_subtabs = tabs
    root.addWidget(tabs)
