# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py
"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
import contextlib
from pathlib import Path
from PySide6.QtWidgets import QMessageBox, QWidget
from ..app_constants import _COLLECTOR_SUBTABS_TO_REMOVE
from ..gui_support import _find_button_by_text, _prune_named_subtabs, _replace_exact_label_text, _safe_disconnect
from ..tool_specs import ToolSpec
__all__: list[str] = []

class _WindowToolPatchesMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    def _on_tool_loaded(self, spec: ToolSpec, widget: QWidget) -> None:
        """Support on tool loaded behavior.
        
        Parameters
        ----------
        spec : ToolSpec
            The spec value.
        widget : QWidget
            The widget value.
        """
        
        self._patch_common_project_root_fields(widget)
        if 'reasoner_context_collector' in spec.source_hint:
            self._collector_widget = widget
            self._patch_collector_widget(widget)
        elif 'daily_rfctr_report' in spec.source_hint:
            self._daily_refactor_widget = widget
            self._patch_daily_refactor_widget(widget)
        if self.current_project_root is not None:
            self._propagate_project_root(self.current_project_root)

    def _lazy_page_for_tab_index(self, index: int) -> QWidget | None:
        """Return the lazy page at a visible tab index after reordering."""
        page = getattr(self, '_lazy_pages_by_tab_index', {}).get(index)
        if page is not None:
            return page
        try:
            widget = self.tabs.widget(index)
        except Exception:
            return None
        if widget.__class__.__name__ == 'LazyToolTab':
            return widget
        return None

    def _load_initial_tab(self) -> None:
        """Support load initial tab behavior.
        """
        
        index = self.tabs.currentIndex()
        page = self._lazy_page_for_tab_index(index)
        if page is not None:
            page.ensure_loaded()

    def _on_tab_changed(self, index: int) -> None:
        """Support on tab changed behavior.
        
        Parameters
        ----------
        index : int
            The index value.
        """
        
        page = self._lazy_page_for_tab_index(index)
        if page is not None:
            page.ensure_loaded()

    def _patch_collector_widget(self, widget: QWidget) -> None:
        """Support patch collector widget behavior.
        
        Parameters
        ----------
        widget : QWidget
            The widget value.
        """
        
        _replace_exact_label_text(widget, 'Output JSON:', 'Output folder:')
        _prune_named_subtabs(widget, _COLLECTOR_SUBTABS_TO_REMOVE)
        if hasattr(widget, 'close_button'):
            widget.close_button.hide()
        if hasattr(widget, 'browse_output_button'):
            widget.browse_output_button.hide()
        if hasattr(widget, 'output_json_edit'):
            widget.output_json_edit.setReadOnly(True)
        if hasattr(widget, 'runtime_trace_json_edit'):
            widget.runtime_trace_json_edit.setReadOnly(True)
        if hasattr(widget, 'project_root_edit'):
            _safe_disconnect(widget.project_root_edit.textChanged)
            widget.project_root_edit.textChanged.connect(self._on_collector_project_root_changed)
            if self.current_project_root is not None:
                widget.project_root_edit.setText(str(self.current_project_root))
        if hasattr(widget, 'run_button') and hasattr(widget, '_run_collector'):
            widget._original_run_collector = widget._run_collector
            _safe_disconnect(widget.run_button.clicked)
            widget.run_button.clicked.connect(lambda: self._run_collector_via_wrapper(widget))
        if hasattr(widget, 'project_root_edit'):
            self._bind_project_root_field(widget.project_root_edit)
            self._on_collector_project_root_changed(widget.project_root_edit.text())

    def _on_collector_project_root_changed(self, text: str) -> None:
        """Support on collector project root changed behavior.
        
        Parameters
        ----------
        text : str
            The text value.
        """
        
        project_root = self._normalize_project_root(text)
        if project_root is None:
            return
        self._propagate_project_root(project_root)

    def _run_collector_via_wrapper(self, widget: QWidget) -> None:
        """Support run collector via wrapper behavior.
        
        Parameters
        ----------
        widget : QWidget
            The widget value.
        """
        
        project_root = self._normalize_project_root(widget.project_root_edit.text())
        if project_root is None:
            widget._original_run_collector()
            return
        self._remember_project_root(project_root)
        if self._output_dirs_have_content(project_root):
            if not self._confirm_delete_existing_outputs(project_root):
                if hasattr(widget, 'status_bar'):
                    with contextlib.suppress(Exception):
                        widget.status_bar.showMessage('Collector run cancelled. Existing files were kept.')
                return
            try:
                self._reset_output_dirs(project_root)
            except Exception as exc:
                show_error_copy_close_window(self, title='Delete failed', message=f'Failed to clear existing files before running the collector.\n\nDetails: {exc}')
                return
        display_folder = self._json_complete_dir(project_root)
        complete_json = self._collector_complete_file(project_root)
        runtime_trace = self._collector_runtime_trace_file(project_root)
        try:
            if hasattr(widget, 'output_json_edit'):
                widget.output_json_edit.setText(str(complete_json))
            if hasattr(widget, 'runtime_trace_json_edit'):
                widget.runtime_trace_json_edit.setText(str(runtime_trace))
            widget._original_run_collector()
        finally:
            if hasattr(widget, 'output_json_edit'):
                widget.output_json_edit.setText(str(display_folder))
            if hasattr(widget, 'runtime_trace_json_edit'):
                widget.runtime_trace_json_edit.setText(str(runtime_trace))
        self._propagate_project_root(project_root)

    def _patch_daily_refactor_widget(self, widget: QWidget) -> None:
        """Support patch daily refactor widget behavior.
        
        Parameters
        ----------
        widget : QWidget
            The widget value.
        """
        
        for line_name in ('domain_edit', 'json_folder_edit', 'json_name_edit', 'ai_bundle_edit'):
            if hasattr(widget, line_name):
                getattr(widget, line_name).setReadOnly(True)
        for button_text in ('Select Project Folder...', 'Choose Folder', 'Set Bundle Path...', 'X  Clear'):
            button = _find_button_by_text(widget, button_text)
            if button is not None:
                button.hide()
        if self.current_project_root is not None:
            self._apply_project_root_to_daily_refactor(self.current_project_root)

    def _propagate_project_root(self, project_root: Path) -> None:
        """Apply the selected project root to every loaded workflow tab."""
        self._remember_project_root(project_root)
        if self._is_propagating_project_root:
            return
        self._is_propagating_project_root = True
        try:
            for widget in self._iter_loaded_tool_widgets():
                for line_edit in self._iter_project_root_fields(widget):
                    self._set_project_root_field_text(line_edit, project_root)
            if self._collector_widget is not None:
                self._apply_project_root_to_collector(self._collector_widget, project_root)
            if self._daily_refactor_widget is not None:
                self._apply_project_root_to_daily_refactor(project_root)
        finally:
            self._is_propagating_project_root = False

    def _apply_project_root_to_collector(self, widget: QWidget, project_root: Path) -> None:
        """Apply the shared project root to the collector tab fields."""
        complete_folder = self._json_complete_dir(project_root)
        runtime_trace = self._collector_runtime_trace_file(project_root)
        if hasattr(widget, 'project_root_edit'):
            self._set_project_root_field_text(widget.project_root_edit, project_root)
        if hasattr(widget, 'output_json_edit'):
            widget.output_json_edit.setText(str(complete_folder))
        if hasattr(widget, 'runtime_trace_json_edit'):
            widget.runtime_trace_json_edit.setText(str(runtime_trace))

    def _apply_project_root_to_daily_refactor(self, project_root: Path) -> None:
        """Support apply project root to daily refactor behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        """
        
        widget = self._daily_refactor_widget
        if widget is None:
            return
        docs_root = self._daily_refactor_output_root(project_root)
        bundle_file = self._daily_refactor_bundle_file(project_root)
        project_name = self._project_name(project_root)
        try:
            widget._domain_root = project_root
        except Exception:
            pass
        try:
            widget._json_folder = docs_root
        except Exception:
            pass
        try:
            widget._json_name = project_name
        except Exception:
            pass
        try:
            widget._ai_bundle_path = bundle_file
        except Exception:
            pass
        if hasattr(widget, 'domain_edit'):
            widget.domain_edit.setText(str(project_root))
        if hasattr(widget, 'domain_label'):
            widget.domain_label.setText(f'Mode A active: {project_name}')
            widget.domain_label.setStyleSheet('color: #2ecc71;')
        if hasattr(widget, 'json_name_edit'):
            widget.json_name_edit.setText(project_name)
        if hasattr(widget, 'json_folder_edit'):
            widget.json_folder_edit.setText(str(docs_root))
        if hasattr(widget, 'ai_bundle_edit'):
            widget.ai_bundle_edit.setText(str(bundle_file))
        if hasattr(widget, '_refresh_config'):
            with contextlib.suppress(Exception):
                widget._refresh_config()
        if hasattr(widget, '_update_ui_for_mode'):
            with contextlib.suppress(Exception):
                widget._update_ui_for_mode()
        if hasattr(widget, 'status_bar'):
            with contextlib.suppress(Exception):
                widget.status_bar.showMessage(f'Auto-configured from Step 4: {project_name} -> {docs_root}')
