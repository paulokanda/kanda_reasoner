"""Public contract for freeze hint intake records.

Patch ZIPs produced by the AI may contain a root-level KANDA_FREEZE_HINT.json
file. This facade preserves the original public import surface while the
implementation lives in focused ordinary Python modules under this package.

Project-specific intake state is stored under the selected project external
support root at:
<project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake.
It does not store project-specific memory in project_freeze_ledger.
"""

from __future__ import annotations

__all__ = [
    "build_freeze_form_inputs_from_latest_hint",
    "build_freeze_hint_intake_paths",
    "FreezeHintIntakeError",
    "FreezeHintIntakePaths",
    "load_latest_freeze_hint_record",
    "mark_latest_freeze_hint_used",
    "merge_validation_evidence_into_latest_hint",
    "read_freeze_hint_from_patch_zip",
    "resolve_freeze_hint_autofill_state",
    "save_freeze_hint_record",
    "scan_and_save_latest_freeze_hint",
]

from .models import (
    CONSUMED_NAME,
    FORM_KEYS,
    FREEZE_HINT_FILENAME,
    HISTORY_REL,
    HINT_FIELD_ALIASES,
    INTAKE_REL,
    LATEST_NAME,
    LIST_TEXT_KEYS,
    MANDATORY_FORM_FIELDS,
    MANDATORY_PROTECTED_PATHS,
    MANDATORY_RULES,
    RECOGNIZABLE_VALIDATION_HINT,
    SCHEMA_VERSION,
    STALE_LOCAL_VALIDATION_PENDING_PATTERNS,
    STARTER_PLACEHOLDER_PATTERNS,
    FreezeHintIntakeError,
    FreezeHintIntakePaths,
)
from .paths_io import (
    build_freeze_hint_intake_paths,
    _resolve_project_root,
    _default_staging_dir,
    _source_signature,
    _safe_mtime_ns,
    _history_filename,
    _safe_slug,
    _coerce_mapping,
    _source_name,
    _utc_now,
    _atomic_write_json,
)
from .form_normalization import (
    _normalize_hint,
    _patch_boundary_allowed_paths,
    _patch_boundary_generated_paths,
    _coerce_path_text_list,
    _do_not_regress_from_architecture_characteristics,
    _is_starter_placeholder,
    _value_or_empty_if_placeholder,
    _field_value_or_empty_if_placeholder,
    _merge_lines,
    _repair_hint_form_inputs_from_raw_hint,
    _form_has_mandatory_freeze_fields,
    _apply_hint_metadata_aliases,
    _has_non_empty_value,
    _hint_path_list,
    _infer_primary_box_from_hint_paths,
    _infer_box_type_from_hint_paths,
    _hint_to_form_inputs,
    _normalize_form_inputs,
    _field_to_text,
    _append_missing_lines,
    _append_text,
    _normalize_validation_evidence_summary,
    _has_recognizable_validation_marker,
    _has_stale_local_validation_pending_text,
    _has_local_validation_completion_marker,
    _has_safe_validation_evidence_marker,
    _clean_stale_pending_text_after_local_validation,
    _strip_stale_pending_validation_text,
    _strip_stale_pending_validation_sentences,
    _normalize_line,
)
from .frozen_matching import (
    _find_matching_frozen_feature,
    _candidate_feature_slugs_from_record,
    _find_matching_frozen_feature_in_index,
    _freeze_index_item_can_consume_hint,
    _freeze_index_item_slugs,
    _find_matching_frozen_feature_in_entry_files,
    _entry_file_frozen_match,
    _freeze_feature_tail_slug,
    _same_feature_id_alias,
    _same_feature_identity,
)
from .records import (
    save_freeze_hint_record,
    load_latest_freeze_hint_record,
    merge_validation_evidence_into_latest_hint,
    mark_latest_freeze_hint_used,
    _consume_latest_hint_if_already_frozen,
    _existing_validated_latest_source_mtime_ns,
    _preserve_existing_validated_record_if_same_hint,
    _same_source_identity,
    _record_has_recognizable_validation_evidence,
)
from .consumed_hints import (
    _load_consumed,
    _remember_consumed_hint,
    _is_consumed,
    _consumed_freeze_id_confirms_hint,
    _same_consumed_source,
)
from .scanner import (
    read_freeze_hint_from_patch_zip,
    scan_and_save_latest_freeze_hint,
)
from .autofill import (
    resolve_freeze_hint_autofill_state,
    build_freeze_form_inputs_from_latest_hint,
    _select_preview_snapshot,
    _select_manual_review_form,
    _merge_record_form_inputs_with_fallback,
    _merge_form_inputs_with_fallback,
    _autofill_state_result,
    _form_has_recognizable_validation_marker,
    _record_feature_title,
)
