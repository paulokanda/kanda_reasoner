# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/_action_summary.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Action-summary counting and console rendering for run orchestration
# EXPORTS       : build_action_summary, print_action_summary
# DEPENDS ON    : pathlib
# REFACTOR DATE : 2026-06-30
# ------------------------------------------------------
"""Action-summary helpers for the docstring insertion orchestrator."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "build_action_summary",
    "print_action_summary",
]


def build_action_summary(
    report_rows: list[dict[str, object]],
    changes: dict[Path, tuple[str, bool]],
) -> dict[str, int]:
    """Build a action summary.
    
    Parameters
    ----------
    report_rows : list[dict[str, object]]
        The report rows value.
    changes : dict[Path, tuple[str, bool]]
        The changes value.
    
    Returns
    -------
    dict[str, int]
        The mapped values.
    """
    
    summary = {
        "files_with_changes": len(changes),
        "files_with_docstring_changes": 0,
        "files_with_file_address_changes": 0,
        "docstring_inserted": 0,
        "module_docstring_inserted": 0,
        "class_docstring_inserted": 0,
        "function_docstring_inserted": 0,
        "method_docstring_inserted": 0,
        "file_address_inserted": 0,
        "file_address_existing": 0,
        "file_address_updated_stale_managed": 0,
        "file_address_legacy_skipped": 0,
        "file_address_outside_root_skipped": 0,
        "skipped": 0,
        "failed": 0,
    }

    docstring_files: set[str] = set()
    file_address_files: set[str] = set()

    for row in report_rows:
        action = str(row.get("action", "") or "")
        target_kind = str(row.get("target_kind", "") or "")
        reason = str(row.get("reason", "") or "").lower()
        row_file = str(row.get("file", "") or "")

        if action == "inserted" and target_kind == "module":
            summary["docstring_inserted"] += 1
            summary["module_docstring_inserted"] += 1
            if row_file:
                docstring_files.add(row_file)
        elif action == "inserted" and target_kind == "class":
            summary["docstring_inserted"] += 1
            summary["class_docstring_inserted"] += 1
            if row_file:
                docstring_files.add(row_file)
        elif action == "inserted" and target_kind == "function":
            summary["docstring_inserted"] += 1
            summary["function_docstring_inserted"] += 1
            if row_file:
                docstring_files.add(row_file)
        elif action == "inserted" and target_kind == "method":
            summary["docstring_inserted"] += 1
            summary["method_docstring_inserted"] += 1
            if row_file:
                docstring_files.add(row_file)
        elif target_kind == "file_address":
            if action in {"inserted", "updated", "updated_stale_managed"} and row_file:
                file_address_files.add(row_file)
            if action == "inserted":
                summary["file_address_inserted"] += 1
            elif action == "existing":
                summary["file_address_existing"] += 1
            elif action in {"updated", "updated_stale_managed"}:
                summary["file_address_updated_stale_managed"] += 1
            elif action == "skipped" and "legacy" in reason:
                summary["file_address_legacy_skipped"] += 1
            elif action == "skipped" and "outside" in reason:
                summary["file_address_outside_root_skipped"] += 1

        if action == "skipped":
            summary["skipped"] += 1
        elif action == "failed":
            summary["failed"] += 1

    summary["files_with_docstring_changes"] = len(docstring_files)
    summary["files_with_file_address_changes"] = len(file_address_files)

    return summary


def print_action_summary(summary: dict[str, int]) -> None:
    """Support print action summary behavior.
    
    Parameters
    ----------
    summary : dict[str, int]
        The summary value.
    """
    
    print("")
    print("Action summary:")
    print(f"  Files with changes: {summary.get('files_with_changes', 0)}")
    print(
        f"  Files with docstring changes: "
        f"{summary.get('files_with_docstring_changes', 0)}"
    )
    print(
        f"  Files with file-address changes: "
        f"{summary.get('files_with_file_address_changes', 0)}"
    )
    print(f"  Docstrings to insert: {summary.get('docstring_inserted', 0)}")
    print(f"    Module: {summary.get('module_docstring_inserted', 0)}")
    print(f"    Class: {summary.get('class_docstring_inserted', 0)}")
    print(f"    Function: {summary.get('function_docstring_inserted', 0)}")
    print(f"    Method: {summary.get('method_docstring_inserted', 0)}")
    print(f"  File-address headers to insert: {summary.get('file_address_inserted', 0)}")
    print(f"  File-address headers already present: {summary.get('file_address_existing', 0)}")
    print(
        "  Stale managed file-address headers to update: "
        f"{summary.get('file_address_updated_stale_managed', 0)}"
    )
    print(
        "  Legacy possible file-address headers skipped: "
        f"{summary.get('file_address_legacy_skipped', 0)}"
    )
    print(
        "  Outside-root file-address headers skipped: "
        f"{summary.get('file_address_outside_root_skipped', 0)}"
    )
    print(f"  Skipped report rows: {summary.get('skipped', 0)}")
    print(f"  Failed report rows: {summary.get('failed', 0)}")
