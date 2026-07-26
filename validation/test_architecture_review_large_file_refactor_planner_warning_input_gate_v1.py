# project-path: validation/test_architecture_review_large_file_refactor_planner_warning_input_gate_v1.py
"""Validation for the Large File Refactor Planner warning-input gate."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.gui_warning_input_gate as _test_protection_gui_warning_input_gate


import py_compile
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "architecture-review-large-file-refactor-planner-warning-input-gate-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLANNER_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"


def _compile_touched_modules() -> None:
    paths = [
        PLANNER_ROOT / "gui_shell.py",
        PLANNER_ROOT / "gui_warning_input_gate.py",
        PLANNER_ROOT / "candidate_discovery.py",
        Path(__file__),
        PROJECT_ROOT / "tools" / "validate_architecture_review_large_file_refactor_planner_warning_input_gate_v1.py",
    ]
    for path in paths:
        py_compile.compile(str(path), doraise=True)


def _assert_module_sizes() -> None:
    paths = [
        PLANNER_ROOT / "gui_shell.py",
        PLANNER_ROOT / "gui_warning_input_gate.py",
        PLANNER_ROOT / "candidate_discovery.py",
        Path(__file__),
    ]
    for path in paths:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            raise AssertionError(f"module exceeds 500 physical lines: {path} -> {line_count}")


def _write_lines(path: Path, count: int) -> None:
    path.write_text("\n".join(f"# line {index}" for index in range(count)), encoding="utf-8")


def _assert_warning_targets_are_exclusive_input() -> None:
    sys.path.insert(0, str(PROJECT_ROOT))
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.candidate_discovery import discover_candidates
    from kanda_reasoner_app.manage_architecture.large_module_target_queue import parse_module_too_large_findings

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pkg").mkdir()
        large = root / "pkg" / "largest.py"
        medium = root / "pkg" / "medium.py"
        hidden = root / "pkg" / "not_in_warning.py"
        _write_lines(large, 720)
        _write_lines(medium, 540)
        _write_lines(hidden, 900)
        output = "\n".join(
            [
                "[finished] mode=validate exit_code=1",
                "WARNING MODULE_TOO_LARGE pkg/medium.py :: Module has 540 lines; split threshold is 500.",
                "WARNING MODULE_TOO_LARGE pkg/largest.py :: Module has 720 lines; split threshold is 500.",
            ]
        )
        targets = parse_module_too_large_findings(output)
        if [target.path for target in targets] != ["pkg/largest.py", "pkg/medium.py"]:
            raise AssertionError("MODULE_TOO_LARGE targets must be sorted largest-first")
        candidates = discover_candidates(
            root,
            audit_targets=targets,
            scan_fallback=False,
        )
        rel_paths = [candidate.relative_path for candidate in candidates]
        if rel_paths != ["pkg/largest.py", "pkg/medium.py"]:
            raise AssertionError(f"planner must use warning modules only: {rel_paths}")


def _assert_static_gui_contract() -> None:
    shell = (PLANNER_ROOT / "gui_shell.py").read_text(encoding="utf-8")
    helper = (PLANNER_ROOT / "gui_warning_input_gate.py").read_text(encoding="utf-8")
    discovery = (PLANNER_ROOT / "candidate_discovery.py").read_text(encoding="utf-8")
    required_shell = [
        "build_warning_input_gate_section(window)",
        "refresh_warning_input_gate(window)",
        "sync_warning_input_selection(window)",
        "window._large_file_refactor_analyze_button = analyze_btn",
    ]
    for fragment in required_shell:
        if fragment not in shell:
            raise AssertionError(f"missing shell contract fragment: {fragment}")
    if "discover_candidates(" in shell:
        raise AssertionError("gui_shell.py must not run fallback large-file discovery directly")
    required_helper = [
        "parse_module_too_large_findings(output_text)",
        "scan_fallback=False",
        "Run Selected Mode with Validate",
        "WARNING MODULE_TOO_LARGE",
        "Browse Target...",
        "size=",
        "missing_docstrings=",
        "<-",
        "->",
    ]
    for fragment in required_helper:
        if fragment not in helper:
            raise AssertionError(f"missing warning-input helper fragment: {fragment}")
    if '".project_reference"' not in discovery or '"_project_reference"' not in discovery:
        raise AssertionError("candidate discovery must exclude .project_reference and _project_reference")


def main() -> int:
    _compile_touched_modules()
    _assert_module_sizes()
    _assert_warning_targets_are_exclusive_input()
    _assert_static_gui_contract()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
