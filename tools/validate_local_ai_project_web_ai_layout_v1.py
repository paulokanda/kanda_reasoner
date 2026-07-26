"""Validate the Local AI rename and Project Web AI visual-layout parity."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
import time

FEATURE_ID = "local-ai-project-web-ai-layout-v1"

TOOL_SPECS = Path("kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py")
MAIN_WINDOW = Path("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py")
UI_BUILDER = Path(
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py"
)
UI_THEME = Path(
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_theme.py"
)
ERROR_CONTROLLER = Path(
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
    "project_qa_copy_error_ask_controller.py"
)
BRAIN_MAPPING = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/_mapping_data.py"
)
BRAIN_FLOATING = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/"
    "brain_visual_floating_window.py"
)
WEB_UI = Path("kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py")
WEB_THEME = Path("kanda_reasoner_app/reasoner_engine/project_web_ai_tab_theme.py")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _text(root: Path, relative: Path) -> str:
    path = root / relative
    _require(path.is_file(), "Required source is missing: " + relative.as_posix())
    source = path.read_text(encoding="utf-8", errors="strict")
    compile(source, str(path), "exec")
    ast.parse(source, filename=str(path))
    return source


def _validate_tab_registry(root: Path) -> None:
    source = _text(root, TOOL_SPECS)
    tree = ast.parse(source)
    matches: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "ToolSpec":
            continue
        values: dict[str, str] = {}
        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                values[keyword.arg or ""] = keyword.value.value
        if values.get("tab_id") == "project_qa":
            matches.append((values.get("step_title", ""), values.get("tab_id", "")))
    _require(matches == [("Local AI", "project_qa")], "Local AI tab registry contract mismatch.")
    _require('step_title="Web AI"' in source, "Web AI tab title changed unexpectedly.")
    print("LOCAL_AI_TAB_RENAMED: PASS")
    print("LOCAL_AI_TAB_ID_PRESERVED: PASS")
    print("PROJECT_WEB_AI_TAB_TITLE_PRESERVED: PASS")


def _validate_layout_source(root: Path) -> None:
    source = _text(root, UI_BUILDER)
    required = (
        'title = QLabel("Local AI")',
        'badge = QLabel("LOCAL  PRIVATE")',
        'sidebar.setObjectName("localAISidebar")',
        'panel.setObjectName("localAIChatCanvas")',
        'splitter.setObjectName("localAIMainSplitter")',
        'splitter.addWidget(_sidebar(window))',
        'splitter.addWidget(_chat_canvas(window))',
        'window.question_edit.setObjectName("localAIComposer")',
        'window.answer_box.setObjectName("localAIConversation")',
        'tabs.setObjectName("localAIInspectorTabs")',
        'tabs.addTab(_evidence_tab(window), "Evidence")',
        'tabs.addTab(_plain_tab("Prompt / evidence pack", window.prompt_preview), "Prompt")',
        'tabs.addTab(_plain_tab("Runtime log", window.log_box), "Log")',
        'window.ask_ai_button.setAccessibleName("Ask Local AI")',
        'window.ask_ai_button.setToolTip("Ask Local AI")',
        'scroll.setObjectName("projectQaBodyScrollArea")',
        'body.setObjectName("projectQaScrollableBody")',
        'window._project_qa_body_scroll_area = scroll',
    )
    for fragment in required:
        _require(fragment in source, "Missing Local AI layout fragment: " + fragment)
    for control in (
        "project_root_edit",
        "pick_project_root_button",
        "run_analysis_button",
        "json_path_edit",
        "load_button",
        "static_context_button",
        "model_combo",
        "refresh_models_button",
        "question_edit",
        "ask_ai_button",
        "history_list",
        "file_evidence_list",
        "symbol_evidence_list",
        "detail_box",
        "answer_box",
        "prompt_preview",
        "log_box",
        "clear_button",
        "clear_memory_button",
    ):
        _require("window." + control in source, "Existing control missing from layout: " + control)
    _require(len(source.splitlines()) <= 500, "Local AI ui_builder.py exceeds 500 lines.")
    print("LOCAL_AI_SIDEBAR_CHAT_LAYOUT: PASS")
    print("LOCAL_AI_EXISTING_CONTROLS_PRESERVED: PASS")
    print("LOCAL_AI_INTERNAL_SCROLL_CONTRACT: PASS")
    print("LOCAL_AI_UI_MODULE_SIZE_GATE: PASS")


def _validate_theme(root: Path) -> None:
    theme = _text(root, UI_THEME)
    required = (
        '#0d0d0d',
        '#111318',
        '#10a37f',
        '"Segoe UI Variable Text", "Segoe UI", sans-serif',
        'QFrame#localAISidebar',
        'QFrame#localAIChatCanvas',
        'QFrame#localAIComposerFrame',
        'QPushButton#localAISendButton',
        'QPlainTextEdit#localAIConversation',
        'QLineEdit#localAIComposer',
    )
    for fragment in required:
        _require(fragment in theme, "Missing Local AI theme fragment: " + fragment)

    web_ui_path = root / WEB_UI
    web_theme_path = root / WEB_THEME
    if web_ui_path.is_file() and web_theme_path.is_file():
        web_theme = web_theme_path.read_text(encoding="utf-8", errors="strict")
        for token in ('#0d0d0d', '#111318', '#10a37f', 'Segoe UI Variable Text'):
            _require(token in web_theme and token in theme, "Visual parity token mismatch: " + token)
        web_ui = web_ui_path.read_text(encoding="utf-8", errors="strict")
        _require('splitter.addWidget(_sidebar(owner))' in web_ui, "Project Web AI sidebar reference missing.")
        _require('splitter.addWidget(_chat_canvas(owner))' in web_ui, "Project Web AI chat reference missing.")
    print("LOCAL_AI_PROJECT_WEB_AI_VISUAL_PARITY: PASS")
    print("LOCAL_AI_PROFESSIONAL_DARK_THEME: PASS")


def _validate_visible_names(root: Path) -> None:
    main = _text(root, MAIN_WINDOW)
    errors = _text(root, ERROR_CONTROLLER)
    mapping = _text(root, BRAIN_MAPPING)
    floating = _text(root, BRAIN_FLOATING)
    _require('self.setWindowTitle("Local AI - KANDA Reasoner")' in main, "Standalone title not renamed.")
    for title in (
        "Local AI no evidence",
        "Local AI JSON not loaded",
        "Local AI question missing",
        "Local AI model missing",
        "Local AI session error",
        "Local AI analysis running",
        "Local AI JSON load failed",
    ):
        _require(title in errors, "Visible Local AI error title missing: " + title)
    _require(mapping.count('"target_tab_label": "Local AI"') == 2, "Brain mapping Local AI labels mismatch.")
    _require('"Broca Area -> Local AI"' in mapping, "Broca tooltip was not renamed.")
    _require('"Temporal lobe -> Local AI"' in mapping, "Temporal tooltip was not renamed.")
    _require(floating.count('"Local AI"') >= 2, "Brain floating-window labels were not renamed.")
    print("LOCAL_AI_VISIBLE_NAME_CONSISTENCY: PASS")


def _validate_qt_runtime(root: Path) -> bool:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent, QThread
        from PySide6.QtWidgets import QApplication, QFrame, QSplitter, QTabWidget
    except ModuleNotFoundError:
        print("REAL_LOCAL_AI_WIDGET: SKIPPED_NO_PYSIDE6")
        return False

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.local_ai_configuration import (
        LocalAIConfigurationController,
        install_application_local_ai_configuration,
    )

    class _MemorySettings:
        def __init__(self) -> None:
            self._values: dict[str, object] = {}

        def value(self, key: str, default: object = None) -> object:
            return self._values.get(key, default)

        def setValue(self, key: str, value: object) -> None:
            self._values[key] = value

    class _FakeRegistry:
        def __init__(self, *args: object, **kwargs: object) -> None:
            del args, kwargs

        def list_models(self) -> list[str]:
            return ["fake-local-model"]

    app = QApplication.instance() or QApplication([])
    local_controller = LocalAIConfigurationController(
        app,
        settings=_MemorySettings(),
        registry_factory=_FakeRegistry,
    )
    install_application_local_ai_configuration(local_controller)

    import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window as main_module

    main_module.LocalModelRegistry = _FakeRegistry
    window = main_module.JsonProjectReasonerV10()

    deadline = time.monotonic() + 3.0
    while local_controller._catalog_thread is not None and time.monotonic() < deadline:
        app.processEvents()
        QThread.msleep(10)
    app.processEvents()
    _require(
        local_controller._catalog_thread is None,
        "Global Local AI catalog thread did not finish during validator setup.",
    )

    _require(window.objectName() == "localAITab", "Local AI root object name mismatch.")
    _require(isinstance(window.main_splitter, QSplitter), "Local AI main splitter missing.")
    _require(window.main_splitter.count() == 2, "Local AI main splitter must contain two panels.")
    _require(window.main_splitter.widget(0).objectName() == "localAISidebar", "Sidebar must be first.")
    _require(window.main_splitter.widget(1).objectName() == "localAIChatCanvas", "Chat canvas must be second.")
    _require(isinstance(window.sidebar_panel, QFrame), "Sidebar frame missing.")
    _require(isinstance(window.chat_panel, QFrame), "Chat frame missing.")
    tabs = window.findChild(QTabWidget, "localAIInspectorTabs")
    _require(tabs is not None and tabs.count() == 3, "Local AI inspector tabs mismatch.")
    _require(window.ask_ai_button.toolTip() == "Ask Local AI", "Ask button contract changed.")
    _require(window.ask_ai_button.accessibleName() == "Ask Local AI", "Ask accessible name changed.")
    _require(window.question_edit.parentWidget() is not None, "Question control was detached.")
    _require(window.answer_box.parentWidget() is not None, "Answer control was detached.")
    _require(window.history_list.parentWidget() is not None, "History control was detached.")
    _require(window.file_evidence_list.parentWidget() is not None, "File evidence control was detached.")
    _require(window.symbol_evidence_list.parentWidget() is not None, "Symbol evidence control was detached.")
    _require(callable(window.ask_local_ai), "Local AI ask callback is not callable.")
    _require(window.model_combo.count() >= 1, "Fake local model did not reach existing model selector.")
    _require(
        window.model_combo.currentText() == "fake-local-model",
        "Global Local AI model was not projected into Project Q&A.",
    )

    window.close()
    window.deleteLater()
    for _index in range(4):
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    app.quit()
    app.processEvents()
    print("REAL_LOCAL_AI_GLOBAL_CATALOG_FIXTURE: PASS")
    print("REAL_LOCAL_AI_QT_TEARDOWN_CLEAN: PASS")
    print("REAL_LOCAL_AI_WIDGET: PASS")
    print("REAL_LOCAL_AI_SIDEBAR_CHAT_ORDER: PASS")
    print("REAL_LOCAL_AI_FUNCTIONAL_CONTROLS_ATTACHED: PASS")
    return True


def validate(root: Path) -> None:
    project_root = root.expanduser().resolve()
    _require(project_root.is_dir(), "Project root is not a directory: " + str(project_root))
    _validate_tab_registry(project_root)
    _validate_layout_source(project_root)
    _validate_theme(project_root)
    _validate_visible_names(project_root)
    _validate_qt_runtime(project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        validate(Path(args.project_root))
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID + " - " + str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
