"""Validate Brick Wall Q16 resolved-path containment enforcement."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PureWindowsPath
from typing import Callable, Sequence

from brick_wall_q16_resolved_path_containment_contract import (
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q16-resolved-path-containment-enforcement-v1"
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
Q15_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q15_canonical_path_authority_v1.py"
)
Q16_CONTRACT_REL = Path(
    "tools/brick_wall_q16_resolved_path_containment_contract.py"
)
Q16_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q16_resolved_path_containment_v1.py"
)
Q17_CONTRACT_REL = Path(
    "tools/brick_wall_q17_preview_shadow_source_contract.py"
)
Q17_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q17_preview_shadow_source_separation_v1.py"
)
MUTATION_LANE_REL = Path(
    "kanda_reasoner_app/engineering_safety/project_mutation_lane.py"
)
TAB1_PLANNING_REL = Path(
    "kanda_reasoner_app/tab1_audit_write_support/planning.py"
)
ZIP_CONTRACT_REL = Path(
    "scripts/validate_ai_response_patch_delivery_contract.py"
)
BOUNDARY_REL = Path("kanda_reasoner_app/project_support_boundary.py")

BRICK_MARKERS = (
    "### Resolved-path containment (Q16)",
    "RESOLVED-PATH CONTAINMENT RECORD",
    "Containment required YES/NO",
    "nearest existing parent",
    "symlink/junction/reparse status",
    "traversal | sibling-prefix | absolute escape | other drive",
    "UNC server/share",
    "case collision/ambiguity",
    "proceed to Q17 Preview/Shadow/source separation YES/NO",
    "may begin coding NO",
    "may write source NO",
    "String-prefix or lexical-only checks",
    "New paths require a verified existing parent",
)
BRIDGE_MARKERS = (
    "## Resolved-path containment gate (Q16)",
    "Q16 resolved-path containment record complete: YES / NO",
    "Containment decision: COMPLETE / NOT_APPLICABLE / BLOCKED",
    "Resolved owner root and candidates structurally contained: YES / NO / N/A",
    "Traversal, sibling-prefix, drive, UNC, case, and link escapes rejected",
    "## Resolved-path containment bridge",
    "String-prefix, lexical-only, unresolved-link, mismatched-anchor",
)
MUTATION_MARKERS = (
    "root = Path(request.project_root).resolve()",
    "path = Path(raw).resolve()",
    "if not _is_relative_to(path, root):",
    "path.resolve().relative_to(root.resolve())",
    "MUTATION_REQUEST_PATH_OUTSIDE_PROJECT_ROOT",
)
TAB1_MARKERS = (
    "root = project_root.resolve()",
    "resolved = candidate.resolve()",
    "if not _path_is_relative_to(resolved, root):",
    "path.relative_to(root)",
)
ZIP_MARKERS = (
    'normalized = name.replace("\\\\", "/")',
    'normalized.startswith("/")',
    're.match(r"^[A-Za-z]:", normalized)',
    'any(part == ".." for part in normalized.split("/"))',
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
    mutation = _read(root / MUTATION_LANE_REL)
    planning = _read(root / TAB1_PLANNING_REL)
    zip_contract = _read(root / ZIP_CONTRACT_REL)
    q15 = _read(root / Q15_VALIDATOR_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)

    _require(brick, BRICK_MARKERS, "Q16_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q16_ROUTER_BRIDGE_CONTRACT")
    _require(mutation, MUTATION_MARKERS, "Q16_MUTATION_LANE_STRUCTURAL_GUARD")
    _require(planning, TAB1_MARKERS, "Q16_TAB1_STRUCTURAL_GUARD")
    _require(zip_contract, ZIP_MARKERS, "Q16_ZIP_LEXICAL_PREFLIGHT_GUARD")
    _gate("Q16_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 6))
    _gate("Q16_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 0))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q16_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    _gate(
        "Q15_FORWARD_COMPATIBLE_Q16_PROGRESSION",
        '"proceed to Q16 resolved-path containment YES/NO"' in q15
        and '"May proceed to Q16 resolved-path containment gate: YES / NO"' in q15
        and '_parse_version(brick_meta.get("version")) >= (2, 5)' in q15
        and '_parse_version(bridge_meta.get("version")) >= (2, 9)' in q15,
    )
    _gate(
        "Q16_FORWARD_COMPATIBLE_Q17_SEPARATION",
        "### Preview, Shadow, and source separation (Q17)" in brick
        and "## Preview, Shadow, and source separation gate (Q17)" in bridge
        and _parse_version(brick_meta.get("version")) >= (2, 7)
        and _parse_version(bridge_meta.get("version")) >= (3, 1),
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q15_VALIDATOR_REL,
        Q16_CONTRACT_REL,
        Q16_VALIDATOR_REL,
        Q17_CONTRACT_REL,
        Q17_VALIDATOR_REL,
        MUTATION_LANE_REL,
        TAB1_PLANNING_REL,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q16_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


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
    _gate("Q16_REQUIRED_CONTAINMENT_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q16_NOT_APPLICABLE_RECORD_ACCEPTED", True)

    _reject(
        "Q16_NEGATIVE_TRAVERSAL_INPUT",
        lambda record: record["candidate_paths"][0].update(
            bounded_relative_input="../escape.py"
        ),
    )
    _reject(
        "Q16_NEGATIVE_SIBLING_PREFIX",
        lambda record: record["candidate_paths"][0].update(
            resolved_candidate=r"E:\\kanda_reasoner_backup\\escape.py"
        ),
    )
    _reject(
        "Q16_NEGATIVE_ABSOLUTE_INPUT",
        lambda record: record["candidate_paths"][0].update(
            bounded_relative_input=r"E:\\escape.py"
        ),
    )
    _reject(
        "Q16_NEGATIVE_CROSS_DRIVE",
        lambda record: record["candidate_paths"][0].update(
            resolved_candidate=r"F:\\kanda_reasoner\\escape.py",
            drive_or_share_match=False,
        ),
    )
    # Q25_MUTATION_GAP_REPAIR_BEGIN
    _reject(
        "Q16_NEGATIVE_TRAVERSAL_GUARD_ISOLATED",
        lambda record: record["candidate_paths"][0].update(
            bounded_relative_input="../escape.py",
            nearest_existing_parent=r"E:\\kanda_reasoner\\..",
            resolved_candidate=r"E:\\kanda_reasoner\\..\\escape.py",
            case_key="e:/kanda_reasoner/../escape.py",
            structural_relative_path="../escape.py",
        ),
    )
    _reject(
        "Q16_NEGATIVE_DRIVE_MATCH_FLAG_ISOLATED",
        lambda record: record["candidate_paths"][0].update(
            drive_or_share_match=False,
        ),
    )
    # Q25_MUTATION_GAP_REPAIR_END
    _reject(
        "Q16_NEGATIVE_UNC_SHARE_ESCAPE",
        lambda record: record.update(
            owner_root=r"\\server\\share\\project",
            resolved_owner_root=r"\\server\\share\\project",
            candidate_paths=[
                {
                    **record["candidate_paths"][0],
                    "nearest_existing_parent": r"\\server\\other\\project",
                    "resolved_owner_root": r"\\server\\share\\project",
                    "resolved_candidate": r"\\server\\other\\project\\file.py",
                    "drive_or_share_match": False,
                }
            ],
        ),
    )
    _reject(
        "Q16_NEGATIVE_CASE_COLLISION",
        lambda record: record["candidate_paths"].append(
            {**record["candidate_paths"][0], "path_id": "case_duplicate"}
        ),
    )
    _reject(
        "Q16_NEGATIVE_LINK_ESCAPE",
        lambda record: record["candidate_paths"][0].update(
            link_status="LINK_RESOLVED_OUTSIDE_OWNER"
        ),
    )
    _reject(
        "Q16_NEGATIVE_UNVERIFIED_PARENT",
        lambda record: record["candidate_paths"][1].update(
            link_status="UNRESOLVED_PARENT"
        ),
    )
    _reject(
        "Q16_NEGATIVE_CONTAINMENT_UNRESOLVED",
        lambda record: record["candidate_paths"][0].update(
            containment_verified=False
        ),
    )
    _reject(
        "Q16_NEGATIVE_BLOCKER_REMAINS",
        lambda record: record["blockers"].append("owner root unresolved"),
    )
    _reject(
        "Q16_NEGATIVE_CODING_AUTHORIZATION",
        lambda record: record.update(may_begin_coding=True),
    )
    _reject(
        "Q16_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
        lambda record: record.update(may_write_source=True),
    )


def _inside(candidate: Path, owner: Path, *, strict: bool) -> bool:
    try:
        resolved_owner = owner.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=strict)
        resolved_candidate.relative_to(resolved_owner)
        return resolved_candidate != resolved_owner
    except (OSError, RuntimeError, ValueError):
        return False


def _windows_inside(candidate: PureWindowsPath, owner: PureWindowsPath) -> bool:
    try:
        candidate.relative_to(owner)
        return candidate != owner
    except ValueError:
        return False


def _create_escape_link(link: Path, target: Path) -> str:
    try:
        os.symlink(target, link, target_is_directory=True)
        return "SYMLINK"
    except (NotImplementedError, OSError):
        pass
    if os.name != "nt":
        return "UNAVAILABLE"
    result = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and link.exists():
        return "JUNCTION"
    return "UNAVAILABLE"


def _remove_escape_link(link: Path, kind: str) -> None:
    if kind == "SYMLINK":
        link.unlink(missing_ok=True)
    elif kind == "JUNCTION":
        os.rmdir(link)


def validate_runtime_paths(root: Path) -> None:
    sys.path.insert(0, str(root))
    fixture_parent: Path | None = None
    try:
        boundary = importlib.import_module(
            "kanda_reasoner_app.project_support_boundary"
        )
        transient = boundary.canonical_transient_garbage_root(root)
        fixture_parent = transient / "q16_containment_fixture"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="runtime_", dir=fixture_parent) as raw:
            base = Path(raw)
            owner = base / "project"
            sibling = base / "project_backup"
            outside = base / "outside"
            owner.mkdir()
            sibling.mkdir()
            outside.mkdir()
            inside_file = owner / "pkg" / "inside.py"
            inside_file.parent.mkdir()
            inside_file.write_text("inside\n", encoding="utf-8")
            outside_file = outside / "outside.py"
            outside_file.write_text("outside\n", encoding="utf-8")

            _gate("Q16_RUNTIME_INSIDE_ACCEPTED", _inside(inside_file, owner, strict=True))
            _gate(
                "Q16_RUNTIME_TRAVERSAL_REJECTED",
                not _inside(owner / ".." / "outside" / "outside.py", owner, strict=True),
            )
            _gate(
                "Q16_RUNTIME_SIBLING_PREFIX_REJECTED",
                not _inside(sibling / "escape.py", owner, strict=False),
            )
            _gate(
                "Q16_RUNTIME_ABSOLUTE_ESCAPE_REJECTED",
                not _inside(outside_file, owner, strict=True),
            )
            new_parent = owner / "generated"
            new_parent.mkdir()
            _gate(
                "Q16_RUNTIME_NEW_PATH_PARENT_VERIFIED",
                _inside(new_parent / "new_file.py", owner, strict=False),
            )

            link = owner / "escape_link"
            link_kind = _create_escape_link(link, outside)
            try:
                if link_kind == "UNAVAILABLE":
                    mutation = _read(root / MUTATION_LANE_REL)
                    planning = _read(root / TAB1_PLANNING_REL)
                    _gate(
                        "Q16_RUNTIME_LINK_ESCAPE_GUARD",
                        "path.resolve().relative_to(root.resolve())" in mutation
                        and "resolved = candidate.resolve()" in planning,
                    )
                else:
                    _gate(
                        "Q16_RUNTIME_LINK_ESCAPE_GUARD",
                        not _inside(link / "outside.py", owner, strict=True),
                    )
            finally:
                _remove_escape_link(link, link_kind)

        win_owner = PureWindowsPath(r"E:\\work\\project")
        _gate(
            "Q16_WINDOWS_CASE_INSENSITIVE_CONTAINMENT",
            _windows_inside(
                PureWindowsPath(r"e:\\WORK\\PROJECT\\pkg\\file.py"),
                win_owner,
            ),
        )
        _gate(
            "Q16_WINDOWS_CROSS_DRIVE_REJECTED",
            not _windows_inside(
                PureWindowsPath(r"F:\\work\\project\\file.py"),
                win_owner,
            ),
        )
        _gate(
            "Q16_WINDOWS_SIBLING_PREFIX_REJECTED",
            not _windows_inside(
                PureWindowsPath(r"E:\\work\\project_backup\\file.py"),
                win_owner,
            ),
        )
        unc_owner = PureWindowsPath(r"\\server\\share\\project")
        _gate(
            "Q16_WINDOWS_UNC_CONTAINMENT",
            _windows_inside(
                PureWindowsPath(r"\\server\\share\\project\\pkg\\file.py"),
                unc_owner,
            )
            and not _windows_inside(
                PureWindowsPath(r"\\server\\other\\project\\file.py"),
                unc_owner,
            )
            and not _windows_inside(
                PureWindowsPath(r"\\other\\share\\project\\file.py"),
                unc_owner,
            ),
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
    validate_runtime_paths(root)
    print("Q16_RESOLVED_PATH_CONTAINMENT_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
