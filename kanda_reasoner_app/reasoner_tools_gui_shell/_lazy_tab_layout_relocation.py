# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py
"""Explicit header-layout relocation behavior for the lazy tool tab host."""

from __future__ import annotations

import contextlib

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from ._lazy_tab_shell_chrome import (
    _ACTIVE_PROJECT_BUTTON_ONLY_SOURCES,
    _ARCHITECTURE_GUI_SOURCE,
    _CONTEXT_COLLECTOR_GUI_SOURCE,
    _DAILY_REFACTOR_GUI_SOURCE,
    _DOCSTRINGS_GUI_SOURCE,
    _ENGINEERING_SAFETY_GUI_SOURCE,
    _ERROR_MEMORY_GUI_SOURCE,
    _FREEZE_AFTER_UPDATE_GUI_SOURCE,
    _PROJECT_QA_GUI_SOURCE,
    _WORKFLOWS_GUI_SOURCE,
)


class LazyTabLayoutRelocationMixin:
    """Own explicit movement of tool-specific controls into shared header rows."""

    def _move_tab1_project_root_controls_to_header_row(self, widget) -> None:
        """Move Tab 1 Project Root controls beside the Architecture Review header."""
        if self.spec.source_hint != _ARCHITECTURE_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self._install_active_project_header_controls(
            label=getattr(widget, "_root_path_label", None),
            path_widget=getattr(widget, "_root_path_edit", None),
            browse_button=getattr(widget, "_browse_root_btn", None),
        )

    def _move_tab1_ai_review_controls_to_header_row(self, widget) -> None:
        """Move Tab 1 AI review controls beside the Architecture Review header."""
        if self.spec.source_hint != _ARCHITECTURE_GUI_SOURCE:
            return

        try:
            widget.move_ai_review_controls_to_layout(self.tab_header_template.ai_group_layout)
        except (AttributeError, TypeError):
            return

    def _move_tab2_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Tab 2 Project Root controls into the header template."""
        if self.spec.source_hint != _WORKFLOWS_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self.tab_header_template.activate_project_root_slot()

    def _move_tab2_ai_review_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Tab 2 AI review controls into the header template."""
        if self.spec.source_hint != _WORKFLOWS_GUI_SOURCE:
            return

        try:
            widget.move_ai_review_controls_to_layout(self.tab_header_template.ai_group_layout)
        except (AttributeError, TypeError):
            return

    def _move_tab3_project_root_controls_to_header_row(self, widget) -> None:
        """Move Tab 3 Project Root controls into the header template."""
        if self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self._install_active_project_header_controls(
            label=getattr(widget, "_root_path_label", None),
            path_widget=getattr(widget, "_root_path_edit", None),
            browse_button=getattr(widget, "_browse_root_button", None),
            path_minimum_width=180,
        )

    def _move_tab3_safe_mode_radio_to_header_row(self, widget) -> None:
        """Move Tab 3 Tab 1 audit source control into the header template."""
        if self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE:
            return

        try:
            widget.move_safe_mode_radio_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return

    def _move_show_project_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Show Project to AI Project Root controls beside the tab header."""
        if self.spec.source_hint != _CONTEXT_COLLECTOR_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self._install_active_project_header_controls(
            label=getattr(widget, "project_root_label", None),
            path_widget=getattr(widget, "project_root_edit", None),
            browse_button=getattr(widget, "browse_project_button", None),
            path_minimum_width=180,
        )

    def _move_error_memory_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Error Memory Project Root controls into the header template."""
        if self.spec.source_hint != _ERROR_MEMORY_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self._install_active_project_header_controls(
            label=getattr(widget, "project_root_header_label", None),
            path_widget=getattr(widget, "project_root_value_label", None),
            browse_button=getattr(widget, "search_project_button", None),
        )

        try:
            export_button = widget.export_button
        except AttributeError:
            export_button = None
        if export_button is not None:
            export_button.setText("Lessons to Clipboard")
            export_button.setToolTip(
                "Copy the complete Error Memory lesson library as JSON to the "
                "clipboard for manual AI transfer."
            )

    def _move_engineering_safety_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Engineering Safety Project Root controls into the header template."""
        if self.spec.source_hint != _ENGINEERING_SAFETY_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self.tab_header_template.activate_project_root_slot()

    def _move_freeze_after_update_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Freeze Feature After Update Project Root controls into the header."""
        if self.spec.source_hint != _FREEZE_AFTER_UPDATE_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self._install_active_project_header_controls(
            label=getattr(widget, "project_root_header_label", None),
            path_widget=getattr(widget, "project_root_edit", None),
            browse_button=getattr(widget, "search_project_button", None),
        )

    def _move_refactor_report_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Refactor Report project-root controls into the header template."""
        if self.spec.source_hint != _DAILY_REFACTOR_GUI_SOURCE:
            return

        try:
            edit = widget.domain_edit
        except AttributeError:
            return

        try:
            label = widget._header_project_root_label
        except AttributeError:
            label = None
        if label is None:
            label = QLabel("Project Root:")
            label_font = QFont(label.font())
            label_font.setBold(True)
            label.setFont(label_font)
            label.setStyleSheet("padding-left: 4px;")
            widget._header_project_root_label = label

        browse_button = self._find_refactor_report_project_root_button(widget)
        if browse_button is not None:
            browse_button.setText("browse project folder")
        controls = [label, edit]
        if browse_button is not None:
            controls.append(browse_button)

        target_index = self.tab_header_template.project_root_layout.count()
        self.tab_header_template.project_root_layout.insertSpacing(target_index, 12)
        offset = 1
        for control in controls:
            self._move_widget_to_layout(
                control,
                self.tab_header_template.project_root_layout,
                target_index + offset,
            )
            offset += 1

        self.tab_header_template.activate_project_root_slot()
        self._hide_refactor_report_mode_a_group(widget)

    def _move_project_qa_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Project Q&A project-root controls into the header template."""
        if self.spec.source_hint != _PROJECT_QA_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return
        self._install_active_project_header_controls(
            label=getattr(widget, "project_root_label", None),
            path_widget=getattr(widget, "project_root_edit", None),
            browse_button=getattr(widget, "pick_project_root_button", None),
        )

    def _move_project_qa_ai_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Project Q&A local-AI controls into the header template."""
        if self.spec.source_hint != _PROJECT_QA_GUI_SOURCE:
            return

        try:
            widget.move_ai_runtime_controls_to_layout(self.tab_header_template.ai_group_layout)
        except (AttributeError, TypeError):
            return

    @staticmethod
    def _style_active_project_label(label: QLabel) -> None:
        """Apply the canonical compact Active Project label appearance."""
        label.setText("Active Project:")
        label_font = QFont(label.font())
        label_font.setBold(True)
        label.setFont(label_font)
        label.setStyleSheet(
            "color: #0B3D91; "
            "font-weight: 700; "
            "padding: 0px;"
        )
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setMinimumWidth(0)
        label.setMargin(0)
        label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

    @staticmethod
    def _style_active_project_path(path_widget: QWidget) -> None:
        """Apply the canonical strong-green Active Project path appearance."""
        path_font = QFont(path_widget.font())
        path_font.setBold(True)
        path_widget.setFont(path_font)
        path_widget.setStyleSheet(
            "color: #166534; "
            "font-weight: 700;"
        )

    def _install_title_active_project_buttons(self) -> None:
        """Install the full Active Project surface for Web AI and Config AI."""
        if self.spec.source_hint not in _ACTIVE_PROJECT_BUTTON_ONLY_SOURCES:
            return
        destination_layout = self.tab_header_template.project_root_layout
        self._install_active_project_proxy_identity(destination_layout)
        self._install_active_project_command_buttons(
            destination_layout=destination_layout,
            insert_index=destination_layout.count(),
        )

    def _install_active_project_proxy_identity(
        self,
        destination_layout: object,
    ) -> None:
        """Install one read-only shell projection of Active Project identity."""
        if self.active_project_label is not None:
            return

        label = QLabel("Active Project:")
        label.setObjectName(
            f"{self.spec.tab_id or 'tool'}_active_project_label"
        )
        self._style_active_project_label(label)

        path_edit = QLineEdit()
        path_edit.setObjectName(
            f"{self.spec.tab_id or 'tool'}_active_project_path_edit"
        )
        path_edit.setReadOnly(True)
        path_edit.setMinimumWidth(0)
        path_edit.setMaximumWidth(360)
        path_edit.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        path_edit.setToolTip("Shell-owned Active Project source root.")
        self._style_active_project_path(path_edit)

        destination_layout.insertWidget(destination_layout.count(), label, 0)
        destination_layout.insertWidget(destination_layout.count(), path_edit, 0)
        self.tab_header_template.activate_project_root_slot()
        self.active_project_label = label
        self.active_project_path_edit = path_edit
        self.refresh_active_project_controls()

    def _install_active_project_header_controls(
        self,
        *,
        label: QWidget | None,
        path_widget: QWidget | None,
        browse_button: QWidget | None,
        path_minimum_width: int = 0,
    ) -> None:
        """Install one tab-local command surface for shell Project authority."""
        if not isinstance(label, QLabel) or not isinstance(path_widget, QWidget):
            return

        self._style_active_project_label(label)
        minimum_width = max(0, int(path_minimum_width))
        path_widget.setMinimumWidth(minimum_width)
        path_widget.setMaximumWidth(360)
        horizontal_policy = (
            QSizePolicy.Preferred
            if minimum_width > 0
            else QSizePolicy.Ignored
        )
        path_widget.setSizePolicy(
            horizontal_policy,
            QSizePolicy.Preferred,
        )
        self._style_active_project_path(path_widget)

        destination_layout = self.tab_header_template.project_root_layout
        label_index = destination_layout.indexOf(label)
        path_index = destination_layout.indexOf(path_widget)
        if label_index >= 0 and path_index != label_index + 1:
            with contextlib.suppress(Exception):
                destination_layout.removeWidget(path_widget)
            destination_layout.insertWidget(label_index + 1, path_widget, 0)
        self.tab_header_template.activate_project_root_slot()
        if isinstance(browse_button, QWidget):
            with contextlib.suppress(Exception):
                destination_layout.removeWidget(browse_button)
            browse_button.hide()

        self._install_active_project_command_buttons(
            destination_layout=destination_layout,
            insert_index=destination_layout.indexOf(path_widget) + 1,
        )

    def _install_active_project_command_buttons(
        self,
        *,
        destination_layout: object,
        insert_index: int,
    ) -> None:
        """Install one proxy button pair for the shell-owned Project commands."""
        if self.active_project_select_button is not None:
            return

        select_button = QPushButton("Select Active Project")
        select_button.setObjectName(
            f"{self.spec.tab_id or 'tool'}_select_active_project_button"
        )
        select_button.clicked.connect(self.request_select_active_project)

        eject_button = QPushButton("Eject Active Project")
        eject_button.setObjectName(
            f"{self.spec.tab_id or 'tool'}_eject_active_project_button"
        )
        eject_button.clicked.connect(self.request_eject_active_project)

        destination_layout.insertWidget(insert_index, select_button, 0)
        destination_layout.insertWidget(insert_index + 1, eject_button, 0)
        self.active_project_select_button = select_button
        self.active_project_eject_button = eject_button
        self.refresh_active_project_controls()

    @staticmethod
    def _find_refactor_report_project_root_button(widget: QWidget) -> QPushButton | None:
        """Return the Refactor Report project-folder browse button."""
        try:
            buttons = widget.findChildren(QPushButton)
        except (AttributeError, TypeError):
            return None
        for button in buttons:
            text = str(button.text() or "")
            if "Select Project Folder" in text:
                return button
        return None

    @staticmethod
    def _hide_refactor_report_mode_a_group(widget: QWidget) -> None:
        """Hide the old Refactor Report Mode A project-files body group."""
        try:
            groups = widget.findChildren(QGroupBox)
        except (AttributeError, TypeError):
            return
        for group in groups:
            title = str(group.title() or "")
            if title.startswith("Mode A: from project files"):
                group.hide()
        try:
            domain_label = widget.domain_label
        except AttributeError:
            domain_label = None
        if domain_label is not None:
            try:
                domain_label.hide()
            except AttributeError:
                pass

    @staticmethod
    def _move_widget_to_layout(widget: QWidget, destination_layout: object, index: int) -> None:
        """Detach one widget from its current layout and insert it elsewhere."""
        parent = widget.parentWidget()
        parent_layout = parent.layout() if parent is not None else None
        if parent_layout is not None:
            with contextlib.suppress(Exception):
                parent_layout.removeWidget(widget)
        widget.setParent(None)
        try:
            destination_layout.insertWidget(index, widget, 0)
        except (AttributeError, TypeError):
            try:
                destination_layout.addWidget(widget, 0)
            except (AttributeError, TypeError):
                return

