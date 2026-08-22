# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_change_preview.py
"""Display Project Web AI Shadow previews and local authorization entry."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
    ProjectWebAIShadowPreview,
)

__all__ = ["ProjectWebAIChangePreviewDialog"]


class ProjectWebAIChangePreviewDialog(QDialog):
    """Show one validated Shadow proposal before local human authorization."""

    def __init__(
        self,
        preview: ProjectWebAIShadowPreview,
        *,
        delete_callback: Callable[[], None],
        apply_callback: Callable[[], None] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Build a read-only Preview dialog for one transient operation."""
        super().__init__(parent)
        self._preview = preview
        self._delete_callback = delete_callback
        self._apply_callback = apply_callback
        self.setWindowTitle("Web AI - Shadow Preview")
        self.setModal(False)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.resize(980, 760)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        heading = QLabel("Validated Shadow Preview")
        heading.setStyleSheet("font-size: 18px; font-weight: 650;")
        root.addWidget(heading)

        warning = QLabel(
            "Project source is unchanged until explicit local authorization. "
            "The remote AI has no write, shell, installation, Error Memory, "
            "or Freeze authority."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "background:#2a2215; color:#ffd58a; padding:10px; "
            "border:1px solid #6a5124; border-radius:6px;"
        )
        root.addWidget(warning)

        form = QFormLayout()
        form.setHorizontalSpacing(12)
        form.addRow("Operation", QLabel(preview.operation_id))
        form.addRow("Shadow root", _selectable_label(preview.shadow_root))
        form.addRow("Summary", _selectable_label(preview.summary))
        root.addLayout(form)

        selector_row = QHBoxLayout()
        selector_row.addWidget(QLabel("Target file"))
        self.target_combo = QComboBox()
        for target in preview.targets:
            self.target_combo.addItem(target.relative_path)
        selector_row.addWidget(self.target_combo, 1)
        root.addLayout(selector_row)

        self.target_details = QPlainTextEdit()
        self.target_details.setReadOnly(True)
        self.target_details.setMaximumHeight(120)
        root.addWidget(self.target_details)

        diff_heading = QLabel("Exact proposed unified diff")
        diff_heading.setStyleSheet("font-weight: 600;")
        root.addWidget(diff_heading)
        self.diff_box = QPlainTextEdit()
        self.diff_box.setReadOnly(True)
        self.diff_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        root.addWidget(self.diff_box, 1)

        evidence = QPlainTextEdit()
        evidence.setReadOnly(True)
        evidence.setMaximumHeight(180)
        evidence.setPlainText(_evidence_text(preview))
        root.addWidget(evidence)

        action_row = QHBoxLayout()
        delete_button = QPushButton("Delete Preview")
        delete_button.setToolTip(
            "Delete the transient Shadow operation. Project source is not touched."
        )
        delete_button.clicked.connect(self._delete_preview)
        action_row.addWidget(delete_button)
        if self._apply_callback is not None:
            apply_button = QPushButton("Record Reviewed Proposal")
            apply_button.setObjectName("projectWebAIAuthorizeApplyButton")
            apply_button.setToolTip(
                "Require exact human confirmation and record support-side proposal evidence only."
            )
            apply_button.clicked.connect(self._authorize_apply)
            action_row.addWidget(apply_button)
        action_row.addStretch(1)
        close_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_buttons.rejected.connect(self.close)
        action_row.addWidget(close_buttons)
        root.addLayout(action_row)

        self.target_combo.currentIndexChanged.connect(self._render_target)
        self._render_target()

    def _render_target(self) -> None:
        """Render the selected target hashes, path, and exact diff."""
        index = self.target_combo.currentIndex()
        if index < 0 or index >= len(self._preview.targets):
            self.target_details.clear()
            self.diff_box.clear()
            return
        target = self._preview.targets[index]
        self.target_details.setPlainText(
            "Relative path: "
            + target.relative_path
            + "\nOriginal SHA-256: "
            + target.original_sha256
            + "\nProposed SHA-256: "
            + target.proposed_sha256
            + "\nPython syntax: "
            + target.python_syntax_status
            + "\nShadow file: "
            + target.shadow_path
        )
        self.diff_box.setPlainText(target.unified_diff)


    def _authorize_apply(self) -> None:
        """Delegate explicit proposal recording to the owning workflow."""
        if self._apply_callback is not None:
            self._apply_callback()

    def _delete_preview(self) -> None:
        """Delete only the transient Preview after explicit confirmation."""
        approved = QMessageBox.question(
            self,
            "Delete Shadow Preview",
            "Delete this transient Shadow Preview? Project source is unchanged.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if approved != QMessageBox.StandardButton.Yes:
            return
        self._delete_callback()
        self.close()


def _selectable_label(text: str) -> QLabel:
    """Return one wrapping label whose text may be copied."""
    label = QLabel(str(text))
    label.setWordWrap(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return label


def _evidence_text(preview: ProjectWebAIShadowPreview) -> str:
    """Return compact validation, contract, validator, and risk evidence."""
    sections = [
        "PREVIEW VALIDATION\n" + "\n".join(preview.validation_markers),
        "AFFECTED PUBLIC CONTRACTS\n"
        + ("\n".join(preview.affected_public_contracts) or "None declared"),
        "REQUIRED INSTALLED-SOURCE VALIDATORS\n"
        + ("\n".join(preview.required_validators) or "None declared"),
        "KNOWN RISKS\n" + ("\n".join(preview.known_risks) or "None declared"),
        "NEXT AUTHORITY\nOnly the local governed write broker may mutate source "
        "after exact human authorization. The remote AI cannot invoke it.",
    ]
    return "\n\n".join(sections)
