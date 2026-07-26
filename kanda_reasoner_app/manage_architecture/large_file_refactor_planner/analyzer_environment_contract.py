# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_environment_contract.py
"""Immutable environment and capability contracts for analyzer execution."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
import platform
import sys
from typing import Iterable

from .advanced_quality_review_contract import AnalyzerAuthorityRole

__all__ = [
    "ANALYZER_RUNTIME_FOUNDATION_FEATURE_ID",
    "AnalyzerCapabilityMode",
    "AnalyzerEnvironmentIdentity",
    "AnalyzerEnvironmentLock",
    "AnalyzerLockEntry",
    "build_analyzer_environment_lock",
    "build_analyzer_runtime_identity",
    "validate_analyzer_environment_lock",
]

ANALYZER_RUNTIME_FOUNDATION_FEATURE_ID = (
    "advanced-quality-review-analyzer-runtime-foundation-v1"
)


class AnalyzerCapabilityMode(str, Enum):
    """Describe whether analyzer evidence may be authoritative for a project."""

    AUTHORITATIVE = "AUTHORITATIVE"
    AVAILABLE_NON_AUTHORITATIVE = "AVAILABLE_NON_AUTHORITATIVE"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class AnalyzerLockEntry:
    """Pin one analyzer executable contract without provisioning it implicitly."""

    engine_id: str
    executable: str
    version_args: tuple[str, ...]
    expected_version: str
    authority_role: AnalyzerAuthorityRole
    capability_mode: AnalyzerCapabilityMode
    configuration_source: str
    cache_routing_supported: bool

    def to_dict(self) -> dict[str, object]:
        """Return one stable JSON-ready lock entry."""
        payload = asdict(self)
        payload["authority_role"] = self.authority_role.value
        payload["capability_mode"] = self.capability_mode.value
        return payload


@dataclass(frozen=True)
class AnalyzerEnvironmentLock:
    """Describe the exact analyzer versions expected by one review runtime."""

    schema_version: str
    entries: tuple[AnalyzerLockEntry, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a canonical JSON-ready lock payload."""
        return {
            "schema_version": self.schema_version,
            "entries": [entry.to_dict() for entry in self.entries],
        }

    @property
    def lock_hash(self) -> str:
        """Return SHA-256 over the canonical lock payload."""
        return _canonical_hash(self.to_dict())


@dataclass(frozen=True)
class AnalyzerEnvironmentIdentity:
    """Bind runtime evidence to Python, platform, and analyzer lock identity."""

    schema_version: str
    python_executable: str
    python_version: str
    implementation: str
    platform_system: str
    platform_release: str
    analyzer_lock_hash: str

    def to_dict(self) -> dict[str, str]:
        """Return a stable JSON-ready environment identity."""
        return asdict(self)

    @property
    def identity_hash(self) -> str:
        """Return SHA-256 over the canonical runtime identity."""
        return _canonical_hash(self.to_dict())


def build_analyzer_environment_lock(
    entries: Iterable[AnalyzerLockEntry],
    *,
    schema_version: str = "1.0",
) -> AnalyzerEnvironmentLock:
    """Validate and build one deterministic analyzer lock."""
    materialized = tuple(sorted(tuple(entries), key=lambda item: item.engine_id))
    lock = AnalyzerEnvironmentLock(
        schema_version=str(schema_version or "").strip(),
        entries=materialized,
    )
    blockers = validate_analyzer_environment_lock(lock)
    if blockers:
        raise ValueError("ANALYZER_ENVIRONMENT_LOCK_INVALID:" + "|".join(blockers))
    return lock


def build_analyzer_runtime_identity(
    environment_lock: AnalyzerEnvironmentLock,
    *,
    schema_version: str = "1.0",
) -> AnalyzerEnvironmentIdentity:
    """Return immutable identity for the current Python runtime and analyzer lock."""
    blockers = validate_analyzer_environment_lock(environment_lock)
    if blockers:
        raise ValueError("ANALYZER_ENVIRONMENT_LOCK_INVALID:" + "|".join(blockers))
    return AnalyzerEnvironmentIdentity(
        schema_version=str(schema_version or "").strip(),
        python_executable=str(sys.executable),
        python_version=platform.python_version(),
        implementation=platform.python_implementation(),
        platform_system=platform.system(),
        platform_release=platform.release(),
        analyzer_lock_hash=environment_lock.lock_hash,
    )


def validate_analyzer_environment_lock(
    environment_lock: AnalyzerEnvironmentLock,
) -> tuple[str, ...]:
    """Return deterministic blockers for an incomplete or ambiguous lock."""
    blockers: list[str] = []
    if not str(environment_lock.schema_version or "").strip():
        blockers.append("ANALYZER_LOCK_SCHEMA_VERSION_EMPTY")
    if not environment_lock.entries:
        blockers.append("ANALYZER_LOCK_ENTRIES_EMPTY")
    seen: set[str] = set()
    for entry in environment_lock.entries:
        engine_id = str(entry.engine_id or "").strip()
        if not engine_id:
            blockers.append("ANALYZER_LOCK_ENGINE_ID_EMPTY")
            continue
        if engine_id in seen:
            blockers.append("ANALYZER_LOCK_ENGINE_DUPLICATE:" + engine_id)
        seen.add(engine_id)
        if not str(entry.executable or "").strip():
            blockers.append("ANALYZER_EXECUTABLE_EMPTY:" + engine_id)
        if not entry.version_args:
            blockers.append("ANALYZER_VERSION_ARGS_EMPTY:" + engine_id)
        if not str(entry.expected_version or "").strip():
            blockers.append("ANALYZER_EXPECTED_VERSION_EMPTY:" + engine_id)
        if not str(entry.configuration_source or "").strip():
            blockers.append("ANALYZER_CONFIGURATION_SOURCE_EMPTY:" + engine_id)
    return tuple(sorted(set(blockers)))


def _canonical_hash(payload: dict[str, object]) -> str:
    """Return SHA-256 for one canonical JSON payload."""
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
