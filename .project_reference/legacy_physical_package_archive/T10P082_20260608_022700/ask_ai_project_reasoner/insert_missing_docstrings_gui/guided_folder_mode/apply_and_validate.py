
"""Apply and post-write validation primitives for Safe Mode."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import py_compile
import shutil

from .apply_gate import FolderApplyPlan, ApprovedDocstringPatch


APPLY_VALIDATION_STATUS_APPLIED = "applied"
APPLY_VALIDATION_STATUS_EMPTY = "empty"
APPLY_VALIDATION_STATUS_FAILED_ROLLED_BACK = "failed_rolled_back"


@dataclass(frozen=True)
class ApplyValidationResult:
    """Store the result of a Safe Mode apply-and-validate operation."""

    success: bool
    status: str
    changed_files: tuple[str, ...] = ()
    validated_files: tuple[str, ...] = ()
    error: str = ""
    rollback_performed: bool = False

    def applied_cleanly(self) -> bool:
        """Return True when patches were applied and validated."""
        return self.success and self.status in {
            APPLY_VALIDATION_STATUS_APPLIED,
            APPLY_VALIDATION_STATUS_EMPTY,
        }


def apply_plan_with_validation(
    project_root: str | Path,
    plan: FolderApplyPlan,
    backup_root: str | Path | None = None,
) -> ApplyValidationResult:
    """Apply approved docstring patches and validate changed files.

    The function writes source files only after the Safe Mode apply gate has
    produced a plan. If any write or validation step fails, original file
    contents are restored from memory and, optionally, copied to backup_root.
    """
    root = Path(project_root).resolve()
    patches = tuple(plan.patches)

    if not patches:
        return ApplyValidationResult(
            success=True,
            status=APPLY_VALIDATION_STATUS_EMPTY,
            changed_files=(),
            validated_files=(),
        )

    grouped = _group_patches_by_file(patches)
    originals: dict[str, str] = {}
    changed_files: list[str] = []

    try:
        for relative_file in sorted(grouped):
            file_path = (root / relative_file).resolve()
            _ensure_inside_root(root, file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Patch target file does not exist: {relative_file}")

            original_text = file_path.read_text(encoding="utf-8")
            originals[relative_file] = original_text

            if backup_root is not None:
                _backup_file(root, file_path, Path(backup_root))

            patched_text = _apply_patches_to_text(original_text, grouped[relative_file])
            file_path.write_text(patched_text, encoding="utf-8", newline="\n")
            changed_files.append(relative_file)

        for relative_file in sorted(grouped):
            file_path = root / relative_file
            _validate_python_file(file_path)
            _validate_patch_docstrings(file_path, grouped[relative_file])

    except Exception as exc:
        for relative_file, original_text in originals.items():
            (root / relative_file).write_text(original_text, encoding="utf-8", newline="\n")

        return ApplyValidationResult(
            success=False,
            status=APPLY_VALIDATION_STATUS_FAILED_ROLLED_BACK,
            changed_files=tuple(sorted(changed_files)),
            validated_files=(),
            error=str(exc),
            rollback_performed=True,
        )

    return ApplyValidationResult(
        success=True,
        status=APPLY_VALIDATION_STATUS_APPLIED,
        changed_files=tuple(sorted(changed_files)),
        validated_files=tuple(sorted(grouped)),
    )


def validate_changed_files(
    project_root: str | Path,
    plan: FolderApplyPlan,
) -> ApplyValidationResult:
    """Validate files referenced by an apply plan without writing them."""
    root = Path(project_root).resolve()
    patches = tuple(plan.patches)

    if not patches:
        return ApplyValidationResult(
            success=True,
            status=APPLY_VALIDATION_STATUS_EMPTY,
            changed_files=(),
            validated_files=(),
        )

    grouped = _group_patches_by_file(patches)
    try:
        for relative_file, file_patches in grouped.items():
            file_path = (root / relative_file).resolve()
            _ensure_inside_root(root, file_path)
            _validate_python_file(file_path)
            _validate_patch_docstrings(file_path, file_patches)
    except Exception as exc:
        return ApplyValidationResult(
            success=False,
            status=APPLY_VALIDATION_STATUS_FAILED_ROLLED_BACK,
            error=str(exc),
            rollback_performed=False,
        )

    return ApplyValidationResult(
        success=True,
        status=APPLY_VALIDATION_STATUS_APPLIED,
        changed_files=tuple(sorted(grouped)),
        validated_files=tuple(sorted(grouped)),
    )


def _apply_patches_to_text(
    text: str,
    patches: tuple[ApprovedDocstringPatch, ...],
) -> str:
    lines = text.splitlines()

    for patch in sorted(patches, key=lambda item: item.insert_line, reverse=True):
        insert_index = patch.insert_line - 1
        if insert_index < 0 or insert_index > len(lines):
            raise ValueError(f"Invalid insert line for {patch.target_name}: {patch.insert_line}")

        indent = _indent_for_insert(lines, insert_index)
        rendered = _render_docstring_for_insert(patch.final_docstring, indent)
        rendered_lines = rendered.splitlines()
        lines[insert_index:insert_index] = rendered_lines

    return "\n".join(lines) + "\n"


def _indent_for_insert(lines: list[str], insert_index: int) -> str:
    if insert_index < len(lines):
        line = lines[insert_index]
    elif lines:
        line = lines[-1]
    else:
        line = ""

    return line[: len(line) - len(line.lstrip(" "))]


def _render_docstring_for_insert(docstring: str, indent: str) -> str:
    stripped = docstring.strip()
    if not stripped:
        raise ValueError("Cannot render empty docstring.")

    return "\n".join(indent + line if line else indent for line in stripped.splitlines())


def _group_patches_by_file(
    patches: tuple[ApprovedDocstringPatch, ...],
) -> dict[str, tuple[ApprovedDocstringPatch, ...]]:
    grouped: dict[str, list[ApprovedDocstringPatch]] = {}
    for patch in patches:
        grouped.setdefault(patch.file_path, []).append(patch)

    return {
        file_path: tuple(sorted(file_patches, key=lambda item: item.insert_line))
        for file_path, file_patches in grouped.items()
    }


def _validate_python_file(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    ast.parse(source, filename=str(path))
    py_compile.compile(str(path), doraise=True)


def _validate_patch_docstrings(
    path: Path,
    patches: tuple[ApprovedDocstringPatch, ...],
) -> None:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    for patch in patches:
        if patch.target_kind == "module":
            if ast.get_docstring(tree) is None:
                raise ValueError(f"Module docstring missing after apply: {patch.file_path}")
            continue

        matching = _find_matching_nodes(tree, patch)
        if not matching:
            raise ValueError(
                f"Target not found after apply: {patch.target_kind} {patch.target_name}"
            )

        if not any(ast.get_docstring(node) is not None for node in matching):
            raise ValueError(
                f"Docstring missing after apply: {patch.target_kind} {patch.target_name}"
            )


def _find_matching_nodes(
    tree: ast.Module,
    patch: ApprovedDocstringPatch,
) -> list[ast.AST]:
    matching: list[ast.AST] = []

    for node in ast.walk(tree):
        if patch.target_kind == "class" and isinstance(node, ast.ClassDef):
            if node.name == patch.target_name:
                matching.append(node)
            continue

        if patch.target_kind in {"function", "method"} and isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            if node.name == patch.target_name and not _is_overload_stub(node):
                matching.append(node)

    return matching


def _is_overload_stub(node: ast.AST) -> bool:
    decorators = getattr(node, "decorator_list", [])
    for decorator in decorators:
        if isinstance(decorator, ast.Name) and decorator.id == "overload":
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == "overload":
            return True
    return False


def _ensure_inside_root(root: Path, path: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path is outside project root: {path}") from exc


def _backup_file(root: Path, source: Path, backup_root: Path) -> None:
    relative = source.relative_to(root)
    target = backup_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
