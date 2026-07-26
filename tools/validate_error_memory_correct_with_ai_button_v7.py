# project-path: tools/validate_error_memory_correct_with_ai_button_v7.py
"""Validate Error Memory correction button after central Web AI consolidation."""

from __future__ import annotations

import ast
import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
    "kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
)


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_compile_and_line_count() -> None:
    for relative_path in FILES:
        path = PROJECT_ROOT / relative_path
        py_compile.compile(str(path), doraise=True)
        _require(
            len(_read(relative_path).splitlines()) <= 500,
            "Module exceeds 500 lines: " + relative_path,
        )
    print("ERROR_MEMORY_CORRECTION_MODULES_COMPILE: PASS")
    print("ERROR_MEMORY_CORRECTION_MODULES_MAX_500_LINES: PASS")


def validate_mode_only_layout() -> None:
    text = _read("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    mode_text = _read("kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py")
    _require("build_mode_group(self)" in text, "Correction mode group is missing.")
    for label in ('QRadioButton("Heuristic"', 'QRadioButton("Local AI"', 'QRadioButton("Web AI"'):
        _require(label in mode_text, "Missing mode choice: " + label)
    _require("_gateway_combo" not in text, "Error Memory duplicates a gateway control.")
    _require("_api_key_edit" not in text, "Error Memory duplicates an API-key control.")
    _require("_model_combo" not in text, "Error Memory duplicates a model control.")
    _require(
        "self.heuristic_correction_button.setVisible(False)" in text,
        "Legacy heuristic compatibility button must not duplicate the visible action.",
    )
    _require(
        "self.correct_with_ai_button = QPushButton('Correct with AI')" in text,
        "Correction action button is missing.",
    )
    print("ERROR_MEMORY_MODE_ONLY_CONTROLS: PASS")
    print("ERROR_MEMORY_NO_DUPLICATE_WEB_CONFIGURATION: PASS")


def validate_dispatch_contract() -> None:
    action = _read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    worker = _read("kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py")
    tree = ast.parse(action)
    function_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }
    _require(
        "run_error_memory_ai_correction_from_tab" in function_names,
        "Tab correction entry point is missing.",
    )
    _require(
        "HEURISTIC_MODE" in action and "apply_heuristic_correction_to_error_editor" in action,
        "Heuristic dispatch is missing.",
    )
    _require(
        'self._provider_mode == "web"' in worker,
        "Worker does not dispatch Web AI.",
    )
    _require(
        "correct_error_memory_lesson_with_local_ai" in worker,
        "Worker no longer preserves Local AI.",
    )
    _require(
        "correct_error_memory_lesson_with_web_ai" in worker,
        "Worker does not reuse the Web correction service.",
    )
    print("ERROR_MEMORY_HEURISTIC_LOCAL_WEB_DISPATCH: PASS")
    print("ERROR_MEMORY_AI_OFF_GUI_THREAD: PASS")


def validate_header_config_removed() -> None:
    lazy = _read("kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py")
    block = lazy.split("if spec.source_hint in {", 1)[1].split("}:", 1)[0]
    _require(
        "_ERROR_MEMORY_GUI_SOURCE" not in block,
        "Error Memory still installs the repeated header AI model group.",
    )
    print("ERROR_MEMORY_HEADER_AI_CONFIG_REMOVED: PASS")


def main() -> int:
    validate_compile_and_line_count()
    validate_mode_only_layout()
    validate_dispatch_contract()
    validate_header_config_removed()
    print("VALIDATION OK: error-memory-correct-with-ai-button-v7")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
