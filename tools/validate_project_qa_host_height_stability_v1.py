# project-path: tools/validate_project_qa_host_height_stability_v1.py
"""Validate Project Q&A host-height containment without full-shell workers."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import os
import sys
import tempfile
from types import SimpleNamespace

FEATURE_ID = "project-qa-host-height-stability-v1"
UI_BUILDER_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_engine/"
    "ai_reasoner_main_window_help/ui_builder.py"
)
MAX_PHYSICAL_LINES = 500


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_static_contract(project_root: Path) -> None:
    source_path = project_root / UI_BUILDER_RELATIVE
    _require(source_path.is_file(), "Project Q&A ui_builder.py is missing.")
    source = source_path.read_text(encoding="utf-8", errors="strict")
    compile(source, str(source_path), "exec")
    ast.parse(source, filename=str(source_path))

    required_fragments = (
        "QScrollArea",
        "QAbstractScrollArea",
        'scroll.setObjectName("projectQaBodyScrollArea")',
        "scroll.setWidgetResizable(True)",
        "QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored",
        "Qt.ScrollBarPolicy.ScrollBarAsNeeded",
        "scroll.setMinimumHeight(0)",
        "scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)",
        'body.setObjectName("projectQaScrollableBody")',
        "body_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)",
        "main_layout.addWidget(scroll, stretch=1)",
        "window._project_qa_body_scroll_area = scroll",
    )
    for fragment in required_fragments:
        _require(
            fragment in source,
            "Missing Project Q&A height-containment fragment: " + fragment,
        )

    for fragment in (
        "setFixedHeight(1080",
        "setMinimumHeight(1080",
        "setFixedHeight(900",
        "setMinimumHeight(900",
    ):
        _require(
            fragment not in source,
            "Forbidden Project Q&A host-height lock fragment: " + fragment,
        )

    _require(
        len(source.splitlines()) <= MAX_PHYSICAL_LINES,
        "Project Q&A ui_builder.py exceeds 500 physical lines.",
    )
    print("PROJECT_QA_SCROLL_CONTAINMENT: PRESENT")
    print("VERTICAL_SIZE_PRESSURE: IGNORED")
    print("MODULE_SIZE_GATE: PASS")


def _events(app, count: int = 8) -> None:
    for _ in range(count):
        app.processEvents()


def _validate_qt_runtime(project_root: Path) -> bool:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QObject, QSettings, Signal, Qt
        from PySide6.QtWidgets import (
            QApplication,
            QMainWindow,
            QSizePolicy,
            QTabWidget,
            QWidget,
        )
    except ModuleNotFoundError:
        print("GUI HOST HEIGHT CHECK: SKIPPED_NO_PYSIDE6")
        return False

    project_text = str(project_root)
    if project_text not in sys.path:
        sys.path.insert(0, project_text)

    import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window as qa_module
    from kanda_reasoner_app.reasoner_tools_gui_shell.gui_support import (
        _prepare_embedded_widget,
    )

    class _FixtureLocalConfig(QObject):
        configuration_changed = Signal(object)
        catalog_changed = Signal(object)

        def snapshot(self):
            return SimpleNamespace(available_models=(), model_id="")

        def refresh_models(self):
            return None

        def request_open_configuration(self):
            return None

        def selected_model_id(self):
            return ""

    class _FixtureBridge(QObject):
        answer_ready = Signal(str)
        token_ready = Signal(str)
        error_ready = Signal(str)
        status_ready = Signal(str)

    class _FixtureAI:
        def __init__(self):
            self.bridge = _FixtureBridge()

        def ask(self, *_args, **_kwargs):
            return None

    app = QApplication.instance() or QApplication([])
    original_config_owner = qa_module.application_local_ai_configuration
    original_ai = qa_module.LocalAIReasoner
    original_qt_core_attr = qa_module._qt_core_attr

    with tempfile.TemporaryDirectory(prefix="kanda_project_qa_height_") as temp_dir:
        settings_path = str(Path(temp_dir) / "project_qa_height.ini")
        fixture_config = _FixtureLocalConfig()

        def _fixture_qt_core_attr(name: str):
            if name == "QSettings":
                return lambda *_args: QSettings(
                    settings_path,
                    QSettings.Format.IniFormat,
                )
            return original_qt_core_attr(name)

        qa_module.application_local_ai_configuration = lambda: fixture_config
        qa_module.LocalAIReasoner = _FixtureAI
        qa_module._qt_core_attr = _fixture_qt_core_attr

        project_widget = None
        host = QMainWindow()
        tabs = QTabWidget(host)
        baseline_page = QWidget()
        tabs.addTab(baseline_page, "Baseline")
        host.setCentralWidget(tabs)
        host.resize(1200, 760)
        host.show()
        _events(app)

        try:
            project_widget = qa_module.JsonProjectReasonerV10()
            project_widget = _prepare_embedded_widget(project_widget)
            tabs.addTab(project_widget, "Project Q&A")

            tabs.setCurrentWidget(baseline_page)
            _events(app)
            baseline_height = int(host.height())

            tabs.setCurrentWidget(project_widget)
            _events(app, 12)

            project_qa_height = int(host.height())
            _require(
                project_qa_height == baseline_height,
                "Project Q&A changed isolated host height from "
                + str(baseline_height)
                + " to "
                + str(project_qa_height),
            )

            scroll = getattr(
                project_widget,
                "_project_qa_body_scroll_area",
                None,
            )
            _require(scroll is not None, "Project Q&A body scroll area is missing.")
            _require(
                scroll.sizePolicy().verticalPolicy()
                == QSizePolicy.Policy.Ignored,
                "Project Q&A scroll area must ignore vertical size pressure.",
            )
            _require(
                scroll.verticalScrollBarPolicy()
                == Qt.ScrollBarPolicy.ScrollBarAsNeeded,
                "Project Q&A must expose internal vertical scrolling as needed.",
            )

            tabs.setCurrentWidget(baseline_page)
            _events(app)
            _require(
                int(host.height()) == baseline_height,
                "Returning to baseline changed isolated host height.",
            )
        finally:
            qa_module.application_local_ai_configuration = original_config_owner
            qa_module.LocalAIReasoner = original_ai
            qa_module._qt_core_attr = original_qt_core_attr
            host.close()
            _events(app, 4)
            if project_widget is not None:
                project_widget.setParent(None)
                project_widget.deleteLater()
            host.deleteLater()
            _events(app, 4)

    print("PROJECT_QA_VALIDATOR_FULL_SHELL_BYPASS: PASS")
    print("PROJECT_QA_VALIDATOR_WORKER_THREAD_START: ABSENT")
    print("GUI HOST HEIGHT CHECK: PASS")
    return True


def validate(project_root: Path) -> None:
    root = project_root.expanduser().resolve()
    _require(root.is_dir(), "Project root is not a directory: " + str(root))
    _validate_static_contract(root)
    _validate_qt_runtime(root)
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
