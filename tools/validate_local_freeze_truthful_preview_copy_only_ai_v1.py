# project-path: tools/validate_local_freeze_truthful_preview_copy_only_ai_v1.py
"""Validate truthful blocked Freeze previews and clipboard-only AI handoff."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "local-freeze-truthful-preview-copy-only-ai-v1"
CHANGED_PYTHON = (
    "kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_preview_presentation.py",
    "tools/validate_local_freeze_truthful_preview_copy_only_ai_v1.py",
)


def _read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_source(root: Path) -> None:
    for relative in CHANGED_PYTHON:
        path = root / relative
        _require(path.is_file(), "Missing changed Python file: " + relative)
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        _require(len(source.splitlines()) <= 500, "Module exceeds 500 lines: " + relative)
        source.encode("ascii")
    print("LOCAL_FREEZE_TRUTHFUL_PREVIEW_PYTHON_SYNTAX: PASS")
    print("LOCAL_FREEZE_TRUTHFUL_PREVIEW_MODULE_SIZE: PASS")
    print("LOCAL_FREEZE_TRUTHFUL_PREVIEW_ASCII_SOURCE: PASS")

    widgets = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    )
    runtime = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    )
    clipboard = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py",
    )
    presentation = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_preview_presentation.py",
    )
    help_md = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/help_source/freeze_feature_after_update_help.md",
    )
    help_html = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/freeze_feature_after_update_help.html",
    )

    _require('QPushButton("Copy Entry to AI")' in widgets, "Copy-only button label missing")
    _require("Copy and Open External AI" not in widgets, "Legacy button label remains")
    _require("without opening an external site" in widgets, "Copy-only tooltip missing")
    _require("copy_freeze_formulary_to_clipboard" in runtime, "Clipboard action not wired")
    _require("handoff_freeze_formulary_to_external_ai" not in runtime, "Open action remains wired")
    _require("handoff_to_selected_external_ai" not in clipboard, "External opener remains in clipboard owner")
    _require("external_ai_workflow" not in clipboard, "Clipboard owner still imports external workflow")
    _require("clipboard.setText(prompt)" in clipboard, "Clipboard write contract missing")
    _require("No external site was opened" in runtime, "User-facing copy-only result missing")
    _require("FREEZE PREVIEW NOT READY" in presentation, "Blocked Preview marker missing")
    _require("intentionally not rendered as a frozen" in presentation, "Truthful Preview rule missing")
    _require("Copy Entry to AI" in help_md and "Copy Entry to AI" in help_html, "Help not updated")
    _require("Copy and Open External AI" not in help_md, "Legacy help action remains in Markdown")
    _require("Copy and Open External AI" not in help_html, "Legacy help action remains in HTML")
    print("LOCAL_FREEZE_COPY_ONLY_BUTTON_CONTRACT: PASS")
    print("LOCAL_FREEZE_EXTERNAL_OPEN_REMOVED: PASS")
    print("LOCAL_FREEZE_HELP_COPY_ONLY_SYNC: PASS")


def _validate_truthful_presentation(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.freeze_after_update_gui._local_freeze_preview_presentation import (
        render_local_freeze_preview,
    )
    from kanda_reasoner_app.freeze_hint_intake.form_text_validation import (
        _has_safe_validation_evidence_marker,
    )

    blocked = {
        "ok": False,
        "is_writable": False,
        "errors": [
            "FREEZE BLOCKED - no recognizable validation evidence found in "
            "validation_evidence_summary."
        ],
        "warnings": [],
        "markdown": (
            "---\nstatus: \"frozen\"\n---\n"
            "Status: `frozen after explicit human confirmation and validation evidence`\n"
        ),
    }
    rendered = render_local_freeze_preview(blocked)
    _require("FREEZE PREVIEW NOT READY" in rendered, "Blocked Preview is not visibly marked")
    _require("no recognizable validation evidence" in rendered, "Blocked reason was lost")
    _require('status: "frozen"' not in rendered, "Blocked Preview exposes frozen frontmatter")
    _require("Status: `frozen" not in rendered, "Blocked Preview exposes frozen status prose")

    validation_blocked = {
        "ok": True,
        "is_writable": True,
        "errors": [],
        "warnings": [],
        "markdown": "status: frozen\n",
    }
    rendered = render_local_freeze_preview(
        validation_blocked,
        {"ok": False, "errors": ["VALIDATION BLOCKED"], "warnings": []},
    )
    _require("FREEZE PREVIEW NOT READY" in rendered, "Validation failure is not marked")
    _require("status: frozen" not in rendered, "Validation failure exposes frozen draft")

    writable = {
        "ok": True,
        "is_writable": True,
        "errors": [],
        "warnings": [],
        "markdown": "# Writable validated Preview\n",
    }
    rendered = render_local_freeze_preview(
        writable,
        {"ok": True, "errors": [], "warnings": []},
    )
    _require(rendered == "# Writable validated Preview\n", "Writable Preview was altered")

    narrative = (
        "Requires source, AST, module-size, isolated registry selection, "
        "real-Qt heartbeat, installer, rollback, and ZIP-contract checks."
    )
    _require(
        not _has_safe_validation_evidence_marker(narrative),
        "Narrative-only evidence was incorrectly recognized",
    )
    exact = "VALIDATION OK: current-feature\nSTATUS: IN_SYNC"
    _require(
        _has_safe_validation_evidence_marker(exact),
        "Literal local validation markers were not recognized",
    )
    print("LOCAL_FREEZE_BLOCKED_PREVIEW_NOT_FROZEN: PASS")
    print("LOCAL_FREEZE_WRITABLE_PREVIEW_PRESERVED: PASS")
    print("LOCAL_FREEZE_NARRATIVE_EVIDENCE_REJECTED: PASS")
    print("LOCAL_FREEZE_LITERAL_EVIDENCE_RECOGNIZED: PASS")


def _validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from PySide6.QtWidgets import QApplication, QPushButton

    from kanda_reasoner_app.freeze_after_update_gui._external_ai_formulary_handoff import (
        copy_freeze_formulary_to_clipboard,
    )
    from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
        build_local_freeze_dialog_widgets,
    )

    app = QApplication.instance() or QApplication([])
    widgets = build_local_freeze_dialog_widgets(None, disabled_action_style="")
    try:
        buttons = {button.text(): button for button in widgets.dialog.findChildren(QPushButton)}
        _require("Copy Entry to AI" in buttons, "Real Qt dialog lacks Copy Entry to AI")
        _require("Copy and Open External AI" not in buttons, "Real Qt dialog exposes legacy open action")
        _require(
            "without opening an external site" in buttons["Copy Entry to AI"].toolTip(),
            "Real Qt copy-only tooltip is missing",
        )
        prompt = copy_freeze_formulary_to_clipboard(
            {
                "feature_title": "Current validated feature",
                "validated_files": "module.py",
                "validation_evidence_summary": (
                    "VALIDATION OK: current-feature\nSTATUS: IN_SYNC"
                ),
            }
        )
        clipboard_text = app.clipboard().text()
        _require(clipboard_text == prompt, "Clipboard does not contain the generated prompt")
        _require("KANDA_FREEZE_FORM_JSON_BEGIN" in clipboard_text, "Transport marker missing")
        _require("VALIDATION OK: current-feature" in clipboard_text, "Validation line lost")
    finally:
        widgets.dialog.close()
        app.processEvents()
    print("LOCAL_FREEZE_COPY_ONLY_REAL_QT: PASS")
    print("LOCAL_FREEZE_TRUTHFUL_PREVIEW_COPY_ONLY_REAL_QT: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    _validate_source(root)
    _validate_truthful_presentation(root)
    _validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
