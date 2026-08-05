# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py
"""Lazy loading tab host for embedded Reasoner tools."""

from __future__ import annotations

from collections.abc import Callable
import traceback

from PySide6.QtCore import Qt, QBasicTimer, QMetaObject, Slot
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from kanda_reasoner_app.portable_smoke_runtime_report import (
    record_portable_smoke_event,
)

from .error_panels import ToolLoadErrorPanel
from .gui_support import _first_existing_attr, _first_imported_module, _prepare_embedded_widget
from .tab_header_template import TabHeaderTemplate
from .tool_specs import ToolSpec
from ._lazy_tab_shell_chrome import (
    LazyTabShellChromeMixin,
    _CANONICAL_PACKAGE_NAME,
    _DAILY_REFACTOR_GUI_SOURCE,
    _DOCSTRINGS_GUI_SOURCE,
    _ENGINEERING_SAFETY_GUI_SOURCE,
    _ERROR_MEMORY_GUI_SOURCE,
    _FREEZE_AFTER_UPDATE_GUI_SOURCE,
    _HEADER_TEMPLATE_ONLY_SOURCES,
    _WORKFLOWS_GUI_SOURCE,
)
from ._lazy_tab_layout_relocation import LazyTabLayoutRelocationMixin
from ._docstring_ai_header_runtime import (
    bind_embedded_docstring_widget,
    install_docstring_header_surface,
)

__all__ = ["LazyToolTab"]


_LEGACY_HEADER_AI_GROUP_SOURCES = {
    _ENGINEERING_SAFETY_GUI_SOURCE,
    _DAILY_REFACTOR_GUI_SOURCE,
}


class LazyToolTab(LazyTabShellChromeMixin, LazyTabLayoutRelocationMixin, QWidget):
    """Represent one lazy-loading tool tab host."""

    def __init__(
        self,
        spec: ToolSpec,
        on_loaded,
        *,
        select_project_handler: Callable[[], None] | None = None,
        eject_project_handler: Callable[[], None] | None = None,
        active_project_provider: Callable[[], object] | None = None,
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        spec : ToolSpec
            The spec value.
        on_loaded : object
            The on loaded value.
        """
        
        super().__init__()
        self.spec = spec
        self._loaded = False
        self._embedded_widget: QWidget | None = None
        self._on_loaded = on_loaded
        self._select_project_handler = select_project_handler
        self._eject_project_handler = eject_project_handler
        self._active_project_provider = active_project_provider
        self.active_project_label: QLabel | None = None
        self.active_project_path_edit: QLineEdit | None = None
        self.active_project_select_button: QPushButton | None = None
        self.active_project_eject_button: QPushButton | None = None
        self._help_dialog: QMainWindow | None = None
        self._pending_intake_loader = None
        self._pending_intake_retry_phase = 0
        self._pending_intake_retry_timer = QBasicTimer()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(10)

        help_handler = self._open_help_catalog if spec.help_catalog else None
        if spec.source_hint == _FREEZE_AFTER_UPDATE_GUI_SOURCE:
            help_handler = self._open_freeze_feature_help
        self.tab_header_template = TabHeaderTemplate(
            spec.step_title,
            help_handler=help_handler,
        )
        self.header_row = self.tab_header_template.layout
        self._header_controls_insert_index = self.header_row.indexOf(
            self.tab_header_template.project_root_host
        )
        self._install_title_active_project_buttons()

        self.python_executable_label: QLabel | None = None
        self.help_button: QPushButton | None = self.tab_header_template.help_button
        if spec.source_hint in _LEGACY_HEADER_AI_GROUP_SOURCES:
            review_handler = None
            if spec.source_hint == _ENGINEERING_SAFETY_GUI_SOURCE:
                review_handler = self._engineering_safety_ai_review_first_check
            self.tab_header_template.install_ai_group_blueprint(
                refresh_handler=self._open_global_local_ai_configuration,
                review_handler=review_handler,
            )
            self._configure_global_local_ai_header()

        if spec.source_hint == _DOCSTRINGS_GUI_SOURCE:
            install_docstring_header_surface(self, outer)
        else:
            outer.addLayout(self.header_row)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        outer.addWidget(line)

        status_source_row = QHBoxLayout()
        self.status_source_row = status_source_row
        self._show_status_source_row = spec.source_hint not in _HEADER_TEMPLATE_ONLY_SOURCES

        self.status_label = QLabel("Tool not loaded yet. It will load when this tab is opened.")
        self.status_label.setWordWrap(False)

        self.source_label: QLabel | None = QLabel(f"Source: {spec.source_hint}")
        self.source_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.source_label.setWordWrap(False)
        self.source_label.setStyleSheet(
            "border: 1px solid black; padding: 2px 6px;"
        )

        self._source_hover_window = None
        if self._show_status_source_row:
            status_source_row.addWidget(self.status_label, 0)
            status_source_row.addSpacing(24)
            status_source_row.addWidget(self.source_label, 0)

            source_hover_message = {
                _WORKFLOWS_GUI_SOURCE: (
                    "Workflow Review:\n"
                    f"Source: {_CANONICAL_PACKAGE_NAME}/manage_workflows/"
                    "manage_workflows_gui.py"
                ),
            }.get(spec.source_hint)
            if source_hover_message:
                self._source_hover_window = attach_floating_window(
                    self.source_label,
                    trigger_word="Source",
                    message=source_hover_message,
                    delay_ms=4000,
                )

        self._status_source_insert_index = status_source_row.count()
        if self._show_status_source_row:
            status_source_row.addStretch(1)
            outer.addLayout(status_source_row)
        else:
            self.status_label.hide()
            self.source_label.hide()


        self.load_button = QPushButton("Load this tool now")
        self.load_button.setObjectName("lazy_tool_load_button")
        outer.addWidget(self.load_button)

        self.content_host = QWidget()
        self.content_layout = QVBoxLayout(self.content_host)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        outer.addWidget(self.content_host, 1)
        QMetaObject.connectSlotsByName(self)

    def request_select_active_project(self) -> None:
        """Invoke the shell-owned active Project selector."""
        handler = self._select_project_handler
        if callable(handler):
            handler()

    def request_eject_active_project(self) -> None:
        """Invoke the shell-owned active Project eject command."""
        handler = self._eject_project_handler
        if callable(handler):
            handler()

    def refresh_active_project_controls(self, active_root: object = None) -> None:
        """Refresh this tab's proxy identity and commands from shell authority."""
        if active_root is None and callable(self._active_project_provider):
            active_root = self._active_project_provider()
        path_text = str(active_root) if active_root is not None else ""
        if self.active_project_path_edit is not None:
            self.active_project_path_edit.setText(path_text)
            self.active_project_path_edit.setToolTip(
                path_text or "No active Project selected."
            )
        if self.active_project_select_button is not None:
            self.active_project_select_button.setEnabled(
                callable(self._select_project_handler)
            )
        if self.active_project_eject_button is not None:
            self.active_project_eject_button.setEnabled(
                callable(self._eject_project_handler) and active_root is not None
            )

    @Slot()
    def on_lazy_tool_load_button_clicked(self) -> None:
        """Load the current tool through Qt object-name auto-connect."""
        self.load_tool()

    @Slot(str)
    def on_lazy_tab_header_ai_model_combo_currentTextChanged(self, text: str) -> None:
        """Apply one auto-connected header model selection to Tab 3."""
        widget = self._embedded_widget
        if widget is not None:
            self._apply_header_ai_model_to_tab3(widget, str(text or ""))

    @Slot(str)
    def on_lazy_tab_body_ai_model_combo_currentTextChanged(self, _text: str) -> None:
        """Mirror one auto-connected Tab 3 model selection into the header."""
        widget = self._embedded_widget
        if widget is not None:
            self._copy_tab3_model_combo_to_header(widget)

    def timerEvent(self, event) -> None:
        """Run the two deferred pending-intake retries without QTimer wiring."""
        if event.timerId() != self._pending_intake_retry_timer.timerId():
            super().timerEvent(event)
            return
        self._pending_intake_retry_timer.stop()
        loader = self._pending_intake_loader
        if callable(loader):
            loader()
        if self._pending_intake_retry_phase == 1:
            self._pending_intake_retry_phase = 2
            self._pending_intake_retry_timer.start(250, self)
            return
        self._pending_intake_retry_phase = 0
        self._pending_intake_loader = None

    def load_tool(self) -> bool:
        """Load the tool.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        if self._loaded:
            return True

        self.status_label.setText("Loading tool...")
        self.status_label.setStyleSheet("")
        QApplication.processEvents()

        try:
            module = _first_imported_module(self.spec.module_candidates)
            widget_class = _first_existing_attr(module, self.spec.class_candidates)
            widget = widget_class()
            widget = _prepare_embedded_widget(widget)
            self._move_tab2_project_root_controls_to_header_row(widget)
            self._move_tab2_ai_review_controls_to_header_row(widget)
            self._move_tab1_project_root_controls_to_header_row(widget)
            self._move_tab1_ai_review_controls_to_header_row(widget)
            self._move_tab3_project_root_controls_to_header_row(widget)
            self._move_tab3_safe_mode_radio_to_header_row(widget)
            if self.spec.source_hint == _DOCSTRINGS_GUI_SOURCE:
                bind_embedded_docstring_widget(self, widget)
            self._bind_tab3_header_ai_model_controls(widget)
            self._move_show_project_project_root_controls_to_header_row(widget)
            self._move_error_memory_project_root_controls_to_header_row(widget)
            self._move_engineering_safety_project_root_controls_to_header_row(widget)
            self._move_freeze_after_update_project_root_controls_to_header_row(widget)
            self._move_refactor_report_project_root_controls_to_header_row(widget)
            self._move_project_qa_project_root_controls_to_header_row(widget)
            self._move_project_qa_ai_controls_to_header_row(widget)
            self.content_layout.addWidget(widget)
            self._embedded_widget = widget

            self.status_label.setText("LOADED")
            self.status_label.setStyleSheet("color: #008000; font-weight: bold;")
            self.load_button.hide()

            self._loaded = True
            self._on_loaded(self.spec, widget)
            record_portable_smoke_event(
                status="PASS",
                kind="lazy_tab",
                source=self.spec.source_hint,
                message="LOADED",
            )

            try:
                pending_loader = widget.load_pending_ai_assisted_error_lesson_intake_now
            except AttributeError:
                pending_loader = None
            if callable(pending_loader):
                try:
                    pending_loader()
                except Exception:
                    pass
                self._pending_intake_loader = pending_loader
                self._pending_intake_retry_phase = 1
                self._pending_intake_retry_timer.start(0, self)

            return True

        except (ImportError, AttributeError, RuntimeError, TypeError):
            error_text = traceback.format_exc()
            record_portable_smoke_event(
                status="FAIL",
                kind="lazy_tab",
                source=self.spec.source_hint,
                message=error_text,
            )
            error_panel = ToolLoadErrorPanel(
                title=self.spec.step_title,
                source_hint=self.spec.source_hint,
                error_text=error_text,
            )

            self.content_layout.addWidget(error_panel)
            self.status_label.setText("FAILED TO LOAD")
            self.status_label.setStyleSheet("color: #B00020; font-weight: bold;")
            self.load_button.setText("Retry loading")
            self._loaded = True
            return False

    def ensure_loaded(self) -> bool:
        """Support ensure loaded behavior.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        if not self._loaded:
            return self.load_tool()
        return True

