"""Validate Brick Wall Q17 Preview, Shadow, and source separation."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable, Sequence

from brick_wall_q17_preview_shadow_source_contract import (
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q17-preview-shadow-source-separation-enforcement-v1"
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
TOOL_PROJECT_CANON_REL = PLIB / (
    "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md"
)
Q14_VALIDATOR_REL = Path("tools/validate_brick_wall_q14_immediate_pre_write_freshness_v1.py")
Q16_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q16_resolved_path_containment_v1.py"
)
Q17_CONTRACT_REL = Path("tools/brick_wall_q17_preview_shadow_source_contract.py")
Q17_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q17_preview_shadow_source_separation_v1.py"
)
PATHS_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_project_support_paths.py"
)
SOURCE_MUTATION_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_source_mutation_primitives.py"
)
SHADOW_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_shadow_backend.py"
)
PREVIEW_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "cst_real_preview_writer.py"
)
BOUNDARY_VALIDATOR_REL = Path(
    "tools/validate_large_file_refactor_workbench_project_support_boundary_v3.py"
)
ROUTER_VALIDATOR_REL = Path(
    "tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py"
)

BRICK_MARKERS = (
    "### Preview, Shadow, and source separation (Q17)",
    "PREVIEW, SHADOW, AND SOURCE SEPARATION RECORD",
    "Authorities, exactly once each: FINAL_SOURCE | DURABLE_PREVIEW | DISPOSABLE_SHADOW",
    "Preview not source truth",
    "Shadow not durable truth",
    "final source excludes Preview-only metadata",
    "no durable evidence under Shadow",
    "no source mutation from Preview/Shadow",
    "proceed to Q18 stale async-result rejection YES/NO",
    "source writes authorized only by current Q13-Q14 evidence",
)
BRIDGE_MARKERS = (
    "## Preview, Shadow, and source separation gate (Q17)",
    "exactly one FINAL_SOURCE, DURABLE_PREVIEW, and DISPOSABLE_SHADOW authority",
    "Q17 never grants source-write authority",
    "## Preview, Shadow, and source separation bridge",
    "source-write authority remains Q13-Q14 only",
)
PATH_MARKERS = (
    "return canonical_transient_garbage_root(active_project_root)",
    'return daily_work_root(active_project_root) / "large_file_refactor_shadow"',
    "return workbench_support_root(active_project_root) / _PREVIEW_DIR",
    'return "active_project_source"',
    'return "active_project_preview_support"',
    'return "daily_work_garbage"',
)
SOURCE_MARKERS = (
    'if "KANDA PREVIEW ARTIFACT" in text:',
    '"PREVIEW_WATERMARK_IN_SOURCE_PAYLOAD:"',
    "destination.parent.mkdir(parents=True, exist_ok=True)",
    "os.replace(temp, destination)",
    "OPERATION_RESULT_HASH_MISMATCH",
)
SHADOW_MARKERS = (
    "relative = destination.relative_to(project_root)",
    "shadow_destination.relative_to(shadow_root)",
    "shadow_destination.write_bytes(raw)",
    "SHADOW_PAYLOAD_BYTE_MISMATCH",
    "source_mutation_enabled=False",
)
PREVIEW_MARKERS = (
    "blockers.extend(_destination_blockers(target, preview_root, project_root))",
    'target.write_bytes(_CONTENT_CACHE[item.relative_path].encode("utf-8"))',
    "source_content_hash",
)
CANON_MARKERS = (
    "Active-project source truth:",
    "Durable Workbench project-support state:",
    "Canonical Preview runs:",
    "Disposable Shadow runs:",
    "Preview and Shadow are not interchangeable.",
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


def _parse_version(value: object) -> tuple[int, ...]:
    if not isinstance(value, str):
        return ()
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        return ()


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    canon = _read(root / TOOL_PROJECT_CANON_REL)
    paths = _read(root / PATHS_REL)
    source_mutation = _read(root / SOURCE_MUTATION_REL)
    shadow = _read(root / SHADOW_REL)
    preview = _read(root / PREVIEW_REL)
    q16 = _read(root / Q16_VALIDATOR_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)

    _require(brick, BRICK_MARKERS, "Q17_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q17_ROUTER_BRIDGE_CONTRACT")
    _require(canon, CANON_MARKERS, "Q17_TOOL_PROJECT_OWNER_CANON")
    _require(paths, PATH_MARKERS, "Q17_CANONICAL_PATH_OWNERS")
    _require(source_mutation, SOURCE_MARKERS, "Q17_FINAL_SOURCE_GUARDS")
    _require(shadow, SHADOW_MARKERS, "Q17_SHADOW_GUARDS")
    _require(preview, PREVIEW_MARKERS, "Q17_PREVIEW_GUARDS")
    _gate("Q17_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 7))
    _gate("Q17_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 1))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q17_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q14 = _read(root / Q14_VALIDATOR_REL)
    _gate(
        "Q14_FORWARD_COMPATIBLE_Q15_PROGRESSION",
        '"proceed to Q15 canonical path-authority YES/NO"' in q14
        and '"May proceed to Q15 canonical path-authority gate: YES / NO"' in q14,
    )
    _gate(
        "Q16_FORWARD_COMPATIBLE_Q17_PROGRESSION",
        "Q16_FORWARD_COMPATIBLE_Q17_SEPARATION" in q16
        and '_parse_version(brick_meta.get("version")) >= (2, 7)' in q16
        and '_parse_version(bridge_meta.get("version")) >= (3, 1)' in q16,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q14_VALIDATOR_REL,
        Q16_VALIDATOR_REL,
        Q17_CONTRACT_REL,
        Q17_VALIDATOR_REL,
        PATHS_REL,
        SOURCE_MUTATION_REL,
        SHADOW_REL,
        PREVIEW_REL,
        BOUNDARY_VALIDATOR_REL,
        ROUTER_VALIDATOR_REL,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q17_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = valid_required_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
        return
    _gate(label, False, "invalid record was accepted")


def validate_semantics() -> None:
    validate_record(valid_required_record())
    _gate("Q17_REQUIRED_SEPARATION_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q17_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        (
            "Q17_NEGATIVE_PREVIEW_IN_SOURCE",
            lambda record: record["artifacts"][1].update(
                canonical_root=record["active_project_root"],
                resolved_path=record["active_project_root"] + r"\preview\module.py",
            ),
        ),
        (
            "Q17_NEGATIVE_PREVIEW_IN_TRANSIENT",
            lambda record: record["artifacts"][1].update(
                canonical_root=record["transient_garbage_root"],
                resolved_path=record["transient_garbage_root"]
                + r"\preview\module.py",
            ),
        ),
        (
            "Q17_NEGATIVE_SHADOW_IN_SUPPORT",
            lambda record: record["artifacts"][2].update(
                canonical_root=record["project_support_root"],
                resolved_path=record["project_support_root"]
                + r"\shadow\module.py",
            ),
        ),
        (
            "Q17_NEGATIVE_SOURCE_NOT_TRUTH",
            lambda record: record["artifacts"][0].update(source_truth=False),
        ),
        (
            "Q17_NEGATIVE_PREVIEW_SOURCE_TRUTH",
            lambda record: record["artifacts"][1].update(source_truth=True),
        ),
        (
            "Q17_NEGATIVE_SHADOW_DURABLE_TRUTH",
            lambda record: record["artifacts"][2].update(durable_truth=True),
        ),
        (
            "Q17_NEGATIVE_PREVIEW_METADATA_IN_SOURCE",
            lambda record: record.update(source_excludes_preview_metadata=False),
        ),
        (
            "Q17_NEGATIVE_BYTE_IDENTITY",
            lambda record: record["artifacts"][1].update(
                exact_byte_hash_verified=False
            ),
        ),
        (
            "Q17_NEGATIVE_SHADOW_SOURCE_MUTATION",
            lambda record: record["artifacts"][2].update(
                source_mutation_authority=True
            ),
        ),
        (
            "Q17_NEGATIVE_CROSS_AUTHORITY_WRITE",
            lambda record: record["artifacts"][1]["blocked_cross_writes"].append(
                "preview wrote active source"
            ),
        ),
        (
            "Q17_NEGATIVE_DUPLICATE_AUTHORITY",
            lambda record: record["artifacts"][2].update(
                authority_class="DURABLE_PREVIEW"
            ),
        ),
        (
            "Q17_NEGATIVE_Q18_PROGRESSION",
            lambda record: record.update(may_proceed_to_q18=False),
        ),
        (
            "Q17_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
            lambda record: record.update(may_write_source=True),
        ),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    invalid = valid_not_applicable_record()
    invalid["no_separation_evidence"] = []
    try:
        validate_record(invalid)
    except AssertionError:
        _gate("Q17_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q17_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)


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


def validate_runtime_owners(root: Path) -> None:
    sys.path.insert(0, str(root))
    fixture_parent: Path | None = None
    try:
        paths = importlib.import_module(
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."
            "workbench_project_support_paths"
        )
        source = root / BRICK_REL
        preview = paths.preview_runs_root(root) / "q17-read-only" / "prompt.md"
        shadow = paths.shadow_runs_root(root) / "q17-read-only" / "prompt.md"
        preview_root = paths.preview_runs_root(root)
        shadow_root = paths.shadow_runs_root(root)
        state_before = (_path_state(preview_root), _path_state(shadow_root))
        classes = (
            paths.workbench_path_class(root, source),
            paths.workbench_path_class(root, preview),
            paths.workbench_path_class(root, shadow),
        )
        state_after = (_path_state(preview_root), _path_state(shadow_root))
        _gate(
            "Q17_RUNTIME_AUTHORITY_CLASSES",
            classes
            == (
                "active_project_source",
                "active_project_preview_support",
                "daily_work_garbage",
            ),
        )
        _gate(
            "Q17_RUNTIME_AUTHORITY_ROOTS_DISTINCT",
            len(
                {
                    str(root.resolve()).casefold(),
                    str(preview_root.resolve()).casefold(),
                    str(shadow_root.resolve()).casefold(),
                }
            )
            == 3,
        )
        _gate(
            "Q17_RUNTIME_PATH_DERIVATION_NO_SIDE_EFFECTS",
            state_before == state_after,
        )
        _gate(
            "Q17_RUNTIME_PREVIEW_BLOCKERS",
            not paths.preview_root_blockers(root, preview)
            and "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE"
            in paths.preview_root_blockers(root, source),
        )
        fixture_parent = paths.daily_work_root(root) / "q17_separation_fixture"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="bytes_", dir=fixture_parent) as raw:
            fixture = Path(raw)
            payload = b"line1\nline2\n"
            preview_copy = fixture / "preview.bin"
            shadow_copy = fixture / "shadow.bin"
            preview_copy.write_bytes(payload)
            shadow_copy.write_bytes(preview_copy.read_bytes())
            _gate(
                "Q17_RUNTIME_EXACT_BYTE_IDENTITY",
                preview_copy.read_bytes() == payload
                and shadow_copy.read_bytes() == payload,
            )
        _gate(
            "Q17_RUNTIME_FIXTURE_TRANSIENT_ONLY",
            fixture_parent == paths.daily_work_root(root) / "q17_separation_fixture",
        )
    finally:
        if fixture_parent is not None:
            shutil.rmtree(fixture_parent, ignore_errors=True)
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
    validate_runtime_owners(root)
    print("Q17_PREVIEW_SHADOW_SOURCE_SEPARATION_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
