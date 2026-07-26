"""Qt dialog for optional ZIP or structured-text external AI return intake."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

__all__ = ["choose_external_ai_return_input"]


def choose_external_ai_return_input(
    *,
    start_path: str | Path,
    parent=None,
) -> tuple[str, str]:
    """Return ('text'|'zip'|'', payload) from one bounded import dialog."""
    dialog = QDialog(parent)
    dialog.setWindowTitle("Import AI Answer")
    dialog.resize(900, 650)
    layout = QVBoxLayout(dialog)
    explanation = QLabel(
        "Paste the complete KANDA_AI_CANDIDATE_RETURN marker-wrapped JSON below, "
        "or choose a governed AI answer ZIP. Both routes use the same lineage and "
        "complete candidate-family validation before creating an append-only Project "
        "Support return generation. No canonical Project source is changed."
    )
    explanation.setWordWrap(True)
    layout.addWidget(explanation)
    editor = QPlainTextEdit()
    editor.setPlaceholderText(
        "KANDA_AI_CANDIDATE_RETURN_BEGIN\n{ ...complete structured answer... }\n"
        "KANDA_AI_CANDIDATE_RETURN_END"
    )
    layout.addWidget(editor)
    buttons = QHBoxLayout()
    text_button = QPushButton("Import Structured Text")
    zip_button = QPushButton("Choose AI Answer ZIP")
    cancel_button = QPushButton("Cancel")
    buttons.addWidget(text_button)
    buttons.addWidget(zip_button)
    buttons.addStretch(1)
    buttons.addWidget(cancel_button)
    layout.addLayout(buttons)
    result: dict[str, str] = {"mode": "", "value": ""}

    def accept_text() -> None:
        text = editor.toPlainText().strip()
        if not text:
            return
        result["mode"] = "text"
        result["value"] = text
        dialog.accept()

    def choose_zip() -> None:
        answer_zip, _ = QFileDialog.getOpenFileName(
            dialog,
            "Import AI Answer ZIP",
            str(start_path),
            "ZIP archives (*.zip)",
        )
        if not answer_zip:
            return
        result["mode"] = "zip"
        result["value"] = answer_zip
        dialog.accept()

    text_button.clicked.connect(accept_text)
    zip_button.clicked.connect(choose_zip)
    cancel_button.clicked.connect(dialog.reject)
    dialog.exec()
    return result["mode"], result["value"]
