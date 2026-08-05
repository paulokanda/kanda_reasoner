# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_project_root.py
"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QWidget,
)

from kanda_reasoner_app.project_root_resolver import normalize_project_root_text
from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRegistryError,
)
from ..project_scope_sync import (
    PROJECT_SCOPED_TAB_IDS,
    apply_project_root_to_widget,
    project_switch_block,
    request_project_scope_settlement,
    reset_project_scoped_widget,
)

_OUTPUT_ROOT_SUFFIXES = ("_show_project_to_AI", "_delete_after_daily_work")
_SHOW_PROJECT_CHILD_NAMES = {
    "first_prompt_files",
    "second_prompt_files",
    "second_prompt_files_building",
    "project_error_memory",
    "project_freeze_after_update",
    "json_splitted",
}
_ERROR_MEMORY_CHILD_NAMES = {
    "pending_ai_assisted_error_lesson_intake",
    "lessons",
    "exports",
    "schemas",
    "freeze_hint_intake",
    "frozen_features_memory",
    "files_to_send_ai",
}

__all__: list[str] = []


class _WindowProjectRootMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    def _remember_project_boundary(self, boundary) -> None:
        """Persist one strict boundary selected through Tool authority."""
        self.current_project_boundary = boundary
        self.current_project_root = boundary.active_project_root
        if hasattr(self, "ignore_rules_tab"):
            self.ignore_rules_tab.set_project_root(
                boundary.active_project_root
            )
        self._set_loaded_project_scopes_enabled(True)
        self._refresh_active_project_controls()
        self._save_prefs()

    def _remember_project_root(self, project_root: Path | None) -> None:
        """Compatibility facade that records only an explicit selection."""
        if project_root is None:
            return
        boundary = self._register_explicit_project_root(project_root)
        if boundary is not None:
            self._remember_project_boundary(boundary)

    def _register_explicit_project_root(self, project_root: Path):
        """Return a strict boundary for one explicit user-selected root."""
        try:
            return self._project_selection_registry.register_explicit_root(
                project_root
            )
        except ProjectSelectionRegistryError as exc:
            QMessageBox.warning(
                self,
                "Project selection rejected",
                "The Project was not selected because its Tool/Project "
                "identity could not be proven.\n\n" + str(exc),
            )
            return None

    def _iter_loaded_tool_widgets(self) -> list[QWidget]:
        """Return every loaded tool widget exactly once."""
        widgets: list[QWidget] = []
        seen: set[int] = set()
        for widget in self._loaded_tools_by_tab_id.values():
            if isinstance(widget, QWidget) and id(widget) not in seen:
                widgets.append(widget)
                seen.add(id(widget))
        ignore_rules = getattr(self, "ignore_rules_tab", None)
        if isinstance(ignore_rules, QWidget) and id(ignore_rules) not in seen:
            widgets.append(ignore_rules)
        return widgets

    def _iter_loaded_project_widgets(self) -> list[tuple[str, QWidget]]:
        """Return loaded project-scoped tabs with their stable tab IDs."""
        items: list[tuple[str, QWidget]] = []
        for tab_id, widget in self._loaded_tools_by_tab_id.items():
            if tab_id in PROJECT_SCOPED_TAB_IDS and isinstance(widget, QWidget):
                items.append((tab_id, widget))
        ignore_rules = getattr(self, "ignore_rules_tab", None)
        if isinstance(ignore_rules, QWidget):
            items.append(("exclusion_rules", ignore_rules))
        return items

    def _refresh_active_project_controls(self) -> None:
        """Refresh shell-level active Project status and command state."""
        root = self.current_project_root
        label = getattr(self, "active_project_value", None)
        if label is not None:
            label.setText(str(root) if root is not None else "No active Project")
        eject_button = getattr(self, "eject_project_button", None)
        if eject_button is not None:
            eject_button.setEnabled(root is not None)
        for page in getattr(self, "_pages", []):
            refresh = getattr(page, "refresh_active_project_controls", None)
            if callable(refresh):
                refresh(root)

    def _select_active_project(self) -> None:
        """Select one Project through the shell-owned global command."""
        start = str(self.current_project_root or Path.cwd())
        selected = QFileDialog.getExistingDirectory(
            self,
            "Select active Project source root",
            start,
        )
        if not selected:
            return
        project_root = self._normalize_project_root(selected)
        if project_root is not None:
            self._propagate_project_root(project_root, explicit_selection=True)

    def _set_loaded_project_scopes_enabled(self, enabled: bool) -> None:
        """Enable or disable loaded Project-scoped tabs as one shell state."""
        for _tab_id, widget in self._iter_loaded_project_widgets():
            widget.setEnabled(bool(enabled))

    def _apply_project_widget_enabled_state(
        self,
        tab_id: str,
        widget: QWidget,
    ) -> None:
        """Apply current active-Project availability to one loaded widget."""
        if tab_id in PROJECT_SCOPED_TAB_IDS:
            widget.setEnabled(self.current_project_root is not None)

    def _request_project_scope_settlement_reasons(self) -> list[str]:
        """Request cooperative settlement and return remaining block reasons."""
        reasons: list[str] = []
        for tab_id, widget in self._iter_loaded_project_widgets():
            block = request_project_scope_settlement(tab_id, widget)
            if block is not None:
                reasons.append(block.tab_id + ": " + block.reason)
        return reasons

    def _clear_loaded_project_root_fields(self) -> None:
        """Clear every shell-bound Project root editor after safe eject."""
        for widget in self._iter_loaded_tool_widgets():
            for field in self._iter_project_root_fields(widget):
                self._clear_project_root_field(field)

    def _perform_project_eject(self) -> tuple[bool, str]:
        """Clear active authority only after all Project work has settled."""
        if self.current_project_root is None:
            self._refresh_active_project_controls()
            return True, ""

        reasons = self._request_project_scope_settlement_reasons()
        if reasons:
            return False, "\n".join(reasons)

        try:
            self._project_selection_registry.clear_current_selection()
        except ProjectSelectionRegistryError as exc:
            return False, str(exc)

        self._is_propagating_project_root = True
        try:
            self._reset_loaded_project_scopes()
            self._project_switch_epoch += 1
            self.current_project_boundary = None
            self.current_project_root = None
            ignore_rules = getattr(self, "ignore_rules_tab", None)
            if ignore_rules is not None:
                ignore_rules.set_project_root(None)
            self._clear_loaded_project_root_fields()
            self._set_loaded_project_scopes_enabled(False)
            self._refresh_active_project_controls()
            self._save_prefs()
        finally:
            self._is_propagating_project_root = False
        return True, ""

    def _eject_active_project(self) -> None:
        """Confirm and perform one fail-closed global Project eject."""
        if self.current_project_root is None:
            QMessageBox.information(
                self,
                "No active Project",
                "KANDA Reasoner currently has no active Project authority.",
            )
            return
        answer = QMessageBox.question(
            self,
            "Eject active Project",
            "Eject the active Project from KANDA Reasoner?\n\n"
            "Project source and durable Project memory will not be deleted.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        completed, reason = self._perform_project_eject()
        if not completed:
            QMessageBox.warning(
                self,
                "Project eject waiting",
                "Cooperative cancellation was requested where supported. "
                "Project eject remains blocked until all Project-scoped work "
                "settles.\n\n" + reason,
            )
            return
        QMessageBox.information(
            self,
            "Project ejected",
            "Active Project authority was cleared. Project source and durable "
            "Project memory were preserved.",
        )

    def _project_switch_block_reason(self) -> str:
        """Return the first loaded-tab reason that blocks a Project switch."""
        for tab_id, widget in self._iter_loaded_project_widgets():
            block = project_switch_block(tab_id, widget)
            if block is not None:
                return block.tab_id + ": " + block.reason
        return ""

    def _reset_loaded_project_scopes(self) -> None:
        """Clear transient old-Project UI state in every loaded project tab."""
        for tab_id, widget in self._iter_loaded_project_widgets():
            reset_project_scoped_widget(tab_id, widget)

    def _apply_root_to_loaded_widget(
        self,
        widget: QWidget,
        project_root: Path,
    ) -> None:
        """Synchronize one loaded widget field and public root facade."""
        for field in self._iter_project_root_fields(widget):
            self._set_project_root_field_text(field, project_root)
        apply_project_root_to_widget(widget, project_root)

    def _restore_canonical_project_root_fields(self) -> None:
        """Restore all root editors after a fail-closed switch rejection."""
        project_root = self.current_project_root
        if project_root is None:
            for widget in self._iter_loaded_tool_widgets():
                for field in self._iter_project_root_fields(widget):
                    self._clear_project_root_field(field)
            self._refresh_active_project_controls()
            return
        self._is_propagating_project_root = True
        try:
            for widget in self._iter_loaded_tool_widgets():
                self._apply_root_to_loaded_widget(widget, project_root)
        finally:
            self._is_propagating_project_root = False

    def _show_project_switch_block(self, reason: str) -> None:
        """Explain why the canonical active Project did not change."""
        QMessageBox.warning(
            self,
            "Project switch blocked",
            "The active Project was not changed because project-scoped work "
            "is still active or unresolved.\n\n" + reason,
        )

    def _iter_project_root_fields(self, widget: QWidget) -> list[QWidget]:
        """Return known project-root editors owned by a loaded tab."""
        fields: list[QWidget] = []
        seen: set[int] = set()

        for field_name in self._project_root_field_names:
            candidate = getattr(widget, field_name, None)
            if isinstance(candidate, (QLineEdit, QComboBox)) and id(candidate) not in seen:
                fields.append(candidate)
                seen.add(id(candidate))

        return fields

    @staticmethod
    def _project_root_field_text(field: QWidget) -> str:
        """Return text from a supported project-root editor."""
        if isinstance(field, QLineEdit):
            return field.text().strip()
        if isinstance(field, QComboBox):
            return field.currentText().strip()
        return ""

    def _bind_project_root_field(self, field: QWidget) -> None:
        """Bind a root editor so project changes are remembered globally."""
        if bool(field.property("pyarchitect_project_root_bound")):
            return
        field.setProperty("pyarchitect_project_root_bound", True)

        if isinstance(field, QLineEdit):
            field.textChanged.connect(self._on_any_project_root_text_changed)
            return

        if isinstance(field, QComboBox):
            field.currentTextChanged.connect(self._on_any_project_root_text_changed)
            try:
                field.editTextChanged.connect(self._on_any_project_root_text_changed)
            except Exception:
                pass

    @staticmethod
    def _clear_project_root_field(field: QWidget) -> None:
        """Clear one editor when the Tool has no active Project authority."""
        if isinstance(field, QLineEdit):
            field.clear()
            return
        if isinstance(field, QComboBox):
            field.setCurrentText("")

    def _set_project_root_field_text(
        self,
        field: QWidget,
        project_root: Path,
    ) -> None:
        """Set a project-root editor without overwriting equivalent text."""
        root_text = str(project_root)
        if self._project_root_field_text(field) == root_text:
            return

        if isinstance(field, QLineEdit):
            field.setText(root_text)
            return

        if isinstance(field, QComboBox):
            if field.findText(root_text) == -1:
                field.insertItem(0, root_text)
            field.setCurrentText(root_text)

    def _patch_common_project_root_fields(self, widget: QWidget) -> None:
        """Bind all root editors and apply the current canonical Project."""
        for field in self._iter_project_root_fields(widget):
            self._bind_project_root_field(field)
        if self.current_project_root is not None:
            self._apply_root_to_loaded_widget(widget, self.current_project_root)
        else:
            for field in self._iter_project_root_fields(widget):
                self._clear_project_root_field(field)

    def _on_any_project_root_text_changed(self, text: str) -> None:
        """Commit any valid field or Browse result as the active Project."""
        if self._is_propagating_project_root:
            return
        project_root = self._normalize_project_root(text)
        if project_root is None:
            return
        self._propagate_project_root(project_root, explicit_selection=True)

    @staticmethod
    def _source_root_peer_from_suffixed_output(path: Path) -> Path | None:
        """Return an existing source-root sibling for a generated output root."""
        for suffix in _OUTPUT_ROOT_SUFFIXES:
            if not path.name.endswith(suffix):
                continue
            base_name = path.name[: -len(suffix)].strip()
            if not base_name:
                return None
            if base_name == path.parent.name and path.parent.exists() and path.parent.is_dir():
                return path.parent.expanduser().resolve(strict=False)
            peer = (path.parent / base_name).expanduser().resolve(strict=False)
            if peer.exists() and peer.is_dir():
                return peer
            return None
        return None

    @classmethod
    def _project_root_from_output_hint(cls, path: Path) -> Path | None:
        """Resolve generated-output hints back to the real project root.

        The shell-level project root must be the source project folder, not
        ``*_show_project_to_AI``, persistent state children, a child output
        folder, or ``*_delete_after_daily_work``.  Returning ``None`` for
        unmatched output hints prevents stale typo output folders from becoming
        the active project.
        """
        candidate = path
        if candidate.name in _ERROR_MEMORY_CHILD_NAMES:
            parent = candidate.parent
            if parent.name == "project_error_memory":
                candidate = parent

        if candidate.name in _SHOW_PROJECT_CHILD_NAMES:
            parent = candidate.parent
            if parent.name.endswith("_show_project_to_AI"):
                candidate = parent

        return cls._source_root_peer_from_suffixed_output(candidate)

    @classmethod
    def _normalize_project_root(cls, text: str) -> Path | None:
        """Normalize a user-provided project root path.

        Live GUI text changes must not create project output roots for partial
        or misspelled paths.  Only existing directories, or generated-output
        hints that can be resolved back to an existing sibling source root, are
        accepted as the shared project root.
        """
        root = normalize_project_root_text(text)
        if root is None:
            return None

        output_root = cls._project_root_from_output_hint(root)
        if output_root is not None:
            return output_root

        if root.name.endswith(_OUTPUT_ROOT_SUFFIXES):
            return None

        if root.name in (_SHOW_PROJECT_CHILD_NAMES | _ERROR_MEMORY_CHILD_NAMES):
            return None

        if not root.exists() or not root.is_dir():
            return None

        return root
