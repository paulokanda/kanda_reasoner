"""Live validation for exact Portable builder member governance."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path


FEATURE_ID = "portable-exact-builder-member-governance-v1"
EXPECTED_BUILDER_FEATURE = "kanda-reasoner-portable-builder-install-v1r12"
EXPECTED_STAGE_FEATURE = (
    "kanda-reasoner-portable-exact-builder-member-governance-v1"
)
EXPECTED_FEATURE_PREFIX = (
    "registry-boundary-gate",
    "packaged-gui-smoke-isolation",
    "governed-root-exact-rollback",
    "runtime-path-hash-allowlist",
    "exact-builder-member-governance",
)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def _expect_failure(callable_object, marker: str) -> None:
    from portable.builder_members import BuilderMemberError
    try:
        callable_object()
    except BuilderMemberError:
        print(marker)
        return
    raise RuntimeError(marker.replace(": PASS", ": FAIL"))


def _load_registry(project_root: Path) -> tuple[Path, str]:
    import hashlib
    drive = Path(project_root.anchor).resolve()
    support_parent = drive if project_root.anchor != "/" else project_root.parent
    registry = (
        support_parent
        / f"{project_root.name}_show_project_to_AI"
        / "tool_project_registry"
        / "projects.json"
    )
    _require(registry.is_file(), "TOOL_REGISTRY_MISSING")
    payload = json.loads(registry.read_text(encoding="utf-8-sig"))
    current_id = str(payload.get("current_project_id") or "")
    projects = payload.get("projects")
    _require(bool(current_id) and isinstance(projects, dict), "TOOL_REGISTRY_INVALID")
    record = projects.get(current_id)
    _require(isinstance(record, dict), "ACTIVE_PROJECT_RECORD_MISSING")
    _require(Path(str(record.get("project_root") or "")).resolve() == project_root, "ACTIVE_PROJECT_ROOT_MISMATCH")
    _require(str(record.get("selection_mode") or "") == "EXPLICIT_SELF_HOSTING", "ACTIVE_PROJECT_MODE_MISMATCH")
    digest = hashlib.sha256(registry.read_bytes()).hexdigest()
    return registry, digest


def _copy_portable(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    project_root = args.project_root.resolve()
    _require(project_root.name.casefold() == "kanda_reasoner", "TOOL_ROOT_NAME_MISMATCH")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(project_root))

    registry, registry_hash = _load_registry(project_root)
    print("PORTABLE BUILDER MEMBER LIVE EXPLICIT SELF-HOSTING AUTHORITY: PASS")

    from portable.builder_members import validate_exact_builder_members
    from portable.constants import (
        BUILDER_MEMBER_FEATURE_ID,
        FEATURE_ID as BUILDER_FEATURE_ID,
        PORTABLE_HARDENING_FEATURES,
        PRODUCTION_PORTABLE_ENABLED,
    )

    portable_root = project_root / "portable"
    manifest_path = portable_root / "PORTABLE_BUILDER_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _require(BUILDER_FEATURE_ID == EXPECTED_BUILDER_FEATURE, "BUILDER_FEATURE_ID_MISMATCH")
    _require(BUILDER_MEMBER_FEATURE_ID == EXPECTED_STAGE_FEATURE, "STAGE5_FEATURE_ID_MISMATCH")
    _require(
        tuple(PORTABLE_HARDENING_FEATURES)[: len(EXPECTED_FEATURE_PREFIX)]
        == EXPECTED_FEATURE_PREFIX,
        "STAGE5_CAPABILITY_PREFIX_MISMATCH",
    )
    _require(manifest.get("builder_member_feature_id") == EXPECTED_STAGE_FEATURE, "MANIFEST_STAGE5_FEATURE_ID_MISMATCH")
    inventory = validate_exact_builder_members(portable_root, manifest)
    _require(not inventory["directories"], "LIVE_PORTABLE_HAS_UNEXPECTED_DIRECTORIES")
    print("PORTABLE BUILDER EXACT MEMBER CONTRACT: PASS")
    print(f"PORTABLE BUILDER EXACT MEMBER FILE COUNT: {len(inventory['files'])}")
    print("PORTABLE BUILDER EXACT MEMBER DIRECTORY COUNT: 0")
    print("PORTABLE BUILDER MANIFEST SELF MEMBER: PASS")

    with tempfile.TemporaryDirectory(prefix="kanda_builder_members_v1_") as temp:
        temp_root = Path(temp)
        base = temp_root / "portable"
        _copy_portable(portable_root, base)
        base_manifest = json.loads((base / "PORTABLE_BUILDER_MANIFEST.json").read_text(encoding="utf-8"))

        stray = base / "UNMANIFESTED.txt"
        stray.write_text("STRAY\n", encoding="ascii")
        _expect_failure(
            lambda: validate_exact_builder_members(base, base_manifest),
            "PORTABLE BUILDER UNMANIFESTED FILE REJECTED: PASS",
        )
        stray.unlink()

        cache = base / "__pycache__"
        cache.mkdir()
        _expect_failure(
            lambda: validate_exact_builder_members(base, base_manifest),
            "PORTABLE BUILDER CACHE DIRECTORY REJECTED: PASS",
        )
        cache.rmdir()

        bytecode = base / "module.pyc"
        bytecode.write_bytes(b"PYC")
        _expect_failure(
            lambda: validate_exact_builder_members(base, base_manifest),
            "PORTABLE BUILDER BYTECODE MEMBER REJECTED: PASS",
        )
        bytecode.unlink()

        empty = base / "unexpected_empty_directory"
        empty.mkdir()
        _expect_failure(
            lambda: validate_exact_builder_members(base, base_manifest),
            "PORTABLE BUILDER EMPTY DIRECTORY REJECTED: PASS",
        )
        empty.rmdir()

        target_relative = next(iter(sorted(base_manifest["files"])))
        target = base / target_relative
        original = target.read_bytes()
        target.write_bytes(original + b"\nMUTATED")
        _expect_failure(
            lambda: validate_exact_builder_members(base, base_manifest),
            "PORTABLE BUILDER MODIFIED MEMBER REJECTED: PASS",
        )
        target.write_bytes(original)

        target.unlink()
        _expect_failure(
            lambda: validate_exact_builder_members(base, base_manifest),
            "PORTABLE BUILDER MISSING MEMBER REJECTED: PASS",
        )

        traversal = copy.deepcopy(base_manifest)
        first = next(iter(traversal["files"]))
        traversal["files"]["../escape.py"] = traversal["files"].pop(first)
        _expect_failure(
            lambda: validate_exact_builder_members(portable_root, traversal),
            "PORTABLE BUILDER TRAVERSAL MEMBER REJECTED: PASS",
        )

    stage4_text = (
        project_root / "tools" / "validate_portable_runtime_path_hash_allowlist_v1r4.py"
    ).read_text(encoding="utf-8")
    _require("REQUIRED_CAPABILITY_PREFIX" in stage4_text, "STAGE4_VALIDATOR_PREFIX_CONTRACT_MISSING")
    _require("manifest.get(\"hardening_stage\") ==" not in stage4_text, "STAGE4_VALIDATOR_PINS_CUMULATIVE_STAGE")
    print("PORTABLE STAGE 4 VALIDATOR FORWARD COMPATIBILITY: PASS")
    print("PORTABLE STAGE 5 VALIDATOR FORWARD COMPATIBILITY: PASS")
    print("PORTABLE EXACT BUILDER MEMBER GOVERNANCE CAPABILITY IDENTITY: PASS")

    _require(PRODUCTION_PORTABLE_ENABLED is False, "PRODUCTION_GATE_OPENED_EARLY")
    import hashlib
    _require(hashlib.sha256(registry.read_bytes()).hexdigest() == registry_hash, "LIVE_REGISTRY_CHANGED")
    print("PORTABLE BUILDER MEMBER LIVE REGISTRY UNCHANGED: PASS")
    print("PORTABLE PRODUCTION BUILD GATE CLOSED: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
