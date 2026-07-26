# project-path: tools/brick_wall_q30_human_confirmation_freeze_protection_contract.py
"""Validation-only Q30 human-confirmation and freeze-protection record."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

__all__: list[str] = []

REQUIRED_FIELDS = (
    "protection_required",
    "no_protection_evidence",
    "q29_decision_complete",
    "primary_box",
    "canonical_owner",
    "preview_read_only",
    "explicit_confirm_and_write",
    "exact_form_binding",
    "selected_project_binding",
    "form_change_invalidates",
    "source_evidence_change_invalidates",
    "target_change_invalidates",
    "project_root_change_invalidates",
    "public_contract_confirmation_check",
    "public_contract_root_binding_check",
    "automatic_error_memory_promotion",
    "automatic_freeze_memory_write",
    "validators",
    "expected_markers",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q31",
    "may_begin_coding",
    "may_write_source",
)

_REQUIRED_TRUE = (
    "q29_decision_complete",
    "preview_read_only",
    "explicit_confirm_and_write",
    "exact_form_binding",
    "selected_project_binding",
    "form_change_invalidates",
    "source_evidence_change_invalidates",
    "target_change_invalidates",
    "project_root_change_invalidates",
    "public_contract_confirmation_check",
    "public_contract_root_binding_check",
    "may_proceed_to_q31",
)


def valid_complete_record() -> dict[str, Any]:
    return {
        "protection_required": True,
        "no_protection_evidence": [],
        "q29_decision_complete": True,
        "primary_box": "kanda_reasoner_app/freeze_after_update",
        "canonical_owner": "kanda_reasoner_app.freeze_after_update.contract",
        "preview_read_only": True,
        "explicit_confirm_and_write": True,
        "exact_form_binding": True,
        "selected_project_binding": True,
        "form_change_invalidates": True,
        "source_evidence_change_invalidates": True,
        "target_change_invalidates": True,
        "project_root_change_invalidates": True,
        "public_contract_confirmation_check": True,
        "public_contract_root_binding_check": True,
        "automatic_error_memory_promotion": False,
        "automatic_freeze_memory_write": False,
        "validators": [
            "tools/validate_brick_wall_q30_human_confirmation_freeze_protection_v1.py",
            "tools/validate_brick_wall_q30_human_confirmation_freeze_protection_real_qt_v1.py",
        ],
        "expected_markers": [
            "Q30_HUMAN_CONFIRMATION_FREEZE_PROTECTION_REGRESSION_SET: PASS",
            "Q30_REAL_QT_CONFIRMATION_INVALIDATION: PASS",
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q31": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        protection_required=False,
        no_protection_evidence=[
            "No canonical or durable write path exists for the audited operation."
        ],
        preview_read_only=False,
        explicit_confirm_and_write=False,
        exact_form_binding=False,
        selected_project_binding=False,
        form_change_invalidates=False,
        source_evidence_change_invalidates=False,
        target_change_invalidates=False,
        project_root_change_invalidates=False,
        public_contract_confirmation_check=False,
        public_contract_root_binding_check=False,
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_record(record: Mapping[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    _assert(not missing, "Q30 record missing fields: " + ", ".join(missing))
    _assert(record["decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q30 decision")
    _assert(record["automatic_error_memory_promotion"] is False, "Automatic Error Memory promotion is forbidden")
    _assert(record["automatic_freeze_memory_write"] is False, "Automatic frozen-memory write is forbidden")
    _assert(record["may_begin_coding"] is False, "Q30 may not authorize coding")
    _assert(record["may_write_source"] is False, "Q30 may not authorize source writing")
    _assert(bool(record["primary_box"]), "Q30 primary box is required")
    _assert(bool(record["canonical_owner"]), "Q30 canonical owner is required")
    _assert(not record["unresolved_fields"], "Q30 unresolved fields remain")
    if record["decision"] == "COMPLETE":
        _assert(record["protection_required"] is True, "COMPLETE requires protection")
        for field in _REQUIRED_TRUE:
            _assert(record[field] is True, "Q30 protection missing: " + field)
        _assert(len(record["validators"]) >= 2, "Focused and real-Qt validators are required")
        _assert(len(record["expected_markers"]) >= 2, "Focused and real-Qt markers are required")
    elif record["decision"] == "NOT_APPLICABLE":
        _assert(record["protection_required"] is False, "N/A must not claim required protection")
        _assert(bool(record["no_protection_evidence"]), "N/A requires evidence")
        _assert(record["q29_decision_complete"] is True, "Q29 baseline is required")
        _assert(record["may_proceed_to_q31"] is True, "Evidence-backed N/A may proceed to Q31")
    else:
        _assert(record["may_proceed_to_q31"] is False, "BLOCKED may not proceed to Q31")
