# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/dialogs.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Provide browsing, confirmation, help, and save-output dialogs.
# EXPORTS       : browse_report_path, browse_root, confirm_write, show_help, save_output
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Dialog helpers for the missing-docstrings GUI."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QMessageBox

from ..mode_options_hlp import MODE_OPTIONS_HELP_TEXT, tool_limitations_summary

__all__ = [
    "browse_report_path",
    "browse_root",
    "confirm_write",
    "show_help",
    "save_output",
]


def browse_report_path(self) -> None:
    """Handle browse report path.
    """

    path, _ = QFileDialog.getSaveFileName(
        self,
        "Choose run report path",
        self._report_path_edit.text().strip() or str(Path.cwd() / "run_report.jsonl"),
        "JSONL Files (*.jsonl);;All Files (*)",
    )
    if path:
        self._report_path_edit.setText(path)
        self._save_prefs()

def browse_root(self) -> None:
    """Handle browse root.
    """

    path = QFileDialog.getExistingDirectory(
        self,
        "Select project root",
        self._root_path_edit.text().strip() or str(Path.cwd()),
    )
    if path:
        self._root_path_edit.setText(path)
        self._save_prefs()

def show_help(self) -> None:
    """Show  help.
    """

    sections: list[str] = []
    for key in ("scan", "diff", "write"):
        description = MODE_OPTIONS_HELP_TEXT.get(key)
        if description:
            sections.append(f"{key.capitalize()}\n- {description}")
    if tool_limitations_summary is not None:
        sections.append("Important limitation\n- " + tool_limitations_summary().replace("\n", "\n- "))
    sections.append(
        "AI model chooser\n"
        "- Refresh installed models queries the local Ollama host for locally installed models.\n"
        "- The model field stays editable so you can type a model name manually."
    )
    sections.append(
        "Review workflow\n"
        "- Every run can write a JSONL report.\n"
        "- The review pane highlights fallback and low-confidence results.\n"
        "- Use the filter to focus on items that likely need human review."
    )
    sections.append(
        "Scope selector\n"
        "- Full project processes all Python files under the root.\n"
        "- Package/folder restricts the run to one selected directory/package.\n"
        "- Module/file restricts the run to one selected Python file."
    )
    QMessageBox.information(self, "Help", "\n\n".join(sections) or "No help text available.")

def save_output(self) -> None:
    """Save  output.
    """

    path, _ = QFileDialog.getSaveFileName(
        self,
        "Save output",
        str(Path.cwd() / "missing_docstrings_output.txt"),
        "Text Files (*.txt)",
    )
    if not path:
        return
    Path(path).write_text(self._output.toPlainText(), encoding="utf-8")
    self.statusBar().showMessage(f"Saved output to {path}")


def confirm_write(self) -> bool:
    """Return whether the user confirms write mode."""
    box = QMessageBox(self)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle("Confirm write")
    box.setText("Write mode will insert missing docstrings into source files.")
    box.setInformativeText("Only missing docstrings will be inserted. Continue?")
    box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    box.setDefaultButton(QMessageBox.No)
    return box.exec() == QMessageBox.Yes
