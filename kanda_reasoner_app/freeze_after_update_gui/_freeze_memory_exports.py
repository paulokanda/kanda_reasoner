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
HOW_TO_FREEZE_PROMPT_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md"
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

    def _how_to_freeze_prompt_path(self) -> Path:
        """Return the Tool-owned canonical How to Freeze prompt path."""
        return (
            Path(__file__).resolve(strict=False).parents[2]
            / HOW_TO_FREEZE_PROMPT_RELATIVE_PATH
        )

    def _copy_how_to_freeze_prompt(self) -> None:
        """Copy the current canonical KPR-03-003 freeze workflow prompt."""
        prompt_path = self._how_to_freeze_prompt_path()
        if not prompt_path.exists() or not prompt_path.is_file():
            show_error_copy_close_window(
                self,
                title="How to Freeze prompt copy failed",
                message="Canonical freeze prompt not found: " + str(prompt_path),
            )
            return
        try:
            prompt_text = prompt_path.read_text(encoding="utf-8")
            QApplication.clipboard().setText(prompt_text)
        except Exception as exc:
            show_error_copy_close_window(
                self,
                title="How to Freeze prompt copy failed",
                message=str(exc),
            )
            return
        self._append_log(
            "Copied canonical How to Freeze prompt to clipboard: "
            + str(prompt_path)
        )
        show_auto_close_action_window(
            self,
            title="How to Freeze",
            message="Canonical KPR-03-003 freeze workflow prompt copied to clipboard.",
            detail_text="Source: freeze_code_intake_and_form_protocol.md",
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
        """Return the canonical audited generic Freeze blueprint for AI."""
        return """KANDA FREEZE FORM - GENERIC RECEIVE-READY TEMPLATE v4

Use this structure only after the strict pre-output governance audit has passed.

```json
{
  "feature_title": "<EXACT EFFECTIVE NON-SUPERSEDED FEATURE TITLE>",
  "primary_box": "<EXACT PROJECT-RELATIVE OWNING BOX OR PATH>",
  "box_type": "<EXACT SUPPORTED TYPE>",

  "validated_files": [
    "<ONLY FILES ACTUALLY COVERED BY CURRENT VALIDATION>"
  ],

  "generated_files": [],

  "protected_paths": [
    "<EVIDENCE-BACKED PROTECTED PATH>",
    "project_freeze_after_update/frozen_features_memory/"
  ],

  "do_not_regress_rules": [
    "<VALIDATED BEHAVIORAL OR ARCHITECTURAL CONTRACT>",
    "<SECOND VALIDATED CONTRACT>",
    "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.",
    "Do not store project-specific frozen memory inside project_freeze_ledger.",
    "Preview Freeze Entry must remain read-only and must not write files.",
    "Confirm and Write must require explicit human confirmation before writing governed freeze memory.",
    "After a local freeze write, the AI startup freeze context must be refreshed."
  ],

  "validation_evidence_summary": [
    "<EXACT CURRENT FEATURE-SPECIFIC PASS MARKER>",
    "<OTHER EXACT CURRENT VALIDATION MARKER IF GENUINELY PRODUCED>",
    "VALIDATION OK: <EXACT_CURRENT_FEATURE_ID>",
    "STATUS: IN_SYNC"
  ],

  "known_warnings": "<STATE ONLY REAL WARNINGS. DISTINGUISH CURRENT VALIDATION FROM HISTORICAL EVIDENCE. IF AN ORIGINAL PATCH ZIP IS UNAVAILABLE, SAY SO. IF ZIP CONTRACT: PASS WAS NOT GENUINELY PRODUCED FOR THIS EXACT RELEASE, DO NOT CLAIM IT. USE n/a ONLY IF THERE ARE GENUINELY NO MATERIAL WARNINGS.>",

  "planned_next_step": "<ONLY ACTION THAT REMAINS GENUINELY PENDING AFTER THE COMPLETE CURRENT CONFIRM AND WRITE TRANSACTION HAS FINISHED. DO NOT REPEAT PREVIEW, CONFIRM AND WRITE, HINT CONSUMPTION, STARTUP/COMPLIANCE REFRESH, INDEXING, OR ANY WRITER/GUI-OWNED ACTION ALREADY COMPLETED. IF NO IMMEDIATE ACTION REMAINS, STATE A FUTURE DURABLE TRIGGER SUCH AS VERIFYING THIS FROZEN CONTRACT IN A LATER SESSION OR CREATING ANOTHER FREEZE ONLY FOR A SEPARATELY VALIDATED LATER REVISION/CORRECTION.>",

  "notes": "Release owner: <KANDA_TOOL_RELEASE | EXTERNAL_PROJECT_RELEASE | NOT_APPLICABLE>. Effective non-superseded feature: <EXACT_FEATURE_ID>. Governing source patch ZIP: <EXACT_PATCH_ZIP_IF_GENUINELY_KNOWN_OR_n/a>. Governing patch SHA-256: <EXACT_SHA256_IF_GENUINELY_KNOWN_OR_n/a>. <SHORT DURABLE SUMMARY OF WHAT THIS FEATURE FREEZES>. <STATE SUPERSESSION RELATIONSHIP ONLY IF VERIFIED>. Project-specific durable frozen memory belongs under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory and not project_freeze_ledger."
}
```

MANDATORY TEMPLATE RULES

1. Never replace unknown information with guessed information.
2. `validated_files` means validated files, not merely related files.
3. For the unified Freeze receiver, `generated_files` must be `[]` when there are no generated files. Never create a synthetic `"n/a"` path entry.
4. `protected_paths` must be evidence-backed and use the verified owner namespace/root convention.
5. `validation_evidence_summary` contains evidence, not rewritten interpretations. Prefer literal validator output when possible.
6. The exact current feature must have `VALIDATION OK: <exact_feature_id>` and `STATUS: IN_SYNC` before the candidate may be emitted.
7. A subordinate checker marker may support the evidence but never substitutes for the exact current-feature marker.
8. Include `ZIP CONTRACT: PASS` only when that exact marker was genuinely produced for the exact release and is applicable to the classified release owner.
9. Historical evidence must be explicitly identifiable as historical when material.
10. Never insert writer-owned fields: `freeze_id`, writer status, writer timestamp/date, owner metadata, durable entry path, `freeze_store_kind`, or `superseded_by`.
11. Before output, inspect the actual current freeze store for an existing same-feature freeze, duplicates, predecessors, superseded entries, conflicting active revisions, and legitimate correction/replacement state.
12. If the required current-state check cannot be performed, stop with `FREEZE CANDIDATE NOT READY`. Do not guess.
13. Classify release provenance as `KANDA_TOOL_RELEASE`, `EXTERNAL_PROJECT_RELEASE`, or `NOT_APPLICABLE` before applying ZIP-specific rules. Never hardcode one release-owner class into a generic template.
14. Resolve every path-bearing field against its actual owner root. Never add or strip `_show_project_to_AI`, `first_prompt_files`, `project_freeze_after_update`, or another prefix by intuition.
15. Treat `KANDA_FREEZE_HINT.json` according to the artifact class: it is governed evidence for a manual candidate, while patch-owned freeze artifacts may have a stricter same-source contract.
16. Before output, strictly parse exactly one JSON object, reject duplicate object keys, reject non-standard `NaN`/`Infinity` constants, verify the exact 11-field schema and field types, and ensure no writer-owned field or chat/tool artifact leaked into the object.
17. Never send a schema-invalid failure object to the Freeze receiver. If a mandatory gate fails, return ordinary chat beginning exactly with `FREEZE CANDIDATE NOT READY` and emit no Freeze JSON candidate.
18. Never send a candidate first and audit it afterward. The candidate shown to the user must already have passed JSON/schema validation, exact feature identity, current freeze-store and supersession audit, validation-evidence and provenance audit, ownership/path audit, complete durable post-write transaction simulation, and a second independent audit.
19. `planned_next_step` must remain true after the full current Confirm and Write transaction returns. It must not repeat Preview, Confirm and Write, automatic hint consumption, startup/compliance refresh, indexing, or another writer/GUI-owned action already completed by that transaction.
20. The canonical AI-produced Freeze candidate is one raw 11-field JSON object with array-valued multiline fields and no mandatory marker or Markdown envelope. Legacy marker/fence input may be accepted by the receiver only as compatibility input.
21. If current receiver/source behavior differs from this template, fail closed and reconcile this prompt plus `Get Blueprint Freeze` before emitting a candidate.
"""

    def _copy_freeze_form_blueprint(self) -> None:
        """Copy the strict freeze-form blueprint prompt for AI."""
        QApplication.clipboard().setText(self._build_freeze_form_blueprint_text())
        self._append_log("Copied KANDA freeze-form blueprint to clipboard.")
        show_auto_close_action_window(
            self,
            title="Get Blueprint Freeze",
            message="KANDA freeze-form blueprint copied to clipboard.",
            detail_text=(
                "Paste it to AI when the local freeze entry formulary needs the "
                "canonical strict 11-field raw JSON structure."
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
