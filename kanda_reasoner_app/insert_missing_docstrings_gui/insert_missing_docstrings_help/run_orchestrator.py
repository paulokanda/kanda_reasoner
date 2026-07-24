# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/run_orchestrator.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Public facade for batch scan, diff, write, and post-write orchestration
# EXPORTS       : run
# DEPENDS ON    : _run_execution.py
# REFACTOR DATE : 2026-06-30
# ------------------------------------------------------
"""Public facade for docstring insertion run orchestration."""

from __future__ import annotations

from pathlib import Path

from ._run_execution import execute_run as _execute_run

__all__ = [
    "run",
]


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
    ai_api_key: str = "",
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
    return _execute_run(
        root,
        mode,
        include_module=include_module,
        include_classes=include_classes,
        include_functions=include_functions,
        insert_file_address_at_top=insert_file_address_at_top,
        include_init=include_init,
        include_relaxed_paths=include_relaxed_paths,
        include_tests=include_tests,
        ai_config_path=ai_config_path,
        ai_api_key=ai_api_key,
        workers=workers,
        include_private=include_private,
        min_confidence=min_confidence,
        no_uncertain=no_uncertain,
        require_ai_success=require_ai_success,
        target_module=target_module,
        target_package=target_package,
        report_path=report_path,
        stop_requested=stop_requested,
        progress_callback=progress_callback,
    )
