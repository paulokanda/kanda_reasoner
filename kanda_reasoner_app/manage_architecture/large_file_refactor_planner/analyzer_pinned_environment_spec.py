# project-path: large_file_refactor_planner/analyzer_pinned_environment_spec.py
"""Pinned analyzer package specification and lock construction for Release 6."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .advanced_quality_review_contract import AnalyzerAuthorityRole
from .analyzer_environment_contract import (
    AnalyzerCapabilityMode,
    AnalyzerEnvironmentLock,
    AnalyzerLockEntry,
    build_analyzer_environment_lock,
)
from .analyzer_tool_runtime_paths import (
    analyzer_environment_python,
    analyzer_environment_script,
)

__all__ = [
    "ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID",
    "PINNED_ANALYZERS",
    "PinnedAnalyzerPackage",
    "build_pinned_analyzer_environment_lock",
    "pinned_analyzer_spec_hash",
    "pinned_requirements_text",
    "validate_pinned_analyzer_spec",
]

ANALYZER_ENVIRONMENT_PROVISIONING_FEATURE_ID = (
    "advanced-quality-review-pinned-analyzer-environment-v1"
)


@dataclass(frozen=True)
class PinnedAnalyzerPackage:
    """Describe one exact external analyzer package and KANDA authority contract."""

    engine_id: str
    distribution_name: str
    version: str
    authority_role: AnalyzerAuthorityRole
    default_capability_mode: AnalyzerCapabilityMode
    configuration_source: str
    cache_routing_supported: bool
    console_script: str

    @property
    def requirement(self) -> str:
        """Return one exact top-level pip requirement line."""
        return f"{self.distribution_name}=={self.version}"

    def to_dict(self) -> dict[str, object]:
        """Return canonical JSON-ready specification evidence."""
        payload = asdict(self)
        payload["authority_role"] = self.authority_role.value
        payload["default_capability_mode"] = self.default_capability_mode.value
        return payload


PINNED_ANALYZERS = (
    PinnedAnalyzerPackage(
        engine_id="ruff",
        distribution_name="ruff",
        version="0.15.21",
        authority_role=AnalyzerAuthorityRole.MANDATORY,
        default_capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
        configuration_source="project_ruff_config_or_kanda_review_default",
        cache_routing_supported=True,
        console_script="ruff",
    ),
    PinnedAnalyzerPackage(
        engine_id="griffe",
        distribution_name="griffe",
        version="2.1.0",
        authority_role=AnalyzerAuthorityRole.MANDATORY,
        default_capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
        configuration_source="kanda_public_api_contract",
        cache_routing_supported=False,
        console_script="griffe",
    ),
    PinnedAnalyzerPackage(
        engine_id="grimp",
        distribution_name="grimp",
        version="3.15",
        authority_role=AnalyzerAuthorityRole.MANDATORY,
        default_capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
        configuration_source="kanda_box_logic_and_project_package_contract",
        cache_routing_supported=True,
        console_script="",
    ),
    PinnedAnalyzerPackage(
        engine_id="mypy",
        distribution_name="mypy",
        version="2.1.0",
        authority_role=AnalyzerAuthorityRole.CONDITIONAL,
        default_capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
        configuration_source="project_typing_configuration_capability_review",
        cache_routing_supported=True,
        console_script="mypy",
    ),
    PinnedAnalyzerPackage(
        engine_id="vulture",
        distribution_name="vulture",
        version="2.16",
        authority_role=AnalyzerAuthorityRole.ADVISORY,
        default_capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
        configuration_source="kanda_dead_code_advisory_policy",
        cache_routing_supported=False,
        console_script="vulture",
    ),
)


def pinned_requirements_text() -> str:
    """Return deterministic exact top-level analyzer requirements."""
    lines = [package.requirement for package in PINNED_ANALYZERS]
    return "\n".join(lines) + "\n"


def pinned_analyzer_spec_hash() -> str:
    """Return SHA-256 over the canonical package and authority specification."""
    payload = [package.to_dict() for package in PINNED_ANALYZERS]
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_pinned_analyzer_environment_lock(
    tool_root: str | Path,
) -> AnalyzerEnvironmentLock:
    """Build the frozen analyzer lock using explicit Tool-runtime executables."""
    python_path = analyzer_environment_python(tool_root)
    entries: list[AnalyzerLockEntry] = []
    for package in PINNED_ANALYZERS:
        executable, version_args = _version_probe_contract(
            tool_root,
            package,
            python_path=python_path,
        )
        entries.append(
            AnalyzerLockEntry(
                engine_id=package.engine_id,
                executable=str(executable),
                version_args=version_args,
                expected_version=package.version,
                authority_role=package.authority_role,
                capability_mode=package.default_capability_mode,
                configuration_source=package.configuration_source,
                cache_routing_supported=package.cache_routing_supported,
            )
        )
    return build_analyzer_environment_lock(entries)


def validate_pinned_analyzer_spec(
    packages: Iterable[PinnedAnalyzerPackage] = PINNED_ANALYZERS,
) -> tuple[str, ...]:
    """Return blockers for duplicate or incomplete package specification entries."""
    materialized = tuple(packages)
    blockers: list[str] = []
    seen_engines: set[str] = set()
    seen_distributions: set[str] = set()
    for package in materialized:
        if not package.engine_id.strip():
            blockers.append("PINNED_ANALYZER_ENGINE_EMPTY")
        if package.engine_id in seen_engines:
            blockers.append("PINNED_ANALYZER_ENGINE_DUPLICATE:" + package.engine_id)
        seen_engines.add(package.engine_id)
        if not package.distribution_name.strip():
            blockers.append("PINNED_ANALYZER_DISTRIBUTION_EMPTY:" + package.engine_id)
        if package.distribution_name in seen_distributions:
            blockers.append(
                "PINNED_ANALYZER_DISTRIBUTION_DUPLICATE:" + package.distribution_name
            )
        seen_distributions.add(package.distribution_name)
        if not package.version.strip():
            blockers.append("PINNED_ANALYZER_VERSION_EMPTY:" + package.engine_id)
        if not package.configuration_source.strip():
            blockers.append("PINNED_ANALYZER_CONFIG_SOURCE_EMPTY:" + package.engine_id)
    expected = {"ruff", "griffe", "grimp", "mypy", "vulture"}
    observed = {package.engine_id for package in materialized}
    if observed != expected:
        blockers.append("PINNED_ANALYZER_ENGINE_SET_MISMATCH")
    return tuple(sorted(set(blockers)))


def _version_probe_contract(
    tool_root: str | Path,
    package: PinnedAnalyzerPackage,
    *,
    python_path: Path,
) -> tuple[Path, tuple[str, ...]]:
    """Return explicit executable and version arguments for one engine."""
    if package.engine_id == "grimp":
        return (
            python_path,
            (
                "-c",
                "import importlib.metadata as m; print(m.version('grimp'))",
            ),
        )
    return analyzer_environment_script(tool_root, package.console_script), (
        "--version",
    )
