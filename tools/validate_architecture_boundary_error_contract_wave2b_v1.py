"""Validate explicit boundary error contracts for architecture wave 2B."""

from __future__ import annotations

import argparse
import ast
import importlib
import importlib.util
import os
import subprocess
import sys
import types
from pathlib import Path
from typing import Any

FEATURE_ID = "architecture-boundary-error-contract-wave2b-v1"

CLIPBOARD_OWNER = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "answer_validate_freeze_memorize_button_private_impl.py"
)
QT_VALIDATORS = (
    Path("tools/validate_architecture_review_run_mode_visual_group_v1.py"),
    Path("tools/validate_config_ai_rich_first_time_help_v1.py"),
    Path("tools/validate_project_scope_memory_reset_v1r1.py"),
    Path("tools/validate_shell_active_project_sync_v1.py"),
)
TARGETS = (CLIPBOARD_OWNER, *QT_VALIDATORS)

PORTABLE_MANIFESTS = (
    Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json"),
    Path("portable/PORTABLE_BUILDER_MANIFEST.json"),
    Path("portable/PORTABLE_EXTERNAL_BUILD_CONTROLS.json"),
)


def require(condition: bool, code: str) -> None:
    """Raise a deterministic validation error when condition is false."""
    if not condition:
        raise RuntimeError(code)


def read_source(root: Path, relative: Path) -> str:
    """Read one governed source file as strict UTF-8."""
    return (root / relative).read_text(encoding="utf-8-sig")


def function_node(tree: ast.Module, name: str) -> ast.FunctionDef:
    """Return one top-level function by exact name."""
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise RuntimeError("FUNCTION_NOT_FOUND:" + name)


def return_annotation_is_bool(node: ast.FunctionDef) -> bool:
    """Return whether one function has the exact bool return annotation."""
    return isinstance(node.returns, ast.Name) and node.returns.id == "bool"


def is_exception_handler(handler: ast.ExceptHandler) -> bool:
    """Return whether one handler catches broad Exception."""
    return isinstance(handler.type, ast.Name) and handler.type.id == "Exception"


def has_logger_exception(handler: ast.ExceptHandler) -> bool:
    """Return whether one handler emits exception-severity evidence."""
    for node in ast.walk(handler):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if (
            isinstance(function, ast.Attribute)
            and function.attr == "exception"
        ):
            return True
    return False


def has_literal_return(handler: ast.ExceptHandler, value: bool) -> bool:
    """Return whether a handler returns one exact boolean literal."""
    return any(
        isinstance(node, ast.Return)
        and isinstance(node.value, ast.Constant)
        and node.value.value is value
        for node in ast.walk(handler)
    )


def validate_clipboard_contract(root: Path) -> None:
    """Validate explicit success/failure behavior and exception evidence."""
    source = read_source(root, CLIPBOARD_OWNER)
    tree = ast.parse(source, filename=str(root / CLIPBOARD_OWNER))
    node = function_node(
        tree,
        "copy_answer_validate_freeze_memorize_to_clipboard",
    )
    require(
        return_annotation_is_bool(node),
        "CLIPBOARD_BOUNDARY_BOOL_RETURN_ANNOTATION_MISSING",
    )
    broad_handlers = [
        handler
        for handler in ast.walk(node)
        if isinstance(handler, ast.ExceptHandler)
        and is_exception_handler(handler)
    ]
    require(
        len(broad_handlers) == 1,
        "CLIPBOARD_BOUNDARY_EXCEPTION_HANDLER_COUNT_INVALID",
    )
    handler = broad_handlers[0]
    require(
        has_logger_exception(handler),
        "CLIPBOARD_BOUNDARY_EXCEPTION_SEVERITY_LOG_MISSING",
    )
    require(
        has_literal_return(handler, False),
        "CLIPBOARD_BOUNDARY_EXPLICIT_FAILURE_RESULT_MISSING",
    )
    require(
        any(
            isinstance(item, ast.Return)
            and isinstance(item.value, ast.Constant)
            and item.value.value is True
            for item in ast.walk(node)
        ),
        "CLIPBOARD_BOUNDARY_EXPLICIT_SUCCESS_RESULT_MISSING",
    )
    print("CLIPBOARD BOUNDARY EXPLICIT SUCCESS FAILURE: PASS")
    print("CLIPBOARD BOUNDARY EXCEPTION SEVERITY: PASS")


def validate_qt_validator_contracts(root: Path) -> None:
    """Require optional Qt skips to catch ImportError only."""
    for relative in QT_VALIDATORS:
        source = read_source(root, relative)
        tree = ast.parse(source, filename=str(root / relative))
        node = function_node(tree, "validate_real_qt")
        require(
            return_annotation_is_bool(node),
            "QT_VALIDATOR_BOOL_RETURN_MISSING:" + relative.as_posix(),
        )
        handlers = [
            handler
            for handler in ast.walk(node)
            if isinstance(handler, ast.ExceptHandler)
        ]
        require(
            len(handlers) == 1,
            "QT_VALIDATOR_HANDLER_COUNT_INVALID:" + relative.as_posix(),
        )
        handler = handlers[0]
        require(
            isinstance(handler.type, ast.Name)
            and handler.type.id == "ImportError",
            "QT_VALIDATOR_NON_IMPORT_ERROR_HANDLER:"
            + relative.as_posix(),
        )
        require(
            has_literal_return(handler, False),
            "QT_VALIDATOR_SKIP_RESULT_MISSING:" + relative.as_posix(),
        )
        require(
            any(
                isinstance(item, ast.Return)
                and isinstance(item.value, ast.Constant)
                and item.value.value is True
                for item in ast.walk(node)
            ),
            "QT_VALIDATOR_PASS_RESULT_MISSING:" + relative.as_posix(),
        )
        helper = function_node(tree, "_is_missing_pyside6_dependency")
        require(
            return_annotation_is_bool(helper),
            "QT_MISSING_DEPENDENCY_HELPER_RETURN_INVALID:"
            + relative.as_posix(),
        )
    print("OPTIONAL QT IMPORT ERROR CONTRACTS: PASS")
    print("UNRELATED QT IMPORT DEFECTS SURFACE: PASS")


def load_clipboard_owner(root: Path) -> Any:
    """Load the clipboard owner directly from the selected Project root."""
    path = root / CLIPBOARD_OWNER
    name = "_kanda_wave2b_clipboard_owner_fixture"
    spec = importlib.util.spec_from_file_location(name, path)
    require(
        spec is not None and spec.loader is not None,
        "CLIPBOARD_OWNER_IMPORT_SPEC_FAILED",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_clipboard_runtime(root: Path) -> None:
    """Exercise both clipboard success and surfaced failure without real Qt."""
    clipboard_values: list[str] = []

    class Clipboard:
        def setText(self, value: str) -> None:
            clipboard_values.append(value)

    clipboard = Clipboard()

    class QApplication:
        @staticmethod
        def clipboard() -> Clipboard:
            return clipboard

    pyside_module = types.ModuleType("PySide6")
    qtwidgets_module = types.ModuleType("PySide6.QtWidgets")
    qtwidgets_module.QApplication = QApplication

    saved_modules = {
        name: sys.modules.get(name)
        for name in ("PySide6", "PySide6.QtWidgets")
    }
    sys.modules["PySide6"] = pyside_module
    sys.modules["PySide6.QtWidgets"] = qtwidgets_module

    try:
        module = load_clipboard_owner(root)

        class Logger:
            def __init__(self) -> None:
                self.messages: list[str] = []

            def exception(self, message: str) -> None:
                self.messages.append(message)

        logger = Logger()
        module._LOGGER = logger

        class Edit:
            def __init__(self, text: str) -> None:
                self._text = text

            def text(self) -> str:
                return self._text

        class Status:
            def __init__(self) -> None:
                self.text_value = ""

            def setText(self, value: str) -> None:
                self.text_value = value

        class Window:
            def __init__(self, value: str) -> None:
                self.project_root_edit = Edit(value)
                self.first_prompt_status_label = Status()
                self.logs: list[str] = []

            def _append_log(self, value: str) -> None:
                self.logs.append(value)

        success_window = Window(str(root))
        success = module.copy_answer_validate_freeze_memorize_to_clipboard(
            success_window
        )
        require(success is True, "CLIPBOARD_SUCCESS_RESULT_INVALID")
        require(
            clipboard_values
            and "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT_BEGIN"
            in clipboard_values[-1],
            "CLIPBOARD_SUCCESS_PAYLOAD_INVALID",
        )
        require(
            success_window.logs
            and success_window.logs[-1].startswith(
                "Copied complete routine for selected Project:"
            ),
            "CLIPBOARD_SUCCESS_FEEDBACK_INVALID",
        )

        failure_window = Window("")
        failure = module.copy_answer_validate_freeze_memorize_to_clipboard(
            failure_window
        )
        require(failure is False, "CLIPBOARD_FAILURE_RESULT_INVALID")
        require(
            logger.messages
            and logger.messages[-1].startswith(
                "[ERROR] Could not copy Answer, Validate, Freeze, "
                "Memorize Error routine:"
            ),
            "CLIPBOARD_FAILURE_EXCEPTION_LOG_INVALID",
        )
        require(
            failure_window.logs
            and failure_window.logs[-1].startswith("[ERROR]"),
            "CLIPBOARD_FAILURE_USER_FEEDBACK_INVALID",
        )
    finally:
        for name, original in saved_modules.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original

    print("CLIPBOARD SUCCESS PATH FUNCTIONAL FIXTURE: PASS")
    print("CLIPBOARD FAILURE PATH FUNCTIONAL FIXTURE: PASS")


def validate_size_and_syntax(root: Path) -> None:
    """Compile every touched Python module and enforce the size law."""
    current_validator = Path(__file__).resolve().relative_to(root)
    for relative in (*TARGETS, current_validator):
        path = root / relative
        source = path.read_text(encoding="utf-8-sig")
        ast.parse(source, filename=str(path))
        require(
            len(source.splitlines()) <= 500,
            "TOUCHED_MODULE_EXCEEDS_500_LINES:" + relative.as_posix(),
        )
    print("WAVE2B PYTHON COMPILE AND SIZE: PASS")


def validate_portable_manifest_non_membership(root: Path) -> None:
    """Prove this patch does not require Portable manifest changes."""
    target_paths = {
        relative.as_posix()
        for relative in (*TARGETS, Path(__file__).resolve().relative_to(root))
    }
    for relative in PORTABLE_MANIFESTS:
        manifest = (root / relative).read_text(encoding="utf-8")
        overlap = sorted(
            target
            for target in target_paths
            if target in manifest
        )
        require(
            not overlap,
            "TARGET_UNEXPECTEDLY_GOVERNED_BY_PORTABLE_MANIFEST:"
            + relative.as_posix()
            + ":"
            + ",".join(overlap),
        )
    print("PORTABLE RUNTIME ALLOWLIST MODIFIED: NO")
    print("PORTABLE BUILDER MANIFEST MODIFIED: NO")
    print("PORTABLE EXTERNAL BUILD CONTROLS MODIFIED: NO")


def validate_architecture_warning_absence(root: Path) -> None:
    """Require the five exact live boundary warnings to be absent."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    architecture = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    _modules, issues, _manifest, _outputs = architecture.scan_project(root)
    target_paths = {relative.as_posix() for relative in TARGETS}
    remaining = [
        issue
        for issue in issues
        if issue.code == "BOUNDARY_ERROR_CONTRACT"
        and issue.path in target_paths
    ]
    require(
        not remaining,
        "WAVE2B_BOUNDARY_WARNING_REMAINS:"
        + repr([(issue.path, issue.message) for issue in remaining]),
    )
    print("WAVE2B TARGET BOUNDARY WARNINGS ABSENT: PASS")


def run_validator(
    root: Path,
    relative: str,
    arguments: list[str],
    marker: str,
    *,
    timeout: int = 1800,
) -> None:
    """Run one inherited validator and require its owned marker."""
    path = root / relative
    require(path.is_file(), "INHERITED_VALIDATOR_MISSING:" + relative)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = str(root)
    completed = subprocess.run(
        [sys.executable, str(path), *arguments],
        cwd=str(root),
        env=environment,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    require(
        completed.returncode == 0,
        "INHERITED_VALIDATOR_FAILED:" + relative,
    )
    require(
        marker in output,
        "INHERITED_VALIDATOR_MARKER_MISSING:" + relative,
    )


def main() -> int:
    """Run static and live validation for boundary-contract wave 2B."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_size_and_syntax(root)
    validate_clipboard_contract(root)
    validate_qt_validator_contracts(root)
    validate_clipboard_runtime(root)
    validate_portable_manifest_non_membership(root)
    validate_architecture_warning_absence(root)

    if not args.static_only:
        run_validator(
            root,
            "tools/"
            "validate_answer_validate_freeze_memorize_"
            "separated_terminal_phases_v1.py",
            ["--root", str(root)],
            "VALIDATION OK: "
            "answer-validate-freeze-memorize-separated-terminal-phases-v1",
        )
        run_validator(
            root,
            "tools/validate_architecture_review_run_mode_visual_group_v1.py",
            ["--root", str(root)],
            "VALIDATION OK: architecture-review-run-mode-visual-group-v1",
        )
        run_validator(
            root,
            "tools/validate_config_ai_rich_first_time_help_v1.py",
            ["--root", str(root)],
            "VALIDATION OK: config-ai-rich-first-time-help-v1",
        )
        run_validator(
            root,
            "tools/validate_project_scope_memory_reset_v1r1.py",
            ["--root", str(root)],
            "VALIDATION OK: project-scope-error-freeze-memory-reset-v1r1",
        )
        run_validator(
            root,
            "tools/validate_shell_active_project_sync_v1.py",
            ["--root", str(root)],
            "VALIDATION OK: shell-active-project-sync-v1",
        )

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
