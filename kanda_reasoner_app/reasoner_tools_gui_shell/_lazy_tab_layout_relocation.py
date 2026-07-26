# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py
"""Explicit header-layout relocation behavior for the lazy tool tab host."""

from __future__ import annotations

import contextlib

from PySide6.QtWidgets import QGroupBox, QLabel, QPushButton, QWidget

from ._lazy_tab_shell_chrome import (
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

    def _move_error_memory_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Error Memory Project Root controls into the header template."""
        if self.spec.source_hint != _ERROR_MEMORY_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return

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

    def _move_freeze_after_update_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Freeze Feature After Update Project Root controls into the header."""
        if self.spec.source_hint != _FREEZE_AFTER_UPDATE_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return

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
            label.setStyleSheet("color: #0B3D91; font-weight: bold; padding-left: 4px;")
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

        self._hide_refactor_report_mode_a_group(widget)

    def _move_project_qa_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Project Q&A project-root controls into the header template."""
        if self.spec.source_hint != _PROJECT_QA_GUI_SOURCE:
            return

        try:
            widget.move_project_root_controls_to_layout(self.tab_header_template.project_root_layout)
        except (AttributeError, TypeError):
            return

    def _move_project_qa_ai_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Project Q&A local-AI controls into the header template."""
        if self.spec.source_hint != _PROJECT_QA_GUI_SOURCE:
            return

        try:
            widget.move_ai_runtime_controls_to_layout(self.tab_header_template.ai_group_layout)
        except (AttributeError, TypeError):
            return

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

