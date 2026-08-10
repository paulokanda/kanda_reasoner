"""Live validation for the committed Portable runtime path-and-hash allowlist."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path


FEATURE_ID = "portable-runtime-path-hash-allowlist-v1r4"
REQUIRED_CAPABILITY_PREFIX = (
    "registry-boundary-gate",
    "packaged-gui-smoke-isolation",
    "governed-root-exact-rollback",
    "runtime-path-hash-allowlist",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def _load_registry(project_root: Path) -> tuple[Path, str]:
    drive = Path(project_root.anchor).resolve()
    support_parent = (
        drive if project_root.anchor != "/" else project_root.parent
    )
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
    active_root = Path(str(record.get("project_root") or "")).resolve()
    mode = str(record.get("selection_mode") or "")
    _require(active_root == project_root, "ACTIVE_PROJECT_ROOT_MISMATCH")
    _require(mode == "EXPLICIT_SELF_HOSTING", "ACTIVE_PROJECT_MODE_MISMATCH")
    return registry, _sha256(registry)


def _expect_failure(callable_object, marker: str) -> None:
    from portable.errors import PortableBuildError

    try:
        callable_object()
    except PortableBuildError:
        print(marker)
        return
    raise RuntimeError(marker.replace(": PASS", ": FAIL"))


def _validate_static_contract(project_root: Path) -> None:
    source = (
        project_root / "portable" / "physical_runtime.py"
    ).read_text(encoding="utf-8")
    _require(".rglob(" not in source, "RUNTIME_RECURSIVE_DISCOVERY_REMAINS")
    _require("RUNTIME_DIRECTORIES" not in source, "LEGACY_RUNTIME_DIRECTORIES_REMAIN")
    _require("PORTABLE_RUNTIME_ALLOWLIST.json" in source, "ALLOWLIST_BINDING_MISSING")
    _require(
        "validate_runtime_allowlist_sources" in source,
        "ALLOWLIST_SOURCE_VALIDATOR_MISSING",
    )
    build_source = (
        project_root / "portable" / "build.py"
    ).read_text(encoding="utf-8")
    _require("hydrate_physical_runtime" in build_source, "WORKFLOW_HYDRATION_MISSING")
    _require("validate_physical_runtime" in build_source, "WORKFLOW_VALIDATION_MISSING")
    print("PORTABLE RUNTIME RECURSIVE DISCOVERY ABSENT: PASS")
    print("PORTABLE RUNTIME WORKFLOW INTEGRATION: PASS")


def _validate_payload_rejections(payload: dict[str, object]) -> None:
    from portable.physical_runtime import validate_runtime_allowlist_payload

    duplicate = copy.deepcopy(payload)
    duplicate["items"][1]["archive_relative"] = (
        duplicate["items"][0]["archive_relative"]
    )
    _expect_failure(
        lambda: validate_runtime_allowlist_payload(duplicate),
        "PORTABLE RUNTIME DUPLICATE ARCHIVE PATH REJECTED: PASS",
    )

    traversal = copy.deepcopy(payload)
    traversal["items"][0]["source_relative"] = "../escape.py"
    _expect_failure(
        lambda: validate_runtime_allowlist_payload(traversal),
        "PORTABLE RUNTIME TRAVERSAL PATH REJECTED: PASS",
    )

    backup_debris = copy.deepcopy(payload)
    backup_debris["items"][0]["source_relative"] = (
        "kanda_prompt_workspace/prompt_tools/"
        "sync_startup_routing_kernel_pack.py."
        "bak_startup_creator_canonical_zz_v11"
    )
    backup_debris["items"][0]["archive_relative"] = (
        "_internal/kanda_prompt_workspace/prompt_tools/"
        "sync_startup_routing_kernel_pack.py."
        "bak_startup_creator_canonical_zz_v11"
    )
    _expect_failure(
        lambda: validate_runtime_allowlist_payload(backup_debris),
        "PORTABLE RUNTIME BACKUP DEBRIS PATH REJECTED: PASS",
    )


def _validate_fixture(project_root: Path) -> None:
    from portable.physical_runtime import (
        RUNTIME_MANIFEST_RELATIVE,
        hydrate_physical_runtime,
        load_runtime_allowlist,
        validate_physical_runtime,
    )
    from portable.physical_runtime_validation import populate_fixture_project

    allowlist = load_runtime_allowlist()
    with tempfile.TemporaryDirectory(
        prefix="kanda_runtime_allowlist_v1_"
    ) as temp:
        root = Path(temp)
        fixture_project = root / "fixture_project"
        populate_fixture_project(
            fixture_project,
            reference_project_root=project_root,
        )
        extra_relative = (
            Path("kanda_prompt_workspace")
            / "prompt_tools"
            / "__unlisted_runtime_fixture__.txt"
        )
        extra = fixture_project / extra_relative
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("UNLISTED\n", encoding="utf-8")

        staged = root / "staged"
        staged.mkdir()
        hydrate_physical_runtime(fixture_project, staged)
        _require(
            not (
                staged
                / "_internal"
                / "kanda_prompt_workspace"
                / "prompt_tools"
                / extra_relative.name
            ).exists(),
            "UNLISTED_SOURCE_WAS_STAGED",
        )
        manifest = validate_physical_runtime(staged)
        _require(
            manifest.get("items") == allowlist.get("items"),
            "GENERATED_MANIFEST_NOT_EXACT",
        )
        _require(
            (staged / RUNTIME_MANIFEST_RELATIVE).is_file(),
            "GENERATED_MANIFEST_MISSING",
        )
        print("PORTABLE RUNTIME UNLISTED SOURCE FILE EXCLUDED: PASS")
        print("PORTABLE RUNTIME GENERATED MANIFEST IDENTITY: PASS")

        first = allowlist["items"][0]
        first_path = fixture_project / Path(str(first["source_relative"]))
        first_bytes = first_path.read_bytes()
        first_path.write_bytes(first_bytes + b"\nMUTATED")
        try:
            _expect_failure(
                lambda: hydrate_physical_runtime(
                    fixture_project,
                    root / "modified_stage",
                ),
                "PORTABLE RUNTIME MODIFIED SOURCE REJECTED: PASS",
            )
        finally:
            first_path.write_bytes(first_bytes)

        second = allowlist["items"][1]
        second_path = fixture_project / Path(str(second["source_relative"]))
        second_bytes = second_path.read_bytes()
        second_path.unlink()
        try:
            _expect_failure(
                lambda: hydrate_physical_runtime(
                    fixture_project,
                    root / "missing_stage",
                ),
                "PORTABLE RUNTIME MISSING SOURCE REJECTED: PASS",
            )
        finally:
            second_path.parent.mkdir(parents=True, exist_ok=True)
            second_path.write_bytes(second_bytes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    _require(project_root.name.casefold() == "kanda_reasoner", "TOOL_ROOT_NAME_MISMATCH")
    sys.path.insert(0, str(project_root))

    registry, registry_before = _load_registry(project_root)
    print("PORTABLE RUNTIME LIVE EXPLICIT SELF-HOSTING AUTHORITY: PASS")

    from portable.constants import (
        BUILDER_VERSION,
        FEATURE_ID as BUILDER_FEATURE_ID,
        PRODUCTION_PORTABLE_ENABLED,
    )
    from portable.physical_runtime import (
        REQUIRED_RUNTIME_ROLES,
        RUNTIME_ALLOWLIST_FEATURE_ID,
        load_runtime_allowlist,
        validate_runtime_allowlist_sources,
    )

    allowlist_path = (
        project_root / "portable" / "PORTABLE_RUNTIME_ALLOWLIST.json"
    )
    _require(allowlist_path.is_file(), "COMMITTED_ALLOWLIST_MISSING")
    payload = load_runtime_allowlist()
    _require(
        payload.get("feature_id") == RUNTIME_ALLOWLIST_FEATURE_ID,
        "COMMITTED_ALLOWLIST_IDENTITY_MISMATCH",
    )
    _require(
        payload.get("builder_feature_id") == BUILDER_FEATURE_ID,
        "COMMITTED_ALLOWLIST_BUILDER_FEATURE_MISMATCH",
    )
    payload_features = tuple(payload.get("hardening_features") or ())
    _require(
        payload_features[: len(REQUIRED_CAPABILITY_PREFIX)]
        == REQUIRED_CAPABILITY_PREFIX,
        "COMMITTED_ALLOWLIST_STAGE4_CAPABILITY_PREFIX_MISMATCH",
    )
    _require(
        set(payload.get("required_roles", [])) == set(REQUIRED_RUNTIME_ROLES),
        "COMMITTED_ALLOWLIST_ROLES_MISMATCH",
    )
    validate_runtime_allowlist_sources(project_root)
    from portable.policy import is_non_runtime_debris_path
    _require(
        not any(
            is_non_runtime_debris_path(str(item["source_relative"]))
            or is_non_runtime_debris_path(str(item["archive_relative"]))
            for item in payload["items"]
        ),
        "COMMITTED_ALLOWLIST_CONTAINS_NON_RUNTIME_DEBRIS",
    )

    print("PORTABLE RUNTIME COMMITTED ALLOWLIST: PASS")
    print("PORTABLE RUNTIME ALLOWLIST NON-RUNTIME DEBRIS ABSENT: PASS")
    print(f"PORTABLE RUNTIME ALLOWLIST ITEM COUNT: {payload['item_count']}")
    print("PORTABLE RUNTIME ALLOWLIST REQUIRED ROLES: PASS")
    print("PORTABLE RUNTIME ALLOWLIST EXACT SOURCE PATHS: PASS")
    print("PORTABLE RUNTIME ALLOWLIST EXACT ARCHIVE PATHS: PASS")
    print("PORTABLE RUNTIME ALLOWLIST EXACT SHA-256: PASS")

    _validate_static_contract(project_root)
    _validate_payload_rejections(payload)
    _validate_fixture(project_root)

    manifest = json.loads(
        (
            project_root
            / "portable"
            / "PORTABLE_BUILDER_MANIFEST.json"
        ).read_text(encoding="utf-8")
    )
    _require(
        manifest.get("feature_id") == BUILDER_FEATURE_ID,
        "BUILDER_MANIFEST_FEATURE_ID_MISMATCH",
    )
    _require(
        manifest.get("builder_version") == BUILDER_VERSION,
        "BUILDER_MANIFEST_VERSION_MISMATCH",
    )
    manifest_features = tuple(manifest.get("hardening_features") or ())
    _require(
        manifest_features[: len(REQUIRED_CAPABILITY_PREFIX)]
        == REQUIRED_CAPABILITY_PREFIX,
        "BUILDER_MANIFEST_STAGE4_CAPABILITY_PREFIX_MISMATCH",
    )
    _require(
        payload.get("builder_version") == BUILDER_VERSION,
        "ALLOWLIST_BUILDER_VERSION_MISMATCH",
    )
    _require(
        manifest.get("exact_physical_runtime_allowlist_pending") is False,
        "ALLOWLIST_PENDING_FLAG_REMAINS",
    )
    _require(
        manifest.get("exact_physical_runtime_path_hash_allowlist") is True,
        "ALLOWLIST_CONTRACT_FLAG_MISSING",
    )
    _require(
        manifest.get("runtime_allowlist_sha256") == _sha256(allowlist_path),
        "BUILDER_MANIFEST_ALLOWLIST_HASH_MISMATCH",
    )
    _require(
        int(manifest.get("runtime_allowlist_item_count", -1))
        == int(payload["item_count"]),
        "BUILDER_MANIFEST_ALLOWLIST_COUNT_MISMATCH",
    )
    validator_contracts = {
        "registry": (
            project_root
            / "tools"
            / "validate_portable_registry_boundary_gate_v1.py"
        ),
        "smoke": (
            project_root
            / "tools"
            / "validate_portable_smoke_isolation_v1.py"
        ),
        "rollback": (
            project_root
            / "tools"
            / "validate_portable_governed_root_rollback_v1.py"
        ),
    }
    validator_text = {
        name: path.read_text(encoding="utf-8-sig")
        for name, path in validator_contracts.items()
    }
    _require(
        '"registry-boundary-gate" in PORTABLE_HARDENING_FEATURES'
        in validator_text["registry"],
        "REGISTRY_VALIDATOR_NOT_CAPABILITY_BASED",
    )
    _require(
        '"packaged-gui-smoke-isolation" in PORTABLE_HARDENING_FEATURES'
        in validator_text["smoke"],
        "SMOKE_VALIDATOR_NOT_CAPABILITY_BASED",
    )
    _require(
        '"governed-root-exact-rollback" not in PORTABLE_HARDENING_FEATURES'
        in validator_text["rollback"],
        "ROLLBACK_VALIDATOR_NOT_CAPABILITY_BASED",
    )
    _require(
        "PORTABLE_HARDENING_STAGE ==" not in validator_text["registry"],
        "REGISTRY_VALIDATOR_STILL_PINS_CUMULATIVE_STAGE",
    )
    print("PORTABLE STAGE 4 VALIDATOR FORWARD COMPATIBILITY: PASS")
    print("PORTABLE PRIOR-STAGE VALIDATOR FORWARD COMPATIBILITY: PASS")
    print("PORTABLE HARDENING CAPABILITY SET IDENTITY: PASS")

    _require(PRODUCTION_PORTABLE_ENABLED is False, "PRODUCTION_GATE_OPENED_EARLY")
    _require(_sha256(registry) == registry_before, "LIVE_REGISTRY_CHANGED")

    print("PORTABLE RUNTIME BUILDER IDENTITY CHAIN: PASS")
    print("PORTABLE RUNTIME BUILDER MANIFEST BINDING: PASS")
    print("PORTABLE RUNTIME LIVE REGISTRY UNCHANGED: PASS")
    print("PORTABLE PRODUCTION BUILD GATE CLOSED: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
