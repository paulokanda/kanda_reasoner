#!/usr/bin/env python3
"""Validate Config AI and the application-scoped Local AI configuration owner."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys
from typing import Iterable

FEATURE_ID = "config-ai-global-local-controller-v1r2"
WEB_TAB_SHA256 = "882956d59d3cc6de1090c6447ba43c7c603ec07124d8ec26d22edec97fcd4843"
CONFIG_AI_SUBTAB_LABELS = (
    "Config Web AI",
    "Direct API Providers",
    "Config Local AI",
)

TOUCHED_MODULES = (
    "kanda_reasoner_app/local_ai_configuration.py",
    "kanda_reasoner_app/local_ai_runtime_state.py",
    "kanda_reasoner_app/reasoner_engine/config_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/config_local_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/v10_model_registry.py",
    "kanda_reasoner_app/reasoner_engine/v10_qwen_ai_models.py",
    "kanda_reasoner_app/reasoner_engine/local_ai_chat_service.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
    "kanda_reasoner_app/reasoner_engine/ai_bridge.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/settings_manager.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/signal_wiring.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_shell_chrome.py",
    "kanda_reasoner_app/manage_architecture/ai_review/adapter.py",
    "kanda_reasoner_app/manage_architecture/ai_review/contracts.py",
    "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py",
    "kanda_reasoner_app/manage_workflows/ai_review/adapter.py",
    "kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_ai_formulary.py",
    "kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    "kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_contracts.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_task_contracts.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_async_runtime.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_openai_compatible_provider_runtime.py",
    "tools/validate_config_web_ai_central_v1.py",
    "tools/validate_freeze_central_web_ai_v1.py",
    "tools/validate_error_memory_central_web_ai_v1.py",
    "tools/validate_docstring_assistant_web_ai_pilot_v1.py",
)


def _text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError("Required source missing: " + str(path))
    return path.read_text(encoding="utf-8-sig")


def _require(text: str, needles: Iterable[str], label: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(label + " missing: " + ", ".join(missing))


def _forbid(text: str, needles: Iterable[str], label: str) -> None:
    found = [needle for needle in needles if needle in text]
    if found:
        raise AssertionError(label + " unexpectedly contains: " + ", ".join(found))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static(root: Path) -> None:
    tool_specs = _text(root, "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py")
    _require(
        tool_specs,
        (
            'step_title="Config AI"',
            '"config_ai_tab"',
            'class_candidates=("ConfigAITab",)',
            'tab_id="config_web_ai"',
        ),
        "Config AI ToolSpec",
    )
    print("CONFIG_AI_TOP_LEVEL_RENAME: PASS")

    composite = _text(root, "kanda_reasoner_app/reasoner_engine/config_ai_tab.py")
    _require(
        composite,
        (
            "ConfigWebAITab()",
            "ConfigDirectWebAITab",
            "application_web_ai_configuration()",
            'addTab(self.web_ai_tab, "Config Web AI")',
            'addTab(self.direct_web_ai_tab, "Direct API Providers")',
            'addTab(self.local_ai_tab, "Config Local AI")',
        ),
        "Config AI composite",
    )
    web_tab = root / "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py"
    if _sha256(web_tab) != WEB_TAB_SHA256:
        raise AssertionError("Existing Config Web AI source changed.")
    print("CONFIG_AI_WEB_SUBTAB_PRESERVED: PASS")
    print("CONFIG_AI_DIRECT_SUBTAB_PRESERVED: PASS")
    print("CONFIG_AI_LOCAL_SUBTAB_PRESENT: PASS")

    local_owner = _text(root, "kanda_reasoner_app/local_ai_configuration.py")
    _require(
        local_owner,
        (
            '"local_ai/base_url"',
            '"local_ai/selected_model_id"',
            "LocalAIConfigurationSnapshot",
            "configuration_changed = Signal(object)",
            "publish_runtime_local_ai_configuration_snapshot",
            "request_open_configuration",
        ),
        "Local AI owner",
    )
    _forbid(
        local_owner,
        (
            "project_support_boundary",
            "active_project_root",
            "active_project_support_root",
            "project_freeze_ledger",
        ),
        "Tool-owned Local AI configuration",
    )
    runtime_state = _text(root, "kanda_reasoner_app/local_ai_runtime_state.py")
    _require(
        runtime_state,
        ("LocalAIConfigurationSnapshot", "runtime_local_ai_configuration_snapshot"),
        "Qt-free Local AI runtime state",
    )
    _forbid(runtime_state, ("PySide6", "project_support", "active_project"), "runtime state")
    print("LOCAL_AI_TOOL_PROJECT_BOUNDARY: PASS")

    competing = []
    for path in (root / "kanda_reasoner_app").rglob("*.py"):
        if path.name == "local_ai_configuration.py":
            continue
        source = path.read_text(encoding="utf-8-sig")
        if "tab2_ai_review_selected_model" in source:
            competing.append(str(path.relative_to(root)))
        if "setValue('selected_model'" in source or 'setValue("selected_model"' in source:
            competing.append(str(path.relative_to(root)))
    if competing:
        raise AssertionError("Competing Local AI settings owner: " + ", ".join(competing))
    print("LOCAL_AI_SINGLE_QSETTINGS_OWNER: PASS")

    registry = _text(root, "kanda_reasoner_app/reasoner_engine/v10_model_registry.py")
    transport = _text(root, "kanda_reasoner_app/reasoner_engine/v10_qwen_ai_models.py")
    service = _text(root, "kanda_reasoner_app/reasoner_engine/local_ai_chat_service.py")
    _require(registry, ("runtime_local_ai_configuration_snapshot", "self._models_url"), "registry")
    _require(transport, ("runtime_local_ai_configuration_snapshot", "self._chat_url"), "transport")
    _require(
        service,
        (
            "configured =",
            "selected = configured or",
            '"base_url": snapshot.base_url',
            "No global Local AI model is configured",
        ),
        "shared Local AI service",
    )
    print("LOCAL_AI_GLOBAL_ENDPOINT_PROPAGATION: PASS")
    print("LOCAL_AI_GLOBAL_MODEL_PROPAGATION: PASS")

    consumer_requirements = {
        "Project Q&A": (
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
            ("application_local_ai_configuration", "Open Config AI", "setEnabled(False)"),
        ),
        "Workflow Review": (
            "kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py",
            ("application_local_ai_configuration", "Open Config AI", "snapshot.revision"),
        ),
        "Audit Project": (
            "kanda_reasoner_app/manage_architecture/ai_review/contracts.py",
            ("_audit_local_ai_configuration.snapshot()", "revision = snapshot.revision"),
        ),
        "Freeze": (
            "kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py",
            ("local_controller.snapshot()", "configuration_revision=local_snapshot.revision"),
        ),
        "Error Memory": (
            "kanda_reasoner_app/error_memory_gui/_ai_correction_contracts.py",
            ("local_configuration(tab).snapshot()", "revision = snapshot.revision"),
        ),
        "Docstring": (
            "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py",
            ("_local_controller(owner).selected_model_id()", "_local_controller(owner).base_url()"),
        ),
    }
    for name, (relative, needles) in consumer_requirements.items():
        _require(_text(root, relative), needles, name)
    for relative in (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_docstring_review.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_staged_protocol.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_diff_review_assistant.py",
    ):
        _require(_text(root, relative), ("chat_with_local_model",), relative)
    print("LOCAL_AI_CONSUMER_COVERAGE: PASS")

    guard_sources = (
        "kanda_reasoner_app/reasoner_engine/ai_bridge.py",
        "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py",
        "kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py",
        "kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py",
        "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_async_runtime.py",
    )
    for relative in guard_sources:
        source = _text(root, relative)
        _require(source, ("configuration_revision",), "stale guard " + relative)
    print("LOCAL_AI_ASYNC_REVISION_GUARDS: PASS")

    project_qa = _text(root, "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py")
    workflow = _text(root, "kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py")
    _require(project_qa, ('QPushButton("Open Config AI")', "model_combo.setEnabled(False)"), "Project Q&A")
    _require(
        workflow,
        (
            "snapshot = controller.snapshot()",
            "model_name = snapshot.model_id",
            "_tab2_ai_review_model_combo = None",
            "_tab2_ai_review_refresh_models_button = None",
        ),
        "Workflow Review",
    )
    _forbid(
        workflow,
        ('QLabel("AI model:")', 'QPushButton("Open Config AI")'),
        "Workflow Review duplicate Local AI controls",
    )
    print("PROJECT_QA_GLOBAL_LOCAL_AI_PROJECTION: PASS")
    print("WORKFLOW_REVIEW_GLOBAL_LOCAL_AI_RUNTIME: PASS")
    print("WORKFLOW_REVIEW_DUPLICATE_LOCAL_AI_CONTROLS_REMOVED: PASS")

    lazy = _text(root, "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py")
    _require(lazy, ("_configure_global_local_ai_header",), "global legacy header projection")
    _forbid(
        lazy,
        (
            "_install_show_project_ai_review_controls(self)",
            "_install_freeze_feature_ai_review_controls(self)",
        ),
        "Show Project/Freeze header regression",
    )
    print("SHOW_PROJECT_FREEZE_HEADER_REGRESSION: PASS")

    oversized = []
    for relative in TOUCHED_MODULES + ("tools/validate_config_ai_global_local_v1.py",):
        lines = len(_text(root, relative).splitlines())
        if lines > 500:
            oversized.append(relative + "=" + str(lines))
    if oversized:
        raise AssertionError("Touched module exceeds 500 lines: " + ", ".join(oversized))
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from PySide6.QtWidgets import QApplication, QComboBox

    from kanda_reasoner_app.local_ai_configuration import (
        LocalAIConfigurationController,
        install_application_local_ai_configuration,
    )
    from kanda_reasoner_app.reasoner_engine.config_ai_tab import ConfigAITab
    from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.runtime_controller import (
        RuntimeController,
    )

    class MemorySettings:
        def __init__(self) -> None:
            self.values: dict[str, object] = {}

        def value(self, key: str, default: object = None, **_kwargs: object) -> object:
            return self.values.get(key, default)

        def setValue(self, key: str, value: object) -> None:
            self.values[key] = value

    class FakeStatusBar:
        def showMessage(self, _message: str) -> None:
            return

    class FakeWindow:
        def __init__(self) -> None:
            self.model_combo = QComboBox()
            self.messages: list[str] = []

        def _append_log(self, message: str) -> None:
            self.messages.append(message)

        def statusBar(self) -> FakeStatusBar:
            return FakeStatusBar()

    app = QApplication.instance() or QApplication([])
    settings = MemorySettings()
    controller = LocalAIConfigurationController(app, settings=settings)
    install_application_local_ai_configuration(controller)
    controller.set_base_url("http://localhost:11999")
    controller.set_selected_model_id("global-test-model:1")
    controller._models = ["other:1", "global-test-model:1"]
    controller._touch()

    composite = ConfigAITab(local_controller=controller)
    labels = tuple(
        composite.subtabs.tabText(i)
        for i in range(composite.subtabs.count())
    )
    if labels != CONFIG_AI_SUBTAB_LABELS:
        raise AssertionError("Unexpected Config AI subtab labels: " + repr(labels))
    if composite.web_ai_tab.__class__.__name__ != "ConfigWebAITab":
        raise AssertionError("Existing Config Web AI widget was not embedded.")
    if composite.direct_web_ai_tab.__class__.__name__ != "ConfigDirectWebAITab":
        raise AssertionError("Direct API Providers widget was not embedded.")
    if composite.local_ai_tab.__class__.__name__ != "ConfigLocalAITab":
        raise AssertionError("Config Local AI widget was not embedded.")
    print("REAL_QT_CONFIG_AI_SUBTABS: PASS")

    local = composite.local_ai_tab
    if local.base_url_edit.text() != "http://localhost:11999/v1":
        raise AssertionError("Local endpoint did not hydrate from central owner.")
    if local.model_combo.currentText() != "global-test-model:1":
        raise AssertionError("Local model did not hydrate from central owner.")
    local.base_url_edit.setText("http://127.0.0.1:11434")
    local._commit_base_url()
    local.model_combo.setCurrentText("changed-model:2")
    app.processEvents()
    if controller.base_url() != "http://127.0.0.1:11434/v1":
        raise AssertionError("Local endpoint edit did not reach central owner.")
    if controller.selected_model_id() != "changed-model:2":
        raise AssertionError("Local model edit did not reach central owner.")
    print("REAL_QT_LOCAL_CONFIG_HYDRATION: PASS")

    fake = FakeWindow()
    RuntimeController().refresh_models(fake)
    if fake.model_combo.isEnabled():
        raise AssertionError("Project Q&A model projection must remain read-only.")
    if fake.model_combo.currentText() != "changed-model:2":
        raise AssertionError("Project Q&A projection is not global.")
    print("REAL_QT_GLOBAL_LOCAL_AI_PROJECTION: PASS")

    from kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window import (
        WorkflowManagerWindow,
    )

    workflow_window = WorkflowManagerWindow()
    if getattr(workflow_window, "_tab2_ai_review_model_combo", object()) is not None:
        raise AssertionError("Workflow Review still owns a Local AI model selector.")
    if getattr(workflow_window, "_tab2_ai_review_refresh_models_button", object()) is not None:
        raise AssertionError("Workflow Review still owns an Open Config AI button.")
    if getattr(workflow_window, "_tab2_ai_review_check_button", None) is None:
        raise AssertionError("Workflow Review lost AI Review First Check.")
    if getattr(workflow_window, "_tab2_ai_review_correction_button", None) is None:
        raise AssertionError("Workflow Review lost AI Review Correction Plan.")
    print("REAL_QT_WORKFLOW_DUPLICATE_LOCAL_AI_CONTROLS_REMOVED: PASS")

    snapshot = controller.snapshot()
    forbidden = ("project", "support", "root", "daily", "source")
    names = tuple(snapshot.__dataclass_fields__) + tuple(controller.__dict__)
    if any(any(token in str(name).lower() for token in forbidden) for name in names):
        raise AssertionError("Global Local AI configuration contains Project-owned state.")
    print("REAL_QT_TOOL_PROJECT_BOUNDARY: PASS")
    workflow_window.deleteLater()
    composite.deleteLater()
    app.processEvents()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root")
    parser.add_argument("--static-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=False)
    validate_static(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
