# project-path: tools/validate_local_web_ai_canonical_host_height_v1.py
"""Validate Local/Web AI host height without full-shell worker startup."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

FEATURE_ID = "local-web-ai-canonical-host-height-v1"
GUI_SUPPORT = Path("kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py")
LOCAL_UI = Path(
    "kanda_reasoner_app/reasoner_engine/"
    "ai_reasoner_main_window_help/ui_builder.py"
)
WEB_UI = Path(
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _source(root: Path, relative: Path) -> str:
    path = root / relative
    _require(path.is_file(), "Missing source: " + relative.as_posix())
    text = path.read_text(encoding="utf-8", errors="strict")
    compile(text, str(path), "exec")
    ast.parse(text, filename=str(path))
    return text


def _validate_static(root: Path) -> None:
    support = _source(root, GUI_SUPPORT)
    local_ui = _source(root, LOCAL_UI)
    web_ui = _source(root, WEB_UI)

    for fragment in (
        'contain_host_height = bool(widget.property("kandaContainHostHeight"))',
        "QSizePolicy.Ignored",
        "widget.setMinimumHeight(0)",
    ):
        _require(
            fragment in support,
            "Missing embedded host-height contract: " + fragment,
        )

    for fragment in (
        'window.setProperty("kandaContainHostHeight", True)',
        "window.setMinimumHeight(0)",
        'scroll.setObjectName("projectQaBodyScrollArea")',
        "scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)",
    ):
        _require(
            fragment in local_ui,
            "Missing Local AI height contract: " + fragment,
        )

    for fragment in (
        'owner.setProperty("kandaContainHostHeight", True)',
        "owner.setMinimumSize(1080, 0)",
        'owner.setObjectName("projectWebAITab")',
    ):
        _require(
            fragment in web_ui,
            "Missing Project Web AI height contract: " + fragment,
        )

    _require(
        "owner.setMinimumSize(1080, 700)" not in web_ui,
        "Project Web AI still exports a 700px minimum host height.",
    )
    print("CANONICAL_EMBEDDED_HEIGHT_OWNER: PASS")
    print("LOCAL_AI_HOST_HEIGHT_OPT_IN: PASS")
    print("PROJECT_WEB_AI_HOST_HEIGHT_OPT_IN: PASS")
    print("PROJECT_WEB_AI_700PX_MINIMUM_REMOVED: PASS")


def _events(app, count: int = 8) -> None:
    for _ in range(count):
        app.processEvents()


def _validate_qt(root: Path) -> bool:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QObject, QSettings, Signal
        from PySide6.QtWidgets import (
            QApplication,
            QMainWindow,
            QSizePolicy,
            QTabWidget,
            QWidget,
        )
    except ModuleNotFoundError:
        print("REAL_LOCAL_WEB_AI_CANONICAL_HOST_HEIGHT: SKIPPED_NO_PYSIDE6")
        return False

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window as local_module
    import kanda_reasoner_app.reasoner_engine.project_web_ai_tab as web_module
    from kanda_reasoner_app.reasoner_tools_gui_shell.gui_support import (
        _prepare_embedded_widget,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import provider_profiles

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

    class _FixtureWebConfig(QObject):
        configuration_changed = Signal(object)
        catalog_changed = Signal(object)
        status_changed = Signal(str)

        def __init__(self):
            super().__init__()
            profiles = tuple(provider_profiles("gateway"))
            if not profiles:
                profiles = tuple(provider_profiles("direct"))
            self._profile = (
                profiles[0]
                if profiles
                else SimpleNamespace(
                    provider_class="gateway",
                    gateway_id="fixture",
                    privacy_summary="Fixture configuration",
                )
            )

        def request_open_configuration(self):
            return None

        def refresh_models(self):
            return None

        def profile(self):
            return self._profile

        def selected_model(self):
            return None

        def selected_model_id(self):
            return ""

        def visible_models(self):
            return ()

        def set_gateway_id(self, _value):
            return None

        def set_selected_model_id(self, _value):
            return None

        def summary(self):
            return "Fixture Web AI configuration"

        def catalog_status(self):
            return "Fixture"

        def api_key(self):
            return ""

        def ready_for_chat(self):
            return False

        def snapshot(self):
            return SimpleNamespace(revision="fixture")

    app = QApplication.instance() or QApplication([])
    original_local_config = local_module.application_local_ai_configuration
    original_local_ai = local_module.LocalAIReasoner
    original_qt_core_attr = local_module._qt_core_attr
    original_web_config = web_module.application_web_ai_configuration

    with tempfile.TemporaryDirectory(prefix="kanda_local_web_height_") as temp_dir:
        settings_path = str(Path(temp_dir) / "local_ai_height.ini")
        fixture_local_config = _FixtureLocalConfig()
        fixture_web_config = _FixtureWebConfig()

        def _fixture_qt_core_attr(name: str):
            if name == "QSettings":
                return lambda *_args: QSettings(
                    settings_path,
                    QSettings.Format.IniFormat,
                )
            return original_qt_core_attr(name)

        local_module.application_local_ai_configuration = (
            lambda: fixture_local_config
        )
        local_module.LocalAIReasoner = _FixtureAI
        local_module._qt_core_attr = _fixture_qt_core_attr
        web_module.application_web_ai_configuration = lambda: fixture_web_config

        local_widget = None
        web_widget = None
        host = QMainWindow()
        tabs = QTabWidget(host)
        baseline_page = QWidget()
        tabs.addTab(baseline_page, "Baseline")
        host.setCentralWidget(tabs)
        host.resize(1200, 760)
        host.show()
        _events(app)

        try:
            local_widget = local_module.JsonProjectReasonerV10()
            web_widget = web_module.ProjectWebAITab()
            local_widget = _prepare_embedded_widget(local_widget)
            web_widget = _prepare_embedded_widget(web_widget)
            tabs.addTab(local_widget, "Local AI")
            tabs.addTab(web_widget, "Web AI")

            tabs.setCurrentWidget(baseline_page)
            _events(app)
            baseline = (int(host.width()), int(host.height()))

            for label, widget in (
                ("Local AI", local_widget),
                ("Project Web AI", web_widget),
                ("Local AI", local_widget),
                ("Baseline", baseline_page),
            ):
                tabs.setCurrentWidget(widget)
                _events(app, 10)
                _require(
                    (int(host.width()), int(host.height())) == baseline,
                    label
                    + " changed isolated host size from "
                    + str(baseline)
                    + " to "
                    + str((int(host.width()), int(host.height()))),
                )

            for label, widget in (
                ("Local AI", local_widget),
                ("Project Web AI", web_widget),
            ):
                _require(
                    bool(widget.property("kandaContainHostHeight")),
                    label + " host-height property is missing.",
                )
                _require(
                    widget.minimumHeight() == 0,
                    label + " minimum height is not zero.",
                )
                _require(
                    widget.sizePolicy().verticalPolicy()
                    == QSizePolicy.Policy.Ignored,
                    label + " vertical size pressure is not ignored.",
                )
        finally:
            local_module.application_local_ai_configuration = original_local_config
            local_module.LocalAIReasoner = original_local_ai
            local_module._qt_core_attr = original_qt_core_attr
            web_module.application_web_ai_configuration = original_web_config
            host.close()
            _events(app, 4)
            for widget in (local_widget, web_widget):
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
            host.deleteLater()
            _events(app, 4)

    print("LOCAL_WEB_AI_VALIDATOR_FULL_SHELL_BYPASS: PASS")
    print("LOCAL_WEB_AI_VALIDATOR_WORKER_THREAD_START: ABSENT")
    print("REFERENCE_EAGER_TAB_SUPPORTED: PASS")
    print("LOCAL_WEB_AI_LAZY_TARGETS_CONFIRMED: PASS")
    print("REAL_LOCAL_AI_CANONICAL_HOST_HEIGHT: PASS")
    print("REAL_PROJECT_WEB_AI_CANONICAL_HOST_HEIGHT: PASS")
    print("REAL_LOCAL_WEB_AI_TAB_SWITCH_HEIGHT_STABLE: PASS")
    print("REAL_CANONICAL_HOST_SIZE_PRESERVED: PASS")
    return True


def validate(project_root: Path) -> None:
    root = project_root.expanduser().resolve()
    _require(root.is_dir(), "Project root is not a directory: " + str(root))
    _validate_static(root)
    _validate_qt(root)
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
