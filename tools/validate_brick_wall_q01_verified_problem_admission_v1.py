"""Validate Q01 verified-problem admission enforcement for Brick Wall."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence


FEATURE_ID = "brick-wall-q01-verified-problem-admission-enforcement-v1"
BRICK_WALL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_WALL_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
BRIDGE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)

RECORD_FIELDS = (
    "Task classification:",
    "Change type: NEW_FEATURE / REPAIR_EXISTING / CONSOLIDATE / "
    "VALIDATOR_ONLY / NO_CHANGE",
    "Concrete problem:",
    "Evidence:",
    "Practical impact:",
    "Existing KANDA capability inspected:",
    "Why current capability is inadequate:",
    "Duplication or parallel-owner risk:",
    "Smallest adequate intervention:",
    "Expected measurable gain:",
    "Disconfirming evidence searched:",
    "Admission decision: ADMIT / REPAIR_EXISTING / CONSOLIDATE / "
    "NO_CHANGE / BLOCK",
    "May proceed to Error Memory preflight: YES / NO",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _parse_version(value: object) -> tuple[int, ...]:
    parts = str(value).strip().split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise AssertionError(f"invalid numeric version: {value}")
    return tuple(int(part) for part in parts)


def _gate(name: str, passed: bool, detail: str = "") -> None:
    if not passed:
        suffix = f" - {detail}" if detail else ""
        raise AssertionError(f"{name}: FAIL{suffix}")
    suffix = f" - {detail}" if detail else ""
    print(f"{name}: PASS{suffix}")


def _validate_source(project_root: Path) -> None:
    brick_path = project_root / BRICK_WALL_REL
    brick_meta_path = project_root / BRICK_WALL_META_REL
    bridge_path = project_root / BRIDGE_REL
    bridge_meta_path = project_root / BRIDGE_META_REL

    for path in (brick_path, brick_meta_path, bridge_path, bridge_meta_path):
        _gate("Q01_REQUIRED_FILE", path.is_file(), str(path))

    brick = _read_text(brick_path)
    bridge = _read_text(bridge_path)
    brick_meta = json.loads(_read_text(brick_meta_path))
    bridge_meta = json.loads(_read_text(bridge_meta_path))

    _gate(
        "Q01_VERIFIED_PROBLEM_RECORD",
        "VERIFIED PROBLEM RECORD" in brick
        and "VERIFIED PROBLEM RECORD" in bridge,
    )
    _gate(
        "Q01_RECORD_FIELD_SET",
        all(field in brick and field in bridge for field in RECORD_FIELDS),
    )
    _gate(
        "Q01_EXISTING_CAPABILITY_COMPARISON",
        "must name the current owner" in brick
        and "Inspect the current canonical owner" in bridge,
    )
    _gate(
        "Q01_DUPLICATION_RISK_GATE",
        "another scanner, schema, state owner, report, context engine" in brick
        and "parallel scanner, schema, state owner, report, context engine" in bridge,
    )
    _gate(
        "Q01_SMALLEST_INTERVENTION_GATE",
        "prefer repairing or consolidating" in brick
        and "Prefer `REPAIR_EXISTING` or `CONSOLIDATE`" in bridge,
    )
    _gate(
        "Q01_MEASURABLE_GAIN_GATE",
        "observable reliability, safety" in brick
        and "Expected measurable gain:" in bridge,
    )
    _gate(
        "Q01_DISCONFIRMATION_SEARCH",
        "Search for disconfirming evidence" in brick
        and "Disconfirming evidence searched:" in bridge,
    )
    _gate(
        "Q01_ADMISSION_DECISION_SET",
        all(
            decision in brick and decision in bridge
            for decision in (
                "ADMIT",
                "REPAIR_EXISTING",
                "CONSOLIDATE",
                "NO_CHANGE",
                "BLOCK",
            )
        ),
    )
    _gate(
        "Q01_ROUTER_BRIDGE_ENFORCEMENT",
        "If the record is incomplete or the decision is `BLOCK`" in bridge
        and "`May implement` must be" in bridge,
    )
    _gate(
        "Q01_IMPLEMENTATION_GATE_LINK",
        "Verified problem admission decision:" in bridge
        and "Q01 evidence complete: YES / NO" in bridge,
    )
    _gate(
        "Q01_NO_NEW_ENGINE_OR_SCHEMA",
        "Do not create a parallel scanner" in bridge
        and "another scanner, schema, state owner, report, context engine" in brick,
    )
    brick_version = _parse_version(brick_meta.get("version"))
    bridge_version = _parse_version(bridge_meta.get("version"))
    _gate(
        "Q01_VERSION_ALIGNMENT",
        f"version: {brick_meta.get('version')}" in brick
        and brick_version >= (1, 1)
        and f"version: {bridge_meta.get('version')}" in bridge
        and bridge_version >= (1, 4),
    )
    brick_stage = str(brick_meta.get("source_stage", "")).strip()
    bridge_stage = str(bridge_meta.get("source_stage", "")).strip()
    _gate(
        "Q01_METADATA_STAGE",
        bool(brick_stage)
        and bool(bridge_stage)
        and brick_meta.get("updated_for") == brick_stage
        and bridge_meta.get("updated_for") == bridge_stage,
    )

    validator_path = project_root / "tools/validate_brick_wall_q01_verified_problem_admission_v1.py"
    for path in (brick_path, bridge_path, validator_path):
        if not path.is_file():
            continue
        line_count = len(_read_text(path).splitlines())
        _gate("Q01_MODULE_SIZE", line_count <= 500, f"{path.name}={line_count}")


def _validate_patch_zip(project_root: Path, patch_zip: Path | None) -> None:
    if patch_zip is None:
        return
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.patch_governance.validator import validate_patch_zip

    report = validate_patch_zip(patch_zip, expect_freeze_hint=True)
    _gate("Q01_EXACT_ZIP_CONTRACT", report.get("ok") is True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip")
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).expanduser().resolve()
    patch_zip = (
        Path(args.patch_zip).expanduser().resolve()
        if args.patch_zip
        else None
    )

    try:
        _validate_source(project_root)
        _validate_patch_zip(project_root, patch_zip)
    except Exception as exc:
        print(f"Q01 VALIDATION ERROR: {type(exc).__name__}: {exc}")
        return 1

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
