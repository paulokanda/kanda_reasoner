"""Validate Brick Wall Q21 parametrized negative boundary matrices."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from collections.abc import Callable, Sequence
import json
import re
from pathlib import Path

from brick_wall_q21_negative_boundary_matrix_contract import (
    CONFIRMATION_STATES,
    NEGATIVE_CONFIRMATIONS,
    NEGATIVE_LIFECYCLE,
    NEGATIVE_PATHS,
    NEGATIVE_TRANSACTIONS,
    NEGATIVE_WORKER,
    PROJECT_MODES,
    evaluate_row,
    mutated_record,
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q21-parametrized-negative-boundary-matrix-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / (
    "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_REL = PLIB / (
    "ACTIVE_PROMPTS/05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
Q20_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q20_shared_isolated_filesystem_fixtures_v1.py"
)
Q21_CONTRACT_REL = Path(
    "tools/brick_wall_q21_negative_boundary_matrix_contract.py"
)
Q21_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q21_parametrized_negative_boundary_matrix_v1.py"
)
Q06_REL = Path("tools/validate_brick_wall_q06_tool_project_identity_v1.py")
Q12_REL = Path("tools/validate_brick_wall_q12_immutable_operation_identity_v1.py")
Q13_REL = Path("tools/validate_brick_wall_q13_explicit_write_authorization_v1.py")
Q14_REL = Path("tools/validate_brick_wall_q14_immediate_pre_write_freshness_v1.py")
Q16_REL = Path("tools/validate_brick_wall_q16_resolved_path_containment_v1.py")
Q18_REL = Path("tools/validate_brick_wall_q18_stale_async_result_rejection_v1.py")

BRICK_MARKERS = (
    "### Parametrized negative boundary matrix (Q21)",
    "PARAMETRIZED NEGATIVE BOUNDARY MATRIX RECORD",
    "self-hosting and external-project controls",
    "path, generation, transaction, and confirmation-bypass negatives",
    "proceed to Q22 public-facade and contract-drift tests YES/NO",
)
BRIDGE_MARKERS = (
    "## Parametrized negative boundary matrix gate (Q21)",
    "Q21 parametrized negative boundary matrix record complete: YES / NO",
    "May proceed to Q22 public-facade and contract-drift tests gate: YES / NO",
    "## Parametrized negative boundary matrix bridge",
    "confirmation bypass must block even when paths are valid",
)
OWNER_MARKERS = {
    Q06_REL: (
        "Q06_SELF_HOSTING_IDENTITY_ACCEPTED",
        "Q06_EXTERNAL_PROJECT_IDENTITY_ACCEPTED",
    ),
    Q12_REL: (
        "Q12_NEGATIVE_TARGET_TRAVERSAL",
        "Q12_NEGATIVE_TRANSACTION_ID_MISSING",
        "Q12_NEGATIVE_GENERATION_MISMATCH",
        "Q12_NEGATIVE_SELF_HOSTING_COLLAPSE",
    ),
    Q13_REL: (
        "Q13_NEGATIVE_PATH_ONLY_AUTHORITY",
        "Q13_NEGATIVE_TRANSACTION_ID_MISSING",
        "Q13_NEGATIVE_HUMAN_AUTHORIZATION_MISSING",
        "Q13_NEGATIVE_GENERATION_MISMATCH",
    ),
    Q14_REL: (
        "Q14_NEGATIVE_TRAVERSAL_TARGET",
        "Q14_NEGATIVE_GENERATION_MISMATCH",
        "Q14_NEGATIVE_TRANSACTION_MISMATCH",
        "Q14_NEGATIVE_HUMAN_AUTHORITY_STALE",
    ),
    Q16_REL: (
        "Q16_NEGATIVE_TRAVERSAL_INPUT",
        "Q16_NEGATIVE_SIBLING_PREFIX",
        "Q16_NEGATIVE_CROSS_DRIVE",
        "Q16_NEGATIVE_UNC_SHARE_ESCAPE",
        "Q16_NEGATIVE_CASE_COLLISION",
        "Q16_NEGATIVE_LINK_ESCAPE",
    ),
    Q18_REL: (
        "Q18_NEGATIVE_GENERATION_MISSING",
        "Q18_NEGATIVE_LATE_RESULT_ACCEPTED",
        "Q18_NEGATIVE_STALE_SOURCE_WRITE",
    ),
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        suffix = " - " + detail if detail else ""
        raise AssertionError(label + ": FAIL" + suffix)
    print(label + ": PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _parse_version(value: object) -> tuple[int, ...]:
    if not isinstance(value, str):
        return ()
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        return ()


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _precode_gate_at_least(text: str, minimum_gate: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",
        text,
        re.DOTALL,
    )
    return bool(match and match.group(1) == match.group(2) and int(match.group(1)) >= minimum_gate)


def validate_source(root: Path) -> None:
    """Validate Q21 prompts, metadata, owners, and Q20 progression."""
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q21_BRICK_WALL_CONTRACT")
    _gate(
        "Q21_FORWARD_COMPATIBLE_Q22_PRECODE_PROGRESSION",
        _precode_gate_at_least(brick, 21),
    )
    _require(bridge, BRIDGE_MARKERS, "Q21_ROUTER_BRIDGE_CONTRACT")
    for rel, markers in OWNER_MARKERS.items():
        _require(_read(root / rel), markers, "Q21_EXISTING_BOUNDARY_OWNER")
    _gate("Q21_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (3, 1))
    _gate("Q21_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 5))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q21_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q20 = _read(root / Q20_VALIDATOR_REL)
    _gate(
        "Q20_FORWARD_COMPATIBLE_Q21_PRECODE_PROGRESSION",
        "Q20_FORWARD_COMPATIBLE_Q21_PRECODE_PROGRESSION" in q20
        and "_precode_gate_at_least(brick, 20)" in q20
        and '_parse_version(brick_meta.get("version")) >= (3, 0)' in q20
        and '_parse_version(bridge_meta.get("version")) >= (3, 4)' in q20,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q20_VALIDATOR_REL,
        Q21_CONTRACT_REL,
        Q21_VALIDATOR_REL,
        *OWNER_MARKERS,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q21_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_contract() -> None:
    """Exercise positive, N/A, and negative Q21 record semantics."""
    validate_record(valid_required_record())
    _gate("Q21_REQUIRED_MATRIX_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q21_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        (
            "Q21_NEGATIVE_DUPLICATE_CASE",
            lambda r: r["rows"].append(dict(r["rows"][0])),
        ),
        (
            "Q21_NEGATIVE_PROJECT_MODE_MISSING",
            lambda r: [row.update(project_mode="SELF_HOSTING") for row in r["rows"]],
        ),
        (
            "Q21_NEGATIVE_PATH_COVERAGE_MISSING",
            lambda r: [
                row.update(path_variant="VALID_INSIDE_OWNER", expected_blockers=[], expected_outcome="ALLOW_CONTROL")
                for row in r["rows"]
                if row["path_variant"] == "LINK_ESCAPE"
            ],
        ),
        (
            "Q21_NEGATIVE_LIFECYCLE_COVERAGE_MISSING",
            lambda r: [
                row.update(lifecycle_generation="CURRENT", expected_blockers=[], expected_outcome="ALLOW_CONTROL")
                for row in r["rows"]
                if row["lifecycle_generation"] == "MISSING"
            ],
        ),
        (
            "Q21_NEGATIVE_WORKER_COVERAGE_MISSING",
            lambda r: [
                row.update(worker_generation="CURRENT", expected_blockers=[], expected_outcome="ALLOW_CONTROL")
                for row in r["rows"]
                if row["worker_generation"] == "MISSING"
            ],
        ),
        (
            "Q21_NEGATIVE_TRANSACTION_COVERAGE_MISSING",
            lambda r: [
                row.update(transaction_state="CURRENT", expected_blockers=[], expected_outcome="ALLOW_CONTROL")
                for row in r["rows"]
                if row["transaction_state"] == "CONSUMED"
            ],
        ),
        (
            "Q21_NEGATIVE_CONFIRMATION_BYPASS_MISSING",
            lambda r: [
                row.update(confirmation_state="CURRENT_EXPLICIT", expected_blockers=[], expected_outcome="ALLOW_CONTROL")
                for row in r["rows"]
                if row["confirmation_state"] == "BOOLEAN_BYPASS"
            ],
        ),
        (
            "Q21_NEGATIVE_EXPECTED_BLOCKER_MISMATCH",
            lambda r: r["rows"][2].update(expected_blockers=[]),
        ),
        (
            "Q21_NEGATIVE_ALLOW_ON_BLOCKED_ROW",
            lambda r: r["rows"][2].update(expected_outcome="ALLOW_CONTROL"),
        ),
        (
            "Q21_NEGATIVE_VALIDATOR_EVIDENCE_MISSING",
            lambda r: r["rows"][2].update(canonical_validators=[]),
        ),
        (
            "Q21_NEGATIVE_DIMENSION_INVENTORY",
            lambda r: r.update(dimensions=["project_mode"]),
        ),
        (
            "Q21_NEGATIVE_Q22_PROGRESSION",
            lambda r: r.update(may_proceed_to_q22=False),
        ),
        (
            "Q21_NEGATIVE_CODING_AUTHORIZATION",
            lambda r: r.update(may_begin_coding=True),
        ),
        (
            "Q21_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
            lambda r: r.update(may_write_source=True),
        ),
    ]
    for label, mutate in tests:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_matrix_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q21_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q21_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    _gate("Q21_PARAMETRIZED_NEGATIVE_BOUNDARY_MATRIX_REGRESSION_SET", True)


def validate_runtime_matrix() -> None:
    """Prove deterministic matrix coverage and blocker evaluation."""
    record = valid_required_record()
    rows = record["rows"]
    controls = [row for row in rows if not evaluate_row(row)]
    _gate(
        "Q21_MATRIX_POSITIVE_CONTROLS",
        {row["project_mode"] for row in controls} == PROJECT_MODES,
    )
    for mode in PROJECT_MODES:
        mode_rows = [row for row in rows if row["project_mode"] == mode]
        _gate(
            "Q21_PROJECT_MODE_NEGATIVE_COVERAGE",
            any(evaluate_row(row) for row in mode_rows),
            mode,
        )
    _gate(
        "Q21_PATH_VARIANT_COVERAGE",
        NEGATIVE_PATHS.issubset({row["path_variant"] for row in rows}),
    )
    _gate(
        "Q21_GENERATION_VARIANT_COVERAGE",
        NEGATIVE_LIFECYCLE.issubset({row["lifecycle_generation"] for row in rows})
        and NEGATIVE_WORKER.issubset({row["worker_generation"] for row in rows}),
    )
    _gate(
        "Q21_TRANSACTION_VARIANT_COVERAGE",
        NEGATIVE_TRANSACTIONS.issubset({row["transaction_state"] for row in rows}),
    )
    _gate(
        "Q21_CONFIRMATION_BYPASS_COVERAGE",
        NEGATIVE_CONFIRMATIONS.issubset({row["confirmation_state"] for row in rows})
        and CONFIRMATION_STATES.issuperset(
            {row["confirmation_state"] for row in rows}
        ),
    )
    _gate(
        "Q21_EXPECTED_BLOCKERS_DETERMINISTIC",
        all(set(row["expected_blockers"]) == evaluate_row(row) for row in rows),
    )
    print("Q21_RUNTIME_PARAMETRIZED_MATRIX: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_contract()
    validate_runtime_matrix()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    run_validation(args.project_root.expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
