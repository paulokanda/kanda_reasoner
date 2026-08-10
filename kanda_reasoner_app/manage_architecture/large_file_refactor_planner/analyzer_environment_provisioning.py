# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_environment_provisioning.py
"""Explicit provisioning workflow for the Tool-owned analyzer environment."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import subprocess
import venv

from .analyzer_capability_preflight import preflight_analyzer_capabilities
from .analyzer_environment_manifest import (
    build_analyzer_environment_manifest,
    load_analyzer_environment_manifest,
    validate_analyzer_environment_manifest,
    write_analyzer_environment_manifest,
)
from .analyzer_pinned_environment_spec import (
    ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
    PINNED_ANALYZERS,
    build_pinned_analyzer_environment_lock,
    pinned_requirements_text,
    validate_pinned_analyzer_spec,
)
from .analyzer_tool_runtime_paths import (
    analyzer_environment_freeze_path,
    analyzer_environment_install_report_path,
    analyzer_environment_manifest_path,
    analyzer_environment_python,
    analyzer_environment_requirements_copy_path,
    analyzer_environment_root,
    analyzer_tool_runtime_root_blockers,
)

__all__ = [
    "AnalyzerProvisioningResult",
    "provision_analyzer_environment",
    "validate_provisioned_analyzer_environment",
    "main",
]


@dataclass(frozen=True)
class AnalyzerProvisioningResult:
    """Summarize one explicit environment provision or idempotent reuse."""

    status: str
    environment_root: str
    manifest_path: str
    analyzer_lock_hash: str
    manifest_hash: str
    diagnostics: tuple[str, ...]


def provision_analyzer_environment(
    tool_root: str | Path,
    *,
    requirements_source: str | Path,
    active_project_root: str | Path | None = None,
    force_recreate: bool = False,
    install_timeout_seconds: float = 900.0,
) -> AnalyzerProvisioningResult:
    """Create or reuse the exact Tool-owned analyzer environment explicitly."""
    source_root = Path(tool_root).expanduser().resolve(strict=True)
    requirements_path = Path(requirements_source).expanduser().resolve(strict=True)
    spec_blockers = validate_pinned_analyzer_spec()
    if spec_blockers:
        raise RuntimeError("ANALYZER_PINNED_SPEC_BLOCKED:" + "|".join(spec_blockers))
    expected_requirements = pinned_requirements_text().encode("utf-8")
    if requirements_path.read_bytes() != expected_requirements:
        raise RuntimeError("ANALYZER_REQUIREMENTS_SOURCE_MISMATCH")
    env_root = analyzer_environment_root(source_root)
    ownership_blockers = analyzer_tool_runtime_root_blockers(
        source_root,
        env_root,
        active_project_root=active_project_root,
    )
    if ownership_blockers:
        raise RuntimeError(
            "ANALYZER_TOOL_RUNTIME_OWNERSHIP_BLOCKED:"
            + "|".join(ownership_blockers)
        )
    if not force_recreate:
        reusable = _reuse_if_valid(
            source_root,
            active_project_root=active_project_root,
        )
        if reusable is not None:
            return reusable
    slot_root = env_root.parent
    backup_root = slot_root.with_name(slot_root.name + ".backup_release6")
    _remove_path(backup_root)
    if slot_root.exists():
        slot_root.rename(backup_root)
    try:
        slot_root.mkdir(parents=True, exist_ok=True)
        _create_virtual_environment(env_root)
        env_python = analyzer_environment_python(source_root)
        if not env_python.is_file():
            raise RuntimeError("ANALYZER_ENVIRONMENT_PYTHON_MISSING")
        metadata_root = analyzer_environment_manifest_path(source_root).parent
        metadata_root.mkdir(parents=True, exist_ok=True)
        requirements_copy = analyzer_environment_requirements_copy_path(source_root)
        requirements_copy.write_bytes(expected_requirements)
        install_report = analyzer_environment_install_report_path(source_root)
        _run_checked(
            [
                str(env_python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-input",
                "--only-binary=:all:",
                "--report",
                str(install_report),
                "-r",
                str(requirements_copy),
            ],
            cwd=source_root,
            timeout_seconds=install_timeout_seconds,
            label="PINNED_ANALYZER_INSTALL",
        )
        _run_checked(
            [str(env_python), "-m", "pip", "check"],
            cwd=source_root,
            timeout_seconds=120.0,
            label="PINNED_ANALYZER_PIP_CHECK",
        )
        freeze_text = _run_capture(
            [str(env_python), "-m", "pip", "freeze", "--all"],
            cwd=source_root,
            timeout_seconds=120.0,
            label="PINNED_ANALYZER_FREEZE",
        )
        freeze_path = analyzer_environment_freeze_path(source_root)
        freeze_path.write_bytes(_normalize_freeze(freeze_text).encode("utf-8"))
        environment_lock = build_pinned_analyzer_environment_lock(source_root)
        capabilities = preflight_analyzer_capabilities(
            environment_lock,
            cwd=source_root,
        )
        blockers = _capability_blockers(capabilities)
        if blockers:
            raise RuntimeError(
                "ANALYZER_PROVISIONED_CAPABILITY_BLOCKED:" + "|".join(blockers)
            )
        runtime_info = _environment_python_info(env_python, source_root)
        observed_versions = {
            item.engine_id: _extract_expected_version(
                item.observed_version,
                item.expected_version,
            )
            for item in capabilities
        }
        manifest = build_analyzer_environment_manifest(
            feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
            tool_root=source_root,
            environment_root=env_root,
            python_executable=env_python,
            python_version=runtime_info["python_version"],
            implementation=runtime_info["implementation"],
            platform_system=runtime_info["platform_system"],
            platform_release=runtime_info["platform_release"],
            environment_lock=environment_lock,
            resolved_freeze_bytes=freeze_path.read_bytes(),
            requirements_bytes=requirements_copy.read_bytes(),
            observed_versions=observed_versions,
        )
        write_analyzer_environment_manifest(source_root, manifest)
        validation_blockers = validate_provisioned_analyzer_environment(
            source_root,
            active_project_root=active_project_root,
        )
        if validation_blockers:
            raise RuntimeError(
                "ANALYZER_PROVISIONED_ENVIRONMENT_INVALID:"
                + "|".join(validation_blockers)
            )
    except Exception:
        _remove_path(slot_root)
        if backup_root.exists():
            backup_root.rename(slot_root)
        raise
    _remove_path(backup_root)
    final_manifest = load_analyzer_environment_manifest(source_root)
    return AnalyzerProvisioningResult(
        status="PROVISIONED",
        environment_root=str(env_root),
        manifest_path=str(analyzer_environment_manifest_path(source_root)),
        analyzer_lock_hash=final_manifest.analyzer_lock_hash,
        manifest_hash=final_manifest.manifest_hash,
        diagnostics=(),
    )


def validate_provisioned_analyzer_environment(
    tool_root: str | Path,
    *,
    active_project_root: str | Path | None = None,
) -> tuple[str, ...]:
    """Validate exact lock, manifest, files, and capability evidence without install."""
    source_root = Path(tool_root).expanduser().resolve(strict=True)
    env_root = analyzer_environment_root(source_root)
    blockers = list(
        analyzer_tool_runtime_root_blockers(
            source_root,
            env_root,
            active_project_root=active_project_root,
        )
    )
    env_python = analyzer_environment_python(source_root)
    if not env_python.is_file():
        blockers.append("ANALYZER_ENVIRONMENT_PYTHON_MISSING")
        return tuple(sorted(set(blockers)))
    manifest_path = analyzer_environment_manifest_path(source_root)
    if not manifest_path.is_file():
        blockers.append("ANALYZER_ENVIRONMENT_MANIFEST_MISSING")
        return tuple(sorted(set(blockers)))
    try:
        manifest = load_analyzer_environment_manifest(source_root)
        environment_lock = build_pinned_analyzer_environment_lock(source_root)
        expected_versions = {
            package.engine_id: package.version for package in PINNED_ANALYZERS
        }
        blockers.extend(
            validate_analyzer_environment_manifest(
                source_root,
                manifest,
                expected_feature_id=ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID,
                environment_lock=environment_lock,
                expected_versions=expected_versions,
            )
        )
        capabilities = preflight_analyzer_capabilities(
            environment_lock,
            cwd=source_root,
        )
        blockers.extend(_capability_blockers(capabilities))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        blockers.append("ANALYZER_ENVIRONMENT_VALIDATION_EXCEPTION:" + type(exc).__name__)
    return tuple(sorted(set(blockers)))


def _reuse_if_valid(
    tool_root: Path,
    *,
    active_project_root: str | Path | None,
) -> AnalyzerProvisioningResult | None:
    """Return an idempotent reuse result only for an exact already-valid environment."""
    blockers = validate_provisioned_analyzer_environment(
        tool_root,
        active_project_root=active_project_root,
    )
    if blockers:
        return None
    manifest = load_analyzer_environment_manifest(tool_root)
    return AnalyzerProvisioningResult(
        status="REUSED_VALID_ENVIRONMENT",
        environment_root=str(analyzer_environment_root(tool_root)),
        manifest_path=str(analyzer_environment_manifest_path(tool_root)),
        analyzer_lock_hash=manifest.analyzer_lock_hash,
        manifest_hash=manifest.manifest_hash,
        diagnostics=(),
    )


def _create_virtual_environment(env_root: Path) -> None:
    """Create a fresh virtual environment with pip from the current Tool Python."""
    env_root.parent.mkdir(parents=True, exist_ok=True)
    builder = venv.EnvBuilder(with_pip=True, clear=True, symlinks=False)
    builder.create(str(env_root))


def _run_checked(
    argv: list[str],
    *,
    cwd: Path,
    timeout_seconds: float,
    label: str,
) -> None:
    """Run one explicit provisioning subprocess with live terminal output."""
    print(label + ": START")
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd),
            shell=False,
            check=False,
            timeout=float(timeout_seconds),
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(label + "_TIMED_OUT") from exc
    if completed.returncode != 0:
        raise RuntimeError(label + "_FAILED:" + str(completed.returncode))
    print(label + ": PASS")


def _run_capture(
    argv: list[str],
    *,
    cwd: Path,
    timeout_seconds: float,
    label: str,
) -> str:
    """Run one bounded metadata subprocess and return strict UTF-8 text."""
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd),
            shell=False,
            check=False,
            timeout=float(timeout_seconds),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(label + "_TIMED_OUT") from exc
    if completed.returncode != 0:
        raise RuntimeError(label + "_FAILED:" + str(completed.returncode))
    return completed.stdout


def _environment_python_info(env_python: Path, cwd: Path) -> dict[str, str]:
    """Read exact Python and platform identity from the provisioned environment."""
    code = (
        "import json,platform; print(json.dumps({"
        "'python_version':platform.python_version(),"
        "'implementation':platform.python_implementation(),"
        "'platform_system':platform.system(),"
        "'platform_release':platform.release()}))"
    )
    text = _run_capture(
        [str(env_python), "-c", code],
        cwd=cwd,
        timeout_seconds=30.0,
        label="ANALYZER_ENVIRONMENT_PYTHON_INFO",
    )
    payload = json.loads(text)
    return {str(key): str(value) for key, value in payload.items()}


def _capability_blockers(capabilities) -> tuple[str, ...]:
    """Return blockers for unavailable or incompatible provisioned analyzers."""
    blockers: list[str] = []
    expected = {package.engine_id: package.version for package in PINNED_ANALYZERS}
    observed_ids = {item.engine_id for item in capabilities}
    if observed_ids != set(expected):
        blockers.append("ANALYZER_CAPABILITY_ENGINE_SET_MISMATCH")
    for item in capabilities:
        if not item.available:
            blockers.append("ANALYZER_CAPABILITY_UNAVAILABLE:" + item.engine_id)
        if not item.compatible:
            blockers.append("ANALYZER_CAPABILITY_VERSION_MISMATCH:" + item.engine_id)
    return tuple(sorted(set(blockers)))


def _extract_expected_version(observed: str, expected: str) -> str:
    """Return exact expected version after compatibility preflight proved presence."""
    if expected.lower() not in observed.lower():
        raise RuntimeError("ANALYZER_OBSERVED_VERSION_MISMATCH:" + expected)
    return expected


def _normalize_freeze(text: str) -> str:
    """Return deterministic sorted pip-freeze text for lock hashing."""
    lines = sorted(line.strip() for line in text.splitlines() if line.strip())
    return "\n".join(lines) + "\n"


def _remove_path(path: Path) -> None:
    """Remove a disposable Tool-runtime provisioning path when present."""
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path, onerror=_clear_readonly_and_retry)
    else:
        path.chmod(0o700)
        path.unlink()


def _clear_readonly_and_retry(function, path, exc_info) -> None:
    """Clear read-only mode only inside a governed disposable provisioning path."""
    del exc_info
    os.chmod(path, 0o700)
    function(path)


def main(argv: list[str] | None = None) -> int:
    """Provision or idempotently reuse the exact pinned analyzer environment."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--project-root", default="")
    parser.add_argument("--force-recreate", action="store_true")
    args = parser.parse_args(argv)
    tool_root = Path(args.tool_root).expanduser().resolve(strict=True)
    project_root = (
        Path(args.project_root).expanduser().resolve(strict=True)
        if str(args.project_root).strip()
        else None
    )
    requirements = (
        tool_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "analyzer_environment_requirements_v1.txt"
    )
    result = provision_analyzer_environment(
        tool_root,
        requirements_source=requirements,
        active_project_root=project_root,
        force_recreate=bool(args.force_recreate),
    )
    print("ANALYZER_ENVIRONMENT_PROVISION_STATUS: " + result.status)
    print("ANALYZER_ENVIRONMENT_ROOT: " + result.environment_root)
    print("ANALYZER_ENVIRONMENT_LOCK_HASH: " + result.analyzer_lock_hash)
    print("ANALYZER_ENVIRONMENT_MANIFEST_HASH: " + result.manifest_hash)
    print("PINNED_ANALYZER_ENVIRONMENT_PROVISIONING: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
