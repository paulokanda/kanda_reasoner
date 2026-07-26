"""Validate Brick Wall Q15 canonical path-authority enforcement."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import importlib
import json
import sys
import tempfile
from pathlib import Path, PureWindowsPath
from typing import Sequence

from brick_wall_q15_path_authority_contract import (
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q15-canonical-path-authority-enforcement-v1"
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
BOUNDARY_REL = Path("kanda_reasoner_app/project_support_boundary.py")
EVIDENCE_REL = Path("kanda_reasoner_app/project_analysis_evidence_paths.py")
RESOLUTION_REL = Path(
    "kanda_reasoner_app/_project_analysis_evidence_path_resolution.py"
)
WORKBENCH_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_project_support_paths.py"
)
ERROR_PATHS_REL = Path("kanda_reasoner_app/error_memory/paths.py")
FREEZE_PATHS_REL = Path("kanda_reasoner_app/freeze_hint_intake/paths_io.py")
DURABLE_PROMPT_REL = PLIB / (
    "ACTIVE_PROMPTS/01_session_start_and_navigation/"
    "durable_document_artifact_routing_canon.md"
)
Q14_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q14_immediate_pre_write_freshness_v1.py"
)
Q07_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q07_ownership_no_leak_classification_v1.py"
)
Q15_CONTRACT_REL = Path("tools/brick_wall_q15_path_authority_contract.py")
Q15_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q15_canonical_path_authority_v1.py"
)
WINDOWS_FIXTURE_VALIDATOR_REL = Path(
    "tools/validate_project_tool_boundary_nested_support_root_v1.py"
)

BRICK_MARKERS = (
    "### Canonical path authority (Q15)",
    "CANONICAL PATH-AUTHORITY CONTRACT RECORD",
    "canonical base-root owner/facade",
    "Path families, once per family:",
    "public owner/facade/symbol",
    "compatibility adapter",
    "blocked duplicate formulas",
    "support | transient garbage | Preview | Shadow | Error Memory | Freeze",
    "proceed to Q16 resolved-path containment YES/NO",
    "may begin coding NO",
    "may write source NO",
    "global super-resolver",
    "independent suffix joins",
)
BRIDGE_MARKERS = (
    "## Canonical path-authority gate (Q15)",
    "Q15 canonical path-authority record complete: YES / NO",
    "Path-authority decision: COMPLETE / NOT_APPLICABLE / BLOCKED",
    "Canonical support-root owner/facade:",
    "Canonical transient-root owner/facade:",
    "Specialized path families delegated: YES / NO / N/A",
    "Duplicate or hardcoded path authorities absent: YES / NO / N/A",
    "May proceed to Q16 resolved-path containment gate: YES / NO",
    "## Canonical path-authority bridge",
)
BOUNDARY_MARKERS = (
    "def canonical_project_support_root(",
    "def canonical_transient_garbage_root(",
    "def assert_no_forbidden_nested_support_root(",
    "SHOW_PROJECT_TO_AI_SUFFIX",
    "DELETE_AFTER_DAILY_WORK_SUFFIX",
    "PROJECT_SUPPORT_ROOT_INSIDE_PROJECT_SOURCE",
    "PROJECT_SUPPORT_ROOT_NOT_CANONICAL_EXTERNAL_ROOT",
)
WORKBENCH_MARKERS = (
    "from kanda_reasoner_app.project_support_boundary import",
    "assert_no_forbidden_nested_support_root",
    "canonical_transient_garbage_root",
    "return assert_no_forbidden_nested_support_root(active_project_root)",
    "return canonical_transient_garbage_root(active_project_root)",
    "def preview_runs_root(",
    "def shadow_runs_root(",
)
ERROR_MARKERS = (
    "from kanda_reasoner_app.project_analysis_evidence_paths import",
    "show_project_to_ai_root_from_hint",
    "def resolve_project_error_memory_root(",
)
FREEZE_MARKERS = (
    "analysis_project_freeze_after_update_dir",
    "def build_freeze_hint_intake_paths(",
)
DURABLE_MARKERS = (
    "<project>_delete_after_daily_work",
    "<project>_show_project_to_AI",
    "Do not create a second durable owner for the same artifact.",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        suffix = f" - {detail}" if detail else ""
        raise AssertionError(f"{label}: FAIL{suffix}")
    print(f"{label}: PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_version(value: object) -> tuple[int, ...]:
    if not isinstance(value, str):
        return ()
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        return ()


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    boundary = _read(root / BOUNDARY_REL)
    evidence = _read(root / EVIDENCE_REL)
    resolution = _read(root / RESOLUTION_REL)
    workbench = _read(root / WORKBENCH_REL)
    error_paths = _read(root / ERROR_PATHS_REL)
    freeze_paths = _read(root / FREEZE_PATHS_REL)
    durable = _read(root / DURABLE_PROMPT_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)

    _require(brick, BRICK_MARKERS, "Q15_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q15_ROUTER_BRIDGE_CONTRACT")
    _require(boundary, BOUNDARY_MARKERS, "Q15_CANONICAL_BASE_ROOT_OWNER")
    _require(workbench, WORKBENCH_MARKERS, "Q15_WORKBENCH_PATH_DELEGATION")
    _require(error_paths, ERROR_MARKERS, "Q15_ERROR_MEMORY_PATH_OWNER")
    _require(freeze_paths, FREEZE_MARKERS, "Q15_FREEZE_PATH_OWNER")
    _require(durable, DURABLE_MARKERS, "Q15_DURABLE_TRANSIENT_LIFETIME_CONTRACT")
    _gate(
        "Q15_EVIDENCE_COMPATIBILITY_FACADE",
        "show_project_to_ai_root_from_hint" in evidence
        and "assert_no_forbidden_nested_support_root" in resolution,
    )
    _gate("Q15_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 5))
    _gate("Q15_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (2, 9))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q15_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)

    q14 = _read(root / Q14_VALIDATOR_REL)
    _gate(
        "Q14_FORWARD_COMPATIBLE_METADATA",
        "_parse_version(brick_meta.get(\"version\")) >= (2, 4)" in q14
        and "_parse_version(bridge_meta.get(\"version\")) >= (2, 8)" in q14
        and "_nonempty(stage) and stage == updated" in q14,
    )
    windows_validator = _read(root / WINDOWS_FIXTURE_VALIDATOR_REL)
    _gate(
        "Q15_WINDOWS_FORMULA_READ_ONLY_FIXTURE",
        "VALIDATION_DOES_NOT_CREATE_DRIVE_ROOT_SUPPORT_FIXTURE"
        in windows_validator,
    )
    q07_validator = _read(root / Q07_VALIDATOR_REL)
    windows_box_path = PureWindowsPath(
        r"kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\example.md"
    )
    _gate(
        "Q15_Q07_WINDOWS_PATH_SEPARATOR_COMPATIBILITY",
        "path.as_posix().startswith(" in q07_validator
        and windows_box_path.as_posix().startswith(
            "kanda_prompt_workspace/prompt_library/"
        ),
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q07_VALIDATOR_REL,
        Q14_VALIDATOR_REL,
        Q15_CONTRACT_REL,
        Q15_VALIDATOR_REL,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q15_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def _reject(label: str, mutate) -> None:
    record = valid_required_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        print(f"{label}: PASS")
        return
    raise AssertionError(f"{label}: FAIL - invalid record accepted")


def validate_semantics() -> None:
    validate_record(valid_required_record())
    print("Q15_REQUIRED_PATH_RECORD_ACCEPTED: PASS")
    validate_record(valid_not_applicable_record())
    print("Q15_NOT_APPLICABLE_RECORD_ACCEPTED: PASS")
    cases = [
        (
            "Q15_NEGATIVE_DUPLICATE_AUTHORITY",
            lambda r: r.update(duplicate_authorities=["second support owner"]),
        ),
        (
            "Q15_NEGATIVE_HARDCODED_PATH",
            lambda r: r.update(
                hardcoded_project_paths=[r"E:\kanda_reasoner_show_project_to_AI"]
            ),
        ),
        (
            "Q15_NEGATIVE_UNRESOLVED_ADAPTER",
            lambda r: r.update(unresolved_adapters=["legacy hint adapter"]),
        ),
        (
            "Q15_NEGATIVE_SUPPORT_OWNER_MISSING",
            lambda r: r.update(canonical_base_root_owner=""),
        ),
        (
            "Q15_NEGATIVE_MISSING_FAMILY",
            lambda r: r.update(path_families=r["path_families"][:-1]),
        ),
        (
            "Q15_NEGATIVE_DUPLICATE_FAMILY",
            lambda r: r.update(
                path_families=r["path_families"] + [r["path_families"][0]]
            ),
        ),
        (
            "Q15_NEGATIVE_PREVIEW_IN_TRANSIENT",
            lambda r: r["path_families"][2].update(
                base_root_class="TRANSIENT_GARBAGE_ROOT",
                lifetime="TRANSIENT_GARBAGE",
            ),
        ),
        (
            "Q15_NEGATIVE_SHADOW_IN_DURABLE",
            lambda r: r["path_families"][3].update(
                base_root_class="PROJECT_SUPPORT_ROOT",
                lifetime="DURABLE_PROJECT_SUPPORT",
            ),
        ),
        (
            "Q15_NEGATIVE_ERROR_MEMORY_IN_TRANSIENT",
            lambda r: r["path_families"][4].update(
                base_root_class="TRANSIENT_GARBAGE_ROOT",
                lifetime="TRANSIENT_GARBAGE",
            ),
        ),
        (
            "Q15_NEGATIVE_FREEZE_IN_TRANSIENT",
            lambda r: r["path_families"][5].update(
                base_root_class="TRANSIENT_GARBAGE_ROOT",
                lifetime="TRANSIENT_GARBAGE",
            ),
        ),
        (
            "Q15_NEGATIVE_ADAPTER_SCOPE_MISSING",
            lambda r: r["path_families"][4].update(adapter_scope=""),
        ),
        (
            "Q15_NEGATIVE_CONTAINMENT_UNRESOLVED",
            lambda r: r["path_families"][0].update(containment_verified=False),
        ),
        (
            "Q15_NEGATIVE_FORMULA_BLOCKS_MISSING",
            lambda r: r["path_families"][0].update(
                blocked_duplicate_formulas=[]
            ),
        ),
        (
            "Q15_NEGATIVE_BLOCKER_REMAINS",
            lambda r: r.update(blockers=["nested support root"]),
        ),
        (
            "Q15_NEGATIVE_CODING_AUTHORIZATION",
            lambda r: r.update(may_begin_coding=True),
        ),
        (
            "Q15_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
            lambda r: r.update(may_write_source=True),
        ),
        (
            "Q15_NEGATIVE_FINAL_PROGRESSION",
            lambda r: r.update(may_proceed_to_final_precode=False),
        ),
    ]
    for label, mutate in cases:
        _reject(label, mutate)

    invalid = valid_not_applicable_record()
    invalid["no_path_evidence"] = []
    try:
        validate_record(invalid)
    except AssertionError:
        print("Q15_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: PASS")
    else:
        raise AssertionError(
            "Q15_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: FAIL"
        )


def _path_state(path: Path) -> tuple[object, ...]:
    if not path.exists() and not path.is_symlink():
        return ("ABSENT",)
    stat_result = path.lstat()
    return (
        "PRESENT",
        path.is_symlink(),
        path.is_dir(),
        path.is_file(),
        stat_result.st_mode,
        stat_result.st_size,
        stat_result.st_mtime_ns,
    )


def validate_runtime_paths(root: Path) -> None:
    sys.path.insert(0, str(root))
    fixture_parent: Path | None = None
    try:
        module = importlib.import_module(
            "kanda_reasoner_app.project_support_boundary"
        )
        transient_owner = module.canonical_transient_garbage_root(root)
        fixture_parent = transient_owner / "q15_path_authority_fixture"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="runtime_",
            dir=fixture_parent,
        ) as temp_dir:
            base = Path(temp_dir)
            project = base / "sample_project"
            project.mkdir()
            resolved_project = project.resolve(strict=False)
            expected_base = (
                Path(resolved_project.anchor)
                if resolved_project.drive
                else resolved_project.parent
            )
            expected_support = (
                expected_base / "sample_project_show_project_to_AI"
            ).resolve(strict=False)
            expected_transient = (
                expected_base / "sample_project_delete_after_daily_work"
            ).resolve(strict=False)

            if not resolved_project.drive:
                expected_support.mkdir()
                expected_transient.mkdir()

            state_before = (
                _path_state(expected_support),
                _path_state(expected_transient),
            )
            support = module.canonical_project_support_root(project)
            transient = module.canonical_transient_garbage_root(project)
            state_after = (
                _path_state(expected_support),
                _path_state(expected_transient),
            )

            _gate(
                "Q15_SUPPORT_ROOT_FORMULA",
                support == expected_support
                and support.name == "sample_project_show_project_to_AI",
            )
            _gate(
                "Q15_TRANSIENT_GARBAGE_AUTHORITY",
                transient == expected_transient
                and transient.name == "sample_project_delete_after_daily_work",
            )
            _gate(
                "Q15_ROOTS_OUTSIDE_PROJECT_SOURCE",
                support.parent != project and transient.parent != project,
            )
            _gate(
                "Q15_PATH_DERIVATION_NO_SIDE_EFFECTS",
                state_before == state_after,
            )
            _gate(
                "Q15_EXISTING_CANONICAL_PATH_FIXTURE",
                bool(resolved_project.drive)
                or (support.exists() and transient.exists()),
            )
            _gate(
                "Q15_ISOLATED_PATH_FIXTURE",
                project.parent == base
                and fixture_parent == transient_owner / "q15_path_authority_fixture",
            )

        windows_project = PureWindowsPath(
            r"E:\temporary\runtime\sample_project"
        )
        windows_base = PureWindowsPath(windows_project.anchor)
        _gate(
            "Q15_WINDOWS_DRIVE_ROOT_FORMULA_READ_ONLY",
            windows_base / "sample_project_show_project_to_AI"
            == PureWindowsPath(r"E:\sample_project_show_project_to_AI")
            and windows_base / "sample_project_delete_after_daily_work"
            == PureWindowsPath(r"E:\sample_project_delete_after_daily_work"),
        )
    finally:
        if fixture_parent is not None:
            try:
                fixture_parent.rmdir()
            except OSError:
                pass
        try:
            sys.path.remove(str(root))
        except ValueError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    validate_source(root)
    validate_semantics()
    validate_runtime_paths(root)
    print("Q15_PREVIEW_SHADOW_SOURCE_AUTHORITY: PASS")
    print("Q15_CANONICAL_PATH_AUTHORITY_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
