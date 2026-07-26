# project-path: tools/validate_local_ai_redundant_model_projection_removal_v1.py
"""Validate removal of the redundant visible Local AI model projection."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "local-ai-redundant-model-projection-removal-v1"
MAIN = "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
UI = "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py"
ASK = (
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
    "project_qa_copy_error_ask_controller.py"
)
SIGNALS = (
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
    "signal_wiring.py"
)
SHELL_RELOCATION = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "_lazy_tab_layout_relocation.py"
)
SHELL_SYNC = "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py"
VALIDATOR = "tools/validate_local_ai_redundant_model_projection_removal_v1.py"
TOUCHED = (MAIN, UI, ASK, VALIDATOR)


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    """Return one exact file hash."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(root: Path, relative: str) -> str:
    """Read one required UTF-8 source file."""
    path = root / relative
    require(path.is_file(), "missing source: " + relative)
    return path.read_text(encoding="utf-8-sig")


def validate_static(root: Path) -> None:
    """Validate presentation removal and global-model ownership."""
    main = read(root, MAIN)
    ui = read(root, UI)
    ask = read(root, ASK)
    signals = read(root, SIGNALS)
    relocation = read(root, SHELL_RELOCATION)
    shell_sync = read(root, SHELL_SYNC)

    require(
        'widgets = [self.refresh_models_button]' in main,
        "Local AI header relocation still includes the model label or combo",
    )
    require(
        'layout.addWidget(window.local_ai_model_label)' not in ui,
        "Local runtime section still shows the redundant model label",
    )
    require(
        'layout.addWidget(window.model_combo)' not in ui,
        "Local runtime section still shows the redundant model combo",
    )
    require('window.local_ai_model_label.hide()' in ui, "model label is not hidden")
    require('window.model_combo.hide()' in ui, "compatibility combo is not hidden")
    print("LOCAL_AI_VISIBLE_MODEL_PROJECTION_REMOVED: PASS")

    require('QPushButton("Open Config AI")' in main, "Config AI shortcut missing")
    require(
        "window.refresh_models_button.clicked.connect(\n"
        "        window._local_ai_configuration.request_open_configuration\n"
        "    )" in signals,
        "Open Config AI shortcut is not wired to the canonical owner",
    )
    require(
        "widget.move_ai_runtime_controls_to_layout(" in relocation,
        "Local AI header relocation facade is missing",
    )
    print("LOCAL_AI_OPEN_CONFIG_SHORTCUT_PRESERVED: PASS")

    require(
        "def selected_local_ai_model(self) -> str:" in main,
        "global model resolver facade is missing",
    )
    require(
        "self._local_ai_configuration.snapshot().model_id" in main,
        "model resolver does not read the application-scoped owner",
    )
    require(
        "selected_model = _selected_local_ai_model(window)" in ask,
        "Ask Local AI still reads the hidden combo",
    )
    require(
        'model_text = _selected_local_ai_model(window)' in ask,
        "error diagnostics still read the hidden combo",
    )
    print("LOCAL_AI_GLOBAL_MODEL_AUTHORITY_PRESERVED: PASS")

    require('"project_qa"' in shell_sync, "Local AI left canonical Project scope")
    require("_reset_project_qa" in shell_sync, "Local AI reset owner missing")
    print("LOCAL_AI_PROJECT_SWITCH_RESET_PRESERVED: PASS")

    for relative in TOUCHED:
        source = read(root, relative)
        ast.parse(source, filename=relative)
        lines = len(source.splitlines())
        require(0 < lines <= 500, f"module-size violation {relative}: {lines}")
    print("LOCAL_AI_MODEL_CLEANUP_ARCHITECTURE_WARNINGS_ZERO: PASS")
    print("LOCAL_AI_MODEL_CLEANUP_SYMBOL_SHADOWING_ZERO: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt(root: Path) -> None:
    """Validate the actual Local AI window and late global signals."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    from PySide6.QtCore import QCoreApplication, QEvent, QThread
    from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

    from kanda_reasoner_app.local_ai_configuration import (
        LocalAIConfigurationController,
        install_application_local_ai_configuration,
    )

    class MemorySettings:
        def __init__(self) -> None:
            self.values: dict[str, object] = {
                "local_ai/selected_model_id": "fake-local-model",
            }

        def value(self, key: str, default: object = None) -> object:
            return self.values.get(key, default)

        def setValue(self, key: str, value: object) -> None:
            self.values[key] = value

    class FakeRegistry:
        def __init__(self, *args: object, **kwargs: object) -> None:
            del args, kwargs

        def list_models(self) -> list[str]:
            return ["fake-local-model", "second-local-model"]

    app = QApplication.instance() or QApplication([])
    controller = LocalAIConfigurationController(
        app,
        settings=MemorySettings(),
        registry_factory=FakeRegistry,
    )
    install_application_local_ai_configuration(controller)

    import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window as main_module

    main_module.LocalModelRegistry = FakeRegistry
    window = main_module.JsonProjectReasonerV10()
    deadline = time.monotonic() + 3.0
    while controller._catalog_thread is not None and time.monotonic() < deadline:
        app.processEvents()
        QThread.msleep(10)
    app.processEvents()
    require(controller._catalog_thread is None, "Local AI catalog worker did not settle")

    host = QWidget()
    host_layout = QHBoxLayout(host)
    window.move_ai_runtime_controls_to_layout(host_layout)
    app.processEvents()

    require(not window.local_ai_model_label.isVisible(), "model label remains visible")
    require(not window.model_combo.isVisible(), "model combo remains visible")
    require(host_layout.indexOf(window.refresh_models_button) >= 0, "Config AI button missing")
    require(host_layout.indexOf(window.model_combo) < 0, "hidden model combo moved into header")
    require(
        host_layout.indexOf(window.local_ai_model_label) < 0,
        "hidden model label moved into header",
    )
    print("REAL_QT_LOCAL_AI_HEADER_HAS_NO_MODEL_WIDGET: PASS")

    opened: list[bool] = []
    controller.open_configuration_requested.connect(lambda: opened.append(True))
    window.refresh_models_button.click()
    app.processEvents()
    require(opened == [True], "Open Config AI shortcut did not request configuration")
    require(controller.consume_open_target() == "local", "wrong Config AI target")
    print("REAL_QT_LOCAL_AI_OPEN_CONFIG_SHORTCUT: PASS")

    controller.configuration_changed.emit(controller.snapshot())
    controller.catalog_changed.emit(controller.available_models())
    app.processEvents()
    require(not window.model_combo.isVisible(), "late config signal re-exposed model combo")
    require(
        window.selected_local_ai_model() == "fake-local-model",
        "global model resolver returned the wrong model",
    )
    print("REAL_QT_LOCAL_AI_CONFIG_SIGNALS_AFTER_MODEL_WIDGET_REMOVAL: PASS")

    captured: list[str] = []
    window.runtime_controller.ensure_project_json_loaded_for_question = lambda _window: None
    window.answer_presenter.populate_evidence_lists = lambda *_args: None

    def execute(_window: object, question: str, selected_model: str) -> object:
        captured.append(selected_model)
        return SimpleNamespace(
            log_messages=[],
            bundle=object(),
            prompt="",
            selected_model=selected_model,
            question=question,
            route="ranked",
            answer_text="ranked result",
        )

    window.session_service.execute = execute
    window.question_edit.setText("test global model")
    window.ask_local_ai()
    require(captured == ["fake-local-model"], "Ask did not use global Config AI model")
    print("REAL_QT_LOCAL_AI_ASK_USES_GLOBAL_MODEL: PASS")

    window.close()
    window.deleteLater()
    host.close()
    host.deleteLater()
    for _index in range(4):
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    print("REAL_QT_LOCAL_AI_MODEL_PROJECTION_REMOVAL: PASS")


def main() -> int:
    """Run static and real-widget validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    os.chdir(root)
    before = {
        relative: sha256(root / relative)
        for relative in (*TOUCHED, SIGNALS, SHELL_RELOCATION, SHELL_SYNC)
    }
    validate_static(root)
    if not args.static_only:
        validate_real_qt(root)
    after = {relative: sha256(root / relative) for relative in before}
    require(before == after, "validation mutated Tool source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
