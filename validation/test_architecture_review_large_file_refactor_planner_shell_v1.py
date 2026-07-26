# project-path: validation/test_architecture_review_large_file_refactor_planner_shell_v1.py
"""Validate the Large File Refactor Planner shell train car."""
from __future__ import annotations

import importlib
import py_compile
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-shell-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
PACKAGE_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture"
PLANNER_ROOT = PACKAGE_ROOT / "large_file_refactor_planner"

CHANGED_SOURCE_FILES = [
    PACKAGE_ROOT / "architecture_review_subtabs.py",
    PLANNER_ROOT / "__init__.py",
    PLANNER_ROOT / "models.py",
    PLANNER_ROOT / "guards.py",
    PLANNER_ROOT / "candidate_discovery.py",
    PLANNER_ROOT / "gui_shell.py",
    Path(__file__).resolve(),
]

ALLOWED_SHORT_FILES = {
    str(PLANNER_ROOT / "__init__.py"),
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _assert_contains(path: Path, fragments: list[str]) -> None:
    text = _read(path)
    missing = [fragment for fragment in fragments if fragment not in text]
    _assert(not missing, f"Missing fragments in {path}: {missing}")


def _line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _line in handle)


def _validate_compile_and_size() -> None:
    for path in CHANGED_SOURCE_FILES:
        _assert(path.exists(), f"Changed file missing: {path}")
        py_compile.compile(str(path), doraise=True)
        lines = _line_count(path)
        _assert(lines <= 500, f"Module exceeds 500 physical lines: {path}={lines}")
        if path.suffix == ".py" and lines < 100 and str(path) not in ALLOWED_SHORT_FILES:
            raise AssertionError(f"Unexpected helper below 100 lines: {path}={lines}")


def _validate_gui_registration() -> None:
    subtabs = PACKAGE_ROOT / "architecture_review_subtabs.py"
    _assert_contains(
        subtabs,
        [
            "Large File Refactor Planner",
            "architecture_review_large_file_refactor_planner_subtab_ear",
            "build_large_file_refactor_planner_page(window)",
            "_activate_subtab(window, 2)",
            "_architecture_review_refactor_planner_page",
        ],
    )
    gui_shell = PLANNER_ROOT / "gui_shell.py"
    _assert_contains(
        gui_shell,
        [
            "1. Candidate file selector",
            "2. Settings panel",
            "3. Analysis evidence panel",
            "4. Proposed split plan panel",
            "5. Preview, validation, and patch panel",
            "Create Patch ZIP",
            "button.setEnabled(False)",
            "No preview files, project split files, or patch payload files were written.",
        ],
    )
    _assert("Apply now" not in _read(gui_shell), "V1 shell must not expose Apply now.")


def _validate_models_and_contracts() -> None:
    models = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models"
    )
    settings = models.PlannerSettings()
    _assert(settings.ideal_physical_lines == 400, "Ideal line default drifted.")
    _assert(settings.maximum_physical_lines == 500, "Maximum line default drifted.")
    _assert(settings.minimum_helper_physical_lines == 100, "Helper minimum drifted.")
    _assert(settings.preserve_public_facade, "Facade preservation default must be on.")
    _assert(settings.generate_missing_docstrings, "Docstring default must be on.")
    _assert(not settings.rewrite_project_imports, "Import rewrite default must be off.")
    _assert(settings.import_migration_preview, "Import preview default must be on.")
    _assert(not settings.use_local_llm, "Local LLM default must be off in shell.")
    _assert(settings.preview_only, "Preview-only default must be on.")
    _assert(
        models.PATCH_ALLOWED_STATE == models.PlannerState.VALIDATION_PASSED,
        "Patch creation must be gated by VALIDATION_PASSED.",
    )


def _validate_no_leak_and_staleness() -> None:
    guards = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.guards"
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir).resolve()
        allowed = root / "allowed"
        outside = root / "outside"
        allowed.mkdir()
        outside.mkdir()
        written = guards.safe_write_text(
            allowed / "note.txt",
            "ok",
            [allowed],
            "validation smoke",
        )
        _assert(written.exists(), "safe_write_text did not write allowed file.")
        try:
            guards.safe_write_text(
                outside / "note.txt",
                "bad",
                [allowed],
                "validation smoke",
            )
        except guards.NoLeakWriteError:
            pass
        else:
            raise AssertionError("No-leak gate allowed an outside-root write.")
        source = allowed / "module.py"
        source.write_text("def public_function():\n    return 1\n", encoding="utf-8")
        snapshot = guards.make_source_snapshot(source)
        guards.assert_source_fresh(source, snapshot)
        source.write_text("def public_function():\n    return 2\n", encoding="utf-8")
        try:
            guards.assert_source_fresh(source, snapshot)
        except guards.StaleSourceError:
            pass
        else:
            raise AssertionError("Staleness gate failed to detect changed source.")


def _validate_candidate_discovery() -> None:
    discovery = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.candidate_discovery"
    )
    large_body = "\n".join(["def public_function():", "    return 1"] * 260)
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir).resolve()
        source = root / "large_module.py"
        source.write_text(large_body, encoding="utf-8")
        support = root / "show_project_to_AI" / "generated.py"
        support.parent.mkdir()
        support.write_text(large_body, encoding="utf-8")
        candidates = discovery.discover_candidates(root, threshold=500)
        paths = {candidate.relative_path for candidate in candidates}
        _assert("large_module.py" in paths, "Fallback scan missed oversized module.")
        _assert(
            "show_project_to_AI/generated.py" not in paths,
            "Generated/support artifact leaked into candidates.",
        )
        candidate = next(item for item in candidates if item.relative_path == "large_module.py")
        _assert(candidate.suggested_action == "Analyze", "Candidate action drifted.")
        _assert(candidate.line_count_physical > 500, "Candidate line count incorrect.")


def main() -> int:
    _validate_compile_and_size()
    _validate_gui_registration()
    _validate_models_and_contracts()
    _validate_no_leak_and_staleness()
    _validate_candidate_discovery()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
