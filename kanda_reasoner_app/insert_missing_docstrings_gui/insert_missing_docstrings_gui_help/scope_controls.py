# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/scope_controls.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Manage project scope selection and target path browsing.
# EXPORTS       : update_scope_controls, effective_target_module, effective_target_package, browse_target_path
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Scope selection helpers for the missing-docstrings GUI."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QFileDialog

__all__ = [
    "update_scope_controls",
    "effective_target_module",
    "effective_target_package",
    "browse_target_path",
]


def update_scope_controls(self, _value: str | None = None) -> None:
    """Handle update scope controls.

    Parameters
    ----------
    _value : str | None, optional
        TODO: describe _value.
    """

    scope = self._scope_combo.currentText()
    enabled = scope != "Full project"
    self._target_path_edit.setEnabled(enabled)
    self._browse_target_button.setEnabled(enabled)
    self._clear_target_button.setEnabled(enabled)
    if scope == "Module/file":
        self._browse_target_button.setText("Browse module...")
        self._target_path_edit.setPlaceholderText("pkg/module.py or pkg.module")
    elif scope == "Package/folder":
        self._browse_target_button.setText("Browse package...")
        self._target_path_edit.setPlaceholderText("pkg/subpkg or pkg.subpkg")
    else:
        self._browse_target_button.setText("Browse...")
        self._target_path_edit.setPlaceholderText("")
        if self._target_path_edit.text().strip():
            self._target_path_edit.clear()

def effective_target_module(self) -> str | None:
    """Handle effective target module.

    Returns
    -------
    str | None
        TODO: describe the return value.
    """

    if self._scope_combo.currentText() != "Module/file":
        return None
    value = self._target_path_edit.text().strip()
    return value or None

def effective_target_package(self) -> str | None:
    """Handle effective target package.

    Returns
    -------
    str | None
        TODO: describe the return value.
    """

    if self._scope_combo.currentText() != "Package/folder":
        return None
    value = self._target_path_edit.text().strip()
    return value or None

def browse_target_path(self) -> None:
    """Handle browse target path.
    """

    root_text = self._root_path_edit.text().strip() or str(Path.cwd())
    root_path = Path(root_text)
    scope = self._scope_combo.currentText()
    if scope == "Module/file":
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Python module/file",
            str(root_path if root_path.exists() else Path.cwd()),
            "Python Files (*.py)",
        )
    elif scope == "Package/folder":
        path = QFileDialog.getExistingDirectory(
            self,
            "Select package/folder",
            str(root_path if root_path.exists() else Path.cwd()),
        )
    else:
        return

    if not path:
        return

    selected = Path(path)
    try:
        display = str(selected.resolve().relative_to(root_path.resolve())).replace("\\", "/")
    except Exception:
        display = str(selected)
    self._target_path_edit.setText(display)
    self._save_prefs()
