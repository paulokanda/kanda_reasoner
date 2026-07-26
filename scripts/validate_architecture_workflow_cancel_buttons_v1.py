"""Validate magenta Cancel buttons for Architecture and Workflow Review tabs."""
from __future__ import annotations

import ast
from pathlib import Path

__all__: list[str] = []


ROOT = Path(__file__).resolve().parents[1]
ARCH_GUI = ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"
ARCH_AI = ROOT / "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py"
WORKFLOW_GUI = ROOT / "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py"
WORKFLOW_AI = ROOT / "kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py"


def _read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def _method_source(path: Path, class_name: str, method_name: str) -> str:
    text = _read(path)
    tree = ast.parse(text)
    lines = text.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return "\n".join(lines[item.lineno - 1 : item.end_lineno])
    raise AssertionError(f"{class_name}.{method_name} not found in {path}")


def _module_method_source(path: Path, method_name: str) -> str:
    text = _read(path)
    tree = ast.parse(text)
    lines = text.splitlines()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError(f"{method_name} not found in {path}")


def _assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def _assert_cancel_button_after_write(build_ui_source: str, object_name: str) -> None:
    write_pos = build_ui_source.find("'write'")
    cancel_pos = build_ui_source.find(object_name)
    if write_pos < 0 or cancel_pos < 0 or cancel_pos <= write_pos:
        raise AssertionError(f"{object_name} must be created after the write quick button block")


def _validate_window(path: Path, class_name: str, object_name: str, tab_label: str) -> None:
    text = _read(path)
    _assert_contains(text, "QTimer", f"{tab_label} QTimer import")
    _assert_contains(text, "_operation_cancel_requested", f"{tab_label} cancel state")
    _assert_contains(text, "_mode_quick_buttons", f"{tab_label} quick button registry")
    _assert_contains(text, object_name, f"{tab_label} cancel button object name")
    _assert_contains(text, "#C2185B", f"{tab_label} magenta cancel color")
    _assert_contains(text, "cancel_running_operation", f"{tab_label} cancel slot")

    build_ui = _method_source(path, class_name, "_build_ui")
    _assert_cancel_button_after_write(build_ui, object_name)
    _assert_contains(build_ui, "setEnabled(False)", f"{tab_label} cancel initially disabled")
    _assert_contains(build_ui, "clicked.connect(self.cancel_running_operation)", f"{tab_label} cancel wiring")

    run_mode = _method_source(path, class_name, "run_mode")
    _assert_contains(run_mode, "Cancel or wait", f"{tab_label} running warning mentions cancel")
    _assert_contains(run_mode, "self._operation_cancel_requested = False", f"{tab_label} clears cancel flag on start")
    _assert_contains(run_mode, "self._set_operation_buttons_running(True)", f"{tab_label} enables cancel during run")

    button_sync = _method_source(path, class_name, "_set_operation_buttons_running")
    _assert_contains(button_sync, "setEnabled(not running)", f"{tab_label} disables run buttons while running")
    _assert_contains(button_sync, "setEnabled(running)", f"{tab_label} enables cancel while running")

    cancel = _method_source(path, class_name, "cancel_running_operation")
    _assert_contains(cancel, "requestInterruption", f"{tab_label} cooperative cancel request")
    _assert_contains(cancel, "quit()", f"{tab_label} thread quit request")
    _assert_contains(cancel, "QTimer.singleShot(300", f"{tab_label} delayed hard-cancel guard")
    _assert_contains(cancel, "finish_error", f"{tab_label} sonar/error state on cancel")
    _assert_contains(cancel, "[cancel requested]", f"{tab_label} cancel evidence line")

    force = _method_source(path, class_name, "_force_cancel_worker_thread")
    _assert_contains(force, "terminate()", f"{tab_label} hard cancellation fallback")
    _assert_contains(force, "wait(1000)", f"{tab_label} bounded wait after terminate")

    success = _method_source(path, class_name, "_handle_worker_success")
    error = _method_source(path, class_name, "_handle_worker_error")
    _assert_contains(success, "late success ignored", f"{tab_label} late success guard")
    _assert_contains(error, "late error ignored", f"{tab_label} late error guard")

    cleanup = _method_source(path, class_name, "_cleanup_worker")
    _assert_contains(cleanup, "_set_operation_buttons_running(False)", f"{tab_label} cleanup resets buttons")


def _validate_ai_integration(path: Path, cancel_thread_name: str, label: str) -> None:
    text = _read(path)
    _assert_contains(text, "_operation_cancel_requested = False", f"{label} clears cancel flag on AI start")
    _assert_contains(text, "_set_operation_buttons_running(True)", f"{label} enables cancel during AI review")
    _assert_contains(text, "late result ignored", f"{label} late AI result guard")
    _assert_contains(text, "_set_operation_buttons_running(False)", f"{label} cleanup resets cancel buttons")
    _assert_contains(text, cancel_thread_name, f"{label} keeps AI thread attribute")


def main() -> int:
    _validate_window(
        ARCH_GUI,
        "ArchitectureManagerWindow",
        "architecture_review_cancel_operation_button",
        "Architecture",
    )
    _validate_window(
        WORKFLOW_GUI,
        "WorkflowManagerWindow",
        "workflow_review_cancel_operation_button",
        "Workflow Review",
    )
    _validate_ai_integration(ARCH_AI, "_ai_review_thread", "Architecture AI review")
    _validate_ai_integration(WORKFLOW_AI, "_tab2_ai_review_thread", "Workflow AI review")

    workflow_text = _read(WORKFLOW_AI)
    _assert_contains(
        workflow_text,
        "if getattr(self, \"_operation_cancel_requested\", False):",
        "Workflow enhanced subclass cancellation guard",
    )
    print("VALIDATION OK: architecture-workflow-cancel-buttons-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
