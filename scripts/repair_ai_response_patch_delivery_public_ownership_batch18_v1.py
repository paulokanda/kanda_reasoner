"""Repair duplicate public ownership in validate_ai_response_patch_delivery helpers.

This script is intentionally AST/static only. Earlier Batch 18 install validation
executed target modules after editing them, which can fail for script modules that
expect normal import context. This repaired version validates ownership with AST
and py_compile only.
"""

from __future__ import annotations

import argparse
import ast
import py_compile
from dataclasses import dataclass
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch18-public-ownership-repair-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

FACADE_PATH = Path("scripts/validate_ai_response_patch_delivery.py")
HELPER_PATHS = (
    Path("scripts/validate_ai_response_patch_delivery_contract.py"),
    Path("scripts/validate_ai_response_patch_delivery_audit_runner.py"),
    Path("scripts/validate_ai_response_patch_delivery_text_helpers.py"),
)
FACADE_PUBLIC_NAMES = (
    "ResponseValidationError",
    "validate_response_text",
    "validate_zip_member_names",
)
HELPER_IMPORT_TARGETS = (
    "scripts.validate_ai_response_patch_delivery_contract",
    "scripts.validate_ai_response_patch_delivery_audit_runner",
    "scripts.validate_ai_response_patch_delivery_text_helpers",
)

__all__ = ["main"]


@dataclass(frozen=True)
class FileEdit:
    """A planned or applied file edit."""

    relative_path: Path
    changed: bool
    reason: str


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when a repair precondition fails."""

    if not condition:
        raise AssertionError(message)


def _parse_file(path: Path) -> ast.Module:
    """Parse a Python file."""

    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _module_docstring_end_line(tree: ast.Module) -> int:
    """Return the one-based end line of the module docstring, or zero."""

    if tree.body and isinstance(tree.body[0], ast.Expr):
        value = tree.body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            return int(getattr(tree.body[0], "end_lineno", tree.body[0].lineno))
    return 0


def _future_import_end_line(tree: ast.Module) -> int:
    """Return the one-based end line after module docstring and future imports."""

    line = _module_docstring_end_line(tree)
    for node in tree.body:
        if node.lineno <= line:
            continue
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            line = int(getattr(node, "end_lineno", node.lineno))
            continue
        break
    return line


def _all_assignment_node(tree: ast.Module) -> ast.Assign | ast.AnnAssign | None:
    """Return the top-level __all__ assignment node, if present."""

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return node
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                return node
    return None


def _literal_all_value(path: Path) -> object:
    """Return literal top-level __all__ value, or None when absent/non-literal."""

    tree = _parse_file(path)
    node = _all_assignment_node(tree)
    if node is None:
        return None
    value_node = node.value if isinstance(node, ast.Assign) else node.value
    if value_node is None:
        return None
    try:
        return ast.literal_eval(value_node)
    except (SyntaxError, ValueError):
        return None


def _assignment_lines(assignment_text: str) -> list[str]:
    """Return assignment lines for file replacement."""

    return assignment_text.splitlines()


def _replace_or_insert_all(path: Path, assignment_text: str, *, write: bool) -> FileEdit:
    """Replace an existing __all__ assignment or insert one after future imports."""

    relative_path = path.relative_to(PROJECT_ROOT)
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    tree = _parse_file(path)
    node = _all_assignment_node(tree)
    replacement = _assignment_lines(assignment_text)
    if node is not None:
        start = node.lineno - 1
        end = int(getattr(node, "end_lineno", node.lineno))
        new_lines = lines[:start] + replacement + lines[end:]
    else:
        insert_at = _future_import_end_line(tree)
        new_lines = lines[:insert_at] + ["", *replacement] + lines[insert_at:]
    new_text = "\n".join(new_lines) + ("\n" if original.endswith("\n") else "")
    changed = new_text != original
    if changed and write:
        path.write_text(new_text, encoding="utf-8")
    reason = "updated __all__" if changed else "already correct"
    return FileEdit(relative_path=relative_path, changed=changed, reason=reason)


def _contains_star_import_of_helpers(source: str) -> list[str]:
    """Return helper module names imported with star-import syntax."""

    tree = ast.parse(source)
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in HELPER_IMPORT_TARGETS:
            if any(alias.name == "*" for alias in node.names):
                found.append(str(node.module))
    return found


def validate_no_star_imports() -> None:
    """Require that no active source depends on helper __all__ via star imports."""

    offenders: list[str] = []
    scan_roots = (PROJECT_ROOT / "scripts", PROJECT_ROOT / "tests")
    for root in scan_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            try:
                source = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            hits = _contains_star_import_of_helpers(source)
            if hits:
                offenders.append(f"{path.relative_to(PROJECT_ROOT)} -> {', '.join(hits)}")
    require(not offenders, "star imports depend on helper __all__: " + "; ".join(offenders))


def validate_required_files() -> None:
    """Require facade and helper files to exist before editing."""

    missing = [str(path) for path in (FACADE_PATH,) + HELPER_PATHS if not (PROJECT_ROOT / path).exists()]
    require(not missing, "missing required file(s): " + ", ".join(missing))


def apply_repair(*, write: bool) -> list[FileEdit]:
    """Apply or preview the public ownership repair."""

    validate_required_files()
    validate_no_star_imports()
    edits: list[FileEdit] = []
    facade_all = "__all__ = [\"ResponseValidationError\", \"validate_response_text\", \"validate_zip_member_names\"]"
    helper_all = "__all__ = []  # Implementation-only module; public facade owns exported validator symbols."
    edits.append(_replace_or_insert_all(PROJECT_ROOT / FACADE_PATH, facade_all, write=write))
    for rel_path in HELPER_PATHS:
        edits.append(_replace_or_insert_all(PROJECT_ROOT / rel_path, helper_all, write=write))
    return edits


def validate_after_repair() -> None:
    """Validate the repaired ownership contract without executing target modules."""

    validate_required_files()
    for rel_path in (FACADE_PATH,) + HELPER_PATHS:
        py_compile.compile(str(PROJECT_ROOT / rel_path), doraise=True)
    require(
        tuple(_literal_all_value(PROJECT_ROOT / FACADE_PATH) or ()) == FACADE_PUBLIC_NAMES,
        "facade __all__ mismatch",
    )
    for rel_path in HELPER_PATHS:
        require(
            _literal_all_value(PROJECT_ROOT / rel_path) == [],
            f"helper __all__ not implementation-only: {rel_path}",
        )


def main(argv: list[str] | None = None) -> int:
    """Run the Batch 18 repair."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate and preview without writing")
    args = parser.parse_args(argv)
    edits = apply_repair(write=not args.check)
    validate_after_repair()
    mode = "CHECK" if args.check else "REPAIR"
    print(f"{mode} OK: {FEATURE_ID}")
    for edit in edits:
        state = "changed" if edit.changed else "unchanged"
        print(f" - {state}: {edit.relative_path} ({edit.reason})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
