#!/usr/bin/env python3
"""Validate Web AI warning resolver routing and Workflow Review AI cleanup."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import py_compile
import sys
from typing import Any

FEATURE_ID = "audit-warning-web-resolver-workflow-ai-cleanup-v1"
MAX_LINES = 500

__all__ = ["main"]

SPLIT_PATH = Path(
    "kanda_reasoner_app/manage_architecture/warning_resolver_split_control.py"
)
SUBTABS_PATH = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
ACTIONS_PATH = Path(
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
)
AUDIT_AI_PATH = Path(
    "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py"
)
WORKFLOW_AI_PATH = Path(
    "kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py"
)
CONFIG_VALIDATOR_PATH = Path("tools/validate_config_ai_global_local_v1.py")

TOUCHED_PRODUCTION = (
    SPLIT_PATH,
    SUBTABS_PATH,
    ACTIONS_PATH,
    WORKFLOW_AI_PATH,
)


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def read_text(root: Path, relative: Path) -> str:
    """Read one required UTF-8 project file."""
    path = root / relative
    require(path.is_file(), "Missing required file: " + relative.as_posix())
    return path.read_text(encoding="utf-8-sig")


def validate_python_sources(root: Path) -> None:
    """Compile and size-gate every changed production module and validator."""
    for relative in (*TOUCHED_PRODUCTION, CONFIG_VALIDATOR_PATH, Path(__file__).relative_to(root)):
        text = read_text(root, relative)
        ast.parse(text, filename=relative.as_posix())
        py_compile.compile(str(root / relative), doraise=True)
        if relative in TOUCHED_PRODUCTION:
            require(
                len(text.splitlines()) <= MAX_LINES,
                relative.as_posix() + " exceeds " + str(MAX_LINES) + " lines",
            )
    print("CHANGED_PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_warning_web_route(root: Path) -> None:
    """Prove the third menu option reuses the central Audit Web AI route."""
    split = read_text(root, SPLIT_PATH)
    subtabs = read_text(root, SUBTABS_PATH)
    actions = read_text(root, ACTIONS_PATH)
    audit_ai = read_text(root, AUDIT_AI_PATH)

    required_split = (
        "web_callback: Callable[[], None] | None = None",
        'menu.addAction("Warning Heuristic Resolver")',
        'menu.addAction("Warning Local AI Resolver")',
        'menu.addAction("Web AI resolver")',
        'state["route"] = "web"',
        'main_button.setText("Web AI resolver")',
        "web_callback()",
    )
    for fragment in required_split:
        require(fragment in split, "Missing Web resolver menu fragment: " + fragment)

    require(
        "web_callback=window.run_warning_web_ai_resolver" in subtabs,
        "Architecture Review does not bind the Web resolver callback.",
    )
    required_action = (
        "def run_warning_web_ai_resolver(self) -> None:",
        "self._warning_resolver_route_busy()",
        'getattr(self, "_ai_review_web_radio", None)',
        'getattr(self, "_ai_review_button", None)',
        "web_radio.setChecked(True)",
        "review_button.click()",
        "Config AI > Config Web AI",
        "remains read-only",
    )
    for fragment in required_action:
        require(fragment in actions, "Missing central Web resolver reuse: " + fragment)

    forbidden_web_ownership = (
        "requests.",
        "urllib.request",
        "httpx",
        "openai",
        "OPENROUTER_API_KEY",
        "/chat/completions",
        "WebAIConfigurationController(",
        "WebAIProviderRuntime(",
    )
    combined = split + "\n" + subtabs + "\n" + actions
    for fragment in forbidden_web_ownership:
        require(
            fragment not in combined,
            "Warning resolver created duplicate Web AI ownership: " + fragment,
        )

    central_requirements = (
        "application_web_ai_configuration()",
        "_request_web_approval",
        "AuditReviewIdentity",
        "configuration_revision",
        "worker.moveToThread(thread)",
        "advisory and read-only",
    )
    for fragment in central_requirements:
        require(
            fragment in audit_ai,
            "Central Audit Web AI contract is missing: " + fragment,
        )

    print("WARNING_RESOLVER_WEB_AI_OPTION: PASS")
    print("WARNING_RESOLVER_REUSES_CENTRAL_WEB_AI: PASS")
    print("WARNING_RESOLVER_NO_DUPLICATE_WEB_TRANSPORT: PASS")
    print("WARNING_RESOLVER_CONCURRENT_ROUTE_GUARD: PASS")


def validate_workflow_cleanup(root: Path) -> None:
    """Prove Workflow Review has actions, not competing Local AI config UI."""
    workflow = read_text(root, WORKFLOW_AI_PATH)
    required = (
        "application_local_ai_configuration()",
        "controller.snapshot()",
        "model_name = snapshot.model_id",
        "snapshot.revision",
        "runtime_local_ai_configuration_snapshot()",
        'QPushButton("AI Review First Check")',
        'QPushButton("AI Review Correction Plan")',
        "_tab2_ai_review_model_label = None",
        "_tab2_ai_review_model_combo = None",
        "_tab2_ai_review_refresh_models_button = None",
        "review_check_button,",
        "review_correction_button,",
    )
    for fragment in required:
        require(fragment in workflow, "Missing Workflow Review contract: " + fragment)

    forbidden = (
        'QLabel("AI model:")',
        'QPushButton("Open Config AI")',
        "QComboBox()",
        "configuration_changed.connect",
        "catalog_changed.connect",
        "QSettings(",
        "selected_model",
    )
    for fragment in forbidden:
        require(
            fragment not in workflow,
            "Workflow Review retains duplicate Local AI ownership: " + fragment,
        )

    require(
        "move_ai_review_controls_to_layout" in workflow,
        "Workflow Review host relocation compatibility was removed.",
    )
    require(
        "row_container.hide()" in workflow,
        "Workflow Review legacy row is not hidden after host relocation.",
    )
    print("WORKFLOW_REVIEW_DUPLICATE_LOCAL_AI_CONTROLS_REMOVED: PASS")
    print("WORKFLOW_REVIEW_AI_ACTIONS_PRESERVED: PASS")
    print("WORKFLOW_REVIEW_GLOBAL_LOCAL_AI_RUNTIME: PASS")
    print("WORKFLOW_REVIEW_LOCAL_AI_REVISION_GUARD: PASS")


def validate_real_qt(root: Path, allow_no_qt: bool) -> None:
    """Exercise the real menu, callback reuse, and Workflow Review widget."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget
    except ImportError:
        if allow_no_qt:
            print("REAL_QT_AI_CONTROL_VALIDATION: SKIPPED_NO_PYSIDE6")
            return
        raise RuntimeError("PySide6 is required for real Qt validation.")

    from kanda_reasoner_app.manage_architecture.architecture_audit_actions_gui import (
        ArchitectureAuditActionsMixin,
    )
    from kanda_reasoner_app.manage_architecture.warning_resolver_split_control import (
        build_warning_resolver_split_control,
    )
    from kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window import (
        WorkflowManagerWindow,
    )

    app = QApplication.instance() or QApplication([])
    widgets: list[Any] = []
    try:
        parent = QWidget()
        widgets.append(parent)
        counts = {"heuristic": 0, "local": 0, "web": 0, "cancel": 0}

        def hit(name: str) -> None:
            counts[name] += 1

        bundle = build_warning_resolver_split_control(
            parent,
            heuristic_callback=lambda: hit("heuristic"),
            model_callback=lambda: hit("local"),
            web_callback=lambda: hit("web"),
            cancel_callback=lambda: hit("cancel"),
        )
        actions = bundle.dropdown_button.menu().actions()
        require(
            [action.text() for action in actions]
            == [
                "Warning Heuristic Resolver",
                "Warning Local AI Resolver",
                "Web AI resolver",
            ],
            "Warning resolver menu does not expose exactly the three required routes.",
        )
        actions[2].trigger()
        require(counts["web"] == 1, "Web resolver action did not call its callback.")
        require(
            bundle.main_button.text() == "Web AI resolver",
            "Web resolver selection did not update the main button.",
        )
        bundle.main_button.click()
        require(counts["web"] == 2, "Selected Web resolver route was not retained.")
        legacy_parent = QWidget()
        widgets.append(legacy_parent)
        legacy_bundle = build_warning_resolver_split_control(
            legacy_parent,
            heuristic_callback=lambda: hit("heuristic"),
            model_callback=lambda: hit("local"),
            cancel_callback=lambda: hit("cancel"),
        )
        require(
            [action.text() for action in legacy_bundle.dropdown_button.menu().actions()]
            == ["Warning Heuristic Resolver", "Warning Local AI Resolver"],
            "Legacy callers without a Web callback no longer retain two routes.",
        )
        print("REAL_QT_WARNING_RESOLVER_LEGACY_TWO_ROUTE_COMPATIBILITY: PASS")
        print("REAL_QT_WARNING_RESOLVER_THREE_OPTIONS: PASS")
        print("REAL_QT_WARNING_WEB_ROUTE_CALLBACK: PASS")

        class _Status:
            def __init__(self) -> None:
                self.message = ""

            def showMessage(self, message: str) -> None:
                self.message = message

        class _Toggle:
            def __init__(self) -> None:
                self.checked = False

            def setChecked(self, value: bool) -> None:
                self.checked = bool(value)

        class _Click:
            def __init__(self) -> None:
                self.count = 0

            def click(self) -> None:
                self.count += 1

        class _Owner:
            def __init__(self) -> None:
                self._ai_review_web_radio = _Toggle()
                self._ai_review_button = _Click()
                self._status = _Status()

            def _warning_resolver_route_busy(self) -> bool:
                return False

            def statusBar(self) -> _Status:
                return self._status

        owner = _Owner()
        ArchitectureAuditActionsMixin.run_warning_web_ai_resolver(owner)
        require(owner._ai_review_web_radio.checked, "Web review mode was not selected.")
        require(owner._ai_review_button.count == 1, "Central review action was not clicked.")
        require("read-only" in owner._status.message, "Read-only route status is absent.")
        print("REAL_QT_WARNING_WEB_REUSES_CENTRAL_REVIEW: PASS")

        workflow = WorkflowManagerWindow()
        widgets.append(workflow)
        require(
            getattr(workflow, "_tab2_ai_review_model_label", "missing") is None,
            "Workflow Review still exposes a Local AI model label.",
        )
        require(
            getattr(workflow, "_tab2_ai_review_model_combo", "missing") is None,
            "Workflow Review still exposes a Local AI model combo.",
        )
        require(
            getattr(workflow, "_tab2_ai_review_refresh_models_button", "missing") is None,
            "Workflow Review still exposes a Local AI config/refresh button.",
        )
        texts = [button.text() for button in workflow.findChildren(QPushButton)]
        label_texts = [label.text() for label in workflow.findChildren(QLabel)]
        require("AI model:" not in label_texts, "Duplicate AI model label remains.")
        require("Open Config AI" not in texts, "Duplicate Config AI button remains.")
        require("AI Review First Check" in texts, "First Check AI action was removed.")
        require(
            "AI Review Correction Plan" in texts,
            "Correction Plan AI action was removed.",
        )
        print("REAL_QT_WORKFLOW_AI_CONTROL_CLEANUP: PASS")
        print("REAL_QT_WORKFLOW_AI_ACTIONS_PRESERVED: PASS")
    finally:
        for widget in reversed(widgets):
            widget.close()
            widget.deleteLater()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        app.processEvents()
        print("REAL_QT_AI_CONTROL_TEARDOWN_CLEAN: PASS")


def parse_args() -> argparse.Namespace:
    """Parse validator command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--allow-no-qt", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Run focused static and optional real-Qt validation."""
    args = parse_args()
    root = args.root.resolve()
    try:
        validate_python_sources(root)
        validate_warning_web_route(root)
        validate_workflow_cleanup(root)
        if not args.static_only:
            validate_real_qt(root, args.allow_no_qt)
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print(str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
