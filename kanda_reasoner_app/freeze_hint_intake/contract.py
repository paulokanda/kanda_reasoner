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

from .autofill import (
    build_freeze_form_inputs_from_latest_hint as _build_freeze_form_inputs,
)
from .autofill import (
    resolve_freeze_hint_autofill_state as _resolve_freeze_hint_autofill_state,
)
from .discard import (
    execute_discard_latest_freeze_hint_candidate as _discard_latest_candidate,
)
from .models import FreezeHintIntakeError as _FreezeHintIntakeError
from .models import FreezeHintIntakePaths as _FreezeHintIntakePaths
from .paths_io import (
    build_freeze_hint_intake_paths as _build_freeze_hint_intake_paths,
)
from .records import (
    load_latest_freeze_hint_record as _load_latest_freeze_hint_record,
)
from .records import (
    mark_latest_freeze_hint_used as _mark_latest_freeze_hint_used,
)
from .records import (
    merge_validation_evidence_into_latest_hint as _merge_validation_evidence,
)
from .records import save_freeze_hint_record as _save_freeze_hint_record
from .scanner import (
    read_freeze_hint_from_patch_zip as _read_freeze_hint_from_patch_zip,
)
from .scanner import (
    scan_and_save_latest_freeze_hint as _scan_and_save_latest_freeze_hint,
)

__all__ = [
    "build_freeze_form_inputs_from_latest_hint",
    "build_freeze_hint_intake_paths",
    "discard_latest_freeze_hint_candidate",
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

FreezeHintIntakeError = _FreezeHintIntakeError
FreezeHintIntakePaths = _FreezeHintIntakePaths
build_freeze_hint_intake_paths = _build_freeze_hint_intake_paths
discard_latest_freeze_hint_candidate = _discard_latest_candidate
save_freeze_hint_record = _save_freeze_hint_record
load_latest_freeze_hint_record = _load_latest_freeze_hint_record
merge_validation_evidence_into_latest_hint = _merge_validation_evidence
mark_latest_freeze_hint_used = _mark_latest_freeze_hint_used
read_freeze_hint_from_patch_zip = _read_freeze_hint_from_patch_zip
scan_and_save_latest_freeze_hint = _scan_and_save_latest_freeze_hint
resolve_freeze_hint_autofill_state = _resolve_freeze_hint_autofill_state
build_freeze_form_inputs_from_latest_hint = _build_freeze_form_inputs
