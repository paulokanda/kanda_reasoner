"""Validate Pass 046 collector responsibility overlap helper split."""

from __future__ import annotations

import ast
import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
_STAGED_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))
TARGET = ROOT / _STAGED_PACKAGE_NAME / "reasoner_context_collector" / "collector_responsibility_overlap.py"
HELP_DIR = ROOT / _STAGED_PACKAGE_NAME / "reasoner_context_collector" / "collector_responsibility_overlap_help"
EXPECTED_ROOT_ALL = [
    "build_overlap_hotspots",
    "build_responsibility_overlap_index",
    "build_responsibility_overlap_summary",
]
HELPER_FILES = [
    HELP_DIR / "__init__.py",
    HELP_DIR / "extraction.py",
    HELP_DIR / "scoring.py",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def literal_all(path: Path) -> list[str] | None:
    tree = ast.parse(read_text(path))
    for node in tree.body:
        value = None
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = node.value
                    break
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                value = node.value
        if isinstance(value, (ast.List, ast.Tuple)):
            names: list[str] = []
            for item in value.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    names.append(item.value)
            return names
    return None


def has_star_import(path: Path) -> bool:
    tree = ast.parse(read_text(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    return True
    return False


def line_count(path: Path) -> int:
    return len(read_text(path).splitlines())


def main() -> int:
    errors: list[str] = []
    paths = [TARGET] + HELPER_FILES

    for path in paths:
        if not path.exists():
            errors.append("Missing file: " + str(path.relative_to(ROOT)))
            continue
        py_compile.compile(str(path), doraise=True)
        if has_star_import(path):
            errors.append("Star import found: " + str(path.relative_to(ROOT)))

    if TARGET.exists():
        actual = literal_all(TARGET)
        if actual != EXPECTED_ROOT_ALL:
            errors.append("Root __all__ mismatch: " + repr(actual))
        if line_count(TARGET) >= 500:
            errors.append("Root file still has 500 or more lines: " + str(line_count(TARGET)))

    for helper in HELPER_FILES:
        if helper.exists():
            helper_all = literal_all(helper)
            if helper_all not in ([], None):
                errors.append(
                    "Helper exports should be empty in "
                    + str(helper.relative_to(ROOT))
                    + ": "
                    + repr(helper_all)
                )

    if errors:
        print("FAIL collector_responsibility_overlap helper manifest")
        for error in errors:
            print("  - " + error)
        return 1

    print("PASS collector_responsibility_overlap helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
