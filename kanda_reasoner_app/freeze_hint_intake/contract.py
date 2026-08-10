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
    FreezeHintIntakeError as _FreezeHintIntakeError,
    FreezeHintIntakePaths as _FreezeHintIntakePaths,
)
from .paths_io import (
    build_freeze_hint_intake_paths as _build_freeze_hint_intake_paths,
)
from .records import (
    save_freeze_hint_record as _save_freeze_hint_record,
    load_latest_freeze_hint_record as _load_latest_freeze_hint_record,
    merge_validation_evidence_into_latest_hint as _merge_validation_evidence_into_latest_hint,
    mark_latest_freeze_hint_used as _mark_latest_freeze_hint_used,
)
from .scanner import (
    read_freeze_hint_from_patch_zip as _read_freeze_hint_from_patch_zip,
    scan_and_save_latest_freeze_hint as _scan_and_save_latest_freeze_hint,
)
from .autofill import (
    resolve_freeze_hint_autofill_state as _resolve_freeze_hint_autofill_state,
    build_freeze_form_inputs_from_latest_hint as _build_freeze_form_inputs_from_latest_hint,
)
FreezeHintIntakeError = _FreezeHintIntakeError
FreezeHintIntakePaths = _FreezeHintIntakePaths
build_freeze_hint_intake_paths = _build_freeze_hint_intake_paths
save_freeze_hint_record = _save_freeze_hint_record
load_latest_freeze_hint_record = _load_latest_freeze_hint_record
merge_validation_evidence_into_latest_hint = _merge_validation_evidence_into_latest_hint
mark_latest_freeze_hint_used = _mark_latest_freeze_hint_used
read_freeze_hint_from_patch_zip = _read_freeze_hint_from_patch_zip
scan_and_save_latest_freeze_hint = _scan_and_save_latest_freeze_hint
resolve_freeze_hint_autofill_state = _resolve_freeze_hint_autofill_state
build_freeze_form_inputs_from_latest_hint = _build_freeze_form_inputs_from_latest_hint

