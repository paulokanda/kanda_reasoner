"""Shared models and constants for freeze hint intake."""

from __future__ import annotations

__all__: list[str] = []


from dataclasses import dataclass
from pathlib import Path

FREEZE_HINT_FILENAME = "KANDA_FREEZE_HINT.json"
INTAKE_REL = Path("freeze_hint_intake")
HISTORY_REL = INTAKE_REL / "history"
LATEST_NAME = "latest_freeze_hint.json"
CONSUMED_NAME = "consumed_freeze_hints.json"
SCHEMA_VERSION = "1.0"

FORM_KEYS = (
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)

LIST_TEXT_KEYS = (
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
)

MANDATORY_PROTECTED_PATHS = (
    "project_freeze_after_update/frozen_features_memory/",
)

MANDATORY_RULES = (
    "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.",
    "Do not store project-specific frozen memory inside project_freeze_ledger.",
    "Preview Freeze Entry must remain read-only and must not write files.",
    "Confirm and Write must require explicit human confirmation before writing governed freeze memory.",
    "After a local freeze write, the AI startup freeze context must be refreshed.",
    "External AI review remains advanced/fallback, not the normal local freeze path.",
)

RECOGNIZABLE_VALIDATION_HINT = (
    "Validation evidence intended for Confirm and Write must include a literal "
    "recognizable marker such as VALIDATION OK: <feature_id> or STATUS: IN_SYNC."
)

HINT_FIELD_ALIASES = {
    "primary_box": (
        "primary_box",
        "owning_box",
        "box",
    ),
    "box_type": (
        "box_type",
        "feature_type",
    ),
    "validated_files": (
        "validated_files",
        "box_paths",
        "updated_files",
        "changed_files",
        "touched_files",
    ),
    "generated_files": (
        "generated_files",
        "generated_paths",
        "created_files",
    ),
    "protected_paths": (
        "protected_paths",
        "box_paths",
    ),
    "do_not_regress_rules": (
        "do_not_regress_rules",
        "do_not_regress",
        "do_not_touch_summary",
    ),
    "known_warnings": (
        "known_warnings",
        "freeze_warning",
        "warnings",
    ),
    "validation_evidence_summary": (
        "validation_evidence_summary",
        "validation_evidence",
        "validation_output",
        "validation_log",
        "validation_summary",
    ),
    "planned_next_step": (
        "planned_next_step",
        "next_step",
    ),
    "notes": (
        "notes",
        "freeze_summary",
        "summary",
    ),
}

STARTER_PLACEHOLDER_PATTERNS = (
    "current validated feature - replace with exact feature title",
    "replace with the primary box for the current feature",
    "replace with the current box type",
    "starter draft only",
    "replace placeholders",
    "starter fallback",
)

STALE_LOCAL_VALIDATION_PENDING_PATTERNS = (
    "local validation pending",
    "pre-validation sidecar",
    "pre validation sidecar",
    "pre-validation sidecar only",
    "pre validation sidecar only",
    "user-local validation must be run",
    "user local validation must be run",
    "user-local validation remains required",
    "user local validation remains required",
    "run the delivered validation block",
    "run the provided validation block",
    "run scripts/validate_release_guard_zip_contract_v1.py after installation",
    "before confirm and write",
    "before freeze confirmation",
    "before freezing",
)

MANDATORY_FORM_FIELDS = (
    "feature_title",
    "primary_box",
    "validated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
)


@dataclass(frozen=True)
class FreezeHintIntakePaths:
    """Resolved paths for one project's freeze hint intake box."""

    project_root: Path
    intake_root: Path
    history_root: Path
    latest_hint: Path
    consumed_hints: Path

class FreezeHintIntakeError(RuntimeError):
    """Raised when freeze hint intake cannot process a sidecar safely."""

