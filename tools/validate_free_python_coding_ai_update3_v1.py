# project-path: tools/validate_free_python_coding_ai_update3_v1.py
"""Validate governed external-AI draft handoffs for Update 3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import py_compile
import sys
from typing import Sequence

FEATURE_ID = "free-python-coding-ai-governed-draft-handoffs-update3-v1"

CHANGED_FILES = ('kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py', 'kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py', 'kanda_reasoner_app/manage_architecture/architecture_audit_external_ai.py', 'kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py', 'kanda_reasoner_app/freeze_after_update_gui/freeze_feature_after_update_help.html', 'kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py', 'kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py', 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py', 'kanda_reasoner_app/error_memory_gui/_clipboard_export.py', 'kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json', 'kanda_reasoner_app/reasoner_tools_gui_help/error_memory.json', 'kanda_reasoner_app/freeze_after_update_gui/help_source/freeze_feature_after_update_help.md', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/architecture_review.md', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/error_memory.md', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/error_memory.html', 'tools/validate_free_python_coding_ai_update3_v1.py')

FROZEN_HASHES = {'kanda_reasoner_app/python_coding_ai_catalog.py': '3c5631cf438fe152c5226ba011edb68c9fd76eb00a5fae26461f1b5fe7db57b6', 'kanda_reasoner_app/external_ai_configuration.py': 'a2c210f425127d76e645517bca24d8a3c9977c32d1c9a5c5b9fa146db3c40eca', 'kanda_reasoner_app/external_ai_handoff.py': 'c17455d7d9dd5636496a992d9dec6d52f9e0b7c31d06bec4bb8b828d83359b8e', 'kanda_reasoner_app/external_ai_workflow.py': 'c3744472d750bc23bfae740b391822b92ff6707dd9b004322fe94fb9a50e95a6', 'kanda_reasoner_app/web_ai_configuration.py': 'd0e2947aa92781b3685922316ab737b8b149ccbe0d2dfd39d3557e86e66f84ce', 'kanda_reasoner_app/web_ai_model_catalog.py': 'c6c49d12f75b32bc93a73e3424c1a038c05734b73abb9d9c88105e17f5e73f36', 'kanda_reasoner_app/web_ai_provider_runtime.py': '6783226e498235e391e874112639c051ac81100c3ad668cd061194dde934ea55', 'kanda_reasoner_app/project_selection_registry.py': '98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1', 'kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py': 'fc48582fd0ee743945e961735b3be0d516e45763fa1c862817a0cd5d28828b23', 'kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py': 'edb2d66c575505e204a7099db4dbfb938b5fe3ca00b407e5473f202c1e941871', 'kanda_reasoner_app/error_memory_gui/_ai_correction_action.py': 'eeadc89407a360d4e47ef8c51951c770ae8d08066074a69ee454179277193e54', 'kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py': 'b822707c0bb06542cbe15324b9696e0171f9cad6861c1c6a41695ca9e485a8cd', 'portable/PORTABLE_RUNTIME_ALLOWLIST.json': '429af7c6564fc9495b66c83eaac9bdb88a91360205bed7b34b19364ee04dfe1f', 'portable/PORTABLE_BUILDER_MANIFEST.json': '1ca9e8d00ca67c1227c0138eba3f8364ddf0b589abfadfc85dee84024bc49c5c', 'tools/validate_free_python_coding_ai_update1_v1.py': '7e199e68e13901e45ef9a889e06506478996c3dc2107fdd37f55d9205c435cbb', 'tools/validate_free_python_coding_ai_update1_validation_wrapper_v1r2.py': '5a31b1ef29a15c6738c3634907aa775bc0ae9836faf054253d509e74fa7fa729', }


class MemorySettings:
    """Minimal QSettings-compatible fixture."""

    def __init__(self) -> None:
        self.values: dict[str, object] = {}

    def value(self, key: str, default: object = None) -> object:
        """Return a stored value or default."""
        return self.values.get(key, default)

    def setValue(self, key: str, value: object) -> None:
        """Store one value in memory."""
        self.values[str(key)] = value


class FakeDesktopServices:
    """Capture official-site open requests without launching a browser."""

    opened_urls: list[str] = []

    @classmethod
    def openUrl(cls, url: object) -> bool:  # noqa: N802
        """Record one QUrl and report a successful request."""
        cls.opened_urls.append(str(url.toString()))
        return True


class FakeStatusBar:
    """Capture status messages for the Audit Project fixture."""

    def __init__(self) -> None:
        self.message = ""

    def showMessage(self, message: str) -> None:  # noqa: N802
        """Record the latest status message."""
        self.message = str(message)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bootstrap(tool_root: Path) -> None:
    root_text = str(tool_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")


def _source(tool_root: Path, relative: str) -> str:
    return (tool_root / relative).read_text(encoding="utf-8")


def _validate_files(tool_root: Path) -> None:
    for relative in CHANGED_FILES:
        path = tool_root / relative
        _require(path.is_file(), "CHANGED FILE PRESENT " + relative)
        if path.suffix == ".py":
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            _require(len(source.splitlines()) <= 500, "MODULE SIZE <=500 " + relative)
            py_compile.compile(str(path), doraise=True)
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
    print("CHANGED PYTHON AST COMPILE AND JSON: PASS")



def _validate_prior_validator_capabilities(tool_root: Path) -> None:
    relative = "tools/validate_free_python_coding_ai_update2_v1.py"
    path = tool_root / relative
    _require(path.is_file(), "PRIOR VALIDATOR PRESENT " + relative)
    source = path.read_text(encoding="utf-8")
    for token in (
        'FEATURE_ID = "free-python-coding-ai-manual-workflow-handoffs-update2-v1"',
        "UPDATE 1 CONFIG EXTERNAL AI FORWARD COMPATIBILITY: PASS",
        "PRIOR-STAGE VALIDATOR FORWARD COMPATIBILITY: PASS",
    ):
        _require(token in source, "UPDATE 2 VALIDATOR CAPABILITY " + token)
    print("UPDATE 2 VALIDATOR FORWARD COMPATIBILITY: PASS")

def _validate_frozen_sources(tool_root: Path) -> None:
    for relative, expected in FROZEN_HASHES.items():
        path = tool_root / relative
        _require(path.is_file(), "FROZEN SOURCE PRESENT " + relative)
        _require(_sha256(path) == expected, "FROZEN SOURCE HASH " + relative)
    _validate_prior_validator_capabilities(tool_root)
    print("UPDATE 1 AND UPDATE 2 FROZEN CONTRACTS PRESERVED: PASS")
    print("DIRECT LOCAL AND WEB AI ENGINES UNCHANGED: PASS")
    print("PROJECT SELECTION AUTHORITY UNCHANGED: PASS")
    print("PORTABLE MANIFESTS MODIFIED: NO: PASS")


def _validate_freeze_contract(tool_root: Path) -> None:
    handoff = _source(
        tool_root,
        "kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py",
    )
    runtime = _source(
        tool_root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    )
    widgets = _source(
        tool_root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    )
    for token in (
        "draft only",
        "Preview",
        "Confirm and Write",
        "Do not claim validation, Freeze, or write authority.",
        "handoff_to_selected_external_ai",
    ):
        _require(token in handoff, "FREEZE EXTERNAL DRAFT TOKEN " + token)
    _require(
        'QPushButton("Copy and Open External AI")' in widgets,
        "FREEZE EXTERNAL HANDOFF BUTTON",
    )
    _require(
        "handoff_freeze_formulary_to_external_ai(collect_inputs())" in runtime,
        "FREEZE USES SELECTED EXTERNAL ASSISTANT",
    )
    for token in (
        "preview_freeze_entry",
        "validate_freeze_entry_preview",
        "write_confirmed_freeze_entry",
        "confirmation_binding",
        "Receive Formulary from AI",
    ):
        _require(token in runtime, "FREEZE HUMAN GATE PRESERVED " + token)
    _require(
        "write_confirmed_freeze_entry" not in handoff,
        "FREEZE EXTERNAL HANDOFF CANNOT WRITE",
    )
    print("FREEZE PREVIEW AND CONFIRM GATES UNCHANGED: PASS")


def _validate_error_memory_contract(tool_root: Path) -> None:
    helper = _source(
        tool_root,
        "kanda_reasoner_app/error_memory_gui/_clipboard_export.py",
    )
    tab = _source(tool_root, "kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    _require(
        helper.count("handoff_to_selected_external_ai(clipboard_text)") == 2,
        "ERROR MEMORY TWO DRAFT HANDOFFS",
    )
    _require(
        tab.count("QPushButton('Copy and Open External AI')") == 2,
        "ERROR MEMORY TWO EXTERNAL HANDOFF BUTTONS",
    )
    for token in (
        "returned lesson remains a draft",
        "human explicitly selects Memorize Error",
        "cannot save, activate, supersede, or",
    ):
        _require(token in helper, "ERROR MEMORY DRAFT AUTHORITY TOKEN " + token)
    _require(
        "memorize_error_button.clicked.connect(self._memorize_error_from_text_window)" in tab,
        "MEMORIZE ERROR HUMAN BUTTON PRESERVED",
    )
    _require(
        "_memorize_error_from_text_window" not in helper,
        "EXTERNAL ERROR HANDOFF CANNOT MEMORIZE",
    )
    print("ERROR MEMORY HUMAN MEMORIZE GATE UNCHANGED: PASS")


def _validate_audit_contract(tool_root: Path) -> None:
    helper = _source(
        tool_root,
        "kanda_reasoner_app/manage_architecture/architecture_audit_external_ai.py",
    )
    ui = _source(
        tool_root,
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
    )
    actions = _source(
        tool_root,
        "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py",
    )
    for token in (
        "KANDA_AUDIT_EXTERNAL_REVIEW_BEGIN",
        "KANDA_AUDIT_EXTERNAL_REVIEW_END",
        "read-only advisory",
        "Do not modify files",
        "write Freeze memory",
        "create Error Memory",
        "handoff_to_selected_external_ai",
    ):
        _require(token in helper, "AUDIT EXTERNAL REVIEW TOKEN " + token)
    _require(
        'QPushButton("Copy and Open External AI")' in ui,
        "AUDIT EXTERNAL HANDOFF BUTTON",
    )
    _require(
        'setObjectName("audit_project_external_ai_handoff")' in ui,
        "AUDIT EXTERNAL HANDOFF STABLE ID",
    )
    _require(
        "copy_audit_results(self)" in actions,
        "AUDIT COPY OWNER CONSOLIDATED",
    )
    forbidden = (
        "write_confirmed_freeze_entry",
        "memorize_error_from_text_window",
        "apply_patch",
        "write_text(",
        "open(.*w",
    )
    lowered = helper.casefold()
    _require(
        not any(token.casefold() in lowered for token in forbidden),
        "AUDIT EXTERNAL REVIEW HAS NO WRITE AUTHORITY",
    )
    print("AUDIT DETERMINISTIC RESULT REMAINS AUTHORITATIVE: PASS")


def _validate_help(tool_root: Path) -> None:
    files = (
        "kanda_reasoner_app/freeze_after_update_gui/help_source/freeze_feature_after_update_help.md",
        "kanda_reasoner_app/freeze_after_update_gui/freeze_feature_after_update_help.html",
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/error_memory.md",
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/error_memory.html",
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/architecture_review.md",
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html",
    )
    for relative in files:
        text = _source(tool_root, relative)
        _require("Copy and Open External AI" in text, "HELP EXTERNAL HANDOFF " + relative)
    error_help = json.loads(_source(tool_root, "kanda_reasoner_app/reasoner_tools_gui_help/error_memory.json"))
    audit_help = json.loads(_source(tool_root, "kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json"))
    _require(
        any("Copy and Open External AI" in line for line in error_help["display_lines"]),
        "ERROR MEMORY FALLBACK HELP UPDATED",
    )
    _require(
        any("Copy and Open External AI" in line for line in audit_help["display_lines"]),
        "AUDIT FALLBACK HELP UPDATED",
    )


def _validate_qt_runtime() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QCheckBox,
            QLineEdit,
            QPlainTextEdit,
            QWidget,
        )
    except ModuleNotFoundError as exc:
        raise RuntimeError("PySide6 is required for the functional GUI smoke.") from exc

    import kanda_reasoner_app.external_ai_handoff as base_handoff
    import kanda_reasoner_app.manage_architecture.architecture_audit_external_ai as audit_handoff
    from kanda_reasoner_app.error_memory_gui import _clipboard_export
    from kanda_reasoner_app.external_ai_configuration import (
        ExternalAIConfigurationController,
        install_application_external_ai_configuration,
    )
    from kanda_reasoner_app.freeze_after_update_gui._external_ai_formulary_handoff import (
        build_freeze_external_ai_prompt,
        handoff_freeze_formulary_to_external_ai,
    )
    from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
        build_local_freeze_dialog_widgets,
    )

    app = QApplication.instance() or QApplication([])
    settings = MemorySettings()
    settings.setValue("external_ai/selected_assistant_id", "deepseek_chat")
    controller = ExternalAIConfigurationController(settings=settings)
    install_application_external_ai_configuration(controller)

    original_desktop = base_handoff.QDesktopServices
    original_notice = audit_handoff.show_auto_close_action_window
    FakeDesktopServices.opened_urls = []
    base_handoff.QDesktopServices = FakeDesktopServices
    audit_handoff.show_auto_close_action_window = lambda *_args, **_kwargs: None
    try:
        form = {
            "feature_title": "Fixture feature",
            "validated_files": "a.py\nb.py",
            "generated_files": "",
            "protected_paths": "portable/",
            "do_not_regress_rules": "Never write automatically.",
            "validation_evidence_summary": "VALIDATION OK: fixture",
        }
        prompt = build_freeze_external_ai_prompt(form)
        _require(
            "Return exactly one valid JSON object" in prompt
            and "KANDA_FREEZE_FORM_JSON_BEGIN" not in prompt
            and '"validated_files": [' in prompt
            and "VALIDATION OK: fixture" in prompt,
            "FREEZE STRICT EXTERNAL PROMPT RUNTIME",
        )
        freeze_result = handoff_freeze_formulary_to_external_ai(form)
        _require(freeze_result.ok, "FREEZE EXTERNAL HANDOFF RUNTIME")
        _require(
            "Return exactly one valid JSON object" in QApplication.clipboard().text()
            and "KANDA_FREEZE_FORM_JSON_END" not in QApplication.clipboard().text(),
            "FREEZE EXTERNAL CLIPBOARD RUNTIME",
        )

        parent = QWidget()
        widgets = build_local_freeze_dialog_widgets(parent, disabled_action_style="")
        _require(
            widgets.copy_to_ai_button.text() == "Copy and Open External AI",
            "FREEZE GUI BUTTON FUNCTIONAL SMOKE",
        )
        widgets.dialog.close()
        parent.close()

        class FakeTab:
            def __init__(self) -> None:
                self.raw_error_edit = QPlainTextEdit()
                self.received_preview_edit = QPlainTextEdit()
                self.actions: list[tuple[str, str, str]] = []

            def _error_lesson_intake_blueprint_clipboard_text(self, *, context_text: str) -> str:
                return "ACTIVE_READY_TEMPLATE\n" + context_text

            def _show_action_done(self, title: str, message: str, detail: str = "") -> None:
                self.actions.append((title, message, detail))

        tab = FakeTab()
        tab.raw_error_edit.setPlainText("Traceback fixture")
        _clipboard_export.copy_ai_assisted_intake_error_draft_to_clipboard(tab)
        _require(
            "SOURCE WINDOW: AI-assisted error lesson intake" in QApplication.clipboard().text(),
            "ERROR MEMORY INTAKE EXTERNAL HANDOFF RUNTIME",
        )
        tab.received_preview_edit.setPlainText('{"lesson_id": "fixture"}')
        _clipboard_export.copy_error_draft_to_clipboard(tab)
        _require(
            "SOURCE WINDOW: Error Editor" in QApplication.clipboard().text(),
            "ERROR MEMORY EDITOR EXTERNAL HANDOFF RUNTIME",
        )
        _require(
            len(tab.actions) == 2
            and all(item[0] == "External AI handoff ready" for item in tab.actions),
            "ERROR MEMORY HANDOFF NOTIFICATION RUNTIME",
        )

        class FakeAuditWindow(QWidget):
            def __init__(self) -> None:
                super().__init__()
                self._output = QPlainTextEdit()
                self._output.setPlainText("AUDIT RESULT FIXTURE")
                self._include_refactor_report_checkbox = QCheckBox()
                self._include_refactor_report_checkbox.setChecked(False)
                self._root_path_edit = QLineEdit("E:\\fixture")
                self._status = FakeStatusBar()

            def statusBar(self) -> FakeStatusBar:  # noqa: N802
                return self._status

        audit_window = FakeAuditWindow()
        audit_result = audit_handoff.handoff_audit_results_to_external_ai(audit_window)
        _require(audit_result.ok, "AUDIT EXTERNAL HANDOFF RUNTIME")
        copied = QApplication.clipboard().text()
        _require(
            "KANDA_AUDIT_EXTERNAL_REVIEW_BEGIN" in copied
            and "AUDIT RESULT FIXTURE" in copied,
            "AUDIT READ-ONLY EXTERNAL PROMPT RUNTIME",
        )
        audit_window.close()
        app.processEvents()
        _require(
            FakeDesktopServices.opened_urls == [
                "https://chat.deepseek.com/",
                "https://chat.deepseek.com/",
                "https://chat.deepseek.com/",
                "https://chat.deepseek.com/",
            ],
            "ALL GOVERNED DRAFT ROUTES USE CONFIGURED OFFICIAL URL",
        )
    finally:
        base_handoff.QDesktopServices = original_desktop
        audit_handoff.show_auto_close_action_window = original_notice
    print("GOVERNED DRAFT GUI FUNCTIONAL SMOKE: PASS")
    print("GOVERNED DRAFT NO-PROJECT CONFIG STATE: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    """Run Update 3 validation against the selected Tool root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--skip-qt", action="store_true")
    args = parser.parse_args(argv)
    tool_root = Path(args.tool_root).expanduser().resolve()
    if not tool_root.is_dir():
        print("VALIDATION BLOCKED: Tool root not found: " + str(tool_root))
        return 1
    try:
        _bootstrap(tool_root)
        _validate_files(tool_root)
        _validate_frozen_sources(tool_root)
        _validate_freeze_contract(tool_root)
        _validate_error_memory_contract(tool_root)
        _validate_audit_contract(tool_root)
        _validate_help(tool_root)
        if args.skip_qt:
            print("QT GOVERNED DRAFT FUNCTIONAL VALIDATION: NOT RUN")
        else:
            _validate_qt_runtime()
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
