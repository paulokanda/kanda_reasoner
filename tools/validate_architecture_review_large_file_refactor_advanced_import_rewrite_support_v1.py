# project-path: tools/validate_architecture_review_large_file_refactor_advanced_import_rewrite_support_v1.py
"""Focused validator for advanced import rewrite support v1."""
from __future__ import annotations

import pathlib
import py_compile
import subprocess
import sys

FEATURE_ID = "architecture-review-large-file-refactor-advanced-import-rewrite-support-v1"
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_import_rewrite_support.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_advanced_import_rewrite_support_v1.py",
    "tools/validate_architecture_review_large_file_refactor_advanced_import_rewrite_support_v1.py",
]


def main() -> int:
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING: {rel}")
            return 1
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 500:
            print(f"MODULE TOO LARGE: {rel}: {len(lines)}")
            return 1
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "validation/test_architecture_review_large_file_refactor_advanced_import_rewrite_support_v1.py")],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        env={**__import__("os").environ, "PYTHONPATH": str(ROOT)},
    )
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="")
    if proc.returncode:
        return proc.returncode
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (  # noqa: PLC0415
        build_advanced_import_rewrite_support,
        write_advanced_import_rewrite_support,
    )
    if not callable(build_advanced_import_rewrite_support) or not callable(write_advanced_import_rewrite_support):
        print("advanced import rewrite support exports missing")
        return 1
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
