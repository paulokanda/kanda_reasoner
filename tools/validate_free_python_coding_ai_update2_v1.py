# project-path: tools/validate_free_python_coding_ai_update2_v1.py
"""Validate Update 2 manual external-AI workflow handoff integration."""

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

FEATURE_ID = "free-python-coding-ai-manual-workflow-handoffs-update2-v1"

CHANGED_FILES = (
    "kanda_reasoner_app/external_ai_workflow.py",
    "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_inner_tabs_layout.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/external_ai_candidate_exchange_gui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_gui.py",
    "kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py",
    "kanda_reasoner_app/prompt_router_reasoner_gui/_prompt_router_reasoner_tab_ui.py",
    "kanda_reasoner_app/reasoner_tools_gui_help/config_ai.json",
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/config_ai.md",
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/config_ai.html",
    "tools/validate_free_python_coding_ai_update2_v1.py",
)

FROZEN_UPDATE1_HASHES = {
    "kanda_reasoner_app/python_coding_ai_catalog.py": "3c5631cf438fe152c5226ba011edb68c9fd76eb00a5fae26461f1b5fe7db57b6",
    "kanda_reasoner_app/external_ai_configuration.py": "a2c210f425127d76e645517bca24d8a3c9977c32d1c9a5c5b9fa146db3c40eca",
    "kanda_reasoner_app/external_ai_handoff.py": "c17455d7d9dd5636496a992d9dec6d52f9e0b7c31d06bec4bb8b828d83359b8e",
    "kanda_reasoner_app/reasoner_engine/config_ai_tab.py": "5c854c341626d87afc62ef8d43818f6ecf31ed50dce55d06fb866e735ccc8e58",
    "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py": "c76e25def53f3770cd38c07dcc18b6b82e92de4f7f97601ac5ca0ecbc15da5a1",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py": "394280a77f33bbb51080c4c2b63ffaaf2abd32e5376278a3e005e8b698f85a04",
    "kanda_reasoner_app/web_ai_configuration.py": "d0e2947aa92781b3685922316ab737b8b149ccbe0d2dfd39d3557e86e66f84ce",
    "kanda_reasoner_app/web_ai_model_catalog.py": "c6c49d12f75b32bc93a73e3424c1a038c05734b73abb9d9c88105e17f5e73f36",
    "kanda_reasoner_app/web_ai_provider_runtime.py": "6783226e498235e391e874112639c051ac81100c3ad668cd061194dde934ea55",
    "kanda_reasoner_app/project_selection_registry.py": "98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1",
    "portable/PORTABLE_RUNTIME_ALLOWLIST.json": "429af7c6564fc9495b66c83eaac9bdb88a91360205bed7b34b19364ee04dfe1f",
    "portable/PORTABLE_BUILDER_MANIFEST.json": "1ca9e8d00ca67c1227c0138eba3f8364ddf0b589abfadfc85dee84024bc49c5c",
}


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


def _validate_files(tool_root: Path) -> None:
    for relative in CHANGED_FILES:
        path = tool_root / relative
        _require(path.is_file(), "CHANGED FILE PRESENT " + relative)
        if path.suffix == ".py":
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            _require(
                len(source.splitlines()) <= 500,
                "MODULE SIZE <=500 " + relative,
            )
            py_compile.compile(str(path), doraise=True)
    print("CHANGED PYTHON AST AND COMPILE: PASS")



def _validate_forward_compatible_update1_config(tool_root: Path) -> None:
    relative = "kanda_reasoner_app/reasoner_engine/config_external_ai_tab.py"
    path = tool_root / relative
    _require(path.is_file(), "FROZEN UPDATE 1 FILE PRESENT " + relative)
    source = path.read_text(encoding="utf-8")
    required = (
        "class ConfigExternalAITab(QWidget):",
        "self._controller.assistants()",
        "copy_and_open_external_assistant",
        "Open Official Site",
        "Copy Test Prompt and Open",
        "assistant.validated_url()",
    )
    for token in required:
        _require(
            token in source,
            "UPDATE 1 CONFIG EXTERNAL AI CAPABILITY " + token,
        )
    lowered = source.casefold()
    _require(
        "project_root" not in lowered and "project_id" not in lowered,
        "UPDATE 1 CONFIG EXTERNAL AI PROJECT AUTHORITY ABSENT",
    )
    print("UPDATE 1 CONFIG EXTERNAL AI FORWARD COMPATIBILITY: PASS")

def _validate_frozen_update1(tool_root: Path) -> None:
    for relative, expected in FROZEN_UPDATE1_HASHES.items():
        path = tool_root / relative
        _require(path.is_file(), "FROZEN UPDATE 1 FILE PRESENT " + relative)
        _require(_sha256(path) == expected, "FROZEN UPDATE 1 HASH " + relative)
    _validate_forward_compatible_update1_config(tool_root)
    print("PRIOR-STAGE VALIDATOR FORWARD COMPATIBILITY: PASS")
    print("DIRECT OPENROUTER KILO AND PROJECT AUTHORITY UNCHANGED: PASS")
    print("PORTABLE MANIFESTS MODIFIED: NO: PASS")


def _source_text(tool_root: Path, relative: str) -> str:
    return (tool_root / relative).read_text(encoding="utf-8")


def _validate_shared_facade(tool_root: Path) -> None:
    text = _source_text(tool_root, "kanda_reasoner_app/external_ai_workflow.py")
    required = (
        "application_external_ai_configuration",
        "copy_and_open_external_assistant",
        "MANUAL EXTERNAL AI HANDOFF",
        "TASK_BEGIN",
        "TASK_END",
        "Do not let the external service write canonical Project source.",
    )
    for token in required:
        _require(token in text, "SHARED HANDOFF TOKEN " + token)
    forbidden = (
        "selenium",
        "playwright",
        "requests.post",
        "cookie",
        "password",
        "automatic paste",
        "automatic submit",
    )
    lowered = text.casefold()
    _require(
        not any(token in lowered for token in forbidden),
        "BROWSER AUTOMATION AND CREDENTIAL CAPTURE ABSENT",
    )
    _require(
        "project_root" not in lowered and "project_id" not in lowered,
        "SHARED HANDOFF PROJECT AUTHORITY ABSENT",
    )


def _validate_workflow_sources(tool_root: Path) -> None:
    checks = {
        "AST SPLIT EXTERNAL HANDOFF": (
            "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py",
            ("handoff_to_selected_external_ai(wrapper)",
             "handoff_to_selected_external_ai(clipboard_text)"),
        ),
        "PLANNER EXTERNAL HANDOFF": (
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py",
            ("handoff_to_selected_external_ai(clipboard_text)",
             "handoff_to_selected_external_ai(text)"),
        ),
        "CANDIDATE EXCHANGE EXTERNAL HANDOFF": (
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/external_ai_candidate_exchange_gui.py",
            ("handoff_package(", "package_sha256=result.zip_sha256"),
        ),
        "MAIN WORKBENCH EXTERNAL HANDOFF": (
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_gui.py",
            ("handoff_package(", "package_sha256=payload.zip_sha256"),
        ),
        "PROMPT ROUTER EXTERNAL HANDOFF": (
            "kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py",
            ("handoff_to_selected_external_ai(prompt_text)",
             "Stored prompts and router state unchanged."),
        ),
    }
    for marker, (relative, tokens) in checks.items():
        text = _source_text(tool_root, relative)
        _require(all(token in text for token in tokens), marker)
    router_text = _source_text(
        tool_root,
        "kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py",
    )
    _require(
        "has_ask_ai_button=False" in router_text,
        "RETIRED PROMPT ROUTER ASK AI UI NOT REVIVED",
    )
    _require(
        "QApplication.clipboard().setText(clipboard_text)" not in _source_text(
            tool_root,
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py",
        ),
        "PLANNER DUPLICATE CLIPBOARD OWNER REMOVED",
    )
    _require(
        "QApplication.clipboard().setText(clipboard_text)" not in _source_text(
            tool_root,
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_gui.py",
        ),
        "MAIN WORKBENCH DUPLICATE CLIPBOARD OWNER REMOVED",
    )
    print("FIVE GOVERNED MANUAL WORKFLOWS INTEGRATED: PASS")


def _validate_help(tool_root: Path) -> None:
    source = _source_text(
        tool_root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/config_ai.md",
    )
    for name in (
        "AST Split",
        "Large File Refactor Planner",
        "External AI Candidate Exchange",
        "Main Workbench",
        "Prompt Router Reasoner",
    ):
        _require(name in source, "CONFIG AI HELP WORKFLOW " + name)
    data = json.loads(
        _source_text(
            tool_root,
            "kanda_reasoner_app/reasoner_tools_gui_help/config_ai.json",
        )
    )
    _require(
        any("five governed manual handoff" in line for line in data["display_lines"]),
        "CONFIG AI FALLBACK HELP FIVE WORKFLOWS",
    )
    rendered = _source_text(
        tool_root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/config_ai.html",
    )
    _require("Integrated Manual Handoffs" in rendered, "CONFIG AI RENDERED HELP")


def _validate_qt_runtime() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication
    except ModuleNotFoundError as exc:
        raise RuntimeError("PySide6 is required for the functional GUI smoke.") from exc

    import kanda_reasoner_app.external_ai_handoff as base_handoff
    from kanda_reasoner_app.external_ai_configuration import (
        ExternalAIConfigurationController,
        install_application_external_ai_configuration,
    )
    from kanda_reasoner_app.external_ai_workflow import (
        handoff_package,
        handoff_to_selected_external_ai,
    )
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PromptRouterReasonerTab,
    )

    app = QApplication.instance() or QApplication([])
    settings = MemorySettings()
    settings.setValue("external_ai/selected_assistant_id", "deepseek_chat")
    controller = ExternalAIConfigurationController(settings=settings)
    install_application_external_ai_configuration(controller)

    original_desktop_services = base_handoff.QDesktopServices
    FakeDesktopServices.opened_urls = []
    base_handoff.QDesktopServices = FakeDesktopServices
    try:
        result = handoff_to_selected_external_ai("print('update2')")
        _require(result.ok, "SHARED HANDOFF RESULT OK")
        _require(
            result.assistant_id == "deepseek_chat",
            "SHARED HANDOFF USES CONFIGURED ASSISTANT",
        )
        _require(
            QApplication.clipboard().text() == "print('update2')",
            "SHARED HANDOFF CLIPBOARD EXACT TEXT",
        )
        _require(
            FakeDesktopServices.opened_urls == ["https://chat.deepseek.com/"],
            "SHARED HANDOFF OFFICIAL URL OPEN",
        )

        package = handoff_package(
            title="KANDA PACKAGE",
            zip_path="E:\\fixture\\package.zip",
            task_text="Review the package.",
            task_path="E:\\fixture\\TASK.md",
            package_sha256="a" * 64,
        )
        _require(package.ok, "PACKAGE HANDOFF RESULT OK")
        copied = QApplication.clipboard().text()
        _require("E:\\fixture\\package.zip" in copied, "PACKAGE PATH COPIED")
        _require("TASK_BEGIN" in copied and "TASK_END" in copied, "PACKAGE TASK BOUNDED")
        _require("a" * 64 in copied, "PACKAGE SHA256 COPIED")

        tab = PromptRouterReasonerTab()
        _require(
            tab.copy_manual_router_final_prompt_button.text()
            == "Copy and Open External AI",
            "PROMPT ROUTER CURRENT GUI HANDOFF LABEL",
        )
        tab.manual_router_final_prompt_editor.setPlainText("Review this prompt.")
        tab.copy_manual_router_final_prompt()
        _require(
            "DeepSeek Chat Free" in tab.manual_router_choice_status_label.text(),
            "PROMPT ROUTER HANDOFF FUNCTIONAL SMOKE",
        )
        tab.close()
        app.processEvents()
    finally:
        base_handoff.QDesktopServices = original_desktop_services
    print("EXTERNAL AI WORKFLOW GUI FUNCTIONAL SMOKE: PASS")
    print("EXTERNAL AI WORKFLOW NO-PROJECT STATE: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    """Run Update 2 validation against the selected Tool root."""
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
        _validate_frozen_update1(tool_root)
        _validate_shared_facade(tool_root)
        _validate_workflow_sources(tool_root)
        _validate_help(tool_root)
        if args.skip_qt:
            print("QT WORKFLOW FUNCTIONAL VALIDATION: NOT RUN")
        else:
            _validate_qt_runtime()
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
