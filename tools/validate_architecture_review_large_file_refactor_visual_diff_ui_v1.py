# project-path: tools/validate_architecture_review_large_file_refactor_visual_diff_ui_v1.py
"""Validator for architecture-review-large-file-refactor-visual-diff-ui-v1."""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path


FEATURE_ID = "architecture-review-large-file-refactor-visual-diff-ui-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/visual_diff_ui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_visual_diff_ui_v1.py",
    "tools/validate_architecture_review_large_file_refactor_visual_diff_ui_v1.py",
]


def _line_count(relpath: str) -> int:
    return len((PROJECT_ROOT / relpath).read_text(encoding="utf-8").splitlines())


def main() -> int:
    for rel in CHANGED:
        path = PROJECT_ROOT / rel
        if not path.exists():
            print(f"MISSING: {rel}")
            return 1
        if rel.endswith(".py"):
            py_compile.compile(str(path), doraise=True)
        if _line_count(rel) > 500:
            print(f"MODULE TOO LARGE: {rel} {_line_count(rel)}")
            return 1
    init_text = (PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py").read_text(encoding="utf-8")
    for name in ("build_visual_diff_report", "write_visual_diff_artifacts"):
        if name not in init_text:
            print(f"EXPORT MISSING: {name}")
            return 1
    module_text = (PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/visual_diff_ui.py").read_text(encoding="utf-8")
    required_snippets = [
        "source_mutation_enabled: bool = False",
        "apply_enabled: bool = False",
        "import_rewrite_apply_enabled: bool = False",
        "Visual diff preview root must not be inside project source",
    ]
    for snippet in required_snippets:
        if snippet not in module_text:
            print(f"REQUIRED GUARD MISSING: {snippet}")
            return 1
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "validation/test_architecture_review_large_file_refactor_visual_diff_ui_v1.py")],
        cwd=str(PROJECT_ROOT),
        env={**__import__('os').environ, "PYTHONPATH": str(PROJECT_ROOT)},
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
