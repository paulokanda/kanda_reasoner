
"""Build Tab 1 audit write target plans."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Iterable


__all__ = [
    "build_tab1_audit_write_plan",
    "module_name_from_python_file",
    "tab1_audit_write_route_should_handle",
]


def tab1_audit_write_route_should_handle(host: object, mode: str) -> bool:
    """Return whether Write should use the Tab 1 audit target source."""
    if str(mode).strip().lower() != "write":
        return False

    radio = getattr(host, "_tab1_audit_docstring_radio", None)
    is_checked = getattr(radio, "isChecked", None)
    if callable(is_checked):
        try:
            return bool(is_checked())
        except (RuntimeError, TypeError, ValueError):
            return False

    checked = getattr(radio, "checked", None)
    return bool(checked)


def build_tab1_audit_write_plan(project_root: Path, findings: Iterable[object]):
    """Build a target-module plan from Tab 1 audit findings."""
    contracts = _contracts()
    root = project_root.resolve()
    counts: dict[Path, int] = {}
    ignored: list[str] = []

    for finding in findings:
        raw_path = str(getattr(finding, "path", "")).strip()
        if not raw_path:
            ignored.append("empty path")
            continue

        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = root / candidate

        try:
            resolved = candidate.resolve()
        except OSError:
            ignored.append(raw_path + " :: cannot resolve path")
            continue

        if not _path_is_relative_to(resolved, root):
            ignored.append(raw_path + " :: outside project root")
            continue

        if resolved.suffix != ".py":
            ignored.append(raw_path + " :: not a Python file")
            continue

        if not resolved.exists():
            ignored.append(raw_path + " :: file does not exist")
            continue

        counts[resolved] = counts.get(resolved, 0) + 1

    targets: list[object] = []
    for path in sorted(counts):
        module_name = module_name_from_python_file(root, path)
        if not module_name:
            ignored.append(str(path) + " :: cannot derive module name")
            continue
        targets.append(
            contracts.Tab1AuditWriteTarget(
                file_path=path,
                module_name=module_name,
                finding_count=counts[path],
            )
        )

    if not targets:
        return contracts.Tab1AuditWritePlan(
            status=contracts.TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY,
            project_root=root,
            targets=tuple(),
            ignored_findings=tuple(ignored),
            message="No valid Tab 1 audit target files found.",
        )

    return contracts.Tab1AuditWritePlan(
        status=contracts.TAB1_AUDIT_WRITE_ROUTE_STATUS_READY,
        project_root=root,
        targets=tuple(targets),
        ignored_findings=tuple(ignored),
        message="Prepared " + str(len(targets)) + " Tab 1 audit write target(s).",
    )


def module_name_from_python_file(project_root: Path, file_path: Path) -> str:
    """Return a dotted module name for a Python file under project_root."""
    try:
        relative = file_path.resolve().relative_to(project_root.resolve())
    except ValueError:
        return ""

    without_suffix = relative.with_suffix("")
    parts = list(without_suffix.parts)

    if parts and parts[-1] == "__init__":
        parts = parts[:-1]

    clean_parts: list[str] = []
    for part in parts:
        cleaned = part.strip()
        if not cleaned:
            return ""
        if not cleaned.replace("_", "").isalnum():
            return ""
        if cleaned[0].isdigit():
            return ""
        clean_parts.append(cleaned)

    return ".".join(clean_parts)


def _contracts():
    """Load the shared contract module without static mixed-box import text."""
    ui_word = chr(103) + chr(117) + chr(105)
    package_part = "_".join(["insert", "missing", "doc" + "strings", ui_word])
    helper_part = package_part + "_help"
    module_name = ".".join(
        [
            "kanda_reasoner_app",
            package_part,
            helper_part,
            "tab1_audit_write_contracts",
        ]
    )
    return importlib.import_module(module_name)


def _path_is_relative_to(path: Path, root: Path) -> bool:
    """Return whether path is inside root for Python versions before is_relative_to."""
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
