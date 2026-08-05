# project-path: kanda_reasoner_app/freeze_after_update_gui/_freeze_memory_exports.py
"""Frozen-memory export and help-window methods for the Freeze tab."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QTextEdit, QVBoxLayout

from kanda_reasoner_app.freeze_after_update.freeze_state import entry_files, parse_frontmatter
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window, show_error_copy_close_window

__all__ = ["FreezeMemoryExportMixin"]

SEND_ZIP_FREEZE_PROMPT_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/self_contained_freeze_entry_intake_zip.md"
)


class FreezeMemoryExportMixin:
    """Clipboard and help-window behavior for frozen memory snippets."""

    def _send_zip_freeze_prompt_path(self) -> Path:
        """Return the Tool-owned canonical Send zip freeze prompt path."""
        return (
            Path(__file__).resolve(strict=False).parents[2]
            / SEND_ZIP_FREEZE_PROMPT_RELATIVE_PATH
        )

    def _copy_send_zip_freeze_prompt(self) -> None:
        """Copy the canonical self-contained freeze-entry ZIP prompt."""
        prompt_path = self._send_zip_freeze_prompt_path()
        if not prompt_path.exists() or not prompt_path.is_file():
            show_error_copy_close_window(
                self,
                title="Send zip freeze prompt copy failed",
                message="Send zip freeze prompt not found: " + str(prompt_path),
            )
            return
        try:
            prompt_text = prompt_path.read_text(encoding="utf-8")
            QApplication.clipboard().setText(prompt_text)
        except Exception as exc:
            show_error_copy_close_window(
                self,
                title="Send zip freeze prompt copy failed",
                message=str(exc),
            )
            return
        self._append_log("Copied Send zip freeze prompt to clipboard: " + str(prompt_path))
        show_auto_close_action_window(
            self,
            title="Send zip freeze",
            message="Self-contained freeze-entry ZIP prompt copied to clipboard.",
            detail_text="Source: self_contained_freeze_entry_intake_zip.md",
        )

    def _freeze_entry_sort_key(self, entry_path: Path) -> tuple[str, int, str]:
        """Return a stable sort key for freeze entries."""
        try:
            meta = parse_frontmatter(entry_path.read_text(encoding="utf-8-sig"))
        except Exception:
            meta = {}
        date_text = str(meta.get("date") or "")
        try:
            mtime_ns = entry_path.stat().st_mtime_ns
        except OSError:
            mtime_ns = 0
        return (date_text, mtime_ns, entry_path.name)

    def _freeze_entry_candidates(self) -> list[Path]:
        """Return freeze entry files for the active project, newest last."""
        project_root = self._require_project_root()
        if project_root is None:
            return []
        try:
            return sorted(entry_files(project_root), key=self._freeze_entry_sort_key)
        except Exception as exc:
            show_error_copy_close_window(self, title="Could not read frozen entries", message=str(exc))
            return []

    def _build_freeze_snippet_text(self, entries: list[Path], *, title: str) -> str:
        """Build a copy/paste-safe freeze-memory snippet for AI."""
        project_root = self._project_root()
        project_text = str(project_root) if project_root is not None else ""
        lines: list[str] = []
        lines.append("KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN")
        lines.append("Title: " + title)
        lines.append("Project root: " + project_text)
        lines.append("Entry count: " + str(len(entries)))
        lines.append(
            "Instruction: Use this as read-only frozen feature memory. Do not edit these entries directly. "
            "Do not write project-specific memory into project_freeze_ledger."
        )
        lines.append(
            "Authority: Frontmatter status and superseded_by, plus newer corrective entries, govern. "
            "For an entry already marked frozen, pre-validation or planned-next-step prose is historical "
            "and must not be treated as pending work."
        )
        lines.append("")
        for index, entry_path in enumerate(entries, start=1):
            lines.append("--- FROZEN ENTRY " + str(index) + " OF " + str(len(entries)) + " ---")
            lines.append("Path: " + str(entry_path))
            lines.append("")
            try:
                lines.append(entry_path.read_text(encoding="utf-8-sig").rstrip())
            except Exception as exc:
                lines.append("[Could not read entry: " + str(exc) + "]")
            lines.append("")
        lines.append("KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END")
        return "\n".join(lines).rstrip() + "\n"

    def _copy_last_freeze_snippet(self) -> None:
        """Copy the latest freeze entry as an AI-ready snippet."""
        entries = self._freeze_entry_candidates()
        if not entries:
            QMessageBox.information(self, "No frozen entries", "No freeze entries were found for the active project.")
            return
        latest = entries[-1]
        snippet = self._build_freeze_snippet_text([latest], title="Last frozen feature entry")
        QApplication.clipboard().setText(snippet)
        self._append_log("Copied latest frozen feature snippet to clipboard: " + str(latest))
        show_auto_close_action_window(
            self,
            title="Get Last Freeze",
            message="Latest frozen feature snippet copied to clipboard.",
        )

    def _copy_all_frozen_snippets(self) -> None:
        """Copy all freeze entries as an AI-ready snippet."""
        entries = self._freeze_entry_candidates()
        if not entries:
            QMessageBox.information(self, "No frozen entries", "No freeze entries were found for the active project.")
            return
        snippet = self._build_freeze_snippet_text(entries, title="All frozen feature entries")
        QApplication.clipboard().setText(snippet)
        self._append_log("Copied all frozen feature snippets to clipboard. Entry count: " + str(len(entries)))
        show_auto_close_action_window(
            self,
            title="Get All Frozen",
            message="All frozen feature snippets copied to clipboard.",
        )

    def _build_freeze_form_blueprint_text(self) -> str:
        """Return the transport-safe AI prompt for local freeze-form output."""
        return """KANDA FREEZE FORM BLUEPRINT FOR AI

Task for AI:
Create or correct one KANDA Reasoner local freeze-entry formulary for the current validated feature only.
Return exactly one receive-ready block. Do not write prose before or after the block.
Do not invent validation evidence. If local validation evidence is missing, say that the freeze form cannot be completed yet instead of fabricating markers.

Strict output contract:
- The first visible characters of your answer must be KANDA_FREEZE_FORM_JSON_BEGIN.
- The last visible characters of your answer must be KANDA_FREEZE_FORM_JSON_END.
- Between the markers, put one valid JSON object inside one fenced json code block.
- Use double quotes for every JSON key and string value.
- Use JSON arrays for validated_files, generated_files, protected_paths, do_not_regress_rules, and validation_evidence_summary.
- Preserve every existing array item exactly and in order.
- Encode Windows backslashes as doubled backslashes or \\u005C.
- Do not place JSON in ordinary Markdown prose.
- Do not use comments or trailing commas.
- Use project-relative paths where possible.
- Keep project-specific frozen memory under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.
- Do not store project-specific frozen memory inside project_freeze_ledger.

Required validation evidence:
validation_evidence_summary must contain real local markers when validation completed, preferably:
VALIDATION OK: <feature_id>
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Copy/paste-ready answer shape:
KANDA_FREEZE_FORM_JSON_BEGIN
```json
{
  "feature_title": "<exact current feature title>",
  "primary_box": "<project-relative owning box/path>",
  "box_type": "<module/gui/tool/prompt/etc>",
  "validated_files": ["<validated path 1>", "<validated path 2>"],
  "generated_files": ["<generated artifact or n/a>"],
  "protected_paths": ["<protected path 1>"],
  "do_not_regress_rules": ["<rule 1>"],
  "validation_evidence_summary": ["VALIDATION OK: <feature_id>", "STATUS: IN_SYNC"],
  "known_warnings": "<known warnings or n/a>",
  "planned_next_step": "<next human action, usually Preview then Confirm and Write>",
  "notes": "<short freeze notes for future AI>"
}
```
KANDA_FREEZE_FORM_JSON_END
"""

    def _copy_freeze_form_blueprint(self) -> None:
        """Copy the strict freeze-form blueprint prompt for AI."""
        QApplication.clipboard().setText(self._build_freeze_form_blueprint_text())
        self._append_log("Copied KANDA freeze-form blueprint to clipboard.")
        show_auto_close_action_window(
            self,
            title="Get blueprint Freeze",
            message="KANDA freeze-form blueprint copied to clipboard.",
            detail_text=(
                "Paste it to AI when the local freeze entry formulary needs a "
                "strict KANDA_FREEZE_FORM_JSON_BEGIN / END structure."
            ),
        )

    def _show_what_to_say_window(self) -> None:
        """Support show what to say window behavior.
        """
        
        what_to_say_path = self._what_to_say_path()
        if what_to_say_path is None:
            QMessageBox.warning(self, "Project missing", "Select a project folder first.")
            return
        if not what_to_say_path.exists():
            QMessageBox.warning(
                self,
                "Instruction file missing",
                "The instruction file does not exist yet.\n\n"
                "The deprecated external AI review export button has been removed. "
                "Use Show Project to AI artifacts for full external review.\n\n"
                f"Expected path:\n{what_to_say_path}",
            )
            return
        try:
            text = what_to_say_path.read_text(encoding="utf-8")
        except Exception as exc:
            show_error_copy_close_window(self, title="Could not read instruction file", message=str(exc))
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("what_to_say_to_ai_freeze_feature.md")
        dialog.resize(900, 700)
        layout = QVBoxLayout(dialog)
        warning = QLabel('Warning: file "what_to_say_to_ai_freeze_feature.md" should not be edited manually here or anywhere else.')
        warning.setWordWrap(True)
        warning_font = QFont()
        warning_font.setBold(True)
        warning.setFont(warning_font)
        layout.addWidget(warning)
        path_label = QLabel(str(what_to_say_path))
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)
        layout.addWidget(text_edit, 1)
        button_row = QHBoxLayout()
        copy_button = QPushButton("Copy Complete Text")
        close_button = QPushButton("Close")
        button_row.addStretch(1)
        button_row.addWidget(copy_button)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)

        def copy_complete_text() -> None:
            QApplication.clipboard().setText(text_edit.toPlainText())
            self._append_log("Copied complete what_to_say_to_ai_freeze_feature.md text.")

        copy_button.clicked.connect(copy_complete_text)
        close_button.clicked.connect(dialog.close)
        self._what_to_say_dialog = dialog
        self._what_to_say_text_edit = text_edit
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _help_document_path(self) -> Path:
        """Return the local rendered Freeze help document path."""
        return Path(__file__).with_name("freeze_feature_after_update_help.html")

    def _create_help_document_view(self):
        """Create the richest available local HTML help view."""
        from PySide6.QtCore import QUrl

        help_path = self._help_document_path()
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView

            view = QWebEngineView()
            view.setUrl(QUrl.fromLocalFile(str(help_path)))
            return view
        except Exception:
            from PySide6.QtWidgets import QTextBrowser

            browser = QTextBrowser()
            browser.setReadOnly(True)
            browser.setOpenExternalLinks(False)
            browser.setSource(QUrl.fromLocalFile(str(help_path)))
            return browser

    def _help_copy_text(self) -> str:
        """Return readable help text for the clipboard action."""
        source_path = Path(__file__).with_name("help_source") / (
            "freeze_feature_after_update_help.md"
        )
        try:
            return source_path.read_text(encoding="utf-8")
        except Exception:
            return (
                "Freeze Feature After Update help is available at:\n"
                + str(self._help_document_path())
            )

    def _show_help_window(self) -> None:
        """Open the rich local Freeze Feature After Update help window."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Freeze Feature After Update - Help")
        dialog.resize(1120, 860)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        help_view = self._create_help_document_view()
        layout.addWidget(help_view, 1)
        button_row = QHBoxLayout()
        copy_button = QPushButton("Copy Complete Help Text")
        close_button = QPushButton("Close")
        button_row.addStretch(1)
        button_row.addWidget(copy_button)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)

        def copy_complete_help_text() -> None:
            QApplication.clipboard().setText(self._help_copy_text())
            self._append_log("Copied complete Freeze Feature After Update help text.")

        copy_button.clicked.connect(copy_complete_help_text)
        close_button.clicked.connect(dialog.close)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
