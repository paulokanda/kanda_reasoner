"""Validate Brick Wall Q20 shared isolated filesystem fixture governance."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from collections.abc import Callable, Sequence
import json
import re
from pathlib import Path

from brick_wall_q20_isolated_filesystem_fixture import (
    expected_external_root_read_only,
    isolated_filesystem_fixture,
    snapshot_path,
)
from brick_wall_q20_isolated_filesystem_fixture_contract import (
    mutated_record,
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q20-shared-isolated-filesystem-fixtures-enforcement-v1"
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
Q19_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q19_real_qt_qsignalspy_decision_v1.py"
)
Q20_FIXTURE_REL = Path("tools/brick_wall_q20_isolated_filesystem_fixture.py")
Q20_CONTRACT_REL = Path(
    "tools/brick_wall_q20_isolated_filesystem_fixture_contract.py"
)
Q20_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q20_shared_isolated_filesystem_fixtures_v1.py"
)
WORKBENCH_FIXTURE_REL = Path(
    "tools/workbench_support_boundary_validation_fixture.py"
)
WORKBENCH_V3_REL = Path(
    "tools/validate_large_file_refactor_workbench_project_support_boundary_v3.py"
)
NESTED_SUPPORT_REL = Path(
    "tools/validate_project_tool_boundary_nested_support_root_v1.py"
)
PATCH5_PROOF_REL = Path(
    "tools/validate_workbench_patch5_executor_proof_status_projection_v1.py"
)
PATCH6_SUPPORT_REL = Path("tools/patch6_controlled_real_module_support.py")
TRANSIENT_WIDGET_REL = Path(
    "tools/validate_real_widget_observability_transient_fixture_v1.py"
)

BRICK_MARKERS = (
    "### Shared isolated filesystem fixtures (Q20)",
    "SHARED ISOLATED FILESYSTEM FIXTURE RECORD",
    "synthetic validators must not mutate real source, support, transient, or drive-root locations",
    "proceed to Q21 parametrized negative boundary matrix YES/NO",
)
BRIDGE_MARKERS = (
    "## Shared isolated filesystem fixtures gate (Q20)",
    "Q20 shared isolated filesystem fixture record complete: YES / NO",
    "May proceed to Q21 parametrized negative boundary matrix gate: YES / NO",
    "## Shared isolated filesystem fixture bridge",
    "no production path may appear in fixture write targets",
)
SHARED_FIXTURE_MARKERS = (
    "class IsolatedFilesystemLayout",
    "def isolated_filesystem_fixture(",
    "def expected_external_root_read_only(",
    "Q20_PROTECTED_PATH_MUTATED",
    "Q20_FIXTURE_CLEANUP_FAILED",
)
WORKBENCH_FIXTURE_MARKERS = (
    'support_base = sandbox / "_isolated_project_support"',
    'daily_base = sandbox / "_isolated_daily_work"',
    "with patch.object(",
)
WORKBENCH_V3_MARKERS = (
    "with TemporaryDirectory(prefix=\"kanda_support_boundary_\")",
    "with isolated_workbench_paths(",
    "WORKBENCH_VALIDATION_SUPPORT_ISOLATED: PASS",
    "WORKBENCH_VALIDATION_DAILY_WORK_ISOLATED: PASS",
    "WORKBENCH_DRIVE_ROOT_FIXTURE_STATE_UNCHANGED: PASS",
)
NESTED_SUPPORT_MARKERS = (
    "VALIDATION_DOES_NOT_CREATE_DRIVE_ROOT_SUPPORT_FIXTURE",
    "WINDOWS_DRIVE_ROOT_VALIDATION_FIXTURE_REGRESSION_BLOCKED",
    "FORBIDDEN_NESTED_PROJECT_SUPPORT_ROOT_CANON",
)
PATCH5_MARKERS = (
    "with tempfile.TemporaryDirectory(prefix=\"kanda_patch5_status_\")",
    'isolated_support_root = fixture_root / "isolated_project_support"',
    "production_state_before = _path_signature(production_support_root)",
    "PATCH5_VALIDATION_DRIVE_ROOT_FIXTURE_STATE_UNCHANGED",
)
PATCH6_MARKERS = (
    "CONTROLLED_VALIDATION_FIXTURE_OUTSIDE_TRANSIENT_GARBAGE_ROOT",
    'work_root = live_root.parent / f"{live_root.name}_delete_after_daily_work"',
    'controlled = work_root / "patch6_controlled_real"',
    'shadow = work_root / "patch6_controlled_shadow"',
)
TRANSIENT_WIDGET_MARKERS = (
    "CONTROLLED_VALIDATION_FIXTURES_UNDER_TRANSIENT_GARBAGE_ROOT",
    "NO_DRIVE_ROOT_SIBLING_CONTROLLED_FIXTURES",
)


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
    """Validate Q20 prompt, metadata, helper, and prior fixture owners."""
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q20_BRICK_WALL_CONTRACT")
    _gate(
        "Q20_FORWARD_COMPATIBLE_Q21_PRECODE_PROGRESSION",
        _precode_gate_at_least(brick, 20),
    )
    _require(bridge, BRIDGE_MARKERS, "Q20_ROUTER_BRIDGE_CONTRACT")
    _require(
        _read(root / Q20_FIXTURE_REL),
        SHARED_FIXTURE_MARKERS,
        "Q20_SHARED_FIXTURE_OWNER",
    )
    _require(
        _read(root / WORKBENCH_FIXTURE_REL),
        WORKBENCH_FIXTURE_MARKERS,
        "Q20_WORKBENCH_SCOPED_OWNER_OVERRIDES",
    )
    _require(
        _read(root / WORKBENCH_V3_REL),
        WORKBENCH_V3_MARKERS,
        "Q20_WORKBENCH_V3_ISOLATION_CONTRACT",
    )
    _require(
        _read(root / NESTED_SUPPORT_REL),
        NESTED_SUPPORT_MARKERS,
        "Q20_NESTED_AND_DRIVE_ROOT_GUARDS",
    )
    _require(
        _read(root / PATCH5_PROOF_REL),
        PATCH5_MARKERS,
        "Q20_PATCH5_PROOF_ISOLATION_CONTRACT",
    )
    _require(
        _read(root / PATCH6_SUPPORT_REL),
        PATCH6_MARKERS,
        "Q20_PATCH6_TRANSIENT_ROOT_CONTRACT",
    )
    _require(
        _read(root / TRANSIENT_WIDGET_REL),
        TRANSIENT_WIDGET_MARKERS,
        "Q20_CONTROLLED_WIDGET_FIXTURE_CONTRACT",
    )
    _gate("Q20_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (3, 0))
    _gate("Q20_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 4))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q20_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q19 = _read(root / Q19_VALIDATOR_REL)
    _gate(
        "Q19_FORWARD_COMPATIBLE_Q20_PRECODE_PROGRESSION",
        "Q19_FORWARD_COMPATIBLE_Q20_PRECODE_PROGRESSION" in q19
        and '_parse_version(brick_meta.get("version")) >= (2, 9)' in q19
        and '_parse_version(bridge_meta.get("version")) >= (3, 3)' in q19,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q19_VALIDATOR_REL,
        Q20_FIXTURE_REL,
        Q20_CONTRACT_REL,
        Q20_VALIDATOR_REL,
        WORKBENCH_FIXTURE_REL,
        WORKBENCH_V3_REL,
        NESTED_SUPPORT_REL,
        PATCH5_PROOF_REL,
        PATCH6_SUPPORT_REL,
        TRANSIENT_WIDGET_REL,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q20_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
        return
    _gate(label, False, "invalid record was accepted")


def validate_semantics() -> None:
    """Run required, N/A, and negative Q20 record tests."""
    validate_record(valid_required_record())
    _gate("Q20_REQUIRED_FIXTURE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q20_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        (
            "Q20_NEGATIVE_DUPLICATE_CASE",
            lambda record: record["cases"].append(record["cases"][0].copy()),
        ),
        (
            "Q20_NEGATIVE_FIXTURE_PATH_ABSOLUTE",
            lambda record: record["cases"][0].update(
                source_fixture_path="E:/synthetic_source"
            ),
        ),
        (
            "Q20_NEGATIVE_WRITE_OUTSIDE_FIXTURE",
            lambda record: record["cases"][0].update(
                write_targets=["<active_project_root>/bad.txt"]
            ),
        ),
        (
            "Q20_NEGATIVE_PRODUCTION_PATH_WRITABLE",
            lambda record: record["cases"][0].update(
                write_targets=["<canonical_project_support_root>"]
            ),
        ),
        (
            "Q20_NEGATIVE_BEFORE_SNAPSHOT_MISSING",
            lambda record: record["cases"][0].update(before_snapshots=[]),
        ),
        (
            "Q20_NEGATIVE_AFTER_SNAPSHOT_MISSING",
            lambda record: record["cases"][0].update(after_snapshots=[]),
        ),
        (
            "Q20_NEGATIVE_CLEANUP_POLICY",
            lambda record: record["cases"][0].update(cleanup_policy="NONE"),
        ),
        (
            "Q20_NEGATIVE_REAL_ROOT_MUTATION",
            lambda record: record["cases"][0].update(no_real_root_mutation=False),
        ),
        (
            "Q20_NEGATIVE_DRIVE_ROOT_CREATION",
            lambda record: record["cases"][0].update(no_drive_root_creation=False),
        ),
        (
            "Q20_NEGATIVE_SOURCE_TREE_FIXTURE",
            lambda record: record["cases"][0].update(no_source_tree_fixture=False),
        ),
        (
            "Q20_NEGATIVE_DURABLE_EVIDENCE_IN_TRANSIENT",
            lambda record: record["cases"][0].update(
                no_durable_evidence_in_transient=False
            ),
        ),
        (
            "Q20_NEGATIVE_PRODUCTION_FORMULA_WRITES",
            lambda record: record["cases"][0].update(
                cross_platform_formula_mode="CREATE_EXPECTED_ROOT"
            ),
        ),
        (
            "Q20_NEGATIVE_COPY_EXCLUSIONS",
            lambda record: record["cases"][0].update(copy_exclusions=[".git"]),
        ),
        (
            "Q20_NEGATIVE_Q21_PROGRESSION",
            lambda record: record.update(may_proceed_to_q21=False),
        ),
        (
            "Q20_NEGATIVE_CODING_AUTHORIZATION",
            lambda record: record.update(may_begin_coding=True),
        ),
        (
            "Q20_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
            lambda record: record.update(may_write_source=True),
        ),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    invalid_na = valid_not_applicable_record()
    invalid_na["no_fixture_evidence"] = []
    try:
        validate_record(invalid_na)
    except AssertionError:
        _gate("Q20_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q20_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    _gate("Q20_SHARED_ISOLATED_FILESYSTEM_FIXTURE_REGRESSION_SET", True)


def validate_runtime_fixture(root: Path) -> None:
    """Write only inside the shared sandbox and prove protected paths unchanged."""
    project_root = root.resolve(strict=True)
    support_root = expected_external_root_read_only(
        project_root,
        "_show_project_to_AI",
    )
    transient_root = expected_external_root_read_only(
        project_root,
        "_delete_after_daily_work",
    )
    forbidden_nested = project_root / (
        project_root.name + "_show_project_to_AI"
    )
    drive_probe = Path(project_root.anchor) / (
        ".kanda_q20_synthetic_probe_" + project_root.name
    )
    protected = (
        project_root / "ARCHITECTURE.md",
        project_root / BRICK_REL,
        forbidden_nested,
        support_root / ".q20_synthetic_probe",
        transient_root / ".q20_synthetic_probe",
        drive_probe,
    )
    before = tuple(snapshot_path(path) for path in protected)
    sandbox: Path | None = None
    with isolated_filesystem_fixture(protected_paths=protected) as layout:
        sandbox = layout.sandbox
        layout.assert_internal_and_distinct()
        (layout.source_root / "module.py").write_text(
            "VALUE = 'synthetic'\n",
            encoding="utf-8",
        )
        (layout.support_root / "preview.json").write_text(
            '{"synthetic": true}\n',
            encoding="utf-8",
        )
        (layout.transient_root / "shadow.py").write_bytes(b"VALUE = 1\n")
        (layout.durable_evidence_root / "evidence.txt").write_text(
            "Q20 synthetic evidence\n",
            encoding="utf-8",
        )
        _gate(
            "Q20_FIXTURE_ROOTS_PAIRWISE_DISTINCT",
            len(set(layout.writable_roots)) == 4,
        )
        _gate(
            "Q20_FIXTURE_WRITES_SANDBOX_ONLY",
            all(path.is_relative_to(layout.sandbox) for path in layout.writable_roots),
        )
        _gate(
            "Q20_DURABLE_EVIDENCE_OUTSIDE_TRANSIENT_FIXTURE",
            not layout.durable_evidence_root.is_relative_to(layout.transient_root),
        )
        _gate(
            "Q20_SYNTHETIC_SOURCE_OUTSIDE_ACTIVE_PROJECT",
            not layout.source_root.is_relative_to(project_root),
        )
        _gate(
            "Q20_PRODUCTION_FORMULAS_READ_ONLY",
            not (support_root / ".q20_synthetic_probe").exists()
            and not (transient_root / ".q20_synthetic_probe").exists()
            and not drive_probe.exists(),
        )
    _gate("Q20_SHARED_ISOLATED_FILESYSTEM_FIXTURE", sandbox is not None)
    _gate("Q20_FIXTURE_CLEANUP_VERIFIED", sandbox is not None and not sandbox.exists())
    after = tuple(snapshot_path(path) for path in protected)
    _gate("Q20_REAL_PATH_SNAPSHOTS_UNCHANGED", before == after)
    _gate("Q20_NO_DRIVE_ROOT_SYNTHETIC_FIXTURE", not drive_probe.exists())
    _gate("Q20_RUNTIME_FIXTURE_ISOLATION", True)


def run(root: Path) -> None:
    """Run the complete Q20 validator."""
    validate_source(root)
    validate_semantics()
    validate_runtime_fixture(root)
    print(
        "VALIDATION OK: "
        "brick-wall-q20-shared-isolated-filesystem-fixtures-enforcement-v1"
    )
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    run(Path(args.project_root).expanduser().resolve(strict=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
