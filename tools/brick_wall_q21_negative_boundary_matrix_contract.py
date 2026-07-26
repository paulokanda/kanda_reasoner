"""Semantic contract for Brick Wall Q21 negative boundary matrices."""

from __future__ import annotations

from copy import deepcopy
from typing import Mapping

__all__: list[str] = []

RECORD_FIELDS = {
    "identity_basis",
    "primary_box",
    "matrix_required",
    "no_matrix_evidence",
    "matrix_owner",
    "matrix_facade",
    "dimensions",
    "rows",
    "unresolved_dimensions",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_q22",
    "may_begin_coding",
    "may_write_source",
}

ROW_FIELDS = {
    "case_id",
    "project_mode",
    "path_variant",
    "lifecycle_generation",
    "worker_generation",
    "transaction_state",
    "confirmation_state",
    "expected_outcome",
    "expected_blockers",
    "canonical_validators",
    "expected_markers",
}

PROJECT_MODES = {"SELF_HOSTING", "EXTERNAL_PROJECT"}
PATH_VARIANTS = {
    "VALID_INSIDE_OWNER",
    "TRAVERSAL",
    "SIBLING_PREFIX",
    "ABSOLUTE_ESCAPE",
    "CROSS_DRIVE",
    "UNC_ESCAPE",
    "CASE_COLLISION",
    "LINK_ESCAPE",
}
LIFECYCLE_GENERATIONS = {"CURRENT", "STALE", "MISSING"}
WORKER_GENERATIONS = {"CURRENT", "STALE", "MISSING"}
TRANSACTION_STATES = {"CURRENT", "MISSING", "MISMATCHED", "CONSUMED"}
CONFIRMATION_STATES = {
    "CURRENT_EXPLICIT",
    "MISSING",
    "STALE",
    "BOOLEAN_BYPASS",
    "PREVIEW_ONLY",
}
EXPECTED_OUTCOMES = {"ALLOW_CONTROL", "BLOCK"}

NEGATIVE_PATHS = PATH_VARIANTS - {"VALID_INSIDE_OWNER"}
NEGATIVE_LIFECYCLE = LIFECYCLE_GENERATIONS - {"CURRENT"}
NEGATIVE_WORKER = WORKER_GENERATIONS - {"CURRENT"}
NEGATIVE_TRANSACTIONS = TRANSACTION_STATES - {"CURRENT"}
NEGATIVE_CONFIRMATIONS = CONFIRMATION_STATES - {"CURRENT_EXPLICIT"}


def _fields(mapping: Mapping[str, object], required: set[str]) -> None:
    missing = required.difference(mapping)
    extra = set(mapping).difference(required)
    if missing or extra:
        raise AssertionError(
            "Q21 field mismatch; missing="
            + repr(sorted(missing))
            + " extra="
            + repr(sorted(extra))
        )


def evaluate_row(row: Mapping[str, object]) -> set[str]:
    """Return the exact blocker set implied by one matrix row."""
    blockers: set[str] = set()
    path_variant = row["path_variant"]
    lifecycle = row["lifecycle_generation"]
    worker = row["worker_generation"]
    transaction = row["transaction_state"]
    confirmation = row["confirmation_state"]
    if path_variant != "VALID_INSIDE_OWNER":
        blockers.add("PATH_" + str(path_variant))
    if lifecycle != "CURRENT":
        blockers.add("LIFECYCLE_GENERATION_" + str(lifecycle))
    if worker != "CURRENT":
        blockers.add("WORKER_GENERATION_" + str(worker))
    if transaction != "CURRENT":
        blockers.add("TRANSACTION_" + str(transaction))
    if confirmation != "CURRENT_EXPLICIT":
        blockers.add("CONFIRMATION_" + str(confirmation))
    return blockers


def _validate_row(row: Mapping[str, object]) -> None:
    _fields(row, ROW_FIELDS)
    if row["project_mode"] not in PROJECT_MODES:
        raise AssertionError("Q21 unknown project mode")
    if row["path_variant"] not in PATH_VARIANTS:
        raise AssertionError("Q21 unknown path variant")
    if row["lifecycle_generation"] not in LIFECYCLE_GENERATIONS:
        raise AssertionError("Q21 unknown lifecycle generation")
    if row["worker_generation"] not in WORKER_GENERATIONS:
        raise AssertionError("Q21 unknown worker generation")
    if row["transaction_state"] not in TRANSACTION_STATES:
        raise AssertionError("Q21 unknown transaction state")
    if row["confirmation_state"] not in CONFIRMATION_STATES:
        raise AssertionError("Q21 unknown confirmation state")
    if row["expected_outcome"] not in EXPECTED_OUTCOMES:
        raise AssertionError("Q21 unknown expected outcome")
    blockers = evaluate_row(row)
    expected = set(row["expected_blockers"])
    if blockers != expected:
        raise AssertionError("Q21 expected blocker mismatch")
    outcome = "BLOCK" if blockers else "ALLOW_CONTROL"
    if row["expected_outcome"] != outcome:
        raise AssertionError("Q21 outcome does not match blockers")
    if not row["canonical_validators"] or not row["expected_markers"]:
        raise AssertionError("Q21 row requires validators and markers")


def _require_coverage(rows: list[Mapping[str, object]]) -> None:
    controls = [row for row in rows if not evaluate_row(row)]
    if {row["project_mode"] for row in controls} != PROJECT_MODES:
        raise AssertionError("Q21 requires one positive control per project mode")
    for variant in NEGATIVE_PATHS:
        if not any(row["path_variant"] == variant for row in rows):
            raise AssertionError("Q21 missing negative path: " + variant)
    for value in NEGATIVE_LIFECYCLE:
        if not any(row["lifecycle_generation"] == value for row in rows):
            raise AssertionError("Q21 missing lifecycle generation: " + value)
    for value in NEGATIVE_WORKER:
        if not any(row["worker_generation"] == value for row in rows):
            raise AssertionError("Q21 missing worker generation: " + value)
    for value in NEGATIVE_TRANSACTIONS:
        if not any(row["transaction_state"] == value for row in rows):
            raise AssertionError("Q21 missing transaction state: " + value)
    for value in NEGATIVE_CONFIRMATIONS:
        if not any(row["confirmation_state"] == value for row in rows):
            raise AssertionError("Q21 missing confirmation state: " + value)
    for mode in PROJECT_MODES:
        mode_rows = [row for row in rows if row["project_mode"] == mode]
        if not any(row["path_variant"] in NEGATIVE_PATHS for row in mode_rows):
            raise AssertionError("Q21 mode missing path negative: " + mode)
        if not any(
            row["lifecycle_generation"] in NEGATIVE_LIFECYCLE
            or row["worker_generation"] in NEGATIVE_WORKER
            for row in mode_rows
        ):
            raise AssertionError("Q21 mode missing generation negative: " + mode)
        if not any(
            row["transaction_state"] in NEGATIVE_TRANSACTIONS
            for row in mode_rows
        ):
            raise AssertionError("Q21 mode missing transaction negative: " + mode)
        if not any(
            row["confirmation_state"] in NEGATIVE_CONFIRMATIONS
            for row in mode_rows
        ):
            raise AssertionError("Q21 mode missing confirmation negative: " + mode)


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q21 record or evidence-backed N/A record."""
    _fields(record, RECORD_FIELDS)
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q21 cannot grant coding or source-write authority")
    required = bool(record["matrix_required"])
    decision = record["decision"]
    rows = record["rows"]
    if required:
        if decision != "COMPLETE" or not record["may_proceed_to_q22"]:
            raise AssertionError("Q21 required matrix must complete and proceed")
        if record["no_matrix_evidence"]:
            raise AssertionError("Q21 required record cannot carry N/A evidence")
        if not record["matrix_owner"] or not record["matrix_facade"]:
            raise AssertionError("Q21 matrix owner and facade are required")
        if record["unresolved_dimensions"] or record["blockers"]:
            raise AssertionError("Q21 required record remains blocked")
        if not isinstance(rows, list) or not rows:
            raise AssertionError("Q21 rows are required")
        ids: set[str] = set()
        for row in rows:
            _validate_row(row)
            case_id = str(row["case_id"])
            if case_id in ids:
                raise AssertionError("Q21 duplicate case id")
            ids.add(case_id)
        _require_coverage(rows)
        dimensions = set(record["dimensions"])
        required_dimensions = {
            "project_mode",
            "path_variant",
            "lifecycle_generation",
            "worker_generation",
            "transaction_state",
            "confirmation_state",
        }
        if dimensions != required_dimensions:
            raise AssertionError("Q21 dimension inventory mismatch")
        if not record["tests"]:
            raise AssertionError("Q21 tests are required")
        return
    if decision != "NOT_APPLICABLE" or record["may_proceed_to_q22"] is not True:
        raise AssertionError("Q21 N/A record must be explicit and proceed")
    if rows or not record["no_matrix_evidence"]:
        raise AssertionError("Q21 N/A record must have evidence and no rows")


def _row(
    case_id: str,
    mode: str,
    *,
    path: str = "VALID_INSIDE_OWNER",
    lifecycle: str = "CURRENT",
    worker: str = "CURRENT",
    transaction: str = "CURRENT",
    confirmation: str = "CURRENT_EXPLICIT",
) -> dict[str, object]:
    row = {
        "case_id": case_id,
        "project_mode": mode,
        "path_variant": path,
        "lifecycle_generation": lifecycle,
        "worker_generation": worker,
        "transaction_state": transaction,
        "confirmation_state": confirmation,
        "expected_outcome": "ALLOW_CONTROL",
        "expected_blockers": [],
        "canonical_validators": ["Q06", "Q12", "Q13", "Q16", "Q18"],
        "expected_markers": ["PASS or explicit rejection marker"],
    }
    blockers = sorted(evaluate_row(row))
    row["expected_blockers"] = blockers
    row["expected_outcome"] = "BLOCK" if blockers else "ALLOW_CONTROL"
    return row


def valid_required_record() -> dict[str, object]:
    """Return a complete parametrized Q21 boundary matrix record."""
    rows = [
        _row("control_self_hosting", "SELF_HOSTING"),
        _row("control_external", "EXTERNAL_PROJECT"),
    ]
    for index, variant in enumerate(sorted(NEGATIVE_PATHS)):
        mode = "SELF_HOSTING" if index % 2 == 0 else "EXTERNAL_PROJECT"
        rows.append(_row("path_" + variant.lower(), mode, path=variant))
    rows.extend(
        [
            _row("lifecycle_stale_self", "SELF_HOSTING", lifecycle="STALE"),
            _row("lifecycle_missing_external", "EXTERNAL_PROJECT", lifecycle="MISSING"),
            _row("worker_stale_external", "EXTERNAL_PROJECT", worker="STALE"),
            _row("worker_missing_self", "SELF_HOSTING", worker="MISSING"),
            _row("transaction_missing_self", "SELF_HOSTING", transaction="MISSING"),
            _row("transaction_mismatch_external", "EXTERNAL_PROJECT", transaction="MISMATCHED"),
            _row("transaction_consumed_self", "SELF_HOSTING", transaction="CONSUMED"),
            _row("confirmation_missing_external", "EXTERNAL_PROJECT", confirmation="MISSING"),
            _row("confirmation_stale_self", "SELF_HOSTING", confirmation="STALE"),
            _row("confirmation_boolean_external", "EXTERNAL_PROJECT", confirmation="BOOLEAN_BYPASS"),
            _row("confirmation_preview_self", "SELF_HOSTING", confirmation="PREVIEW_ONLY"),
        ]
    )
    return {
        "identity_basis": "current Q20 freeze and exact boundary validator inventory",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "matrix_required": True,
        "no_matrix_evidence": [],
        "matrix_owner": "tools/brick_wall_q21_negative_boundary_matrix_contract.py",
        "matrix_facade": "valid_required_record and validate_record",
        "dimensions": [
            "project_mode",
            "path_variant",
            "lifecycle_generation",
            "worker_generation",
            "transaction_state",
            "confirmation_state",
        ],
        "rows": rows,
        "unresolved_dimensions": [],
        "blockers": [],
        "tests": ["positive controls", "single-axis negatives", "mode coverage"],
        "decision": "COMPLETE",
        "may_proceed_to_q22": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return an evidence-backed Q21 not-applicable record."""
    record = valid_required_record()
    record.update(
        matrix_required=False,
        no_matrix_evidence=["no governed boundary behavior exists"],
        matrix_owner="",
        matrix_facade="",
        dimensions=[],
        rows=[],
        tests=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    """Return a deep copy suitable for focused negative mutations."""
    return deepcopy(valid_required_record())
