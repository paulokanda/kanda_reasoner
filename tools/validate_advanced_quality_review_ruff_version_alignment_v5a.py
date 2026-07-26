# project-path: tools/validate_advanced_quality_review_ruff_version_alignment_v5a.py
"""Validate AQR Ruff version alignment with the canonical project policy."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
from importlib import import_module
import json
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import zipfile

__all__ = [
    "main",
]

FEATURE_ID = "advanced-quality-review-ruff-version-alignment-v5a"
REQUIRED_RUFF_VERSION = "0.15.21"
OLD_PINNED_SPEC_HASH = (
    "08f2fe77086f2cec6d15619b3cfbcb550cd90efef25ffb45db3a7977ec11a783"
)
EXPECTED_PATCH_MEMBERS = {
    "KANDA_FREEZE_HINT.json",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "analyzer_environment_requirements_v1.txt",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "analyzer_pinned_environment_spec.py",
    "tools/validate_advanced_quality_review_pinned_analyzer_environment_v1.py",
    "tools/validate_advanced_quality_review_ruff_version_alignment_v5a.py",
}
UNCHANGED_OWNER_HASHES = {
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "analyzer_environment_manifest.py": (
        "42290d5c76c081bf51afb7895c0dc635e90c7b19c7ec3774d5a96f1fc3a80674"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "analyzer_environment_provisioning.py": (
        "8d304fc140493db647317256992a45ad424e7726afa63f08ba9ea2eaa28686bd"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "advanced_quality_review_orchestration.py": (
        "289ba6c50583db84836f38b21e9c78ffd96e445d06a1b67e65ef3eb8943c3f96"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "ruff_fitness_adapter.py": (
        "4582dea14445bac29c525e05923265777643c841b10e75ed22d7192208143c6d"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_post_apply_ruff_validation.py": (
        "7fd0612441caeef2e4ecec54d58c2d7ad7aef90bfd5abdf7c9d39792417a8ced"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_post_apply_validator.py": (
        "b07b022cd1057163b61b4ef9620b8c51994df72dbf20c8ee663e272be1c129cc"
    ),
}


_PLANNER_PACKAGE = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."


def _planner_module(name: str):
    return import_module(_PLANNER_PACKAGE + name)


EXPECTED_VERSIONS = {
    "ruff": "0.15.21",
    "griffe": "2.1.0",
    "grimp": "3.15",
    "mypy": "2.1.0",
    "vulture": "2.16",
}


def _ok(marker: str) -> None:
    print(marker + ": PASS")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _bootstrap(project_root: Path) -> None:
    text = str(project_root)
    if text not in sys.path:
        sys.path.insert(0, text)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_digest(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    for item in sorted(
        candidate for candidate in path.rglob("*") if candidate.is_file()
    ):
        relative = item.relative_to(path).as_posix().encode("utf-8")
        data = item.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def _validate_patch_members(patch_zip: Path) -> None:
    with zipfile.ZipFile(patch_zip) as archive:
        members = {name.replace("\\", "/") for name in archive.namelist()}
    _assert(members == EXPECTED_PATCH_MEMBERS, "PATCH_MEMBER_SCOPE_CHANGED")
    _ok("PATCH_MEMBER_SCOPE_RUFF_VERSION_ALIGNMENT_ONLY")


def _validate_owner_identity(project_root: Path) -> None:
    for relative, expected in UNCHANGED_OWNER_HASHES.items():
        path = project_root / relative
        _assert(path.is_file(), "UNCHANGED_OWNER_MISSING:" + relative)
        _assert(_sha256(path) == expected, "UNCHANGED_OWNER_DRIFT:" + relative)
    _ok("AQR_ORCHESTRATION_AND_PHASE4_BYTE_IDENTITY")


def _validate_spec_and_policy(project_root: Path) -> None:
    spec_module = _planner_module("analyzer_pinned_environment_spec")
    policy_module = import_module(
        "kanda_reasoner_app.source_hygiene.ruff_policy_identity"
    )
    PINNED_ANALYZERS = spec_module.PINNED_ANALYZERS
    pinned_analyzer_spec_hash = spec_module.pinned_analyzer_spec_hash
    pinned_requirements_text = spec_module.pinned_requirements_text
    validate_pinned_analyzer_spec = spec_module.validate_pinned_analyzer_spec
    resolve_ruff_policy_identity = policy_module.resolve_ruff_policy_identity

    _assert(not validate_pinned_analyzer_spec(), "PINNED_ANALYZER_SPEC_BLOCKED")
    observed = {item.engine_id: item.version for item in PINNED_ANALYZERS}
    _assert(observed == EXPECTED_VERSIONS, "PINNED_ANALYZER_VERSION_SET_MISMATCH")
    _assert(
        pinned_analyzer_spec_hash() != OLD_PINNED_SPEC_HASH,
        "PINNED_SPEC_HASH_DID_NOT_CHANGE",
    )
    requirements_path = (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "analyzer_environment_requirements_v1.txt"
    )
    _assert(
        requirements_path.read_text(encoding="utf-8") == pinned_requirements_text(),
        "PINNED_REQUIREMENTS_NOT_IN_SYNC",
    )
    identity = resolve_ruff_policy_identity(project_root)
    _assert(
        identity.required_version == "==" + REQUIRED_RUFF_VERSION,
        "PROJECT_RUFF_POLICY_VERSION_MISMATCH",
    )
    _assert(
        observed["ruff"] == identity.required_version.removeprefix("=="),
        "AQR_RUFF_AND_PROJECT_POLICY_NOT_ALIGNED",
    )
    _ok("AQR_PINNED_RUFF_VERSION_0_15_21")
    _ok("AQR_RUFF_PROJECT_POLICY_VERSION_ALIGNMENT")
    _ok("PINNED_REQUIREMENTS_SPEC_IN_SYNC")


def _validate_manifest_contract(project_root: Path) -> None:
    manifest_module = _planner_module("analyzer_environment_manifest")
    spec_module = _planner_module("analyzer_pinned_environment_spec")
    runtime_module = _planner_module("analyzer_tool_runtime_paths")
    build_analyzer_environment_manifest = (
        manifest_module.build_analyzer_environment_manifest
    )
    validate_analyzer_environment_manifest = (
        manifest_module.validate_analyzer_environment_manifest
    )
    ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID = (
        spec_module.ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID
    )
    build_pinned_analyzer_environment_lock = (
        spec_module.build_pinned_analyzer_environment_lock
    )
    pinned_requirements_text = spec_module.pinned_requirements_text
    analyzer_environment_freeze_path = runtime_module.analyzer_environment_freeze_path
    analyzer_environment_requirements_copy_path = (
        runtime_module.analyzer_environment_requirements_copy_path
    )
    analyzer_environment_root = runtime_module.analyzer_environment_root
    analyzer_tool_runtime_root = runtime_module.analyzer_tool_runtime_root
    analyzer_tool_runtime_root_blockers = (
        runtime_module.analyzer_tool_runtime_root_blockers
    )

    fixture_root = (
        analyzer_tool_runtime_root(project_root)
        / "validation_fixtures"
        / "aqr_ruff_version_alignment_v5a"
    )
    shutil.rmtree(fixture_root, ignore_errors=True)
    tool_root = fixture_root / "tool"
    tool_root.mkdir(parents=True)
    env_root = analyzer_environment_root(tool_root)
    env_root.mkdir(parents=True)
    requirements_bytes = pinned_requirements_text().encode("utf-8")
    requirements_path = analyzer_environment_requirements_copy_path(tool_root)
    requirements_path.parent.mkdir(parents=True, exist_ok=True)
    requirements_path.write_bytes(requirements_bytes)
    freeze_bytes = (
        "\n".join(sorted(pinned_requirements_text().splitlines())) + "\n"
    ).encode("utf-8")
    freeze_path = analyzer_environment_freeze_path(tool_root)
    freeze_path.write_bytes(freeze_bytes)
    lock = build_pinned_analyzer_environment_lock(tool_root)
    manifest = build_analyzer_environment_manifest(
        feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        tool_root=tool_root,
        environment_root=env_root,
        python_executable=env_root / "python",
        python_version="3.10.0",
        implementation="CPython",
        platform_system="controlled",
        platform_release="controlled",
        environment_lock=lock,
        resolved_freeze_bytes=freeze_bytes,
        requirements_bytes=requirements_bytes,
        observed_versions=EXPECTED_VERSIONS,
    )
    blockers = validate_analyzer_environment_manifest(
        tool_root,
        manifest,
        expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        environment_lock=lock,
        expected_versions=EXPECTED_VERSIONS,
    )
    _assert(not blockers, "CURRENT_MANIFEST_CONTRACT_BLOCKED:" + "|".join(blockers))
    stale_spec = replace(manifest, pinned_spec_hash=OLD_PINNED_SPEC_HASH)
    stale_spec_blockers = validate_analyzer_environment_manifest(
        tool_root,
        stale_spec,
        expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        environment_lock=lock,
        expected_versions=EXPECTED_VERSIONS,
    )
    _assert(
        "ANALYZER_MANIFEST_PINNED_SPEC_HASH_MISMATCH" in stale_spec_blockers,
        "STALE_PINNED_SPEC_MANIFEST_NOT_BLOCKED",
    )
    stale_versions = dict(EXPECTED_VERSIONS)
    stale_versions["ruff"] = "0.15.20"
    stale_version_manifest = replace(
        manifest,
        observed_versions=tuple(
            replace(item, observed_version=stale_versions[item.engine_id])
            for item in manifest.observed_versions
        ),
    )
    stale_version_blockers = validate_analyzer_environment_manifest(
        tool_root,
        stale_version_manifest,
        expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        environment_lock=lock,
        expected_versions=EXPECTED_VERSIONS,
    )
    _assert(
        "ANALYZER_MANIFEST_OBSERVED_VERSION_SET_MISMATCH" in stale_version_blockers,
        "STALE_RUFF_VERSION_MANIFEST_NOT_BLOCKED",
    )
    ownership_blockers = analyzer_tool_runtime_root_blockers(
        tool_root,
        env_root,
        active_project_root=project_root,
    )
    _assert(
        not ownership_blockers,
        "TOOL_RUNTIME_OWNERSHIP_BLOCKED:" + "|".join(ownership_blockers),
    )
    shutil.rmtree(fixture_root, ignore_errors=True)
    _ok("AQR_STALE_0_15_20_MANIFEST_FAILS_CLOSED")
    _ok("AQR_0_15_21_MANIFEST_CONTRACT")


def _validate_python_files(project_root: Path) -> None:
    relative_paths = (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "analyzer_pinned_environment_spec.py",
        "tools/validate_advanced_quality_review_pinned_analyzer_environment_v1.py",
        "tools/validate_advanced_quality_review_ruff_version_alignment_v5a.py",
    )
    for relative in relative_paths:
        path = project_root / relative
        raw = path.read_bytes()
        raw.decode("ascii")
        compile_root = project_root.parent / (
            project_root.name + "_delete_after_daily_work"
        )
        compile_root.mkdir(parents=True, exist_ok=True)
        compiled_path = compile_root / (path.name + ".v5a.pyc")
        py_compile.compile(str(path), cfile=str(compiled_path), doraise=True)
        compiled_path.unlink(missing_ok=True)
        _assert(
            len(path.read_text(encoding="utf-8").splitlines()) < 500,
            "MODULE_SIZE_LAW_VIOLATION:" + relative,
        )
    _ok("PYTHON_COMPILE")
    _ok("ASCII_PYTHON_SOURCE")
    _ok("MODULE_SIZE_LAW_BELOW_500")


def _validate_runtime_ruff(project_root: Path, executable: Path) -> None:
    _assert(executable.is_file(), "RUFF_EXECUTABLE_MISSING")
    version = subprocess.run(
        [str(executable), "--version"],
        cwd=str(project_root),
        shell=False,
        check=False,
        timeout=30.0,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    _assert(version.returncode == 0, "RUFF_VERSION_COMMAND_FAILED")
    _assert(
        version.stdout.strip() == "ruff " + REQUIRED_RUFF_VERSION,
        "RUFF_RUNTIME_VERSION_MISMATCH:" + version.stdout.strip(),
    )
    fixture = (
        project_root.parent
        / (project_root.name + "_delete_after_daily_work")
        / "aqr_v5a_ruff_smoke"
    )
    shutil.rmtree(fixture, ignore_errors=True)
    fixture.mkdir(parents=True)
    source = fixture / "sample.py"
    source.write_text('"""Controlled Ruff smoke."""\n\nVALUE = 1\n', encoding="utf-8")
    before = _sha256(source)
    cache_path = project_root / ".ruff_cache"
    cache_before = _tree_digest(cache_path)
    commands = (
        [
            str(executable),
            "check",
            "--config",
            str(project_root / "ruff.toml"),
            "--no-cache",
            str(source),
        ],
        [
            str(executable),
            "format",
            "--check",
            "--config",
            str(project_root / "ruff.toml"),
            "--no-cache",
            str(source),
        ],
    )
    for command in commands:
        result = subprocess.run(
            command,
            cwd=str(project_root),
            shell=False,
            check=False,
            timeout=60.0,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
        _assert(
            result.returncode == 0,
            "RUFF_RUNTIME_SMOKE_FAILED:"
            + json.dumps(command)
            + "\n"
            + result.stdout
            + result.stderr,
        )
    _assert(_sha256(source) == before, "RUFF_RUNTIME_SMOKE_MUTATED_SOURCE")
    _assert(
        _tree_digest(cache_path) == cache_before,
        "PROJECT_RUFF_CACHE_STATE_CHANGED",
    )
    shutil.rmtree(fixture, ignore_errors=True)
    _ok("RUNTIME_RUFF_0_15_21")
    _ok("RUNTIME_RUFF_POLICY_COMPATIBILITY")
    _ok("RUNTIME_RUFF_READ_ONLY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--ruff-executable", default="")
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    patch_zip = Path(args.patch_zip).expanduser().resolve(strict=True)
    _bootstrap(project_root)
    _validate_patch_members(patch_zip)
    _validate_owner_identity(project_root)
    _validate_spec_and_policy(project_root)
    _validate_manifest_contract(project_root)
    _validate_python_files(project_root)
    if str(args.ruff_executable).strip():
        _validate_runtime_ruff(
            project_root,
            Path(args.ruff_executable).expanduser().resolve(strict=True),
        )
    _ok("PATCH_ZIP_CONTRACT")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
