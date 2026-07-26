"""Validation-only Brick Wall Q26 ZIP hardening record contract."""
from __future__ import annotations

from copy import deepcopy
from typing import Mapping

__all__: list[str] = []
FEATURE_ID = "brick-wall-q26-zip-containment-collision-hardening-enforcement-v1"
PROTECTIONS = (
    "ABSOLUTE_PATH", "DRIVE_QUALIFIED_PATH", "UNC_PATH", "TRAVERSAL",
    "DUPLICATE_MEMBER", "WINDOWS_CASE_FOLD_COLLISION",
    "FILE_DIRECTORY_COLLISION", "UNEXPECTED_LINK", "UNDECLARED_INSTALL_PATH",
)
REQUIRED_FIELDS = (
    "hardening_required", "no_hardening_evidence", "q25_decision_complete",
    "primary_box", "canonical_owner", "public_facade", "private_helper",
    "exact_final_zip_required", "protections", "manifest_authority",
    "payload_namespace", "validators", "expected_markers", "unresolved_fields",
    "decision", "may_proceed_to_q27", "may_begin_coding", "may_write_source",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, *, empty: bool = False) -> bool:
    return isinstance(value, list) and (empty or bool(value)) and all(_text(item) for item in value)


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("Q26 record missing fields: " + ", ".join(missing))
    for field in (
        "hardening_required", "q25_decision_complete", "exact_final_zip_required",
        "may_proceed_to_q27", "may_begin_coding", "may_write_source",
    ):
        if not isinstance(record[field], bool):
            raise AssertionError("Q26 invalid boolean field: " + field)
    if record["decision"] not in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}:
        raise AssertionError("Q26 invalid decision")
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q26 cannot authorize coding or source writes")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]:
        raise AssertionError("Q26 remains blocked")
    if not record["may_proceed_to_q27"]:
        raise AssertionError("Q27 progression not approved")
    if not record["hardening_required"]:
        if record["decision"] != "NOT_APPLICABLE" or not _texts(record["no_hardening_evidence"]):
            raise AssertionError("Q26 N/A evidence incomplete")
        return
    if record["decision"] != "COMPLETE" or record["no_hardening_evidence"]:
        raise AssertionError("Q26 applicable decision incomplete")
    if not record["q25_decision_complete"] or not record["exact_final_zip_required"]:
        raise AssertionError("Q25 baseline or exact final ZIP requirement incomplete")
    for field in ("primary_box", "canonical_owner", "public_facade", "private_helper", "manifest_authority", "payload_namespace"):
        if not _text(record[field]):
            raise AssertionError("Q26 owner/authority field incomplete: " + field)
    if record["canonical_owner"] != "kanda_reasoner_app.patch_governance.validator":
        raise AssertionError("Q26 canonical owner drift")
    if record["public_facade"] != "kanda_reasoner_app.patch_governance.validate_patch_zip":
        raise AssertionError("Q26 public facade drift")
    if record["payload_namespace"] != "payload/":
        raise AssertionError("Q26 payload namespace drift")
    protections = record["protections"]
    if not isinstance(protections, list) or set(protections) != set(PROTECTIONS):
        raise AssertionError("Q26 protection inventory incomplete")
    if not _texts(record["validators"]) or not _texts(record["expected_markers"]):
        raise AssertionError("Q26 validator evidence incomplete")


def valid_complete_record() -> dict[str, object]:
    return {
        "hardening_required": True,
        "no_hardening_evidence": [],
        "q25_decision_complete": True,
        "primary_box": "kanda_reasoner_app/patch_governance",
        "canonical_owner": "kanda_reasoner_app.patch_governance.validator",
        "public_facade": "kanda_reasoner_app.patch_governance.validate_patch_zip",
        "private_helper": "kanda_reasoner_app.patch_governance.zip_member_contract",
        "exact_final_zip_required": True,
        "protections": list(PROTECTIONS),
        "manifest_authority": "root INSTALL_MANIFEST.json declares every payload/ file",
        "payload_namespace": "payload/",
        "validators": [
            "scripts/validate_patch_zip.py",
            "tools/validate_brick_wall_q26_zip_containment_collision_hardening_v1.py",
        ],
        "expected_markers": [
            "Q26_ZIP_MEMBER_CONTAINMENT: PASS",
            "Q26_ZIP_COLLISION_REJECTION: PASS",
            "Q26_ZIP_LINK_REJECTION: PASS",
            "Q26_ZIP_MANIFEST_DECLARATION: PASS",
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q27": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_complete_record()
    record.update(
        hardening_required=False,
        no_hardening_evidence=["No installable or downloadable ZIP is in task scope."],
        exact_final_zip_required=False,
        protections=[],
        validators=[],
        expected_markers=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    return deepcopy(valid_complete_record())
