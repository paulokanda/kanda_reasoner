# project-path: kanda_reasoner_app/freeze_hint_intake/__init__.py
"""Freeze hint intake box for KANDA freeze-after-update workflows."""

from .contract import (
    build_freeze_form_inputs_from_latest_hint,
    merge_validation_evidence_into_latest_hint,
    load_latest_freeze_hint_record,
    mark_latest_freeze_hint_used,
    read_freeze_hint_from_patch_zip,
    resolve_freeze_hint_autofill_state,
    scan_and_save_latest_freeze_hint,
)

__all__ = [
    "build_freeze_form_inputs_from_latest_hint",
    "merge_validation_evidence_into_latest_hint",
    "load_latest_freeze_hint_record",
    "mark_latest_freeze_hint_used",
    "read_freeze_hint_from_patch_zip",
    "resolve_freeze_hint_autofill_state",
    "scan_and_save_latest_freeze_hint",
]
