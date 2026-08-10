"""Live validation for external Portable build-control hash binding."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "portable-external-build-control-hash-binding-v1r1"
EXPECTED_BUILDER_FEATURE = "kanda-reasoner-portable-builder-install-v1r12"
EXPECTED_STAGE_FEATURE = (
    "kanda-reasoner-portable-external-build-control-hash-binding-v1r1"
)
EXPECTED_FEATURES = (
    "registry-boundary-gate",
    "packaged-gui-smoke-isolation",
    "governed-root-exact-rollback",
    "runtime-path-hash-allowlist",
    "exact-builder-member-governance",
    "external-build-control-hash-binding",
)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_registry(project_root: Path) -> tuple[Path, str]:
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
    return registry, _sha256(registry)


def _expect_external_failure(callable_object, marker: str) -> None:
    from portable.external_controls import ExternalControlError
    try:
        callable_object()
    except ExternalControlError:
        print(marker)
        return
    raise RuntimeError(marker.replace(": PASS", ": FAIL"))


def _copy_control_fixture(project_root: Path, destination: Path) -> Path:
    fixture = destination / "kanda_reasoner"
    (fixture / "portable").mkdir(parents=True)
    shutil.copyfile(
        project_root / "portable" / "PORTABLE_EXTERNAL_BUILD_CONTROLS.json",
        fixture / "portable" / "PORTABLE_EXTERNAL_BUILD_CONTROLS.json",
    )
    manifest = json.loads(
        (fixture / "portable" / "PORTABLE_EXTERNAL_BUILD_CONTROLS.json").read_text(encoding="utf-8")
    )
    for item in manifest["items"]:
        relative = Path(str(item["source_relative"]))
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(project_root / relative, target)
    return fixture


def _write_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _functional_build_order_fixture(project_root: Path) -> None:
    from portable.build import build_application
    import portable.build as build_module
    from portable.errors import PortableBuildError
    from portable.models import BuildPaths

    with tempfile.TemporaryDirectory(prefix="kanda_external_control_build_v1_") as temp:
        temp_root = Path(temp)
        fixture = _copy_control_fixture(project_root, temp_root)
        run_root = temp_root / "run"
        dummy = temp_root / "dummy"
        paths = BuildPaths(
            project_root=fixture,
            drive_root=temp_root,
            project_support_root=dummy,
            transient_root=dummy,
            run_root=run_root,
            pyinstaller_work=run_root / "work",
            pyinstaller_dist=run_root / "dist",
            pyinstaller_config=run_root / "config",
            temporary_root=run_root / "temp",
            stage_parent=run_root / "stage",
            candidate_zip=run_root / "candidate.zip",
            clean_extract_root=run_root / "extract",
            final_zip=run_root / "final.zip",
            spec_path=fixture / "KandaReasonerWindows.spec",
            governed_python=Path(sys.executable),
            zip_helper=dummy,
        )
        target = fixture / "KandaReasonerWindows.spec"
        original = target.read_bytes()
        target.write_bytes(original + b"\nMUTATED")
        called = {"value": False}
        original_run_command = build_module.run_command
        def forbidden_run_command(*args, **kwargs):
            called["value"] = True
        build_module.run_command = forbidden_run_command
        try:
            try:
                build_application(paths)
            except PortableBuildError:
                _require(not called["value"], "PYINSTALLER_STARTED_BEFORE_CONTROL_REJECTION")
                print("PORTABLE EXTERNAL CONTROL PRE-PYINSTALLER MUTATION REJECTED: PASS")
            else:
                raise RuntimeError("PRE_PYINSTALLER_MUTATION_ACCEPTED")
        finally:
            build_module.run_command = original_run_command
            target.write_bytes(original)

        def mutate_during_command(command, *, cwd, environment=None):
            app = paths.pyinstaller_dist / "kanda_reasoner"
            internal = app / "_internal"
            internal.mkdir(parents=True, exist_ok=True)
            (app / "kanda_reasoner.exe").write_bytes(b"MZ")
            (internal / "QtWebEngineProcess.exe").write_bytes(b"MZ")
            (internal / "qwindows.dll").write_bytes(b"DLL")
            target.write_bytes(original + b"\nTOCTOU")
        build_module.run_command = mutate_during_command
        try:
            try:
                build_application(paths)
            except PortableBuildError:
                print("PORTABLE EXTERNAL CONTROL PYINSTALLER TOCTOU MUTATION REJECTED: PASS")
            else:
                raise RuntimeError("PYINSTALLER_TOCTOU_MUTATION_ACCEPTED")
        finally:
            build_module.run_command = original_run_command
            target.write_bytes(original)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    project_root = args.project_root.resolve()
    _require(project_root.name.casefold() == "kanda_reasoner", "TOOL_ROOT_NAME_MISMATCH")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(project_root))
    registry, registry_hash = _load_registry(project_root)
    print("PORTABLE EXTERNAL CONTROL LIVE EXPLICIT SELF-HOSTING AUTHORITY: PASS")

    from portable.constants import (
        EXTERNAL_CONTROL_FEATURE_ID,
        FEATURE_ID as BUILDER_FEATURE_ID,
        PORTABLE_HARDENING_FEATURES,
        PRODUCTION_PORTABLE_ENABLED,
    )
    from portable.external_controls import (
        REQUIRED_EXTERNAL_CONTROLS,
        validate_external_build_controls,
    )
    portable_root = project_root / "portable"
    manifest_path = portable_root / "PORTABLE_BUILDER_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _require(BUILDER_FEATURE_ID == EXPECTED_BUILDER_FEATURE, "BUILDER_FEATURE_ID_MISMATCH")
    _require(EXTERNAL_CONTROL_FEATURE_ID == EXPECTED_STAGE_FEATURE, "STAGE6_FEATURE_ID_MISMATCH")
    _require(tuple(PORTABLE_HARDENING_FEATURES) == EXPECTED_FEATURES, "STAGE6_CAPABILITY_SET_MISMATCH")
    _require(manifest.get("external_control_feature_id") == EXPECTED_STAGE_FEATURE, "MANIFEST_STAGE6_FEATURE_ID_MISMATCH")
    _require(manifest.get("external_control_hash_binding_pending") is False, "EXTERNAL_CONTROL_BINDING_STILL_PENDING")
    _require(manifest.get("external_control_hash_binding") is True, "EXTERNAL_CONTROL_BINDING_FLAG_MISSING")
    evidence = validate_external_build_controls(project_root, portable_root)
    _require(evidence["item_count"] == len(REQUIRED_EXTERNAL_CONTROLS) == 7, "EXTERNAL_CONTROL_COUNT_MISMATCH")
    _require(manifest.get("external_control_manifest_sha256") == evidence["manifest_sha256"], "BUILDER_MANIFEST_EXTERNAL_CONTROL_HASH_MISMATCH")
    _require(int(manifest.get("external_control_item_count", -1)) == 7, "BUILDER_MANIFEST_EXTERNAL_CONTROL_COUNT_MISMATCH")
    print("PORTABLE EXTERNAL BUILD CONTROL MANIFEST: PASS")
    print("PORTABLE EXTERNAL BUILD CONTROL ITEM COUNT: 7")
    print("PORTABLE EXTERNAL BUILD CONTROL EXACT PATHS: PASS")
    print("PORTABLE EXTERNAL BUILD CONTROL EXACT SIZES: PASS")
    print("PORTABLE EXTERNAL BUILD CONTROL EXACT SHA-256: PASS")
    print("PORTABLE EXTERNAL BUILD CONTROL SET SHA-256: PASS")

    with tempfile.TemporaryDirectory(prefix="kanda_external_controls_v1_") as temp:
        fixture = _copy_control_fixture(project_root, Path(temp))
        fixture_portable = fixture / "portable"
        fixture_manifest_path = fixture_portable / "PORTABLE_EXTERNAL_BUILD_CONTROLS.json"
        baseline = json.loads(fixture_manifest_path.read_text(encoding="utf-8"))
        first_relative = Path(str(baseline["items"][0]["source_relative"]))
        first_path = fixture / first_relative
        original = first_path.read_bytes()
        first_path.write_bytes(original + b"\nMUTATED")
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL MODIFIED FILE REJECTED: PASS",
        )
        first_path.write_bytes(original)
        first_path.unlink()
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL MISSING FILE REJECTED: PASS",
        )
        first_path.parent.mkdir(parents=True, exist_ok=True)
        first_path.write_bytes(original)

        unlisted = copy.deepcopy(baseline)
        unlisted["items"].append(copy.deepcopy(unlisted["items"][0]))
        unlisted["item_count"] = len(unlisted["items"])
        _write_manifest(fixture_manifest_path, unlisted)
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL UNLISTED MANIFEST ITEM REJECTED: PASS",
        )

        duplicate = copy.deepcopy(baseline)
        duplicate["items"][1]["source_relative"] = duplicate["items"][0]["source_relative"]
        _write_manifest(fixture_manifest_path, duplicate)
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL DUPLICATE PATH REJECTED: PASS",
        )

        traversal = copy.deepcopy(baseline)
        traversal["items"][0]["source_relative"] = "../escape.spec"
        _write_manifest(fixture_manifest_path, traversal)
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL TRAVERSAL PATH REJECTED: PASS",
        )

        reordered = copy.deepcopy(baseline)
        reordered["items"] = list(reversed(reordered["items"]))
        _write_manifest(fixture_manifest_path, reordered)
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL ORDER REJECTED: PASS",
        )

        role = copy.deepcopy(baseline)
        role["items"][0]["role"] = "unexpected_role"
        _write_manifest(fixture_manifest_path, role)
        _expect_external_failure(
            lambda: validate_external_build_controls(fixture, fixture_portable),
            "PORTABLE EXTERNAL CONTROL ROLE MISMATCH REJECTED: PASS",
        )
        _write_manifest(fixture_manifest_path, baseline)

    _functional_build_order_fixture(project_root)
    environment_text = (portable_root / "environment.py").read_text(encoding="utf-8")
    build_text = (portable_root / "build.py").read_text(encoding="utf-8")
    _require("validate_external_build_controls" in environment_text, "ENVIRONMENT_PREFLIGHT_BINDING_MISSING")
    _require(build_text.count("validate_external_build_controls") >= 2, "PRE_POST_PYINSTALLER_BINDING_MISSING")
    _require(build_text.index("validate_external_build_controls") < build_text.index("run_command("), "CONTROL_CHECK_AFTER_PYINSTALLER")
    print("PORTABLE EXTERNAL CONTROLS VERIFIED BEFORE PYINSTALLER: PASS")
    print("PORTABLE EXTERNAL CONTROLS UNCHANGED THROUGH PYINSTALLER: PASS")

    stage5_text = (
        project_root / "tools" / "validate_portable_exact_builder_member_governance_v1.py"
    ).read_text(encoding="utf-8")
    _require("EXPECTED_FEATURE_PREFIX" in stage5_text, "STAGE5_VALIDATOR_PREFIX_CONTRACT_MISSING")
    _require("tuple(PORTABLE_HARDENING_FEATURES) == EXPECTED_FEATURES" not in stage5_text, "STAGE5_VALIDATOR_PINS_CUMULATIVE_SET")
    print("PORTABLE STAGE 5 VALIDATOR FORWARD COMPATIBILITY: PASS")
    print("PORTABLE EXTERNAL BUILD CONTROL HASH BINDING CAPABILITY IDENTITY: PASS")
    _require(PRODUCTION_PORTABLE_ENABLED is False, "PRODUCTION_GATE_OPENED_EARLY")
    _require(_sha256(registry) == registry_hash, "LIVE_REGISTRY_CHANGED")
    print("PORTABLE EXTERNAL CONTROL LIVE REGISTRY UNCHANGED: PASS")
    print("PORTABLE PRODUCTION BUILD GATE CLOSED: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
