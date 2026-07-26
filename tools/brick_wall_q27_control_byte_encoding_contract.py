"""Validation-only Brick Wall Q27 control-byte and encoding contract."""
from __future__ import annotations

from copy import deepcopy
from typing import Mapping

__all__: list[str] = []
FEATURE_ID = "brick-wall-q27-control-byte-encoding-guards-enforcement-v1"
ALLOWED_C0_CODES = (9, 10, 13)
LEGACY_READ_ENCODINGS = ("UTF-8", "UTF-8 BOM", "UTF-16LE BOM")
REQUIRED_FIELDS = (
    "guards_required",
    "no_guard_evidence",
    "q26_decision_complete",
    "primary_box",
    "evidence_reader",
    "operational_scripts",
    "output_encoding",
    "legacy_read_encodings",
    "allowed_c0_codes",
    "forbidden_control_bytes_rejected",
    "invalid_encoding_rejected",
    "safe_windows_path_generation",
    "validators",
    "expected_markers",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q28",
    "may_begin_coding",
    "may_write_source",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, *, empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (empty or bool(value))
        and all(_text(item) for item in value)
    )


def validate_powershell_bytes(data: bytes) -> None:
    """Reject hidden C0 bytes in governed PowerShell source."""
    for index, value in enumerate(data):
        if value < 32 and value not in ALLOWED_C0_CODES:
            raise AssertionError(
                f"POWERSHELL_FORBIDDEN_CONTROL_BYTE: 0x{value:02X} at byte {index}"
            )
    try:
        data.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError as exc:
        raise AssertionError("POWERSHELL_ENCODING_INVALID: " + str(exc)) from exc


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("Q27 record missing fields: " + ", ".join(missing))
    for field in (
        "guards_required",
        "q26_decision_complete",
        "forbidden_control_bytes_rejected",
        "invalid_encoding_rejected",
        "safe_windows_path_generation",
        "may_proceed_to_q28",
        "may_begin_coding",
        "may_write_source",
    ):
        if not isinstance(record[field], bool):
            raise AssertionError("Q27 invalid boolean field: " + field)
    if record["decision"] not in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}:
        raise AssertionError("Q27 invalid decision")
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q27 cannot authorize coding or source writes")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]:
        raise AssertionError("Q27 remains blocked")
    if not record["may_proceed_to_q28"]:
        raise AssertionError("Q28 progression not approved")
    if not record["guards_required"]:
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("Q27 N/A decision incomplete")
        if not _texts(record["no_guard_evidence"]):
            raise AssertionError("Q27 N/A evidence incomplete")
        return
    if record["decision"] != "COMPLETE" or record["no_guard_evidence"]:
        raise AssertionError("Q27 applicable decision incomplete")
    if not record["q26_decision_complete"]:
        raise AssertionError("Q26 baseline incomplete")
    for field in ("primary_box", "evidence_reader", "output_encoding"):
        if not _text(record[field]):
            raise AssertionError("Q27 owner/encoding field incomplete: " + field)
    if record["evidence_reader"] != "scripts/merge_freeze_validation_evidence.py":
        raise AssertionError("Q27 evidence reader drift")
    if record["output_encoding"] != "UTF-8 without BOM":
        raise AssertionError("Q27 output encoding drift")
    if tuple(record["legacy_read_encodings"]) != LEGACY_READ_ENCODINGS:
        raise AssertionError("Q27 legacy encoding inventory incomplete")
    if tuple(record["allowed_c0_codes"]) != ALLOWED_C0_CODES:
        raise AssertionError("Q27 allowed C0 inventory incomplete")
    scripts = record["operational_scripts"]
    if set(scripts) != {"INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"}:
        raise AssertionError("Q27 operational script inventory incomplete")
    for field in (
        "forbidden_control_bytes_rejected",
        "invalid_encoding_rejected",
        "safe_windows_path_generation",
    ):
        if not record[field]:
            raise AssertionError("Q27 protection incomplete: " + field)
    if not _texts(record["validators"]) or not _texts(record["expected_markers"]):
        raise AssertionError("Q27 validator evidence incomplete")


def valid_complete_record() -> dict[str, object]:
    return {
        "guards_required": True,
        "no_guard_evidence": [],
        "q26_decision_complete": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "evidence_reader": "scripts/merge_freeze_validation_evidence.py",
        "operational_scripts": ["INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"],
        "output_encoding": "UTF-8 without BOM",
        "legacy_read_encodings": list(LEGACY_READ_ENCODINGS),
        "allowed_c0_codes": list(ALLOWED_C0_CODES),
        "forbidden_control_bytes_rejected": True,
        "invalid_encoding_rejected": True,
        "safe_windows_path_generation": True,
        "validators": [
            "tools/validate_brick_wall_q27_control_byte_encoding_guards_v1.py",
            "scripts/merge_freeze_validation_evidence.py",
        ],
        "expected_markers": [
            "Q27_UTF8_OUTPUT: PASS",
            "Q27_BOM_AWARE_LEGACY_READS: PASS",
            "Q27_UTF16LE_FIXTURE: PASS",
            "Q27_CONTROL_BYTE_REJECTION: PASS",
            "Q27_SAFE_WINDOWS_PATH_GENERATION: PASS",
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q28": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_complete_record()
    record.update(
        guards_required=False,
        no_guard_evidence=[
            "No PowerShell delivery or persisted validation evidence is in task scope."
        ],
        operational_scripts=[],
        legacy_read_encodings=[],
        allowed_c0_codes=[],
        forbidden_control_bytes_rejected=False,
        invalid_encoding_rejected=False,
        safe_windows_path_generation=False,
        validators=[],
        expected_markers=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    return deepcopy(valid_complete_record())
