# project-path: tools/validate_architecture_review_large_file_refactor_behavior_test_presets_v1.py
"""Validate behavior-test preset discovery train."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-behavior-test-presets-v1"
ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/behavior_test_presets.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_behavior_test_presets_v1.py",
    "tools/validate_architecture_review_large_file_refactor_behavior_test_presets_v1.py",
]


def _line_count(path: Path) -> int:
    """Return physical line count."""
    return sum(1 for _ in path.open("r", encoding="utf-8"))


def main() -> int:
    """Run deterministic validation for behavior-test presets."""
    missing = [rel for rel in FILES if not (ROOT / rel).exists()]
    if missing:
        print("Missing expected files: " + ", ".join(missing), file=sys.stderr)
        return 1
    for rel in FILES:
        path = ROOT / rel
        if _line_count(path) > 500:
            print(f"Module too large after patch: {rel}", file=sys.stderr)
            return 1
        py_compile.compile(str(path), doraise=True)
    test_path = ROOT / "validation/test_architecture_review_large_file_refactor_behavior_test_presets_v1.py"
    completed = subprocess.run(
        [sys.executable, str(test_path)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        return completed.returncode
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        build_behavior_test_presets,
        write_behavior_test_presets,
    )
    if build_behavior_test_presets is None or write_behavior_test_presets is None:
        print("Behavior preset exports unavailable", file=sys.stderr)
        return 1
    module_text = (ROOT / FILES[0]).read_text(encoding="utf-8")
    for required in [
        "source_mutation_enabled: bool = False",
        "test_execution_enabled: bool = False",
        "behavior_validation_claimed: bool = False",
        "import_rewrite_apply_enabled: bool = False",
    ]:
        if required not in module_text:
            print("Missing no-write behavior flag: " + required, file=sys.stderr)
            return 1
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
