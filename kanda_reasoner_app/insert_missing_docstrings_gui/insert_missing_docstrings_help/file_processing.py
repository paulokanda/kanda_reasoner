# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Per-file processing and batch change collection
# EXPORTS       : load_manifest, collect_changes
# DEPENDS ON    : project_exclusion_rules.py, source_io.py, insertion_collector.py, insertion_formatting.py, ast_safety.py, reporting.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Per-file processing and batch change collection."""

from __future__ import annotations

import logging

import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from .ast_safety import validate_docstring_only_change
from .insertion_collector import collect_missing_docstring_insertions
from .insertion_formatting import apply_insertions_to_text
from .project_exclusion_rules import (
    iter_selected_python_files,
    load_project_exclusion_rules,
    normalize_rel_path,
    should_exclude_path,
)
from .reporting import build_report_row as _report_row
from .source_io import parse_source

__all__ = [
    "load_manifest",
    "collect_changes",
]

def load_manifest(root: Path) -> dict | None:
    """Load  manifest.
    
    Parameters
    ----------
    root : Path
        TODO: describe root.
    
    Returns
    -------
    dict | None
        TODO: describe the return value.
    """
    
    manifest_path = root / "architecture_manifest.json"
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        logging.exception("Boundary failure in load_manifest")
        return None

_HEADER_SCAN_LIMIT = 30
_MANAGED_FILE_ADDRESS_PREFIX = "# project-path: "

@dataclass
class _FileAddressHeaderResult:
    """Describe one file-address header audit or edit result."""

    action: str
    expected_line: str
    old_line: str = ""
    line_number: int | None = None
    reason: str = ""


def _relative_project_path_for_header(root: Path, path: Path) -> str:
    """Return a project-relative POSIX path, or an empty string if outside root."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return ""


def _expected_file_address_line(root: Path, path: Path) -> str:
    """Return the managed file-address header line for one source file."""
    rel_path = _relative_project_path_for_header(root, path)
    if not rel_path:
        return ""
    return _MANAGED_FILE_ADDRESS_PREFIX + rel_path


def _looks_like_legacy_file_address_header(line: str) -> bool:
    """Return whether a comment looks like an old bare file-address header."""
    stripped = line.strip()
    if not stripped.startswith("#"):
        return False
    payload = stripped[1:].strip()
    lowered = payload.lower()
    if not payload or lowered.startswith("project-path:"):
        return False
    if " " in payload or "\t" in payload:
        return False
    if not lowered.endswith(".py"):
        return False
    return "/" in payload or "\\" in payload


def _audit_file_address_header(
    text: str,
    expected_line: str,
) -> _FileAddressHeaderResult:
    """Audit the top header zone for managed or legacy file-address comments."""
    if not expected_line:
        return _FileAddressHeaderResult(
            action="skipped_outside_project_root",
            expected_line="",
            reason="file is outside the selected project root",
        )

    for index, line in enumerate(text.splitlines()[:_HEADER_SCAN_LIMIT]):
        stripped = line.strip()
        line_number = index + 1
        if stripped == expected_line:
            return _FileAddressHeaderResult(
                action="exact",
                expected_line=expected_line,
                old_line=stripped,
                line_number=line_number,
                reason="managed project-path header already present",
            )
        if stripped.startswith(_MANAGED_FILE_ADDRESS_PREFIX):
            return _FileAddressHeaderResult(
                action="stale_managed",
                expected_line=expected_line,
                old_line=stripped,
                line_number=line_number,
                reason="stale managed project-path header will be updated",
            )
        if _looks_like_legacy_file_address_header(stripped):
            return _FileAddressHeaderResult(
                action="legacy_possible",
                expected_line=expected_line,
                old_line=stripped,
                line_number=line_number,
                reason="legacy possible file-address header found; not duplicated",
            )

    return _FileAddressHeaderResult(
        action="absent",
        expected_line=expected_line,
        reason="managed project-path header missing",
    )


def _is_coding_comment(line: str) -> bool:
    """Return whether a line is a Python coding declaration."""
    stripped = line.lstrip().lower()
    return stripped.startswith("#") and "coding" in stripped


def _is_legal_header_comment(line: str) -> bool:
    """Return whether a comment should remain above the project-path header."""
    stripped = line.strip().lower()
    if not stripped.startswith("#"):
        return False
    return (
        stripped.startswith("# spdx-")
        or stripped.startswith("# copyright")
        or stripped.startswith("# license")
    )


def _file_address_insert_index(lines: list[str]) -> int:
    """Return where to insert a managed project-path header."""
    index = 0
    if index < len(lines) and lines[index].startswith("#!"):
        index += 1

    if index < len(lines) and _is_coding_comment(lines[index]):
        index += 1

    while index < len(lines):
        line = lines[index]
        if line.strip() == "":
            index += 1
            continue
        if _is_legal_header_comment(line):
            index += 1
            continue
        break

    return index


def _compose_lines_with_original_final_newline(
    lines: list[str],
    original_text: str,
) -> str:
    """Join lines and preserve a final newline when the source had one."""
    desired = "\n".join(lines)
    if original_text.endswith("\n") or original_text == "":
        desired += "\n"
    return desired


def _apply_file_address_header(
    text: str,
    root: Path,
    path: Path,
) -> tuple[str, _FileAddressHeaderResult]:
    """Insert or update a managed project-path header when safe."""
    expected_line = _expected_file_address_line(root, path)
    audit = _audit_file_address_header(text, expected_line)

    if audit.action in {"exact", "legacy_possible", "skipped_outside_project_root"}:
        return text, audit

    lines = text.splitlines()
    if audit.action == "stale_managed" and audit.line_number is not None:
        lines[audit.line_number - 1] = expected_line
        desired = _compose_lines_with_original_final_newline(lines, text)
        return desired, _FileAddressHeaderResult(
            action="updated_stale_managed",
            expected_line=expected_line,
            old_line=audit.old_line,
            line_number=audit.line_number,
            reason="stale managed project-path header updated",
        )

    insert_index = _file_address_insert_index(lines)
    lines.insert(insert_index, expected_line)
    desired = _compose_lines_with_original_final_newline(lines, text)
    return desired, _FileAddressHeaderResult(
        action="inserted",
        expected_line=expected_line,
        line_number=insert_index + 1,
        reason="managed project-path header inserted",
    )

def _process_docstring_file_candidate(
    root: Path,
    path: Path,
    *,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    include_init: bool,
    insert_file_address_at_top: bool = False,
    include_relaxed_paths: bool,
    include_tests: bool,
    manifest: dict | None,
    generator: "AIDocstringGenerator | None",
    project_exclusion_rules: dict[str, list[str]],
) -> tuple[Path, tuple[str, bool] | None, list[str], list[dict[str, object]]]:
    """Process one file candidate and return a safe change plus report rows."""
    skipped_messages: list[str] = []
    report_rows: list[dict[str, object]] = []

    rel_path = normalize_rel_path(root, path)
    if should_exclude_path(
        rel_path,
        path.name,
        include_relaxed_paths=include_relaxed_paths,
        include_tests=include_tests,
        project_exclusion_rules=project_exclusion_rules,
    ):
        report_rows.append(
            _report_row(
                root,
                path,
                target_kind="file",
                target_name=path.name,
                line=None,
                action="skipped",
                reason="excluded by path or test/relaxed rules",
            )
        )
        return path, None, skipped_messages, report_rows

    insertions, skipped, current, had_bom, file_report_rows = (
        collect_missing_docstring_insertions(
            root,
            path,
            include_module=include_module,
            include_classes=include_classes,
            include_functions=include_functions,
            include_init=include_init,
            manifest=manifest,
            generator=generator,
        )
    )

    skipped_messages.extend(skipped)
    report_rows.extend(file_report_rows)

    desired = current
    if insertions:
        desired = apply_insertions_to_text(current, insertions)

    file_address_inserted = False
    if insert_file_address_at_top:
        desired, file_address_result = _apply_file_address_header(
            desired,
            root,
            path,
        )
        file_address_inserted = file_address_result.action in {
            "inserted",
            "updated_stale_managed",
        }

        report_action = file_address_result.action
        if report_action == "exact":
            report_action = "existing"
        elif report_action in {
            "legacy_possible",
            "skipped_outside_project_root",
        }:
            report_action = "skipped"
        elif report_action == "updated_stale_managed":
            report_action = "updated"

        target_name = file_address_result.expected_line or path.name
        if file_address_result.old_line:
            target_name = file_address_result.old_line

        report_rows.append(
            _report_row(
                root,
                path,
                target_kind="file_address",
                target_name=target_name,
                line=file_address_result.line_number,
                insert_line=(
                    file_address_result.line_number
                    if file_address_result.action in {
                        "inserted",
                        "updated_stale_managed",
                    }
                    else None
                ),
                action=report_action,
                reason=file_address_result.reason,
                source="file_address_header",
                confidence="high",
            )
        )

    if not insertions and not file_address_inserted:
        return path, None, skipped_messages, report_rows

    if desired == current:
        return path, None, skipped_messages, report_rows

    try:
        parse_source(desired, path)
    except SyntaxError as exc:
        skipped_messages.append(
            f"{path}: generated insertion would create invalid syntax; skipped ({exc})"
        )
        report_rows.append(
            _report_row(
                root,
                path,
                target_kind="file",
                target_name=path.name,
                line=None,
                action="failed",
                reason=f"generated insertion would create invalid syntax: {exc}",
            )
        )
        return path, None, skipped_messages, report_rows

    ast_guard_error = validate_docstring_only_change(current, desired, path)
    if ast_guard_error:
        skipped_messages.append(f"{path}: {ast_guard_error}; skipped")
        report_rows.append(
            _report_row(
                root,
                path,
                target_kind="file",
                target_name=path.name,
                line=None,
                action="failed",
                reason=ast_guard_error,
            )
        )
        return path, None, skipped_messages, report_rows

    return path, (desired, had_bom), skipped_messages, report_rows

def collect_changes(
    root: Path,
    *,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    include_init: bool,
    include_relaxed_paths: bool,
    include_tests: bool,
    insert_file_address_at_top: bool = False,
    target_module: str | None = None,
    target_package: str | None = None,
    generator: "AIDocstringGenerator | None" = None,
    workers: int = 1,
) -> tuple[
    dict[Path, tuple[str, bool]],
    list[str],
    list[dict[str, object]],
    dict[str, object],
]:
    """Collect safe docstring changes across selected files."""
    changes: dict[Path, tuple[str, bool]] = {}
    skipped_messages: list[str] = []
    report_rows: list[dict[str, object]] = []
    manifest = load_manifest(root)
    project_exclusion_rules = load_project_exclusion_rules(root)

    paths = list(
        iter_selected_python_files(
            root,
            target_module=target_module,
            target_package=target_package,
            project_exclusion_rules=project_exclusion_rules,
        )
    )

    requested_workers = max(1, workers)
    parallel_enabled = requested_workers > 1 and generator is None and len(paths) > 1
    telemetry: dict[str, object] = {
        "files_selected": len(paths),
        "workers_requested": requested_workers,
        "workers_used": requested_workers if parallel_enabled else 1,
        "parallel_file_processing_enabled": parallel_enabled,
        "parallel_reason": (
            "enabled"
            if parallel_enabled
            else (
                "disabled because AI generator is active"
                if generator is not None and requested_workers > 1
                else "disabled"
            )
        ),
    }

    def _process(path: Path) -> tuple[
        Path,
        tuple[str, bool] | None,
        list[str],
        list[dict[str, object]],
    ]:
        """Handle process.
        
        Parameters
        ----------
        path : Path
            TODO: describe path.
        
        Returns
        -------
        tuple[Path, tuple[str, bool] | None, list[str], list[dict[str, object]]]
            TODO: describe the return value.
        """
        
        return _process_docstring_file_candidate(
            root,
            path,
            include_module=include_module,
            include_classes=include_classes,
            include_functions=include_functions,
            include_init=include_init,
            insert_file_address_at_top=insert_file_address_at_top,
            include_relaxed_paths=include_relaxed_paths,
            include_tests=include_tests,
            manifest=manifest,
            generator=generator,
            project_exclusion_rules=project_exclusion_rules,
        )

    if parallel_enabled:
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=requested_workers) as pool:
            futures = {pool.submit(_process, path): path for path in paths}
            for future in as_completed(futures):
                path, changed, skipped, rows = future.result()
                with lock:
                    skipped_messages.extend(skipped)
                    report_rows.extend(rows)
                    if changed is not None:
                        changes[path] = changed
    else:
        for path in paths:
            path, changed, skipped, rows = _process(path)
            skipped_messages.extend(skipped)
            report_rows.extend(rows)
            if changed is not None:
                changes[path] = changed

    return changes, skipped_messages, report_rows, telemetry


def _stop_requested_value(stop_requested) -> bool:
    """Return whether a cooperative stop callback asks to stop."""
    if stop_requested is None:
        return False
    try:
        return bool(stop_requested())
    except Exception:
        logging.exception("Boundary failure while reading stop callback")
        return False


def _emit_progress(progress_callback, *, total: int, audited: int) -> None:
    """Emit a best-effort file-audit progress update."""
    if progress_callback is None:
        return
    remaining = max(0, int(total) - int(audited))
    try:
        progress_callback({
            "total_files_to_audit": int(total),
            "files_audited": int(audited),
            "files_to_go": remaining,
        })
    except Exception:
        logging.exception("Boundary failure while emitting progress callback")


def collect_changes(
    root: Path,
    *,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    include_init: bool,
    include_relaxed_paths: bool,
    include_tests: bool,
    insert_file_address_at_top: bool = False,
    target_module: str | None = None,
    target_package: str | None = None,
    generator: "AIDocstringGenerator | None" = None,
    workers: int = 1,
    stop_requested=None,
    progress_callback=None,
) -> tuple[
    dict[Path, tuple[str, bool]],
    list[str],
    list[dict[str, object]],
    dict[str, object],
]:
    """Collect safe docstring changes with cooperative stop support."""
    changes: dict[Path, tuple[str, bool]] = {}
    skipped_messages: list[str] = []
    report_rows: list[dict[str, object]] = []
    manifest = load_manifest(root)
    project_exclusion_rules = load_project_exclusion_rules(root)

    paths = list(
        iter_selected_python_files(
            root,
            target_module=target_module,
            target_package=target_package,
            project_exclusion_rules=project_exclusion_rules,
        )
    )

    requested_workers = max(1, workers)
    parallel_enabled = requested_workers > 1 and generator is None and len(paths) > 1
    telemetry: dict[str, object] = {
        "files_selected": len(paths),
        "workers_requested": requested_workers,
        "workers_used": requested_workers if parallel_enabled else 1,
        "parallel_file_processing_enabled": parallel_enabled,
        "parallel_reason": (
            "enabled"
            if parallel_enabled
            else (
                "disabled because AI generator is active"
                if generator is not None and requested_workers > 1
                else "disabled"
            )
        ),
        "stopped_by_user": False,
        "files_processed_before_stop": 0,
    }

    def _process(path: Path) -> tuple[
        Path,
        tuple[str, bool] | None,
        list[str],
        list[dict[str, object]],
    ]:
        """Process one file candidate."""
        return _process_docstring_file_candidate(
            root,
            path,
            include_module=include_module,
            include_classes=include_classes,
            include_functions=include_functions,
            include_init=include_init,
            insert_file_address_at_top=insert_file_address_at_top,
            include_relaxed_paths=include_relaxed_paths,
            include_tests=include_tests,
            manifest=manifest,
            generator=generator,
            project_exclusion_rules=project_exclusion_rules,
        )

    _emit_progress(progress_callback, total=len(paths), audited=0)

    if _stop_requested_value(stop_requested):
        telemetry["stopped_by_user"] = True
        skipped_messages.append("Stopped by user before file processing started.")
        return changes, skipped_messages, report_rows, telemetry

    if parallel_enabled:
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=requested_workers) as pool:
            futures = {pool.submit(_process, path): path for path in paths}
            for future in as_completed(futures):
                if _stop_requested_value(stop_requested):
                    telemetry["stopped_by_user"] = True
                    for pending in futures:
                        pending.cancel()
                    skipped_messages.append("Stopped by user after current safe checkpoint.")
                    break
                path, changed, skipped, rows = future.result()
                with lock:
                    telemetry["files_processed_before_stop"] += 1
                    skipped_messages.extend(skipped)
                    report_rows.extend(rows)
                    if changed is not None:
                        changes[path] = changed
                    _emit_progress(
                        progress_callback,
                        total=len(paths),
                        audited=int(telemetry["files_processed_before_stop"]),
                    )
    else:
        for path in paths:
            if _stop_requested_value(stop_requested):
                telemetry["stopped_by_user"] = True
                skipped_messages.append("Stopped by user after current safe checkpoint.")
                break
            path, changed, skipped, rows = _process(path)
            telemetry["files_processed_before_stop"] += 1
            skipped_messages.extend(skipped)
            report_rows.extend(rows)
            if changed is not None:
                changes[path] = changed
            _emit_progress(
                progress_callback,
                total=len(paths),
                audited=int(telemetry["files_processed_before_stop"]),
            )

    return changes, skipped_messages, report_rows, telemetry
