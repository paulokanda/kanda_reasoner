"""Validate Brick Wall Q22 public-facade and contract-drift governance."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Callable, Sequence

from brick_wall_q22_public_facade_contract import (
    mutated_record,
    run_isolated_facade_fixture,
    validate_record,
    valid_not_applicable_record,
    valid_required_record,
)

__all__: list[str] = []

FEATURE_ID = "brick-wall-q22-public-facade-contract-drift-enforcement-v1"
BRICK_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md")
BRIDGE_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
BRICK_META_REL = Path("kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json")
BRIDGE_META_REL = Path("kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json")
Q09_REL = Path("tools/validate_brick_wall_q09_public_contract_communication_v1.py")
Q19_REL = Path("tools/validate_brick_wall_q19_real_qt_qsignalspy_decision_v1.py")
Q20_REL = Path("tools/validate_brick_wall_q20_shared_isolated_filesystem_fixtures_v1.py")
Q21_REL = Path("tools/validate_brick_wall_q21_parametrized_negative_boundary_matrix_v1.py")
Q22_CONTRACT_REL = Path("tools/brick_wall_q22_public_facade_contract.py")
Q22_VALIDATOR_REL = Path("tools/validate_brick_wall_q22_public_facade_contract_drift_v1.py")
WORKFLOW_FACADE_REL = Path("kanda_reasoner_app/manage_workflows/manage_workflows_gui.py")
WORKFLOW_PACKAGE_REL = Path("kanda_reasoner_app/manage_workflows/__init__.py")
CONSUMER_COMPAT_REL = Path("kanda_reasoner_app/manage_architecture/large_file_refactor_planner/facade_consumer_compatibility.py")
GRIFFE_SURFACE_REL = Path("kanda_reasoner_app/manage_architecture/large_file_refactor_planner/griffe_public_surface.py")
AQR_VALIDATOR_REL = Path("tools/validate_aqr_griffe_alias_preview_facade_consumer_compatibility_repair_v1.py")
ERROR_MEMORY_IMPORT_VALIDATOR_REL = Path("scripts/validate_error_memory_gui_mixin_import_surface_repair_v1.py")
PUBLIC_OWNER_VALIDATOR_REL = Path("scripts/validate_architecture_warning_cleanup_batch21_public_api_facade_ownership_v1.py")

BRICK_MARKERS = (
    "### Public-facade and contract-drift tests (Q22)",
    "PUBLIC-FACADE AND CONTRACT-DRIFT TEST RECORD",
    "canonical import path",
    "signature/defaults/annotations/docstring policy",
    "fallback preserved",
    "no private reach-in or duplicate public ownership",
    "proceed to Q23 deterministic MCard transition tests YES/NO",
    "all applicable pre-code items",
    "complete YES/NO",
)
BRIDGE_MARKERS = (
    "## Public-facade and contract-drift tests gate (Q22)",
    "Q22 public-facade and contract-drift test record complete: YES / NO",
    "May proceed to Q23 deterministic MCard transition tests gate: YES / NO",
    "## Public-facade and contract-drift bridge",
    "Package-root assumptions, contract drift, fallback loss",
)
OWNER_MARKERS = {
    Q09_REL: (
        "Q09_NEGATIVE_PRIVATE_REACH_IN",
        "Q09_NEGATIVE_PACKAGE_ROOT_ASSUMPTION",
        "Q09_NEGATIVE_CONSUMER_SUBSET",
        "Q09_NEGATIVE_PRIVATE_ALL_REEXPORT",
    ),
    CONSUMER_COMPAT_REL: (
        "build_facade_consumer_compatibility_report",
        "FACADE_CONSUMER_STAR_IMPORT_REQUIRES_MANUAL_REVIEW",
        "FACADE_CONSUMER_COMPATIBILITY_REEXPORTS_REQUIRED",
    ),
    GRIFFE_SURFACE_REL: (
        "child_public_override",
        "explicit_export",
        "kind == \"alias\"",
    ),
    AQR_VALIDATOR_REL: (
        "GRIFFE_EXPLICIT_ALIAS_EXPORT_REMAINS_PUBLIC",
        "FACADE_CONSUMER_STAR_IMPORT_FAILS_CLOSED",
        "CURRENT_AQR_MYPY_FIVE_MISSING_FACADE_SYMBOLS_DISCOVERED",
    ),
    ERROR_MEMORY_IMPORT_VALIDATOR_REL: (
        "lesson_from_current_windows_or_selection",
        "Preserve the prior import-surface repair",
    ),
    PUBLIC_OWNER_VALIDATOR_REL: (
        "validate_provider_empty_public_surface",
        "validate_facade_alias_pattern",
        "DUPLICATE_PUBLIC_SYMBOL",
    ),
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _parse_version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError:
        return ()


def _precode_gate_at_least(text: str, minimum_gate: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",
        text,
        re.DOTALL,
    )
    return bool(match and match.group(1) == match.group(2) and int(match.group(1)) >= minimum_gate)


def _literal_all(text: str) -> list[str]:
    for node in ast.parse(text).body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value = node.value
        else:
            continue
        if any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
            if not isinstance(value, (ast.List, ast.Tuple)):
                raise AssertionError("Q22 __all__ is not literal")
            return [
                item.value
                for item in value.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            ]
    return []


def validate_source(root: Path) -> None:
    """Validate Q22 prompts, metadata, owners, and forward compatibility."""
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q22_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q22_ROUTER_BRIDGE_CONTRACT")
    _gate("Q22_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (3, 2))
    _gate("Q22_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 6))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        _gate(
            "Q22_METADATA_ALIGNMENT",
            isinstance(stage, str) and stage == meta.get("updated_for"),
            label,
        )
    _gate("Q22_PRECODE_PROGRESSION", _precode_gate_at_least(brick, 22))
    _gate("Q22_FORWARD_COMPATIBLE_Q23_PRECODE_PROGRESSION", _precode_gate_at_least(brick, 23))
    for rel, markers in OWNER_MARKERS.items():
        _require(_read(root / rel), markers, "Q22_EXISTING_FACADE_OWNER")
    workflow_facade = _read(root / WORKFLOW_FACADE_REL)
    workflow_package = _read(root / WORKFLOW_PACKAGE_REL)
    exports = _literal_all(workflow_facade)
    _gate("Q22_WORKFLOW_PUBLIC_ENTRYPOINT", "WorkflowManagerWindow" in exports)
    _gate(
        "Q22_WORKFLOW_PACKAGE_ROOT_NOT_ASSUMED",
        "WorkflowManagerWindow" not in _literal_all(workflow_package)
        and "WorkflowManagerWindow" not in workflow_package,
    )
    _gate(
        "Q22_WORKFLOW_PRIVATE_PROVIDER_FACADE_ONLY",
        "from .manage_workflows_gui_help import (" in workflow_facade,
    )
    _gate(
        "Q22_FORWARD_COMPATIBLE_PREVIOUS_GATES",
        all(
            marker in _read(root / rel)
            for rel, marker in (
                (Q19_REL, "_precode_gate_at_least(brick, 19)"),
                (Q20_REL, "_precode_gate_at_least(brick, 20)"),
                (Q21_REL, "_precode_gate_at_least(brick, 21)"),
            )
        ),
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q19_REL,
        Q20_REL,
        Q21_REL,
        Q22_CONTRACT_REL,
        Q22_VALIDATOR_REL,
        *OWNER_MARKERS,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q22_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


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
    """Exercise positive, N/A, and negative Q22 record semantics."""
    validate_record(valid_required_record())
    _gate("Q22_REQUIRED_FACADE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q22_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        ("Q22_NEGATIVE_DUPLICATE_CASE", lambda r: r["cases"].append(dict(r["cases"][0]))),
        ("Q22_NEGATIVE_PACKAGE_ROOT_ASSUMPTION", lambda r: r["cases"][0].update(canonical_import_path="kanda_reasoner_app.manage_workflows.WorkflowManagerWindow")),
        ("Q22_NEGATIVE_PUBLIC_SYMBOLS_MISSING", lambda r: r["cases"][0].update(public_symbols=[])),
        ("Q22_NEGATIVE_SIGNATURE_POLICY", lambda r: r["cases"][0].update(signature_policy="NONE")),
        ("Q22_NEGATIVE_FALLBACK_EVIDENCE", lambda r: r["cases"][0].update(fallback_evidence=[])),
        ("Q22_NEGATIVE_REQUIRED_CONSUMER_MISSING", lambda r: r["cases"][1].update(current_consumers=[])),
        ("Q22_NEGATIVE_PRIVATE_REACH_IN", lambda r: r["cases"][1].update(current_consumer_imports=["kanda_reasoner_app.manage_architecture.large_file_refactor_planner._private_facade_consumer"])),
        ("Q22_NEGATIVE_DUPLICATE_PUBLIC_OWNER", lambda r: r["cases"][1].update(duplicate_public_owners=["private helper"])),
        ("Q22_NEGATIVE_VALIDATOR_MARKERS_MISSING", lambda r: r["cases"][0].update(expected_markers=[])),
        ("Q22_NEGATIVE_Q23_PROGRESSION", lambda r: r.update(may_proceed_to_q23=False)),
        ("Q22_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q22_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
    ]
    for label, mutate in tests:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_test_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q22_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q22_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q22_PUBLIC_FACADE_CONTRACT_DRIFT_REGRESSION_SET: PASS")


def validate_runtime_fixture() -> None:
    run_isolated_facade_fixture()
    print("Q22_CANONICAL_IMPORT_FIXTURE: PASS")
    print("Q22_SIGNATURE_DEFAULT_ANNOTATION_DOCSTRING_DRIFT: PASS")
    print("Q22_FALLBACK_PRESERVATION_FIXTURE: PASS")
    print("Q22_REQUIRED_CONSUMER_SUBSET_FIXTURE: PASS")
    print("Q22_PRIVATE_DEPENDENCY_REJECTION_FIXTURE: PASS")
    print("Q22_DUPLICATE_PUBLIC_OWNER_REJECTION_FIXTURE: PASS")
    print("Q22_RUNTIME_PUBLIC_FACADE_CONTRACT_DRIFT: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_contract()
    validate_runtime_fixture()
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
