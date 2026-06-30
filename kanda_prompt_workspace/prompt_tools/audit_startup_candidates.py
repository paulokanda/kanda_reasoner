#!/usr/bin/env python3
"""
audit_startup_candidates.py

Thin compatibility facade for startup routing kernel candidate auditing.
Runtime logic lives in cohesive audit_startup_candidates_* modules.
"""

from __future__ import annotations

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "kanda_prompt_workspace.prompt_tools"

from .audit_startup_candidates_models import (
    AuditResult,
    SourceMapEntry,
    StartupCandidate,
    read_json_file,
    read_text_utf8_strict,
    sha256_file,
    utc_now_iso,
    write_text_utf8,
)
from .audit_startup_candidates_paths import (
    detect_workspace_root,
    is_hidden_or_cache_path,
    is_relative_to_safe,
    is_valid_workspace,
    normalize_rel_path,
)
from .audit_startup_candidates_source_map import (
    detect_stale_entries,
    load_source_map_object,
    parse_source_map,
    suggested_next_filename_number,
    suggested_next_load_order,
)
from .audit_startup_candidates_sidecars import (
    allowed_scan_roots,
    compare_candidates_to_source_map,
    find_sidecar_candidates,
    sidecar_to_candidate,
    validate_candidate_set,
)
from .audit_startup_candidates_report import (
    append_items,
    ask_yes_no,
    create_report,
    explain_missing_candidates,
    proposed_entry_for_candidate,
)
from .audit_startup_candidates_runner import (
    atomic_write_text,
    handle_interactive_update,
    main,
    parse_args,
    run_audit,
    run_sync_generator,
    update_source_map_with_candidates,
)

__all__ = [
    'allowed_scan_roots',
    'append_items',
    'ask_yes_no',
    'atomic_write_text',
    'AuditResult',
    'compare_candidates_to_source_map',
    'create_report',
    'detect_stale_entries',
    'detect_workspace_root',
    'explain_missing_candidates',
    'find_sidecar_candidates',
    'handle_interactive_update',
    'is_hidden_or_cache_path',
    'is_relative_to_safe',
    'is_valid_workspace',
    'load_source_map_object',
    'main',
    'normalize_rel_path',
    'parse_args',
    'parse_source_map',
    'proposed_entry_for_candidate',
    'read_json_file',
    'read_text_utf8_strict',
    'run_audit',
    'run_sync_generator',
    'sha256_file',
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
