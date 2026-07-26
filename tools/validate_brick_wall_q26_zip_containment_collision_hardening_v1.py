\
"""Validate Brick Wall Q26 ZIP containment and collision hardening."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import stat
import sys
from tempfile import TemporaryDirectory
from typing import Callable, Sequence
import warnings
import zipfile

from brick_wall_q26_zip_containment_collision_contract import (
    PROTECTIONS,
    mutated_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

__all__: list[str] = []
FEATURE_ID = "brick-wall-q26-zip-containment-collision-hardening-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
OWNER_REL = Path("kanda_reasoner_app/patch_governance/validator.py")
HELPER_REL = Path("kanda_reasoner_app/patch_governance/zip_member_contract.py")
Q25_REL = Path("tools/validate_brick_wall_q25_mutation_testing_pilot_decision_v1.py")
CONTRACT_REL = Path("tools/brick_wall_q26_zip_containment_collision_contract.py")
VALIDATOR_REL = Path("tools/validate_brick_wall_q26_zip_containment_collision_hardening_v1.py")
BRICK_MARKERS = (
    "### ZIP containment and collision hardening (Q26)",
    "ZIP CONTAINMENT AND COLLISION HARDENING RECORD",
    "absolute/drive/UNC/traversal/duplicate/case-fold/file-directory/link/undeclared install paths",
    "proceed to Q27 control-byte and encoding guards YES/NO",
)
BRIDGE_MARKERS = (
    "## ZIP containment and collision hardening gate (Q26)",
    "Q26 ZIP containment/collision hardening record complete: YES / NO",
    "May proceed to Q27 control-byte and encoding guards: YES / NO",
    "## ZIP containment and collision hardening bridge",
)


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(item) for item in str(value).split("."))
    except ValueError:
        return ()


def _precode(text: str, minimum: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",
        text,
        re.DOTALL,
    )
    return bool(match and match.group(1) == match.group(2) and int(match.group(1)) >= minimum)


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    bm = _load(root / BRICK_META_REL)
    rm = _load(root / BRIDGE_META_REL)
    owner = _read(root / OWNER_REL)
    helper = _read(root / HELPER_REL)
    _require(brick, BRICK_MARKERS, "Q26_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q26_ROUTER_BRIDGE_CONTRACT")
    _gate("Q26_BRICK_VERSION", _version(bm.get("version")) >= (3, 6))
    _gate("Q26_BRIDGE_VERSION", _version(rm.get("version")) >= (4, 0))
    for label, meta in (("brick", bm), ("bridge", rm)):
        source_stage = str(meta.get("source_stage") or "").strip()
        updated_for = str(meta.get("updated_for") or "").strip()
        _gate(
            "Q26_METADATA_ALIGNMENT",
            bool(source_stage) and source_stage == updated_for,
            label,
        )
    _gate("Q26_PRECODE_PROGRESSION", _precode(brick, 26))
    _gate(
        "Q26_FORWARD_COMPATIBLE_Q27_PROGRESSION",
        "### Control-byte and encoding guards (Q27)" in brick
        and "## Control-byte and encoding guards gate (Q27)" in bridge
        and _precode(brick, 27),
    )
    _gate(
        "Q25_FORWARD_COMPATIBLE_Q26_PROGRESSION",
        "Q25_FORWARD_COMPATIBLE_Q26_PRECODE_PROGRESSION" in _read(root / Q25_REL),
    )
    _require(
        owner,
        (
            "validate_zip_member_contract",
            "ZipMemberContractError",
            '"zip_member_contract": True',
            '"declared_payload_member_count"',
        ),
        "Q26_CANONICAL_OWNER_INTEGRATION",
    )
    _require(
        helper,
        (
            "ZIP_MEMBER_ABSOLUTE_PATH",
            "ZIP_MEMBER_DRIVE_QUALIFIED_PATH",
            "ZIP_MEMBER_UNC_PATH",
            "ZIP_MEMBER_TRAVERSAL",
            "ZIP_MEMBER_DUPLICATE",
            "ZIP_MEMBER_WINDOWS_CASE_COLLISION",
            "ZIP_MEMBER_FILE_DIRECTORY_COLLISION",
            "ZIP_MEMBER_UNEXPECTED_LINK",
            "ZIP_PAYLOAD_UNDECLARED",
        ),
        "Q26_PRIVATE_HELPER_CONTRACT",
    )
    for rel in (
        BRICK_REL, BRIDGE_REL, OWNER_REL, HELPER_REL, Q25_REL, CONTRACT_REL, VALIDATOR_REL,
    ):
        _gate("Q26_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500, str(rel))


def _reject_record(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_governance_record() -> None:
    validate_record(valid_complete_record())
    _gate("Q26_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q26_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests = (
        ("Q26_NEGATIVE_Q25_BASELINE", lambda r: r.update(q25_decision_complete=False)),
        ("Q26_NEGATIVE_OWNER_DRIFT", lambda r: r.update(canonical_owner="parallel.zip.validator")),
        ("Q26_NEGATIVE_FACADE_DRIFT", lambda r: r.update(public_facade="private.helper")),
        ("Q26_NEGATIVE_EXACT_FINAL_ZIP", lambda r: r.update(exact_final_zip_required=False)),
        ("Q26_NEGATIVE_PROTECTION_INVENTORY", lambda r: r["protections"].remove(PROTECTIONS[0])),
        ("Q26_NEGATIVE_MANIFEST_AUTHORITY", lambda r: r.update(manifest_authority="")),
        ("Q26_NEGATIVE_VALIDATOR_EVIDENCE", lambda r: r.update(validators=[])),
        ("Q26_NEGATIVE_Q27_PROGRESSION", lambda r: r.update(may_proceed_to_q27=False)),
        ("Q26_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q26_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in tests:
        _reject_record(label, mutate)
    record = valid_not_applicable_record()
    record["no_hardening_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q26_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q26_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q26_ZIP_CONTAINMENT_COLLISION_HARDENING_REGRESSION_SET: PASS")


def _hint() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "patch_name": "q26_fixture",
        "feature_id": "q26-fixture",
        "feature_title": "Q26 Fixture",
        "primary_box": "kanda_reasoner_app/patch_governance",
        "box_type": "validation fixture",
        "validated_files": ["tools/example.py"],
        "generated_files": ["validation/evidence.txt"],
        "protected_paths": ["tools/example.py"],
        "do_not_regress_rules": ["ZIP member hardening remains active."],
        "validation_evidence_summary": "Q26 fixture evidence.",
        "known_warnings": "Synthetic fixture only.",
        "planned_next_step": "Run focused validation.",
        "notes": "No source write authority.",
    }


def _manifest(paths: list[str]) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "patch_name": "q26_fixture",
        "feature_id": "q26-fixture",
        "primary_box": "kanda_reasoner_app/patch_governance",
        "files": [
            {
                "path": path,
                "before_sha256": None,
                "after_sha256": "0" * 64,
                "required_before_state": "absent",
                "receiver": "SOURCE_PATCH",
            }
            for path in paths
        ],
    }


def _write_zip(
    path: Path,
    members: list[tuple[str | zipfile.ZipInfo, bytes]],
    *,
    manifest_paths: list[str] | None = None,
    include_manifest: bool = True,
) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(_hint()))
            if include_manifest:
                archive.writestr(
                    "INSTALL_MANIFEST.json",
                    json.dumps(_manifest(manifest_paths or [])),
                )
            for name, data in members:
                archive.writestr(name, data)


def _expect_block(
    validate_patch_zip: Callable[..., dict[str, object]],
    directory: Path,
    case_id: str,
    code: str,
    members: list[tuple[str | zipfile.ZipInfo, bytes]],
    *,
    manifest_paths: list[str] | None = None,
    include_manifest: bool = True,
) -> None:
    path = directory / (case_id + ".zip")
    _write_zip(
        path,
        members,
        manifest_paths=manifest_paths,
        include_manifest=include_manifest,
    )
    try:
        validate_patch_zip(path)
    except Exception as exc:
        _gate(case_id, code in str(exc), str(exc))
    else:
        _gate(case_id, False, "archive was accepted")


def _expect_raw_backslash_block(
    validate_patch_zip: Callable[..., dict[str, object]],
    directory: Path,
) -> None:
    case_id = "Q26_NEGATIVE_BACKSLASH_SEPARATOR"
    path = directory / (case_id + ".zip")
    forward_name = "payload/tools/a.py"
    backslash_name = "payload\\tools\\a.py"
    _write_zip(
        path,
        [(forward_name, b"1")],
        manifest_paths=["tools/a.py"],
    )
    data = path.read_bytes()
    forward_bytes = forward_name.encode("utf-8")
    backslash_bytes = backslash_name.encode("utf-8")
    _gate(
        "Q26_RAW_BACKSLASH_FIXTURE_NAME_LENGTH",
        len(forward_bytes) == len(backslash_bytes),
    )
    occurrence_count = data.count(forward_bytes)
    _gate(
        "Q26_RAW_BACKSLASH_FIXTURE_HEADER_COUNT",
        occurrence_count == 2,
        str(occurrence_count),
    )
    path.write_bytes(data.replace(forward_bytes, backslash_bytes))
    try:
        validate_patch_zip(path)
    except Exception as exc:
        _gate(case_id, "ZIP_MEMBER_BACKSLASH_SEPARATOR" in str(exc), str(exc))
    else:
        _gate(case_id, False, "archive was accepted")


def validate_runtime(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.patch_governance import validate_patch_zip

    with TemporaryDirectory(prefix="kanda_q26_zip_") as temp:
        directory = Path(temp)
        valid = directory / "valid.zip"
        _write_zip(
            valid,
            [("payload/tools/example.py", b"print('ok')\n")],
            manifest_paths=["tools/example.py"],
        )
        report = validate_patch_zip(valid)
        _gate("Q26_VALID_DECLARED_ZIP_ACCEPTED", bool(report.get("zip_member_contract")))
        _gate("Q26_VALID_DECLARED_PAYLOAD_COUNT", report.get("declared_payload_member_count") == 1)

        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_ABSOLUTE_PATH", "ZIP_MEMBER_ABSOLUTE_PATH", [("/escape.py", b"x")])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_DRIVE_PATH", "ZIP_MEMBER_DRIVE_QUALIFIED_PATH", [("C:/escape.py", b"x")])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_UNC_PATH", "ZIP_MEMBER_UNC_PATH", [("//server/share/escape.py", b"x")])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_TRAVERSAL", "ZIP_MEMBER_TRAVERSAL", [("payload/../escape.py", b"x")])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_DUPLICATE_MEMBER", "ZIP_MEMBER_DUPLICATE", [("payload/tools/a.py", b"1"), ("payload/tools/a.py", b"2")], manifest_paths=["tools/a.py"])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_WINDOWS_CASE_COLLISION", "ZIP_MEMBER_WINDOWS_CASE_COLLISION", [("payload/tools/A.py", b"1"), ("payload/tools/a.py", b"2")], manifest_paths=["tools/A.py", "tools/a.py"])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_FILE_DIRECTORY_COLLISION", "ZIP_MEMBER_FILE_DIRECTORY_COLLISION", [("payload/tools/node", b"1"), ("payload/tools/node/child.py", b"2")], manifest_paths=["tools/node", "tools/node/child.py"])
        link = zipfile.ZipInfo("payload/tools/link.py")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_UNEXPECTED_LINK", "ZIP_MEMBER_UNEXPECTED_LINK", [(link, b"target.py")], manifest_paths=["tools/link.py"])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_UNDECLARED_PAYLOAD", "ZIP_PAYLOAD_UNDECLARED", [("payload/tools/a.py", b"1"), ("payload/tools/extra.py", b"2")], manifest_paths=["tools/a.py"])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_DECLARED_PAYLOAD_MISSING", "ZIP_PAYLOAD_DECLARED_MISSING", [("payload/tools/a.py", b"1")], manifest_paths=["tools/a.py", "tools/missing.py"])
        _expect_block(validate_patch_zip, directory, "Q26_NEGATIVE_MANIFEST_MISSING", "ZIP_INSTALL_MANIFEST_MISSING", [("payload/tools/a.py", b"1")], include_manifest=False)
        _expect_raw_backslash_block(validate_patch_zip, directory)

    print("Q26_ZIP_MEMBER_CONTAINMENT: PASS")
    print("Q26_ZIP_COLLISION_REJECTION: PASS")
    print("Q26_ZIP_LINK_REJECTION: PASS")
    print("Q26_ZIP_MANIFEST_DECLARATION: PASS")
    print("Q26_RUNTIME_ZIP_CONTAINMENT_COLLISION_HARDENING: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_governance_record()
    validate_runtime(root)
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
