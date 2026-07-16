#!/usr/bin/env python3
# project-path: kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py
"""
audit_startup_candidates.py

Thin compatibility facade for startup routing kernel candidate auditing.
Runtime logic lives in cohesive audit_startup_candidates_* modules.
"""

from __future__ import annotations


def _ensure_script_package() -> None:
    """Prepare package imports when this facade is executed as a script."""

    global __package__

    if __package__ in (None, ""):
        import sys
        from pathlib import Path

        workspace_root = Path(__file__).resolve().parents[2]
        workspace_text = str(workspace_root)
        if workspace_text not in sys.path:
            sys.path.insert(0, workspace_text)
        __package__ = "kanda_prompt_workspace.prompt_tools"


_ensure_script_package()

from .audit_startup_candidates_models import (
    AuditResult as _public_AuditResult,
    SourceMapEntry as _public_SourceMapEntry,
    StartupCandidate as _public_StartupCandidate,
    read_json_file as _public_read_json_file,
    read_text_utf8_strict as _public_read_text_utf8_strict,
    sha256_file as _public_sha256_file,
    utc_now_iso as _public_utc_now_iso,
    write_text_utf8 as _public_write_text_utf8,
)
from .audit_startup_candidates_paths import (
    detect_workspace_root as _public_detect_workspace_root,
    is_hidden_or_cache_path as _public_is_hidden_or_cache_path,
    is_relative_to_safe as _public_is_relative_to_safe,
    is_valid_workspace as _public_is_valid_workspace,
    normalize_rel_path as _public_normalize_rel_path,
)
from .audit_startup_candidates_source_map import (
    detect_stale_entries as _public_detect_stale_entries,
    load_source_map_object as _public_load_source_map_object,
    parse_source_map as _public_parse_source_map,
    suggested_next_filename_number as _public_suggested_next_filename_number,
    suggested_next_load_order as _public_suggested_next_load_order,
)
from .audit_startup_candidates_sidecars import (
    allowed_scan_roots as _public_allowed_scan_roots,
    compare_candidates_to_source_map as _public_compare_candidates_to_source_map,
    find_sidecar_candidates as _public_find_sidecar_candidates,
    sidecar_to_candidate as _public_sidecar_to_candidate,
    validate_candidate_set as _public_validate_candidate_set,
)
from .audit_startup_candidates_report import (
    append_items as _public_append_items,
    ask_yes_no as _public_ask_yes_no,
    create_report as _public_create_report,
    explain_missing_candidates as _public_explain_missing_candidates,
    proposed_entry_for_candidate as _public_proposed_entry_for_candidate,
)
from .audit_startup_candidates_runner import (
    atomic_write_text as _public_atomic_write_text,
    handle_interactive_update as _public_handle_interactive_update,
    main as _public_main,
    parse_args as _public_parse_args,
    run_audit as _public_run_audit,
    run_sync_generator as _public_run_sync_generator,
    update_source_map_with_candidates as _public_update_source_map_with_candidates,
)

AuditResult = _public_AuditResult
SourceMapEntry = _public_SourceMapEntry
StartupCandidate = _public_StartupCandidate
read_json_file = _public_read_json_file
read_text_utf8_strict = _public_read_text_utf8_strict
sha256_file = _public_sha256_file
utc_now_iso = _public_utc_now_iso
write_text_utf8 = _public_write_text_utf8
detect_workspace_root = _public_detect_workspace_root
is_hidden_or_cache_path = _public_is_hidden_or_cache_path
is_relative_to_safe = _public_is_relative_to_safe
is_valid_workspace = _public_is_valid_workspace
normalize_rel_path = _public_normalize_rel_path
detect_stale_entries = _public_detect_stale_entries
load_source_map_object = _public_load_source_map_object
parse_source_map = _public_parse_source_map
suggested_next_filename_number = _public_suggested_next_filename_number
suggested_next_load_order = _public_suggested_next_load_order
allowed_scan_roots = _public_allowed_scan_roots
compare_candidates_to_source_map = _public_compare_candidates_to_source_map
find_sidecar_candidates = _public_find_sidecar_candidates
sidecar_to_candidate = _public_sidecar_to_candidate
validate_candidate_set = _public_validate_candidate_set
append_items = _public_append_items
ask_yes_no = _public_ask_yes_no
create_report = _public_create_report
explain_missing_candidates = _public_explain_missing_candidates
proposed_entry_for_candidate = _public_proposed_entry_for_candidate
atomic_write_text = _public_atomic_write_text
handle_interactive_update = _public_handle_interactive_update
main = _public_main
parse_args = _public_parse_args
run_audit = _public_run_audit
run_sync_generator = _public_run_sync_generator
update_source_map_with_candidates = _public_update_source_map_with_candidates

__all__ = [
    'allowed_scan_roots',
    'append_items',
    'ask_yes_no',
    'AuditResult',
    'compare_candidates_to_source_map',
    'create_report',
    'detect_stale_entries',
    'explain_missing_candidates',
    'find_sidecar_candidates',
    'handle_interactive_update',
    'is_hidden_or_cache_path',
    'is_relative_to_safe',
    'is_valid_workspace',
    'load_source_map_object',
    'main',
    'parse_source_map',
    'proposed_entry_for_candidate',
    'read_json_file',
    'read_text_utf8_strict',
    'run_audit',
    'run_sync_generator',
    'sidecar_to_candidate',
    'SourceMapEntry',
    'StartupCandidate',
    'suggested_next_filename_number',
    'suggested_next_load_order',
    'update_source_map_with_candidates',
    'validate_candidate_set',
    'write_text_utf8',
]


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv[1:]))
