# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_environment_manifest.py
"""Immutable manifest and verification contract for the provisioned analyzer environment."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping

from .analyzer_environment_contract import AnalyzerEnvironmentLock
from .analyzer_pinned_environment_spec import pinned_analyzer_spec_hash
from .analyzer_tool_runtime_paths import (
    analyzer_environment_freeze_path,
    analyzer_environment_manifest_path,
    analyzer_environment_requirements_copy_path,
)

__all__ = [
    "AnalyzerEnvironmentManifest",
    "AnalyzerObservedVersion",
    "build_analyzer_environment_manifest",
    "load_analyzer_environment_manifest",
    "manifest_lock_hash",
    "validate_analyzer_environment_manifest",
    "write_analyzer_environment_manifest",
]


@dataclass(frozen=True)
class AnalyzerObservedVersion:
    """Record one observed analyzer version from the provisioned environment."""

    engine_id: str
    observed_version: str

    def to_dict(self) -> dict[str, str]:
        """Return stable JSON-ready observed version evidence."""
        return asdict(self)


@dataclass(frozen=True)
class AnalyzerEnvironmentManifest:
    """Bind one Tool runtime environment to exact specification and resolved lock."""

    schema_version: str
    feature_id: str
    tool_root_name: str
    environment_root: str
    python_executable: str
    python_version: str
    implementation: str
    platform_system: str
    platform_release: str
    pinned_spec_hash: str
    analyzer_lock_hash: str
    resolved_freeze_hash: str
    requirements_hash: str
    observed_versions: tuple[AnalyzerObservedVersion, ...]

    def to_dict(self) -> dict[str, object]:
        """Return canonical JSON-ready environment manifest evidence."""
        payload = asdict(self)
        payload["observed_versions"] = [
            item.to_dict() for item in self.observed_versions
        ]
        return payload

    @property
    def manifest_hash(self) -> str:
        """Return SHA-256 over the canonical manifest payload."""
        return _hash_json(self.to_dict())


def build_analyzer_environment_manifest(
    *,
    feature_id: str,
    tool_root: str | Path,
    environment_root: str | Path,
    python_executable: str | Path,
    python_version: str,
    implementation: str,
    platform_system: str,
    platform_release: str,
    environment_lock: AnalyzerEnvironmentLock,
    resolved_freeze_bytes: bytes,
    requirements_bytes: bytes,
    observed_versions: Mapping[str, str],
) -> AnalyzerEnvironmentManifest:
    """Build one immutable manifest from exact environment evidence."""
    versions = tuple(
        AnalyzerObservedVersion(str(engine_id), str(version))
        for engine_id, version in sorted(observed_versions.items())
    )
    return AnalyzerEnvironmentManifest(
        schema_version="1.0",
        feature_id=str(feature_id).strip(),
        tool_root_name=Path(tool_root).resolve(strict=False).name,
        environment_root=str(Path(environment_root).resolve(strict=False)),
        python_executable=str(Path(python_executable).resolve(strict=False)),
        python_version=str(python_version).strip(),
        implementation=str(implementation).strip(),
        platform_system=str(platform_system).strip(),
        platform_release=str(platform_release).strip(),
        pinned_spec_hash=pinned_analyzer_spec_hash(),
        analyzer_lock_hash=environment_lock.lock_hash,
        resolved_freeze_hash=hashlib.sha256(resolved_freeze_bytes).hexdigest(),
        requirements_hash=hashlib.sha256(requirements_bytes).hexdigest(),
        observed_versions=versions,
    )


def write_analyzer_environment_manifest(
    tool_root: str | Path,
    manifest: AnalyzerEnvironmentManifest,
) -> Path:
    """Write strict UTF-8 no-BOM manifest JSON into Tool runtime support."""
    path = analyzer_environment_manifest_path(tool_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        manifest.to_dict(),
        sort_keys=True,
        indent=2,
        ensure_ascii=True,
    ) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(payload.encode("utf-8"))
    temporary.replace(path)
    return path


def load_analyzer_environment_manifest(
    tool_root: str | Path,
) -> AnalyzerEnvironmentManifest:
    """Read strict manifest JSON and reconstruct immutable typed evidence."""
    path = analyzer_environment_manifest_path(tool_root)
    data = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    versions = tuple(
        AnalyzerObservedVersion(
            engine_id=str(item["engine_id"]),
            observed_version=str(item["observed_version"]),
        )
        for item in data.get("observed_versions", [])
    )
    return AnalyzerEnvironmentManifest(
        schema_version=str(data["schema_version"]),
        feature_id=str(data["feature_id"]),
        tool_root_name=str(data["tool_root_name"]),
        environment_root=str(data["environment_root"]),
        python_executable=str(data["python_executable"]),
        python_version=str(data["python_version"]),
        implementation=str(data["implementation"]),
        platform_system=str(data["platform_system"]),
        platform_release=str(data["platform_release"]),
        pinned_spec_hash=str(data["pinned_spec_hash"]),
        analyzer_lock_hash=str(data["analyzer_lock_hash"]),
        resolved_freeze_hash=str(data["resolved_freeze_hash"]),
        requirements_hash=str(data["requirements_hash"]),
        observed_versions=versions,
    )


def validate_analyzer_environment_manifest(
    tool_root: str | Path,
    manifest: AnalyzerEnvironmentManifest,
    *,
    expected_feature_id: str,
    environment_lock: AnalyzerEnvironmentLock,
    expected_versions: Mapping[str, str],
) -> tuple[str, ...]:
    """Return blockers for manifest drift, missing files, or version mismatch."""
    blockers: list[str] = []
    if manifest.feature_id != str(expected_feature_id).strip():
        blockers.append("ANALYZER_MANIFEST_FEATURE_ID_MISMATCH")
    if manifest.pinned_spec_hash != pinned_analyzer_spec_hash():
        blockers.append("ANALYZER_MANIFEST_PINNED_SPEC_HASH_MISMATCH")
    if manifest.analyzer_lock_hash != environment_lock.lock_hash:
        blockers.append("ANALYZER_MANIFEST_LOCK_HASH_MISMATCH")
    freeze_path = analyzer_environment_freeze_path(tool_root)
    requirements_path = analyzer_environment_requirements_copy_path(tool_root)
    if not freeze_path.is_file():
        blockers.append("ANALYZER_MANIFEST_FREEZE_FILE_MISSING")
    elif _hash_file(freeze_path) != manifest.resolved_freeze_hash:
        blockers.append("ANALYZER_MANIFEST_FREEZE_HASH_MISMATCH")
    if not requirements_path.is_file():
        blockers.append("ANALYZER_MANIFEST_REQUIREMENTS_FILE_MISSING")
    elif _hash_file(requirements_path) != manifest.requirements_hash:
        blockers.append("ANALYZER_MANIFEST_REQUIREMENTS_HASH_MISMATCH")
    observed = {
        item.engine_id: item.observed_version for item in manifest.observed_versions
    }
    if observed != {str(key): str(value) for key, value in expected_versions.items()}:
        blockers.append("ANALYZER_MANIFEST_OBSERVED_VERSION_SET_MISMATCH")
    return tuple(sorted(set(blockers)))


def manifest_lock_hash(manifest: AnalyzerEnvironmentManifest) -> str:
    """Return stable manifest hash for AnalysisIdentity lock/config binding."""
    return manifest.manifest_hash


def _hash_file(path: Path) -> str:
    """Return SHA-256 for exact file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_json(payload: dict[str, object]) -> str:
    """Return canonical JSON SHA-256."""
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
