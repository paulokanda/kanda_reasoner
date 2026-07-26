"""UI builder for Project Structure 3D and its independent JSON owner."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

__all__ = ["build_project_structure_3d_ui"]


def _build_json_controls(widget, root: QVBoxLayout) -> None:
    frame = QFrame()
    frame.setObjectName("projectStructure3DJsonControls")
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(10, 8, 10, 8)
    layout.setSpacing(8)

    widget.json_required_label = QLabel("JSON is necessary for visualization")
    widget.json_required_label.setObjectName("projectStructure3DJsonRequiredLabel")
    layout.addWidget(widget.json_required_label)

    widget.create_project_json_button = QPushButton("Create Project JSON")
    widget.create_project_json_button.setObjectName("createProjectJsonButton")
    widget.create_project_json_button.clicked.connect(widget._create_project_json)
    layout.addWidget(widget.create_project_json_button)

    widget.update_project_json_button = QPushButton("Update JSON Incrementally")
    widget.update_project_json_button.setObjectName("updateProjectJsonIncrementallyButton")
    widget.update_project_json_button.clicked.connect(
        widget._update_project_json_incrementally
    )
    layout.addWidget(widget.update_project_json_button)

    widget.json_artifact_status_label = QLabel("JSON: project not selected")
    widget.json_artifact_status_label.setObjectName("projectStructure3DJsonStatus")
    widget.json_artifact_status_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    layout.addWidget(widget.json_artifact_status_label, 1)
    root.addWidget(frame)


def _build_loaded_toolbar(widget, content: QVBoxLayout) -> None:
    toolbar_frame = QFrame()
    toolbar_frame.setObjectName("projectStructure3DToolbar")
    toolbar = QHBoxLayout(toolbar_frame)
    toolbar.setContentsMargins(10, 8, 10, 8)
    toolbar.setSpacing(8)

    widget.source_badge = QLabel("READ-ONLY FIXTURE")
    widget.source_badge.setObjectName("projectStructure3DBadge")
    toolbar.addWidget(widget.source_badge)

    widget.project_label = QLabel("Project: not selected")
    widget.project_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    toolbar.addWidget(widget.project_label)

    widget.project_structure_help_button = QPushButton("Help")
    widget.project_structure_help_button.setToolTip(
        "Open the Project Structure 3D first-time user help."
    )
    widget.project_structure_help_button.clicked.connect(
        widget._open_project_structure_3d_help
    )
    toolbar.addWidget(widget.project_structure_help_button)
    widget._project_structure_help_dialog = None
    toolbar.addStretch(1)

    widget.view_mode_combo = QComboBox()
    widget.view_mode_combo.setObjectName("projectStructure3DViewMode")
    widget.view_mode_combo.addItem("Architecture", "architecture")
    widget.view_mode_combo.addItem("Structure", "structure")
    widget.view_mode_combo.setCurrentIndex(1)
    widget.view_mode_combo.currentIndexChanged.connect(widget._on_view_options_changed)
    toolbar.addWidget(widget.view_mode_combo)

    widget.imports_checkbox = QCheckBox("Imports")
    widget.imports_checkbox.setChecked(True)
    widget.imports_checkbox.toggled.connect(widget._on_view_options_changed)
    toolbar.addWidget(widget.imports_checkbox)

    widget.external_checkbox = QCheckBox("External")
    widget.external_checkbox.setChecked(True)
    widget.external_checkbox.toggled.connect(widget._on_view_options_changed)
    toolbar.addWidget(widget.external_checkbox)

    widget.symbols_checkbox = QCheckBox("Symbols")
    widget.symbols_checkbox.setChecked(True)
    widget.symbols_checkbox.toggled.connect(widget._on_view_options_changed)
    toolbar.addWidget(widget.symbols_checkbox)

    widget.semantic_checkbox = QCheckBox("Semantic")
    widget.semantic_checkbox.setChecked(True)
    widget.semantic_checkbox.toggled.connect(widget._on_view_options_changed)
    toolbar.addWidget(widget.semantic_checkbox)

    refresh_button = QPushButton("Refresh evidence")
    refresh_button.clicked.connect(widget._refresh_evidence)
    toolbar.addWidget(refresh_button)

    widget.search_edit = QLineEdit()
    widget.search_edit.setObjectName("projectStructure3DSearch")
    widget.search_edit.setPlaceholderText(
        "Search package, module, class, function, dependency, or path"
    )
    widget.search_edit.setClearButtonEnabled(True)
    widget.search_edit.setMaximumWidth(300)
    widget.search_edit.returnPressed.connect(widget._search_graph)
    toolbar.addWidget(widget.search_edit)

    search_button = QPushButton("Search")
    search_button.clicked.connect(widget._search_graph)
    toolbar.addWidget(search_button)

    fit_button = QPushButton("Fit graph")
    fit_button.clicked.connect(lambda: widget._run_renderer_command("fitGraph"))
    toolbar.addWidget(fit_button)

    reset_button = QPushButton("Reset camera")
    reset_button.clicked.connect(lambda: widget._run_renderer_command("resetCamera"))
    toolbar.addWidget(reset_button)

    browser_button = QPushButton("Open in browser")
    browser_button.setObjectName("projectStructure3DOpenBrowser")
    browser_button.clicked.connect(widget._open_in_browser)
    toolbar.addWidget(browser_button)
    content.addWidget(toolbar_frame)


def build_project_structure_3d_ui(widget) -> None:
    """Build JSON controls, loaded controls, viewport, and status surfaces."""
    root = QVBoxLayout(widget)
    root.setContentsMargins(0, 0, 0, 0)
    root.setSpacing(8)
    _build_json_controls(widget, root)

    container = QFrame()
    container.setObjectName("projectStructure3DContainer")
    content = QVBoxLayout(container)
    content.setContentsMargins(0, 0, 0, 0)
    content.setSpacing(8)
    _build_loaded_toolbar(widget, content)
    widget._install_navigation_bar(content)

    splitter = QSplitter(Qt.Horizontal)
    splitter.setObjectName("projectStructure3DSplitter")
    widget.viewport_host = QWidget()
    viewport_layout = QVBoxLayout(widget.viewport_host)
    viewport_layout.setContentsMargins(0, 0, 0, 0)
    viewport_layout.setSpacing(0)
    widget._viewport_layout = viewport_layout
    splitter.addWidget(widget.viewport_host)

    widget.details = QTextBrowser()
    widget.details.setObjectName("projectStructure3DDetails")
    widget.details.setOpenExternalLinks(False)
    widget.details.setMinimumWidth(270)
    widget.details.setMaximumWidth(420)
    splitter.addWidget(widget.details)
    splitter.setStretchFactor(0, 1)
    splitter.setStretchFactor(1, 0)
    splitter.setSizes([900, 320])
    content.addWidget(splitter, 1)

    widget.status_label = QLabel("Preparing local renderer...")
    widget.status_label.setObjectName("projectStructure3DStatus")
    content.addWidget(widget.status_label)
    root.addWidget(container, 1)
    widget._show_overview_details()
    widget._apply_style()
    widget._refresh_complete_json_status()
