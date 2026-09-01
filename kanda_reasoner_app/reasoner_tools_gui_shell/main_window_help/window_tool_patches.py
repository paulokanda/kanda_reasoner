# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py
"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
from kanda_reasoner_app.portable_smoke_runtime_report import (
    record_portable_smoke_event,
)
import contextlib
from pathlib import Path
from PySide6.QtWidgets import QWidget
from ..app_constants import _COLLECTOR_SUBTABS_TO_REMOVE
from ..gui_support import _find_button_by_text, _prune_named_subtabs, _replace_exact_label_text, _safe_disconnect
from ..tool_specs import ToolSpec
__all__: list[str] = []

class _WindowToolPatchesMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    def _on_tool_loaded(self, spec: ToolSpec, widget: QWidget) -> None:
        """Register one loaded tool and bind it to the canonical Project."""
        if spec.tab_id:
            self._loaded_tools_by_tab_id[spec.tab_id] = widget
        self._patch_common_project_root_fields(widget)
        self._apply_project_widget_enabled_state(spec.tab_id, widget)
        if 'reasoner_context_collector' in spec.source_hint:
            self._collector_widget = widget
            self._patch_collector_widget(widget)
        elif 'daily_rfctr_report' in spec.source_hint:
            self._daily_refactor_widget = widget
            self._patch_daily_refactor_widget(widget)
        if self.current_project_root is not None:
            self._propagate_project_root(
                self.current_project_root,
                boundary=self.current_project_boundary,
            )

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
        """Load the initial tab without changing canonical shell geometry."""
        index = self.tabs.currentIndex()
        page = self._lazy_page_for_tab_index(index)
        if page is None:
            return

        self._record_lazy_tab_activation(page)
        try:
            before_size = self.size()
            was_maximized = self.isMaximized()
        except Exception:
            before_size = None
            was_maximized = False

        page.ensure_loaded()
        if before_size is None or was_maximized:
            return

        try:
            from PySide6.QtCore import QTimer

            QTimer.singleShot(
                0,
                lambda size=before_size: self._restore_tab_switch_size(size),
            )
        except Exception:
            self._restore_tab_switch_size(before_size)

    @staticmethod
    def _record_lazy_tab_activation(page: QWidget) -> None:
        """Record the tab boundary before packaged lazy construction begins."""
        spec = getattr(page, "spec", None)
        source = str(getattr(spec, "source_hint", "") or "")
        record_portable_smoke_event(
            status="PASS",
            kind="lazy_tab_activation",
            source=source,
            message="ACTIVATING",
        )

    def _on_tab_changed(self, index: int) -> None:
        """Keep the user's current shell size stable across tab loading."""
        page = self._lazy_page_for_tab_index(index)
        try:
            before_size = self.size()
            was_maximized = self.isMaximized()
        except Exception:
            before_size = None
            was_maximized = False

        if page is not None:
            self._record_lazy_tab_activation(page)
            page.ensure_loaded()

        if before_size is None or was_maximized:
            return

        try:
            from PySide6.QtCore import QTimer

            QTimer.singleShot(
                0,
                lambda size=before_size: self._restore_tab_switch_size(size),
            )
        except Exception:
            self._restore_tab_switch_size(before_size)

    def _restore_tab_switch_size(self, size) -> None:
        """Restore the exact pre-switch size after lazy tab loading."""
        try:
            if bool(self.property("kandaMainWindowFixedSize")):
                return
            if self.isMaximized():
                return
            self.setMinimumSize(0, 0)
            self.resize(size)
        except Exception:
            return

    def _patch_collector_widget(self, widget: QWidget) -> None:
        """Support patch collector widget behavior.
        
        Parameters
        ----------
        widget : QWidget
            The widget value.
        """
        
        _replace_exact_label_text(widget, 'Output JSON:', 'Output folder:')
        _prune_named_subtabs(widget, _COLLECTOR_SUBTABS_TO_REMOVE)
        for control_name in (
            'project_root_label',
            'project_root_edit',
            'backup_every_day_button',
            'cancel_backup_button',
        ):
            control = getattr(widget, control_name, None)
            if isinstance(control, QWidget):
                control.show()
        if self.current_project_root is None and hasattr(widget, 'project_root_edit'):
            widget.project_root_edit.clear()
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
            widget.project_root_edit.setProperty(
                "pyarchitect_project_root_bound",
                False,
            )
            widget.project_root_edit.textChanged.connect(
                self._on_collector_project_root_changed
            )
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
        self._propagate_project_root(project_root, explicit_selection=True)

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
        if not self._propagate_project_root(
            project_root,
            explicit_selection=True,
        ):
            return
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
        self._propagate_project_root(
            project_root,
            boundary=self.current_project_boundary,
        )

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

    def _propagate_project_root(
        self,
        project_root: Path,
        *,
        explicit_selection: bool = False,
        boundary=None,
    ) -> bool:
        """Switch the canonical observed Project through explicit selection."""
        if self._is_propagating_project_root:
            return False

        old_root = self.current_project_root
        changed = old_root is None or old_root != project_root
        if changed:
            block_reason = self._project_switch_block_reason()
            if block_reason:
                self._restore_canonical_project_root_fields()
                self._show_project_switch_block(block_reason)
                return False

        next_boundary = boundary
        if next_boundary is None and explicit_selection:
            next_boundary = self._register_explicit_project_root(project_root)
        if next_boundary is None:
            current = getattr(self, "current_project_boundary", None)
            if (
                current is not None
                and current.active_project_root == project_root
            ):
                next_boundary = current
        if next_boundary is None:
            return False

        self._is_propagating_project_root = True
        try:
            if changed:
                self._reset_loaded_project_scopes()
                self._project_switch_ticket += 1
                self._remember_project_boundary(next_boundary)

            for widget in self._iter_loaded_tool_widgets():
                self._apply_root_to_loaded_widget(widget, project_root)

            if self._collector_widget is not None:
                self._apply_project_root_to_collector(
                    self._collector_widget,
                    project_root,
                )
            if self._daily_refactor_widget is not None:
                self._apply_project_root_to_daily_refactor(project_root)
            self._set_loaded_project_scopes_enabled(True)
            self._refresh_active_project_controls()
        finally:
            self._is_propagating_project_root = False
        return True

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
