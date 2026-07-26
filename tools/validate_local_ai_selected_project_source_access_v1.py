#!/usr/bin/env python3
"""Validate bounded Local AI access to the selected Project source."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import tempfile
import types
from pathlib import Path

FEATURE_ID = "local-ai-selected-project-source-access-v1"
TOUCHED_MODULES = (
    "kanda_reasoner_app/reasoner_engine/index_loader.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
    "runtime_controller.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
    "session_service.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "retriever_core_mixin.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "live_source_fallback.py",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _marker(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print(name + ": PASS")


def _install_qt_import_stubs() -> None:
    if "PySide6" not in sys.modules:
        pyside = types.ModuleType("PySide6")
        widgets = types.ModuleType("PySide6.QtWidgets")
        widgets.QFileDialog = type("QFileDialog", (), {})
        widgets.QMessageBox = type("QMessageBox", (), {})
        pyside.QtWidgets = widgets
        sys.modules["PySide6"] = pyside
        sys.modules["PySide6.QtWidgets"] = widgets

    ui_name = (
        "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help."
        "ui_components"
    )
    if ui_name not in sys.modules:
        ui_module = types.ModuleType(ui_name)
        ui_module.shorten_path = lambda value: str(value)
        sys.modules[ui_name] = ui_module

    floating_name = "kanda_reasoner_app.templates.floating_windows"
    if floating_name not in sys.modules:
        floating = types.ModuleType(floating_name)
        floating.show_auto_close_action_window = lambda *args, **kwargs: None
        floating.show_error_copy_close_window = lambda *args, **kwargs: None
        sys.modules[floating_name] = floating


class _TextWidget:
    def __init__(self, value: str = "") -> None:
        self._value = value

    def text(self) -> str:
        return self._value

    def setText(self, value: str) -> None:
        self._value = str(value)


class _RuntimeWindow:
    def __init__(self, project_root: Path, project_index: object) -> None:
        self.project_root_edit = _TextWidget(str(project_root))
        self.json_path_edit = _TextWidget("")
        self.project_index = project_index
        self.logs: list[str] = []

    def _append_log(self, message: str) -> None:
        self.logs.append(str(message))


def _validate_source_contract(root: Path) -> None:
    for relative in TOUCHED_MODULES:
        path = root / relative
        text = path.read_text(encoding="utf-8")
        _marker("ASCII_ONLY_" + path.stem.upper(), text.isascii())
        _marker(
            "MODULE_MAX_500_LINES_" + path.stem.upper(),
            len(text.splitlines()) <= 500,
        )

    runtime_text = (root / TOUCHED_MODULES[1]).read_text(encoding="utf-8")
    session_text = (root / TOUCHED_MODULES[2]).read_text(encoding="utf-8")
    retriever_text = (root / TOUCHED_MODULES[3]).read_text(encoding="utf-8")
    fallback_text = (root / TOUCHED_MODULES[4]).read_text(encoding="utf-8")

    _marker(
        "LIVE_PROJECT_MODE_IS_IN_MEMORY_ONLY",
        "initialize_live_project(str(project_root))" in runtime_text,
    )
    _marker(
        "SELECTED_PROJECT_ROOT_FORWARDED_TO_RETRIEVER",
        "project_root_override=effective_project_root" in session_text,
    )
    _marker(
        "RETRIEVER_PUBLIC_OVERRIDE_IS_OPTIONAL",
        'project_root_override: str = ""' in retriever_text,
    )
    _marker(
        "LIVE_SOURCE_SCAN_LINK_GUARDS_PRESENT",
        "followlinks=False" in fallback_text
        and "is_symlink()" in fallback_text
        and "_is_reparse_point" in fallback_text,
    )
    _marker(
        "LIVE_SOURCE_PATH_VERIFIED_BEFORE_CONTENT_READ",
        "path_result = verify_live_source_path(root, relative)"
        in fallback_text,
    )
    _marker(
        "PROJECT_SUPPORT_PATHS_EXCLUDED",
        '_show_project_to_ai")' in fallback_text,
    )
    forbidden = ("subprocess", "os.system", "Popen(", "write_text(", "write_bytes(")
    _marker(
        "LOCAL_AI_LIVE_SOURCE_HAS_NO_WRITE_OR_SHELL",
        not any(token in fallback_text for token in forbidden),
    )


def _validate_runtime(root: Path) -> None:
    sys.path.insert(0, str(root))
    try:
        from kanda_reasoner_app.reasoner_engine.index_loader import JsonProjectIndex
        from kanda_reasoner_app.reasoner_engine.reasoner_retriever import (
            ProjectRetriever,
        )

        _install_qt_import_stubs()
        runtime_module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine."
            "ai_reasoner_main_window_help.runtime_controller"
        )
        RuntimeController = runtime_module.RuntimeController

        with tempfile.TemporaryDirectory() as temp_text:
            temp_root = Path(temp_text)
            project = temp_root / "sample_project"
            project.mkdir()
            source = project / "provider_errors.py"
            source.write_text(
                "class ProviderResponseError(RuntimeError):\n"
                "    pass\n\n"
                "def raise_provider_error():\n"
                "    raise ProviderResponseError('failed')\n",
                encoding="utf-8",
            )
            secret = project / ".env"
            secret.write_text(
                "ProviderResponseError=must_not_be_read\n", encoding="utf-8"
            )
            support = temp_root / "sample_project_show_project_to_AI"
            support.mkdir()
            (support / "support_only.py").write_text(
                "ProviderResponseError = 'support'\n", encoding="utf-8"
            )
            outside = temp_root / "outside.py"
            outside.write_text(
                "ProviderResponseError = 'outside'\n", encoding="utf-8"
            )
            link_created = False
            try:
                (project / "linked_outside.py").symlink_to(outside)
                link_created = True
            except OSError:
                pass

            auxiliary = temp_root / "error_lessons_compact.json"
            auxiliary.write_text(
                json.dumps(
                    {
                        "artifact_type": "error_memory_ai_export",
                        "lessons": [],
                    }
                ),
                encoding="utf-8",
            )
            auxiliary_hash = _sha256(auxiliary)

            auxiliary_index = JsonProjectIndex()
            auxiliary_index.load_json(str(auxiliary))
            _marker(
                "AUXILIARY_JSON_HAS_NO_EMBEDDED_PROJECT_ROOT",
                auxiliary_index.project_root == "",
            )

            retriever = ProjectRetriever(auxiliary_index)
            bundle = retriever.retrieve(
                "Find where ProviderResponseError is defined and raised.",
                file_limit=10,
                symbol_limit=10,
                snippet_limit=6,
                project_root_override=str(project),
            )
            paths = [item.path.replace("\\", "/") for item in bundle.file_evidence]
            snippets = list(bundle.snippet_evidence)
            _marker(
                "AUXILIARY_JSON_SELECTED_ROOT_LIVE_SOURCE_FOUND",
                "provider_errors.py" in paths,
            )
            _marker(
                "LIVE_SOURCE_SNIPPET_HAS_EXACT_IDENTIFIER",
                any(
                    item.get("path") == "provider_errors.py"
                    and item.get("anchor")
                    == "LIVE_SOURCE:ProviderResponseError"
                    and "class ProviderResponseError" in item.get("text", "")
                    for item in snippets
                ),
            )
            _marker(
                "PROJECT_SUPPORT_NOT_READ",
                all("show_project_to_ai" not in path.lower() for path in paths),
            )
            _marker("SECRET_FILE_NOT_READ", ".env" not in paths)
            if link_created:
                _marker("SYMLINK_FILE_NOT_READ", "linked_outside.py" not in paths)
            else:
                print("SYMLINK_FILE_NOT_READ: NOT_APPLICABLE")
            _marker(
                "AUXILIARY_JSON_NOT_OVERWRITTEN",
                _sha256(auxiliary) == auxiliary_hash,
            )

            live_index = JsonProjectIndex()
            runtime_window = _RuntimeWindow(project, live_index)
            controller = RuntimeController()
            resolved = controller.ensure_project_json_loaded_for_question(
                runtime_window
            )
            _marker("MISSING_COMPLETE_JSON_ENTERS_LIVE_MODE", bool(resolved))
            _marker(
                "LIVE_MODE_USES_SELECTED_PROJECT_ROOT",
                live_index.project_root == str(project.resolve()),
            )
            _marker(
                "LIVE_MODE_ARTIFACT_IDENTITY",
                live_index.index_data.get("artifact_type")
                == "local_ai_live_project_source",
            )
            _marker(
                "LIVE_MODE_LOGGED_EXPLICITLY",
                any("bounded read-only live Project source" in item
                    for item in runtime_window.logs),
            )

            live_retriever = ProjectRetriever(live_index)
            live_bundle = live_retriever.retrieve(
                "ProviderResponseError",
                file_limit=10,
                symbol_limit=10,
                snippet_limit=6,
            )
            _marker(
                "NO_JSON_LIVE_MODE_RETRIEVES_SOURCE",
                any(
                    item.path == "provider_errors.py"
                    for item in live_bundle.file_evidence
                ),
            )

            session_module = importlib.import_module(
                "kanda_reasoner_app.reasoner_engine."
                "ai_reasoner_main_window_help.session_service"
            )

            class _BoolWidget:
                def isChecked(self) -> bool:
                    return False

            class _ComboWidget:
                def currentText(self) -> str:
                    return "Concise"

            class _PromptBuilder:
                def __init__(self) -> None:
                    self.last_project_root = ""

                def build(self, **kwargs: object) -> str:
                    self.last_project_root = str(
                        kwargs.get("project_root", "")
                    )
                    return "BOUNDED LIVE PROJECT PROMPT"

            session_module.capture_session_prompt_router_reasoner_review = (
                lambda **kwargs: object()
            )
            session_module.summarize_session_capture_result = (
                lambda result: "capture skipped in focused fixture"
            )
            prompt_builder = _PromptBuilder()
            session_window = types.SimpleNamespace(
                project_index=auxiliary_index,
                project_root_edit=_TextWidget(str(project)),
                retriever=ProjectRetriever(auxiliary_index),
                debug_checkbox=_BoolWidget(),
                prefer_code_radio=_BoolWidget(),
                verbosity_combo=_ComboWidget(),
                prompt_builder=prompt_builder,
            )
            session_window._rebuild_retriever_for_active_profile = lambda: None
            session_result = session_module.SessionService().execute(
                session_window,
                "Where is ProviderResponseError defined and raised?",
                "qwen3-coder:30b",
            )
            _marker(
                "SESSION_SERVICE_USES_SELECTED_PROJECT_ROOT",
                prompt_builder.last_project_root == str(project.resolve()),
            )
            _marker(
                "SESSION_SERVICE_RETURNS_LIVE_SOURCE_EVIDENCE",
                any(
                    item.path == "provider_errors.py"
                    for item in session_result.bundle.file_evidence
                ),
            )
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()

    _validate_source_contract(root)
    _validate_runtime(root)
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
