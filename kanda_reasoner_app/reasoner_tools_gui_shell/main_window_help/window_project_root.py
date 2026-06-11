"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QLineEdit, QWidget

from kanda_reasoner_app.project_root_resolver import normalize_project_root_text

__all__: list[str] = []


class _WindowProjectRootMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    def _remember_project_root(self, project_root: Path | None) -> None:
        """Persist the last selected project root for the whole tool shell."""
        if project_root is None:
            return
        self.current_project_root = project_root
        if hasattr(self, "ignore_rules_tab"):
            self.ignore_rules_tab.set_project_root(project_root)
        self._save_prefs()

    def _iter_loaded_tool_widgets(self) -> list[QWidget]:
        """Return embedded widgets that are already loaded in lazy tabs."""
        widgets: list[QWidget] = []
        for page in self._pages:
            widget = getattr(page, "_embedded_widget", None)
            if isinstance(widget, QWidget):
                widgets.append(widget)
        return widgets

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
        """Bind and synchronize common project-root fields for any tab."""
        for field in self._iter_project_root_fields(widget):
            self._bind_project_root_field(field)
            if self.current_project_root is not None:
                self._set_project_root_field_text(
                    field,
                    self.current_project_root,
                )

    def _on_any_project_root_text_changed(self, text: str) -> None:
        """Remember and propagate project-root changes from any loaded tab."""
        if self._is_propagating_project_root:
            return

        project_root = self._normalize_project_root(text)
        if project_root is None:
            return

        self._propagate_project_root(project_root)

    @staticmethod
    def _normalize_project_root(text: str) -> Path | None:
        """Normalize a user-provided project root path."""
        return normalize_project_root_text(text)
