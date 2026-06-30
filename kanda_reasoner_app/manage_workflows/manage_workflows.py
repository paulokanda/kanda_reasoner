#!/usr/bin/env python3
# project-path: kanda_reasoner_app/manage_workflows/manage_workflows.py
"""Public CLI entry point for workflow validation governance.

AI CONTEXT - REFACTORED MODULE
Implementation logic lives in kanda_reasoner_app.manage_workflows.manage_workflows_help.
Keep this file as the stable user-facing import and launch module.
"""

from __future__ import annotations

# Reconfigure Windows console output early so captured workflow reports
# can print replacement characters instead of crashing on cp1252.
import sys as _workflow_stdio_sys

def _workflow_reconfigure_stdio_for_utf8() -> None:
    """Support workflow reconfigure stdio for utf8 behavior.
    """
    
    for _stream_name in ("stdout", "stderr"):
        _stream = getattr(_workflow_stdio_sys, _stream_name, None)
        if _stream is None:
            continue
        _reconfigure = getattr(_stream, "reconfigure", None)
        if _reconfigure is None:
            continue
        try:
            _reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

_workflow_reconfigure_stdio_for_utf8()

# Support both package import and direct script execution by path.
try:
    from .manage_workflows_help.workflow_cli import (
        main,
        validate_project,
    )
    from .manage_workflows_help.workflow_command_runner import (
        build_command,
        command_list_results,
        execute_command,
        maybe_stringify_command,
        replace_placeholders,
        run_tests,
    )
    from .manage_workflows_help.workflow_constants import (
        DEFAULT_EXCLUDE_DIRS,
        ENTRY_FILENAMES,
        GUI_IMPORT_MARKERS,
        HISTORY_FILE,
        HISTORY_MAX_ROOTS,
        IMPORT_PROBE_CODE,
        MANAGED_BY,
        WORKFLOWS_DOC_NAME,
        WORKFLOW_MANIFEST_NAME,
    )
    from .manage_workflows_help.workflow_generation import (
        collect_generated_outputs,
        generate_manifest,
        generate_workflows_md,
        load_manifest_or_default,
    )
    from .manage_workflows_help.workflow_history import (
        clear_history,
        get_history_roots,
        print_history,
        record_root,
    )
    from .manage_workflows_help.workflow_import_checks import (
        run_import_checks,
    )
    from .manage_workflows_help.workflow_io import (
        diff_text,
        load_ignore_rules,
        normalize_generated_output_for_diff,
        read_text,
        should_generate_json_manifest,
        should_generate_workflows_doc,
        utc_now_iso,
        write_text_if_changed,
    )
    from .manage_workflows_help.workflow_models import (
        CheckResult,
    )
    from .manage_workflows_help.workflow_project_scan import (
        has_gui_marker,
        has_main_guard,
        is_test_path,
        iter_python_files,
        module_id_for_path,
        pytest_available,
        scan_project,
        should_skip_dir,
    )
    from .manage_workflows_help.workflow_reporting import (
        print_results,
        summarize_results,
    )
except ImportError:
    from manage_workflows_help.workflow_cli import (
        main,
        validate_project,
    )
    from manage_workflows_help.workflow_command_runner import (
        build_command,
        command_list_results,
        execute_command,
        maybe_stringify_command,
        replace_placeholders,
        run_tests,
    )
    from manage_workflows_help.workflow_constants import (
        DEFAULT_EXCLUDE_DIRS,
        ENTRY_FILENAMES,
        GUI_IMPORT_MARKERS,
        HISTORY_FILE,
        HISTORY_MAX_ROOTS,
        IMPORT_PROBE_CODE,
        MANAGED_BY,
        WORKFLOWS_DOC_NAME,
        WORKFLOW_MANIFEST_NAME,
    )
    from manage_workflows_help.workflow_generation import (
        collect_generated_outputs,
        generate_manifest,
        generate_workflows_md,
        load_manifest_or_default,
    )
    from manage_workflows_help.workflow_history import (
        clear_history,
        get_history_roots,
        print_history,
        record_root,
    )
    from manage_workflows_help.workflow_import_checks import (
        run_import_checks,
    )
    from manage_workflows_help.workflow_io import (
        diff_text,
        load_ignore_rules,
        normalize_generated_output_for_diff,
        read_text,
        should_generate_json_manifest,
        should_generate_workflows_doc,
        utc_now_iso,
        write_text_if_changed,
    )
    from manage_workflows_help.workflow_models import (
        CheckResult,
    )
    from manage_workflows_help.workflow_project_scan import (
        has_gui_marker,
        has_main_guard,
        is_test_path,
        iter_python_files,
        module_id_for_path,
        pytest_available,
        scan_project,
        should_skip_dir,
    )
    from manage_workflows_help.workflow_reporting import (
        print_results,
        summarize_results,
    )

__all__ = [
    "CheckResult",
    "clear_history",
    "collect_generated_outputs",
    "command_list_results",
    "generate_manifest",
    "generate_workflows_md",
    "get_history_roots",
    "load_manifest_or_default",
    "main",
    "print_history",
    "print_results",
    "run_import_checks",
    "run_tests",
    "scan_project",
    "summarize_results",
    "validate_project",
]


if __name__ == "__main__":
    raise SystemExit(main())
