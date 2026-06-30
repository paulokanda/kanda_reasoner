# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/manual_docstring_review_editor.py
"""Manual docstring review dialog for Tab 3."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
)

from kanda_reasoner_app.tab3_manual_review_runtime.review_support import (
    _classify_location_after_tab1_refresh,
    _docstring_text_or_placeholder,
    _format_review_row_context,
    _save_manual_review_state,
)

__all__ = [
    "DocstringReviewEditorDialog",
]


class _DocstringReviewEditorDialog(QDialog):
    """Review and persist one proposed docstring row."""

    def __init__(self, owner: object, row: dict) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        owner : object
            The owning object.
        row : dict
            The row data.
        """
        
        super().__init__(owner)
        self._owner = owner
        self._row = row
        self.setWindowTitle("Manual docstring review")
        self.resize(980, 720)
        self._build_ui()

    def _build_ui(self) -> None:
        """Build dialog controls."""
        layout = QVBoxLayout(self)
        self._context = QPlainTextEdit()
        self._context.setReadOnly(True)
        self._context.setPlainText(_format_review_row_context(self._owner, self._row))

        self._classification_combo = QComboBox()
        self._classification_combo.addItems(
            [
                "unsaved/new",
                "corrected",
                "still_missing",
                "dubious",
            ]
        )
        saved_classification = str(self._row.get("classification", "") or "")
        if saved_classification:
            self._classification_combo.setCurrentText(saved_classification)

        self._draft_edit = QPlainTextEdit()
        state = str(self._row.get("classification") or "unsaved/new")
        draft = str(self._row.get("draft_docstring") or "")
        self._draft_edit.setPlainText(draft or _docstring_text_or_placeholder(self._row, state))

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save
            | QDialogButtonBox.Cancel
            | QDialogButtonBox.Apply
        )
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        apply_button = buttons.button(QDialogButtonBox.Apply)
        if apply_button is not None:
            apply_button.clicked.connect(self._refresh_from_tab1)

        layout.addWidget(QLabel("Source context"))
        layout.addWidget(self._context, 2)
        layout.addWidget(QLabel("Classification"))
        layout.addWidget(self._classification_combo)
        layout.addWidget(QLabel("Reviewed docstring draft"))
        layout.addWidget(self._draft_edit, 1)
        layout.addWidget(buttons)

    def _save_and_accept(self) -> None:
        """Persist the current review decision and close the dialog."""
        self._save_state()
        self.accept()

    def _refresh_from_tab1(self) -> None:
        """Refresh classification from Tab 1 audit evidence."""
        classification, message = _classify_location_after_tab1_refresh(
            self._owner,
            self._row,
        )
        self._classification_combo.setCurrentText(classification)
        self._context.setPlainText(
            _format_review_row_context(self._owner, self._row) + message
        )
        self._save_state()

    def _save_state(self) -> None:
        """Save this row's review state to the sidecar state file."""
        self._row["classification"] = self._classification_combo.currentText()
        self._row["draft_docstring"] = self._draft_edit.toPlainText()
        if not str(self._row.get("approval_state", "")).strip():
            self._row["approval_state"] = "approved"
        _save_manual_review_state(self._owner, self._row, self._draft_edit.toPlainText())


DocstringReviewEditorDialog = _DocstringReviewEditorDialog
