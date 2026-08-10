# project-path: tools/validate_free_python_coding_ai_update4_v1.py
"""Validate Project Web AI manual external-assistant export Update 4."""

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

FEATURE_ID = "free-python-coding-ai-project-web-ai-external-export-update4-v1"

CHANGED_FILES = ('kanda_reasoner_app/reasoner_engine/project_web_ai_external_handoff.py', 'kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py', 'kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py', 'kanda_reasoner_app/reasoner_tools_gui_help/web_ai.json', 'tools/validate_free_python_coding_ai_update4_v1.py')

FROZEN_HASHES = {'kanda_reasoner_app/error_memory_gui/_ai_correction_action.py': 'eeadc89407a360d4e47ef8c51951c770ae8d08066074a69ee454179277193e54', 'kanda_reasoner_app/error_memory_gui/_clipboard_export.py': '1bb2aa849894714ca4c70f3e9a2af0308f1ab6fe5710b7cd29647d1c90325028', 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py': 'a12b7cef6895a6c7e39e0d2b0ba24b0c0e972504426ceee5f05dfb5e9936cbdc', 'kanda_reasoner_app/external_ai_configuration.py': 'a2c210f425127d76e645517bca24d8a3c9977c32d1c9a5c5b9fa146db3c40eca', 'kanda_reasoner_app/external_ai_handoff.py': 'c17455d7d9dd5636496a992d9dec6d52f9e0b7c31d06bec4bb8b828d83359b8e', 'kanda_reasoner_app/external_ai_workflow.py': 'c3744472d750bc23bfae740b391822b92ff6707dd9b004322fe94fb9a50e95a6', 'kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py': 'ebeecddb582bf2a8179c8e4aba81853b3da4d1fda2c5622b66e0bd2fd9d6ec39', 'kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py': 'edb2d66c575505e204a7099db4dbfb938b5fe3ca00b407e5473f202c1e941871', 'kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py': 'e6882d6ed582d9aa8fa72887cddf6ccd199f8f4ad278847eeb5b4fd25233ccc1', 'kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py': '887c8d99f136b888c66fc242b7d0a2702dff3c61a2c62ae2b0fa9bee5337316d', 'kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py': 'fc48582fd0ee743945e961735b3be0d516e45763fa1c862817a0cd5d28828b23', 'kanda_reasoner_app/freeze_after_update_gui/freeze_feature_after_update_help.html': 'c29aeff683a28e8ba124a3d9546150ae6cfaf1c8d3a9935984fa80c5cef45919', 'kanda_reasoner_app/freeze_after_update_gui/help_source/freeze_feature_after_update_help.md': 'ed5dff142d7907a985ba67c431c99ecc73ea92ae871635f77d663d8805c2c8be', 'kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py': 'b822707c0bb06542cbe15324b9696e0171f9cad6861c1c6a41695ca9e485a8cd', 'kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py': 'b2edb0e919e9cb9be049b6fe7894d1c5c459967fab916e2d73a2dbf06992bc41', 'kanda_reasoner_app/manage_architecture/architecture_audit_external_ai.py': '40753f11230281a2d906cad68f806107bf7bb13919d4c21439ec9d315ebc3e3a', 'kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py': '02530a9d9d31abd13cae246e69bfd9f45ae98269efc34c30e6f4c31efa73ab09', 'kanda_reasoner_app/project_selection_registry.py': '98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1', 'kanda_reasoner_app/python_coding_ai_catalog.py': '3c5631cf438fe152c5226ba011edb68c9fd76eb00a5fae26461f1b5fe7db57b6', 'kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py': '5e69e2f2ddb9554a427aa61dde3493e717a654835863f5b6677441e7fd370911', 'kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py': '276c5c2c66469243a31fd5d9bb28a7516badb0393d4fc2c0353ab23895173e1f', 'kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py': 'e32125dfc3d5c4570df6e4abd193bfd2a899eb1d81c6275d072ef183bcaa68ec', 'kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py': 'e73d3292808238d604294cf02905a1a83f7bfd0f2f12cea1d9a9c361d66eab25', 'kanda_reasoner_app/reasoner_tools_gui_help/error_memory.json': '3278f4107c6803bfb824333495325d324a194d49250ff1fe75fcaa9f170b5b21', 'kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json': '3d8af1c8780971b5a2ccc195f244a625b283fb648b7302b09243f7113bab0345', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/architecture_review.html': 'b228cc916e7d7ab50bbbcaa8987075ce58a60f6ee4e8ca2916db9c8d9e1d954d', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/error_memory.html': '956ca8a0839201d633a63b6902cff2b53edee2701bf9400c389a607273311a3c', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/architecture_review.md': '503e2b3e357b3aeedb8458f68b7dc3cea2001704e46e7c1331fb6afab2249110', 'kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/error_memory.md': '1301ab7607a8054153e92d21ce9de18d2ec736185df1d4816ff6d7259783d8f8', 'kanda_reasoner_app/web_ai_configuration.py': 'd0e2947aa92781b3685922316ab737b8b149ccbe0d2dfd39d3557e86e66f84ce', 'kanda_reasoner_app/web_ai_model_catalog.py': 'c6c49d12f75b32bc93a73e3424c1a038c05734b73abb9d9c88105e17f5e73f36', 'kanda_reasoner_app/web_ai_provider_runtime.py': '6783226e498235e391e874112639c051ac81100c3ad668cd061194dde934ea55', 'portable/PORTABLE_BUILDER_MANIFEST.json': '1ca9e8d00ca67c1227c0138eba3f8364ddf0b589abfadfc85dee84024bc49c5c', 'portable/PORTABLE_RUNTIME_ALLOWLIST.json': '429af7c6564fc9495b66c83eaac9bdb88a91360205bed7b34b19364ee04dfe1f', 'tools/validate_free_python_coding_ai_update1_v1.py': '7e199e68e13901e45ef9a889e06506478996c3dc2107fdd37f55d9205c435cbb', 'tools/validate_free_python_coding_ai_update1_validation_wrapper_v1r2.py': '5a31b1ef29a15c6738c3634907aa775bc0ae9836faf054253d509e74fa7fa729', 'tools/validate_free_python_coding_ai_update3_validation_wrapper_v1r1.py': 'b2e580f2b33bd749afddb654faa3cfd0897f48edd4fb503396fe065bb49de0a5'}


class MemorySettings:
    """Minimal QSettings-compatible fixture."""

    def __init__(self) -> None:
        self.values: dict[str, object] = {}

    def value(self, key: str, default: object = None) -> object:
        """Return a stored value or default."""
        return self.values.get(key, default)

    def setValue(self, key: str, value: object) -> None:  # noqa: N802
        """Store one value in memory."""
        self.values[str(key)] = value


class FakeDesktopServices:
    """Capture official-site requests without opening a browser."""

    opened_urls: list[str] = []

    @classmethod
    def openUrl(cls, url: object) -> bool:  # noqa: N802
        """Record one URL and report a successful open request."""
        cls.opened_urls.append(str(url.toString()))
        return True


class FakeMessageBox:
    """Approve the handoff without showing modal dialogs."""

    class StandardButton:
        Yes = 1
        No = 2

    @classmethod
    def question(cls, *_args: object, **_kwargs: object) -> int:
        """Return explicit approval for the functional fixture."""
        return cls.StandardButton.Yes

    @classmethod
    def warning(cls, *_args: object, **_kwargs: object) -> None:
        """Accept warning calls in negative-path fixtures."""
        return None


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
    checks = {
        "tools/validate_free_python_coding_ai_update2_v1.py": (
            'FEATURE_ID = "free-python-coding-ai-manual-workflow-handoffs-update2-v1"',
            "UPDATE 1 CONFIG EXTERNAL AI FORWARD COMPATIBILITY: PASS",
        ),
        "tools/validate_free_python_coding_ai_update3_v1.py": (
            'FEATURE_ID = "free-python-coding-ai-governed-draft-handoffs-update3-v1"',
            "UPDATE 2 VALIDATOR FORWARD COMPATIBILITY: PASS",
        ),
    }
    for relative, tokens in checks.items():
        path = tool_root / relative
        _require(path.is_file(), "PRIOR VALIDATOR PRESENT " + relative)
        source = path.read_text(encoding="utf-8")
        for token in tokens:
            _require(token in source, "PRIOR VALIDATOR CAPABILITY " + token)
    print("UPDATES 2-3 VALIDATOR FORWARD COMPATIBILITY: PASS")

def _validate_frozen_sources(tool_root: Path) -> None:
    for relative, expected in FROZEN_HASHES.items():
        path = tool_root / relative
        _require(path.is_file(), "FROZEN SOURCE PRESENT " + relative)
        _require(_sha256(path) == expected, "FROZEN SOURCE HASH " + relative)
    _validate_prior_validator_capabilities(tool_root)
    print("UPDATES 1-3 FROZEN CONTRACTS PRESERVED: PASS")
    print("DIRECT WEB AI PROVIDER AND APPLY OWNERS UNCHANGED: PASS")
    print("PROJECT SELECTION AUTHORITY UNCHANGED: PASS")
    print("PORTABLE MANIFESTS MODIFIED: NO: PASS")


def _validate_export_contract(tool_root: Path) -> None:
    helper = _source(
        tool_root,
        "kanda_reasoner_app/reasoner_engine/project_web_ai_external_handoff.py",
    )
    tab = _source(
        tool_root,
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    )
    ui = _source(
        tool_root,
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    )
    for token in (
        "KANDA_PROJECT_WEB_AI_EXTERNAL_HANDOFF_BEGIN",
        "MANUAL_EXTERNAL_CONVERSATION: YES",
        "NOT_PART_OF_DIRECT_WEB_AI_SESSION: YES",
        "NO_AUTOMATIC_RESPONSE_INTAKE: YES",
        "NO_SOURCE_WRITE_AUTHORITY: YES",
        "build_project_messages",
        "handoff_to_selected_external_ai",
        "Approve copy and open?",
        "no answer returns automatically",
    ):
        _require(token in helper, "PROJECT WEB AI EXPORT TOKEN " + token)
    for forbidden in (
        "requests.",
        "urllib.request",
        "selenium",
        "playwright",
        "_begin_chat_turn",
        "_on_chat_token",
        "write_confirmed_freeze_entry",
        "memorize_error",
        "write_text(",
    ):
        _require(forbidden not in helper, "PROJECT WEB AI EXPORT FORBIDS " + forbidden)
    _require(
        "ProjectWebAIExternalHandoffMixin" in tab
        and "self._initialize_external_handoff()" in tab
        and "self._update_external_handoff_state(locked)" in tab,
        "PROJECT WEB AI TAB MIXIN INTEGRATION",
    )
    _require(
        'QPushButton("Copy and Open External AI")' in ui
        and '"projectWebAIExternalHandoffButton"' in ui,
        "PROJECT WEB AI EXTERNAL HANDOFF BUTTON",
    )
    _require(
        "Direct API + manual export" in ui
        and "no response is imported automatically" in ui,
        "PROJECT WEB AI SEPARATE CONVERSATION LABEL",
    )
    _require(
        "self._web_config.ready_for_chat()" in tab
        and "ProjectWebAIChatWorker" in tab,
        "DIRECT OPENROUTER KILO CHAT CONTRACT PRESERVED",
    )
    print("PROJECT WEB AI MANUAL EXPORT HAS NO RESPONSE INTAKE: PASS")
    print("PROJECT WEB AI DIRECT SESSION HISTORY REMAINS SEPARATE: PASS")


def _validate_help(tool_root: Path) -> None:
    data = json.loads(
        _source(tool_root, "kanda_reasoner_app/reasoner_tools_gui_help/web_ai.json")
    )
    lines = data.get("display_lines")
    _require(isinstance(lines, list), "PROJECT WEB AI HELP DISPLAY LINES")
    text = "\n".join(str(item) for item in lines)
    for token in (
        "Copy and Open External AI",
        "separate",
        "does not paste, submit, read, or import",
        "OpenRouter or Kilo",
    ):
        _require(token in text, "PROJECT WEB AI HELP TOKEN " + token)


POWERSHELL_FILES = (
    "RUN_INSTALL.ps1",
    "INSTALL.ps1",
    "RUN_VALIDATE.ps1",
    "VALIDATE.ps1",
    "PREPARE_FREEZE.ps1",
    "NATIVE_PROCESS.ps1",
)

REQUIRED_PATH_TOKENS = (
    '$ToolsRoot = Join-Path $ProjectPath "tools"',
    '$Update1Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update1_v1.py"',
    '$Update2Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update2_v1.py"',
    '$Update3Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update3_v1.py"',
    '$Update4Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update4_v1.py"',
    '$ScriptsRoot = Join-Path $ProjectPath "scripts"',
    '$ZipValidator = Join-Path $ScriptsRoot "validate_patch_zip.py"',
)


def _invalid_control_offsets(raw: bytes) -> list[int]:
    return [
        index
        for index, value in enumerate(raw)
        if value < 32 and value not in {9, 10, 13}
    ]


def _validate_package_delivery(package_root: Path) -> None:
    _require(package_root.is_dir(), "VALIDATOR PACKAGE ROOT")
    for name in POWERSHELL_FILES:
        path = package_root / name
        _require(path.is_file(), "POWERSHELL SCRIPT PRESENT: " + name)
        _require(
            not _invalid_control_offsets(path.read_bytes()),
            "POWERSHELL CONTROL CHARACTERS ABSENT: " + name,
        )
    fixture = b"tools" + bytes([11]) + b"alidate_example.py"
    _require(
        bool(_invalid_control_offsets(fixture)),
        "POWERSHELL CONTROL CHARACTER FIXTURE REJECTED",
    )
    print("POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS")

    validate_text = (package_root / "VALIDATE.ps1").read_text(encoding="utf-8")
    for token in REQUIRED_PATH_TOKENS:
        _require(token in validate_text, "VALIDATOR PATH TOKEN " + token)
    lowered = validate_text.casefold()
    _require("toolsvalidate_" not in lowered, "CONCATENATED TOOLSVALIDATE PATH ABSENT")
    _require('"tools\\validate_' not in lowered, "ESCAPE-SENSITIVE TOOLS PATH ABSENT")
    _require('"scripts\\validate_' not in lowered, "ESCAPE-SENSITIVE SCRIPTS PATH ABSENT")
    _require("\\x0b" not in repr((package_root / "VALIDATE.ps1").read_bytes()), "VERTICAL TAB BYTE ABSENT")
    print("VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS")


def _validate_qt_runtime() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QPlainTextEdit,
            QPushButton,
            QWidget,
        )
    except ModuleNotFoundError as exc:
        raise RuntimeError("PySide6 is required for the functional GUI smoke.") from exc

    import kanda_reasoner_app.external_ai_handoff as base_handoff
    import kanda_reasoner_app.reasoner_engine.project_web_ai_external_handoff as export_module
    from kanda_reasoner_app.external_ai_configuration import (
        ExternalAIConfigurationController,
        install_application_external_ai_configuration,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_external_handoff import (
        ProjectWebAIExternalHandoffMixin,
        build_project_web_ai_external_prompt,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot

    app = QApplication.instance() or QApplication([])
    settings = MemorySettings()
    settings.setValue("external_ai/selected_assistant_id", "deepseek_chat")
    controller = ExternalAIConfigurationController(settings=settings)
    install_application_external_ai_configuration(controller)

    context = ContextSnapshot(
        tool_project_slug="kanda_reasoner",
        tool_source_root=r"E:\kanda_reasoner",
        project_slug="fixture_project",
        project_id="fixture-id",
        project_root=r"E:\fixture_project",
        project_root_fingerprint="fixture-root-fingerprint",
        support_root=r"E:\fixture_project_show_project_to_AI",
        daily_work_root=r"E:\fixture_project_delete_after_daily_work",
        self_hosting_mode=False,
        support_identity_status="VERIFIED",
        collector_status="complete",
        snapshot_id="fixture-snapshot",
        context_hash="a" * 64,
        generated_at_utc="2026-08-02T00:00:00Z",
        trusted_boundary_text="TRUSTED BOUNDARY FIXTURE",
        context_text="UNTRUSTED PROJECT EVIDENCE FIXTURE",
        context_bytes=34,
        artifacts_loaded=("ai_briefing",),
        omitted_sections=(),
    )
    history = [
        {"role": "user", "content": "Earlier question"},
        {"role": "assistant", "content": "Earlier advisory answer"},
    ]
    prompt = build_project_web_ai_external_prompt(
        question="Review this Python architecture.",
        context=context,
        history=history,
    )
    for token in (
        "KANDA_PROJECT_WEB_AI_EXTERNAL_HANDOFF_BEGIN",
        "CURRENT QUESTION",
        "Review this Python architecture.",
        "Earlier advisory answer",
        "UNTRUSTED PROJECT EVIDENCE FIXTURE",
        "NO_AUTOMATIC_RESPONSE_INTAKE: YES",
    ):
        _require(token in prompt, "PROJECT WEB AI PROMPT RUNTIME TOKEN " + token)

    class Fixture(ProjectWebAIExternalHandoffMixin, QWidget):
        def __init__(self) -> None:
            super().__init__()
            self._context = context
            self._history = list(history)
            self.question_edit = QPlainTextEdit()
            self.question_edit.setPlainText("Review this Python architecture.")
            self.status_value = QLabel()
            self.external_assistant_value = QLabel()
            self.external_handoff_button = QPushButton()
            self.open_external_config_button = QPushButton()
            self._initialize_external_handoff()

        def _update_send_state(self) -> None:
            self._update_external_handoff_state(False)

    original_desktop = base_handoff.QDesktopServices
    original_message_box = export_module.QMessageBox
    FakeDesktopServices.opened_urls = []
    base_handoff.QDesktopServices = FakeDesktopServices
    export_module.QMessageBox = FakeMessageBox
    try:
        fixture = Fixture()
        fixture._update_send_state()
        _require(
            fixture.external_handoff_button.isEnabled(),
            "PROJECT WEB AI EXPORT INDEPENDENT OF DIRECT API READINESS",
        )
        original_history = list(fixture._history)
        fixture.handoff_current_request_to_external_ai()
        copied = QApplication.clipboard().text()
        _require(
            copied.startswith("KANDA_PROJECT_WEB_AI_EXTERNAL_HANDOFF_BEGIN"),
            "PROJECT WEB AI EXTERNAL CLIPBOARD RUNTIME",
        )
        _require(
            FakeDesktopServices.opened_urls == ["https://chat.deepseek.com/"],
            "PROJECT WEB AI CONFIGURED OFFICIAL URL RUNTIME",
        )
        _require(
            fixture._history == original_history,
            "PROJECT WEB AI DIRECT HISTORY NOT MUTATED",
        )
        _require(
            "no answer returns automatically" in fixture.status_value.text(),
            "PROJECT WEB AI NO AUTOMATIC RESPONSE STATUS",
        )
        fixture._context = None
        fixture._update_send_state()
        _require(
            not fixture.external_handoff_button.isEnabled(),
            "PROJECT WEB AI EXTERNAL HANDOFF NO-PROJECT STATE",
        )
        fixture.close()
        app.processEvents()
    finally:
        base_handoff.QDesktopServices = original_desktop
        export_module.QMessageBox = original_message_box
    print("PROJECT WEB AI EXTERNAL EXPORT GUI FUNCTIONAL SMOKE: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    """Run Update 4 validation against the selected Tool root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--skip-qt", action="store_true")
    args = parser.parse_args(argv)
    tool_root = Path(args.tool_root).expanduser().resolve()
    package_root = Path(args.package_root).expanduser().resolve()
    if not tool_root.is_dir():
        print("VALIDATION BLOCKED: Tool root not found: " + str(tool_root))
        return 1
    try:
        _bootstrap(tool_root)
        _validate_package_delivery(package_root)
        _validate_files(tool_root)
        _validate_frozen_sources(tool_root)
        _validate_export_contract(tool_root)
        _validate_help(tool_root)
        if args.skip_qt:
            print("QT PROJECT WEB AI EXTERNAL EXPORT VALIDATION: NOT RUN")
        else:
            _validate_qt_runtime()
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
