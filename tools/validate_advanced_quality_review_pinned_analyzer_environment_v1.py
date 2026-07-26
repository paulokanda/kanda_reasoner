# project-path: tools/validate_advanced_quality_review_pinned_analyzer_environment_v1.py
"""Validate Release 6 pinned analyzer environment ownership and real smoke behavior."""

from __future__ import annotations

import argparse
import hashlib
from importlib import import_module
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

FEATURE_ID = "advanced-quality-review-pinned-analyzer-environment-v1"


_PLANNER_PACKAGE = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."


def _planner_module(name: str):
    return import_module(_PLANNER_PACKAGE + name)


def _bootstrap(tool_root: Path) -> None:
    text = str(tool_root)
    if text not in sys.path:
        sys.path.insert(0, text)


def _ok(marker: str) -> None:
    print(marker + ": PASS")


def _fail(message: str) -> None:
    raise AssertionError(message)


def _hash_python_source_tree(root: Path) -> str:
    digest = hashlib.sha256()
    source_files = sorted(path for path in root.rglob("*.py") if path.is_file())
    for path in source_files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(relative)
        digest.update(data)
    return digest.hexdigest()


def _run(
    argv: list[str], cwd: Path, *, allowed: set[int]
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=str(cwd),
        shell=False,
        check=False,
        timeout=120.0,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    if result.returncode not in allowed:
        _fail(
            "COMMAND_FAILED:"
            + " ".join(argv)
            + "\nstdout="
            + result.stdout
            + "\nstderr="
            + result.stderr
        )
    return result


def _write_executable(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _controlled_contract_validation(
    real_tool_root: Path,
    real_project_root: Path,
) -> None:
    manifest_module = _planner_module("analyzer_environment_manifest")
    spec_module = _planner_module("analyzer_pinned_environment_spec")
    runtime_module = _planner_module("analyzer_tool_runtime_paths")
    support_module = _planner_module("workbench_project_support_paths")

    build_analyzer_environment_manifest = (
        manifest_module.build_analyzer_environment_manifest
    )
    load_analyzer_environment_manifest = (
        manifest_module.load_analyzer_environment_manifest
    )
    validate_analyzer_environment_manifest = (
        manifest_module.validate_analyzer_environment_manifest
    )
    write_analyzer_environment_manifest = (
        manifest_module.write_analyzer_environment_manifest
    )
    ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID = (
        spec_module.ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID
    )
    PINNED_ANALYZERS = spec_module.PINNED_ANALYZERS
    build_pinned_analyzer_environment_lock = (
        spec_module.build_pinned_analyzer_environment_lock
    )
    pinned_analyzer_spec_hash = spec_module.pinned_analyzer_spec_hash
    pinned_requirements_text = spec_module.pinned_requirements_text
    validate_pinned_analyzer_spec = spec_module.validate_pinned_analyzer_spec
    analyzer_environment_freeze_path = runtime_module.analyzer_environment_freeze_path
    analyzer_environment_manifest_path = (
        runtime_module.analyzer_environment_manifest_path
    )
    analyzer_environment_python = runtime_module.analyzer_environment_python
    analyzer_environment_requirements_copy_path = (
        runtime_module.analyzer_environment_requirements_copy_path
    )
    analyzer_environment_root = runtime_module.analyzer_environment_root
    analyzer_tool_runtime_root = runtime_module.analyzer_tool_runtime_root
    analyzer_tool_runtime_root_blockers = (
        runtime_module.analyzer_tool_runtime_root_blockers
    )
    daily_work_root = support_module.daily_work_root
    project_support_root = support_module.project_support_root

    if validate_pinned_analyzer_spec():
        _fail("PINNED_SPEC_INVALID")
    expected_versions = {
        "ruff": "0.15.21",
        "griffe": "2.1.0",
        "grimp": "3.15",
        "mypy": "2.1.0",
        "vulture": "2.16",
    }
    observed_versions = {item.engine_id: item.version for item in PINNED_ANALYZERS}
    if observed_versions != expected_versions:
        _fail("PINNED_VERSION_SET_MISMATCH")
    if not pinned_analyzer_spec_hash():
        _fail("PINNED_SPEC_HASH_EMPTY")
    _ok("PINNED_ANALYZER_VERSION_SPEC_EXACT")

    fixture_owner = daily_work_root(real_project_root) / "release6_environment_fixture"
    shutil.rmtree(fixture_owner, ignore_errors=True)
    tool_root = fixture_owner / "controlled_tool"
    project_root = fixture_owner / "controlled_project"
    tool_root.mkdir(parents=True)
    project_root.mkdir(parents=True)
    runtime_root = analyzer_tool_runtime_root(tool_root)
    env_root = analyzer_environment_root(tool_root)
    blockers = analyzer_tool_runtime_root_blockers(
        tool_root,
        env_root,
        active_project_root=project_root,
    )
    if blockers:
        _fail("SEPARATE_RUNTIME_BLOCKED:" + "|".join(blockers))
    if runtime_root == tool_root or runtime_root.is_relative_to(tool_root):
        _fail("TOOL_RUNTIME_NOT_SEPARATE_FROM_TOOL_SOURCE")
    for bad_path, expected in (
        (tool_root / "bad", "ANALYZER_RUNTIME_INSIDE_TOOL_SOURCE_ROOT"),
        (project_root / "bad", "ANALYZER_RUNTIME_INSIDE_PROJECT_SOURCE_ROOT"),
        (
            project_support_root(project_root) / "bad",
            "ANALYZER_RUNTIME_INSIDE_PROJECT_SUPPORT_ROOT",
        ),
        (
            daily_work_root(project_root) / "bad",
            "ANALYZER_RUNTIME_INSIDE_PROJECT_DAILY_WORK_ROOT",
        ),
    ):
        bad = analyzer_tool_runtime_root_blockers(
            tool_root,
            bad_path,
            active_project_root=project_root,
        )
        if expected not in bad:
            _fail("OWNERSHIP_BLOCKER_MISSING:" + expected)
    _ok("TOOL_RUNTIME_CONTAINER_SEPARATE_FROM_PROJECT_CONTAINERS")

    env_root.mkdir(parents=True, exist_ok=True)
    requirements_path = analyzer_environment_requirements_copy_path(tool_root)
    requirements_path.parent.mkdir(parents=True, exist_ok=True)
    requirements_path.write_bytes(pinned_requirements_text().encode("utf-8"))
    freeze_path = analyzer_environment_freeze_path(tool_root)
    freeze_path.write_bytes(
        ("\n".join(sorted(pinned_requirements_text().splitlines())) + "\n").encode(
            "utf-8"
        )
    )
    lock = build_pinned_analyzer_environment_lock(tool_root)
    manifest = build_analyzer_environment_manifest(
        feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        tool_root=tool_root,
        environment_root=env_root,
        python_executable=analyzer_environment_python(tool_root),
        python_version="3.12.0",
        implementation="CPython",
        platform_system=os.name,
        platform_release="controlled",
        environment_lock=lock,
        resolved_freeze_bytes=freeze_path.read_bytes(),
        requirements_bytes=requirements_path.read_bytes(),
        observed_versions=expected_versions,
    )
    write_analyzer_environment_manifest(tool_root, manifest)
    loaded = load_analyzer_environment_manifest(tool_root)
    manifest_blockers = validate_analyzer_environment_manifest(
        tool_root,
        loaded,
        expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        environment_lock=lock,
        expected_versions=expected_versions,
    )
    if manifest_blockers:
        _fail("MANIFEST_BLOCKED:" + "|".join(manifest_blockers))
    raw = analyzer_environment_manifest_path(tool_root).read_bytes()
    raw.decode("utf-8", errors="strict")
    if raw.startswith(b"\xef\xbb\xbf"):
        _fail("MANIFEST_HAS_UTF8_BOM")
    _ok("ANALYZER_ENVIRONMENT_MANIFEST_IMMUTABLE_IDENTITY")
    _ok("ANALYZER_ENVIRONMENT_METADATA_UTF8_NO_BOM")
    _ok("CONTROLLED_ENVIRONMENT_FIXTURE_PLATFORM_NEUTRAL")

    requirements_path.write_bytes(b"tampered\n")
    tampered = validate_analyzer_environment_manifest(
        tool_root,
        loaded,
        expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
        environment_lock=lock,
        expected_versions=expected_versions,
    )
    if "ANALYZER_MANIFEST_REQUIREMENTS_HASH_MISMATCH" not in tampered:
        _fail("MANIFEST_TAMPER_NOT_DETECTED")
    _ok("ANALYZER_ENVIRONMENT_LOCK_DRIFT_FAILS_CLOSED")
    shutil.rmtree(fixture_owner, ignore_errors=True)

    provisioner_source = (
        real_tool_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "analyzer_environment_provisioning.py"
    ).read_text(encoding="utf-8")
    preflight_source = (
        real_tool_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "analyzer_capability_preflight.py"
    ).read_text(encoding="utf-8")
    if 'pip",\n                "install' not in provisioner_source:
        _fail("EXPLICIT_PROVISIONER_INSTALL_CONTRACT_MISSING")
    if "pip install" in preflight_source or "subprocess" in preflight_source:
        _fail("CAPABILITY_PREFLIGHT_MAY_INSTALL_OR_MUTATE")
    _ok("PROVISIONING_EXPLICIT_NOT_REVIEW_BUTTON_SILENT_INSTALL")


def _real_environment_validation(tool_root: Path, project_root: Path) -> None:
    manifest_module = _planner_module("analyzer_environment_manifest")
    provisioning_module = _planner_module("analyzer_environment_provisioning")
    spec_module = _planner_module("analyzer_pinned_environment_spec")
    runtime_module = _planner_module("analyzer_tool_runtime_paths")
    support_module = _planner_module("workbench_project_support_paths")

    load_analyzer_environment_manifest = (
        manifest_module.load_analyzer_environment_manifest
    )
    validate_provisioned_analyzer_environment = (
        provisioning_module.validate_provisioned_analyzer_environment
    )
    build_pinned_analyzer_environment_lock = (
        spec_module.build_pinned_analyzer_environment_lock
    )
    analyzer_environment_python = runtime_module.analyzer_environment_python
    analyzer_environment_script = runtime_module.analyzer_environment_script
    daily_work_root = support_module.daily_work_root

    blockers = validate_provisioned_analyzer_environment(
        tool_root,
        active_project_root=project_root,
    )
    if blockers:
        _fail("REAL_ENVIRONMENT_BLOCKED:" + "|".join(blockers))
    manifest = load_analyzer_environment_manifest(tool_root)
    lock = build_pinned_analyzer_environment_lock(tool_root)
    if manifest.analyzer_lock_hash != lock.lock_hash:
        _fail("REAL_ENVIRONMENT_LOCK_HASH_MISMATCH")
    _ok("REAL_ANALYZER_ENVIRONMENT_LOCK_IDENTITY")

    fixture = daily_work_root(project_root) / "release6_real_analyzer_smoke"
    shutil.rmtree(fixture, ignore_errors=True)
    package = fixture / "samplepkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_bytes(b"from .api import public_value\n")
    (package / "api.py").write_bytes(
        b"import os\n\npublic_value = 1\n\ndef unused_function():\n    return 2\n"
    )
    type_bad = fixture / "type_bad.py"
    type_bad.write_bytes(b"value: int = 'bad'\n")
    smoke_cache = daily_work_root(project_root) / "release6_real_analyzer_smoke_cache"
    shutil.rmtree(smoke_cache, ignore_errors=True)
    before = _hash_python_source_tree(fixture)

    ruff = _run(
        [
            str(analyzer_environment_script(tool_root, "ruff")),
            "check",
            "--no-cache",
            "--output-format",
            "json",
            str(package / "api.py"),
        ],
        fixture,
        allowed={0, 1},
    )
    if not isinstance(json.loads(ruff.stdout), list):
        _fail("RUFF_REAL_SMOKE_JSON_INVALID")
    _ok("RUFF_REAL_ENVIRONMENT_SMOKE")

    griffe = _run(
        [
            str(analyzer_environment_script(tool_root, "griffe")),
            "dump",
            "--search",
            str(fixture),
            "samplepkg",
        ],
        fixture,
        allowed={0},
    )
    if not isinstance(json.loads(griffe.stdout), dict):
        _fail("GRIFFE_REAL_SMOKE_JSON_INVALID")
    _ok("GRIFFE_REAL_ENVIRONMENT_SMOKE")

    probe = (
        tool_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "grimp_graph_probe.py"
    )
    grimp = _run(
        [
            str(analyzer_environment_python(tool_root)),
            str(probe),
            "--root",
            str(fixture),
            "--package",
            "samplepkg",
            "--cache-dir",
            str(smoke_cache / "grimp"),
        ],
        fixture,
        allowed={0},
    )
    grimp_payload = json.loads(grimp.stdout)
    if not isinstance(grimp_payload.get("edges"), list):
        _fail("GRIMP_REAL_SMOKE_GRAPH_INVALID")
    _ok("GRIMP_REAL_ENVIRONMENT_SMOKE")

    mypy = _run(
        [
            str(analyzer_environment_script(tool_root, "mypy")),
            "--output",
            "json",
            "--cache-dir",
            str(smoke_cache / "mypy"),
            str(type_bad),
        ],
        fixture,
        allowed={0, 1},
    )
    json_lines = [line for line in mypy.stdout.splitlines() if line.strip()]
    if not json_lines:
        _fail("MYPY_REAL_SMOKE_OUTPUT_EMPTY")
    for line in json_lines:
        json.loads(line)
    _ok("MYPY_REAL_ENVIRONMENT_SMOKE")

    vulture = _run(
        [
            str(analyzer_environment_script(tool_root, "vulture")),
            str(package / "api.py"),
            "--min-confidence",
            "0",
        ],
        fixture,
        allowed={0, 3},
    )
    combined = vulture.stdout + "\n" + vulture.stderr
    if "confidence" not in combined.lower():
        _fail("VULTURE_REAL_SMOKE_CONFIDENCE_MISSING")
    _ok("VULTURE_REAL_ENVIRONMENT_SMOKE")

    cache_paths = (
        fixture / ".ruff_cache",
        fixture / ".mypy_cache",
        fixture / ".grimp_cache",
    )
    unexpected_caches = [path.name for path in cache_paths if path.exists()]
    if unexpected_caches:
        _fail("ANALYZER_CACHE_LEAKED_INTO_SMOKE_FIXTURE:" + "|".join(unexpected_caches))
    if not smoke_cache.is_relative_to(daily_work_root(project_root)):
        _fail("ANALYZER_SMOKE_CACHE_OUTSIDE_DAILY_WORK")
    _ok("ANALYZER_SMOKE_CACHES_TRANSIENT_GARBAGE_ONLY")

    after = _hash_python_source_tree(fixture)
    if before != after:
        _fail("REAL_ANALYZER_SMOKE_MUTATED_SOURCE")
    _ok("REAL_ANALYZER_SMOKE_SOURCE_IMMUTABILITY")
    shutil.rmtree(fixture, ignore_errors=True)
    shutil.rmtree(smoke_cache, ignore_errors=True)


def main() -> int:
    """Run controlled contracts and optional real analyzer smoke tests."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", default=".")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--require-real-environment", action="store_true")
    args = parser.parse_args()

    tool_root = Path(args.tool_root).expanduser().resolve(strict=True)
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    _bootstrap(tool_root)
    _controlled_contract_validation(tool_root, project_root)
    if args.require_real_environment:
        _real_environment_validation(tool_root, project_root)
    _ok("PINNED_ANALYZER_ENVIRONMENT_RELEASE6")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
