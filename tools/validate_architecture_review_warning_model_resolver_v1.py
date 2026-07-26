# project-path: tools/validate_architecture_review_warning_model_resolver_v1.py
"""Validate Warning Resolver split routes and Local AI test-protection escalation."""

from __future__ import annotations

import ast
import py_compile
from pathlib import Path
import subprocess
import sys

FEATURE_ID = "architecture-review-warning-local-ai-resolver-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_LINES = 500

__all__ = ["main"]

PRODUCTION_FILES = (
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py",
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
    "kanda_reasoner_app/manage_architecture/warning_resolver_split_control.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py",
    "kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py",
)
TEST_FILES = (
    "tests/test_warning_model_test_protection_resolver.py",
    "tests/test_warning_resolver_split_control.py",
    "tests/test_warning_resolver_shared_worker_routes.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(relative: str) -> str:
    path = PROJECT_ROOT / relative
    require(path.is_file(), "Missing expected file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_python_syntax_and_size() -> None:
    for relative in PRODUCTION_FILES + TEST_FILES:
        text = read(relative)
        ast.parse(text, filename=relative)
        py_compile.compile(str(PROJECT_ROOT / relative), doraise=True)
        if relative in PRODUCTION_FILES:
            require(
                len(text.splitlines()) <= MAX_LINES,
                relative + " exceeds " + str(MAX_LINES) + " lines",
            )
    print("WARNING_MODEL_RESOLVER_PYTHON_SYNTAX: PASS")
    print("WARNING_MODEL_RESOLVER_MODULE_SIZE_GATE: PASS")


def validate_split_button_contract() -> None:
    split_text = read(
        "kanda_reasoner_app/manage_architecture/warning_resolver_split_control.py"
    )
    subtabs = read(
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
    )
    required = (
        'qt.QPushButton("Warning Heuristic Resolver"',
        'menu.addAction("Warning Heuristic Resolver")',
        'menu.addAction("Warning Local AI Resolver")',
        "qt.QToolButton.InstantPopup",
        'state = {"route": "heuristic"}',
        'state["route"] = "model"',
    )
    for fragment in required:
        require(fragment in split_text, "Missing split-control fragment: " + fragment)
    require("QComboBox" not in split_text, "Resolver dropdown must not add a model selector")
    require("_ai_review_model_combo" not in split_text, "Split control must not own model selection")
    require(
        "build_warning_resolver_split_control(" in subtabs,
        "Architecture Review must install split control",
    )
    print("WARNING_RESOLVER_SPLIT_DROPDOWN_TWO_ROUTES_ONLY: PASS")


def validate_auto_local_model_resolution() -> None:
    actions = read(
        "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
    )
    context = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py"
    )
    require(
        'model_selection = ""' in actions,
        "Warning Local AI route must use automatic local-model resolution",
    )
    require(
        "controller.start(" in actions,
        "Automatic Local AI selection must cross the controller boundary",
    )
    require(
        "return models[0]" in context,
        "Automatic Local AI selection must resolve dynamically from available models",
    )
    require(
        '_ai_review_model_combo' not in actions,
        "Architecture Review must not restore the removed local-model selector",
    )
    print("WARNING_MODEL_RESOLVER_AUTO_LOCAL_MODEL_RESOLUTION: PASS")
    print("WARNING_MODEL_RESOLVER_NO_MODEL_DROPDOWN: PASS")


def validate_qthread_and_gui_boundary() -> None:
    actions = read(
        "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
    )
    controller = read(
        "kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_controller.py"
    )
    worker = read(
        "kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_worker.py"
    )
    require("QThread" in controller, "model resolver controller must use QThread")
    require("worker.moveToThread(thread)" in controller, "Worker must move to QThread")
    require("build_model_test_protection_plan(" in worker, "Heavy model-assisted planning must run in worker")
    require("chat_with_local_model" not in actions, "GUI action layer must not call model transport directly")
    require("_warning_resolver_controller" in actions, "GUI must reuse the shared warning resolver controller")
    require('route="model"' in actions, "Local AI GUI route must select model mode explicitly")
    print("WARNING_MODEL_RESOLVER_QTHREAD_NON_BLOCKING_ROUTE: PASS")


def validate_fail_closed_ai_contract() -> None:
    context = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py"
    )
    resolver = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py"
    )
    required_context = (
        "Never invent a test path",
        "Use web_ai when evidence is ambiguous",
        "confidence < _MIN_AI_CONFIDENCE",
        "candidate is None",
        "not _relationship_gate(candidate)",
        "Local AI did not produce a sufficiently grounded existing-test link",
    )
    for fragment in required_context:
        require(fragment in context, "Missing fail-closed model-assisted contract: " + fragment)
    require("for attempt in range(2):" in resolver, "model JSON contract gets at most one retry")
    require(
        "apply_test_protection_gap_plan" in resolver,
        "model-assisted writes must reuse existing guarded test-link writer",
    )
    print("WARNING_MODEL_RESOLVER_FAIL_CLOSED_JSON_CONTRACT: PASS")
    print("WARNING_MODEL_RESOLVER_GUARDED_WRITER_REUSE: PASS")


def validate_direct_test_protection_imports() -> None:
    combined = "\n".join(read(path) for path in TEST_FILES)
    modules = (
        "warning_resolver_split_control",
        "warning_model_test_protection_context",
        "warning_model_test_protection_resolver",
        "warning_model_test_protection_formatting",
        "warning_model_resolver_sonar",
    )
    for module in modules:
        require(module in combined, "Focused tests lack direct protection import for: " + module)
    print("WARNING_MODEL_RESOLVER_FOCUSED_TEST_PROTECTION_IMPORTS: PASS")


def run_focused_tests() -> None:
    for relative in TEST_FILES:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / relative)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.stderr:
            print(completed.stderr.rstrip())
        require(completed.returncode == 0, "Focused test failed: " + relative)
    print("WARNING_MODEL_RESOLVER_FOCUSED_TESTS: PASS")


def main() -> int:
    try:
        validate_python_syntax_and_size()
        validate_split_button_contract()
        validate_auto_local_model_resolution()
        validate_qthread_and_gui_boundary()
        validate_fail_closed_ai_contract()
        validate_direct_test_protection_imports()
        run_focused_tests()
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print(str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
