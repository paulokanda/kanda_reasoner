# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Batch scan, diff, write, and post-write orchestration
# EXPORTS       : run
# DEPENDS ON    : project_exclusion_rules.py, source_io.py, file_processing.py, reporting.py, diff_output.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Batch scan, diff, write, and post-write orchestration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .diff_output import diff_text
from .file_processing import collect_changes
from .project_exclusion_rules import normalize_rel_path
from .reporting import (
    mark_report_rows_for_write_result as _mark_report_rows_for_write_result,
    print_post_write_verification as _print_post_write_verification,
    write_report_jsonl,
)
from .source_io import read_source_text, write_source_text

try:
    from ..ai_config import AIConfig
    from ..ai_docstring_generator import AIDocstringGenerator
    from ..docstring_policy import DocstringPolicy
    _AI_AVAILABLE = True
except ImportError:
    try:
        from ai_config import AIConfig
        from ai_docstring_generator import AIDocstringGenerator
        from docstring_policy import DocstringPolicy
        _AI_AVAILABLE = True
    except ImportError:
        _AI_AVAILABLE = False

__all__ = [
    "run",
]


def _build_action_summary(
    report_rows: list[dict[str, object]],
    changes: dict[Path, tuple[str, bool]],
) -> dict[str, int]:
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


def _print_action_summary(summary: dict[str, int]) -> None:
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

def _post_write_verification_summary(
    root: Path,
    *,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    insert_file_address_at_top: bool,
    include_init: bool,
    include_relaxed_paths: bool,
    include_tests: bool,
    target_module: str | None,
    target_package: str | None,
    workers: int,
) -> dict[str, object]:
    """Re-scan the same scope after write mode to detect remaining gaps."""
    remaining_changes, remaining_skipped, remaining_rows, telemetry = collect_changes(
        root,
        include_module=include_module,
        include_classes=include_classes,
        include_functions=include_functions,
        insert_file_address_at_top=insert_file_address_at_top,
        include_init=include_init,
        include_relaxed_paths=include_relaxed_paths,
        include_tests=include_tests,
        target_module=target_module,
        target_package=target_package,
        generator=None,
        workers=workers,
    )

    remaining_files = [
        normalize_rel_path(root, path)
        for path in sorted(remaining_changes)
    ]

    remaining_targets = [
        row
        for row in remaining_rows
        if row.get("action") == "inserted"
    ]

    return {
        "files_with_missing_docstrings": len(remaining_changes),
        "remaining_files": remaining_files,
        "remaining_insertable_targets": len(remaining_targets),
        "skipped": remaining_skipped,
        "workers_used": telemetry.get("workers_used", 1),
        "parallel_file_processing_enabled": telemetry.get(
            "parallel_file_processing_enabled",
            False,
        ),
    }

def run(
    root: Path,
    mode: str,
    *,
    include_module: bool = True,
    include_classes: bool = True,
    include_functions: bool = True,
    insert_file_address_at_top: bool = False,
    include_init: bool = False,
    include_relaxed_paths: bool = False,
    include_tests: bool = False,
    ai_config_path: str | None = None,
    workers: int = 1,
    include_private: bool = True,
    min_confidence: str = "low",
    no_uncertain: bool = False,
    require_ai_success: bool = False,
    target_module: str | None = None,
    target_package: str | None = None,
    report_path: str | None = None,
) -> int:
    """Handle run.
    
    Parameters
    ----------
    root : Path
        TODO: describe root.
    mode : str
        TODO: describe mode.
    include_module : bool, optional
        TODO: describe include_module.
    include_classes : bool, optional
        TODO: describe include_classes.
    include_functions : bool, optional
        TODO: describe include_functions.
    insert_file_address_at_top : bool, optional
        Insert a top file-address comment for each processed module when missing.
    include_init : bool, optional
        TODO: describe include_init.
    include_relaxed_paths : bool, optional
        TODO: describe include_relaxed_paths.
    include_tests : bool, optional
        TODO: describe include_tests.
    ai_config_path : str | None, optional
        TODO: describe ai_config_path.
    workers : int, optional
        TODO: describe workers.
    include_private : bool, optional
        TODO: describe include_private.
    min_confidence : str, optional
        TODO: describe min_confidence.
    no_uncertain : bool, optional
        TODO: describe no_uncertain.
    require_ai_success : bool, optional
        TODO: describe require_ai_success.
    target_module : str | None, optional
        TODO: describe target_module.
    target_package : str | None, optional
        TODO: describe target_package.
    report_path : str | None, optional
        TODO: describe report_path.
    
    Returns
    -------
    int
        TODO: describe the return value.
    """
    
    generator = None
    if ai_config_path is not None:
        if not _AI_AVAILABLE:
            print(
                "AI mode is unavailable because ai_config.py, context_builder.py, "
                "or ai_docstring_generator.py could not be imported.",
                file=sys.stderr,
            )
            return 2

        cfg = AIConfig.from_json(ai_config_path) if ai_config_path != "default" else AIConfig.default()
        cfg.workers = max(1, workers)
        cfg.include_private = include_private
        cfg.min_confidence = min_confidence
        if no_uncertain:
            cfg.uncertain_annotation = False
        cfg.require_ai_success = require_ai_success
        if require_ai_success:
            cfg.fallback_to_heuristic = False

        policy = DocstringPolicy.load_for_project(root)

        def _on_fallback(symbol_name: str, reason: str) -> None:
            """Handle on fallback.
            
            Parameters
            ----------
            symbol_name : str
                TODO: describe symbol_name.
            reason : str
                TODO: describe reason.
            """
            
            print(f"FALLBACK {symbol_name}: {reason}")

        def _on_low_confidence(symbol_name: str, issues: list[str]) -> None:
            """Handle on low confidence.
            
            Parameters
            ----------
            symbol_name : str
                TODO: describe symbol_name.
            issues : list[str]
                TODO: describe issues.
            """
            
            print(f"LOW-CONFIDENCE {symbol_name}: {'; '.join(issues)}")

        generator = AIDocstringGenerator(
            config=cfg,
            project_root=root,
            policy=policy,
            on_fallback=_on_fallback,
            on_low_confidence=_on_low_confidence,
        )

    changes, skipped_messages, report_rows, run_telemetry = collect_changes(
        root,
        include_module=include_module,
        include_classes=include_classes,
        include_functions=include_functions,
        insert_file_address_at_top=insert_file_address_at_top,
        include_init=include_init,
        include_relaxed_paths=include_relaxed_paths,
        include_tests=include_tests,
        target_module=target_module,
        target_package=target_package,
        generator=generator,
        workers=workers,
    )

    if generator is not None:
        generator.flush_cache()

    action_summary = _build_action_summary(report_rows, changes)

    if mode != "write":
        for row in report_rows:
            if row.get("action") == "inserted":
                row["write_state"] = "preview"
        write_report_jsonl(report_path, report_rows, root=root, mode=mode)

    if mode == "scan":
        summary = {
            "project_root": str(root),
            "include_module": include_module,
            "include_classes": include_classes,
            "include_functions": include_functions,
            "insert_file_address_at_top": insert_file_address_at_top,
            "include_init": include_init,
            "include_relaxed_paths": include_relaxed_paths,
            "include_tests": include_tests,
            "target_module": target_module,
            "target_package": target_package,
            "workers_requested": run_telemetry.get("workers_requested", max(1, workers)),
            "workers_used": run_telemetry.get("workers_used", 1),
            "parallel_write_enabled": False,
            "parallel_file_processing_enabled": run_telemetry.get(
                "parallel_file_processing_enabled",
                False,
            ),
            "parallel_reason": run_telemetry.get("parallel_reason", "disabled"),
            "docstring_only_ast_guard": True,
            "report_path": report_path,
            "report_rows": len(report_rows),
            "action_summary": action_summary,
            "files_with_changes": action_summary.get("files_with_changes", len(changes)),
            "files_with_docstring_changes": action_summary.get("files_with_docstring_changes", 0),
            "files_with_file_address_changes": action_summary.get("files_with_file_address_changes", 0),
            "files_with_missing_docstrings": len(changes),
            "files": [str(path.relative_to(root)).replace("\\", "/") for path in sorted(changes)],
            "skipped": skipped_messages,
        }
        if generator is not None:
            summary["ai_generation_stats"] = generator.stats.summary_line()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    if mode == "diff":
        if not changes and not skipped_messages:
            print("No missing docstrings found.")
            if generator is not None:
                print(f"\nAI generation stats: {generator.stats.summary_line()}")
            return 0

        _print_action_summary(action_summary)

        for msg in skipped_messages:
            print(f"SKIPPED {msg}")

        for path, (desired, _had_bom) in sorted(changes.items()):
            current, _ = read_source_text(path)
            print(
                diff_text(
                    current,
                    desired,
                    f"{path} (current)",
                    f"{path} (generated)",
                )
            )
        if generator is not None:
            print(f"\nAI generation stats: {generator.stats.summary_line()}")
        return 0

    if mode == "write":
        if not changes and not skipped_messages:
            print("No missing docstrings found.")
            write_report_jsonl(report_path, report_rows, root=root, mode=mode)
            if generator is not None:
                print(f"\nAI generation stats: {generator.stats.summary_line()}")
            return 0

        _print_action_summary(action_summary)

        for msg in skipped_messages:
            print(f"SKIPPED {msg}")

        if not changes:
            print("No safe docstring insertions to write.")
            write_report_jsonl(report_path, report_rows, root=root, mode=mode)
            if generator is not None:
                print(f"\nAI generation stats: {generator.stats.summary_line()}")
            return 0

        changed = 0
        written_paths: set[Path] = set()

        for path, (desired, had_bom) in sorted(changes.items()):
            write_source_text(path, desired, had_bom)
            print(f"WROTE {path}")
            written_paths.add(path)
            changed += 1

        _mark_report_rows_for_write_result(
            report_rows,
            written_paths,
            root=root,
        )

        verification_summary = _post_write_verification_summary(
            root,
            include_module=include_module,
            include_classes=include_classes,
            include_functions=include_functions,
            insert_file_address_at_top=insert_file_address_at_top,
            include_init=include_init,
            include_relaxed_paths=include_relaxed_paths,
            include_tests=include_tests,
            target_module=target_module,
            target_package=target_package,
            workers=workers,
        )

        for row in report_rows:
            row["post_write_files_with_missing_docstrings"] = (
                verification_summary.get("files_with_missing_docstrings", 0)
            )
            row["post_write_remaining_insertable_targets"] = (
                verification_summary.get("remaining_insertable_targets", 0)
            )

        write_report_jsonl(report_path, report_rows, root=root, mode=mode)

        print(f"\nDone. Updated {changed} file(s).")
        _print_post_write_verification(verification_summary)

        if generator is not None:
            print(f"\nAI generation stats: {generator.stats.summary_line()}")
        return 0

    raise ValueError(f"Unsupported mode: {mode}")


def _stop_requested_value(stop_requested) -> bool:
    """Return whether a cooperative stop callback asks to stop."""
    if stop_requested is None:
        return False
    try:
        return bool(stop_requested())
    except Exception:
        return False


def run(
    root: Path,
    mode: str,
    *,
    include_module: bool = True,
    include_classes: bool = True,
    include_functions: bool = True,
    insert_file_address_at_top: bool = False,
    include_init: bool = False,
    include_relaxed_paths: bool = False,
    include_tests: bool = False,
    ai_config_path: str | None = None,
    workers: int = 1,
    include_private: bool = True,
    min_confidence: str = "low",
    no_uncertain: bool = False,
    require_ai_success: bool = False,
    target_module: str | None = None,
    target_package: str | None = None,
    report_path: str | None = None,
    stop_requested=None,
    progress_callback=None,
) -> int:
    """Run the selected docstring mode with cooperative stop support."""
    from .file_processing import collect_changes as _collect_changes_with_stop

    if _stop_requested_value(stop_requested):
        print("Stopped by user before run started.")
        return 130

    generator = None
    if ai_config_path is not None:
        if not _AI_AVAILABLE:
            print(
                "AI mode is unavailable because ai_config.py, context_builder.py, "
                "or ai_docstring_generator.py could not be imported.",
                file=sys.stderr,
            )
            return 2

        cfg = AIConfig.from_json(ai_config_path) if ai_config_path != "default" else AIConfig.default()
        cfg.workers = max(1, workers)
        cfg.include_private = include_private
        cfg.min_confidence = min_confidence
        if no_uncertain:
            cfg.uncertain_annotation = False
        cfg.require_ai_success = require_ai_success
        if require_ai_success:
            cfg.fallback_to_heuristic = False

        policy = DocstringPolicy.load_for_project(root)

        def _on_fallback(symbol_name: str, reason: str) -> None:
            print(f"FALLBACK {symbol_name}: {reason}")

        def _on_low_confidence(symbol_name: str, issues: list[str]) -> None:
            print(f"LOW-CONFIDENCE {symbol_name}: {'; '.join(issues)}")

        generator = AIDocstringGenerator(
            config=cfg,
            project_root=root,
            policy=policy,
            on_fallback=_on_fallback,
            on_low_confidence=_on_low_confidence,
        )

    changes, skipped_messages, report_rows, run_telemetry = _collect_changes_with_stop(
        root,
        include_module=include_module,
        include_classes=include_classes,
        include_functions=include_functions,
        insert_file_address_at_top=insert_file_address_at_top,
        include_init=include_init,
        include_relaxed_paths=include_relaxed_paths,
        include_tests=include_tests,
        target_module=target_module,
        target_package=target_package,
        generator=generator,
        workers=workers,
        stop_requested=stop_requested,
        progress_callback=progress_callback,
    )

    if generator is not None:
        generator.flush_cache()

    if run_telemetry.get("stopped_by_user") or _stop_requested_value(stop_requested):
        print("Stopped by user after current safe checkpoint.")
        print(
            "Files processed before stop: "
            + str(run_telemetry.get("files_processed_before_stop", 0))
            + " of "
            + str(run_telemetry.get("files_selected", 0))
        )
        return 130

    action_summary = _build_action_summary(report_rows, changes)

    if mode != "write":
        for row in report_rows:
            if row.get("action") == "inserted":
                row["write_state"] = "preview"
        write_report_jsonl(report_path, report_rows, root=root, mode=mode)

    if mode == "scan":
        summary = {
            "project_root": str(root),
            "include_module": include_module,
            "include_classes": include_classes,
            "include_functions": include_functions,
            "insert_file_address_at_top": insert_file_address_at_top,
            "include_init": include_init,
            "include_relaxed_paths": include_relaxed_paths,
            "include_tests": include_tests,
            "target_module": target_module,
            "target_package": target_package,
            "workers_requested": run_telemetry.get("workers_requested", max(1, workers)),
            "workers_used": run_telemetry.get("workers_used", 1),
            "parallel_write_enabled": False,
            "parallel_file_processing_enabled": run_telemetry.get(
                "parallel_file_processing_enabled",
                False,
            ),
            "parallel_reason": run_telemetry.get("parallel_reason", "disabled"),
            "docstring_only_ast_guard": True,
            "report_path": report_path,
            "report_rows": len(report_rows),
            "action_summary": action_summary,
            "files_with_changes": action_summary.get("files_with_changes", len(changes)),
            "files_with_docstring_changes": action_summary.get("files_with_docstring_changes", 0),
            "files_with_file_address_changes": action_summary.get("files_with_file_address_changes", 0),
            "files_with_missing_docstrings": len(changes),
            "files": [str(path.relative_to(root)).replace("\\", "/") for path in sorted(changes)],
            "skipped": skipped_messages,
        }
        if generator is not None:
            summary["ai_generation_stats"] = generator.stats.summary_line()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    if mode == "diff":
        if not changes and not skipped_messages:
            print("No missing docstrings found.")
            if generator is not None:
                print(f"\nAI generation stats: {generator.stats.summary_line()}")
            return 0

        _print_action_summary(action_summary)

        for msg in skipped_messages:
            print(f"SKIPPED {msg}")

        for path, (desired, _had_bom) in sorted(changes.items()):
            if _stop_requested_value(stop_requested):
                print("Stopped by user before diff output completed.")
                return 130
            current, _ = read_source_text(path)
            print(
                diff_text(
                    current,
                    desired,
                    f"{path} (current)",
                    f"{path} (generated)",
                )
            )
        if generator is not None:
            print(f"\nAI generation stats: {generator.stats.summary_line()}")
        return 0

    if mode == "write":
        if not changes and not skipped_messages:
            print("No missing docstrings found.")
            write_report_jsonl(report_path, report_rows, root=root, mode=mode)
            if generator is not None:
                print(f"\nAI generation stats: {generator.stats.summary_line()}")
            return 0

        _print_action_summary(action_summary)

        for msg in skipped_messages:
            print(f"SKIPPED {msg}")

        if not changes:
            print("No safe docstring insertions to write.")
            write_report_jsonl(report_path, report_rows, root=root, mode=mode)
            if generator is not None:
                print(f"\nAI generation stats: {generator.stats.summary_line()}")
            return 0

        if _stop_requested_value(stop_requested):
            print("Stopped by user before write started. No files were written.")
            return 130

        changed = 0
        written_paths: set[Path] = set()

        for path, (desired, had_bom) in sorted(changes.items()):
            if _stop_requested_value(stop_requested):
                print("Stopped by user during write. No further files will be written.")
                break
            write_source_text(path, desired, had_bom)
            print(f"WROTE {path}")
            written_paths.add(path)
            changed += 1

        _mark_report_rows_for_write_result(
            report_rows,
            written_paths,
            root=root,
        )

        verification_summary = _post_write_verification_summary(
            root,
            include_module=include_module,
            include_classes=include_classes,
            include_functions=include_functions,
            insert_file_address_at_top=insert_file_address_at_top,
            include_init=include_init,
            include_relaxed_paths=include_relaxed_paths,
            include_tests=include_tests,
            target_module=target_module,
            target_package=target_package,
            workers=workers,
        )

        for row in report_rows:
            row["post_write_files_with_missing_docstrings"] = (
                verification_summary.get("files_with_missing_docstrings", 0)
            )
            row["post_write_remaining_insertable_targets"] = (
                verification_summary.get("remaining_insertable_targets", 0)
            )

        write_report_jsonl(report_path, report_rows, root=root, mode=mode)

        print(f"\nDone. Updated {changed} file(s).")
        _print_post_write_verification(verification_summary)

        if generator is not None:
            print(f"\nAI generation stats: {generator.stats.summary_line()}")
        return 130 if _stop_requested_value(stop_requested) else 0

    raise ValueError(f"Unsupported mode: {mode}")
