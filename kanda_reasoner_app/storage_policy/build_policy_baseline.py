# project-path: kanda_reasoner_app/storage_policy/build_policy_baseline.py
"""Build and ignore policy baseline for Kanda Reasoner storage policy.

This module declares source-cleanliness and packaging policy data used by later
validators. It is side-effect free: importing it must not create files, modify
.gitignore, write build policy files, move files, delete files, or scan the live
source tree.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

POLICY_MODE_DEV = "dev"
POLICY_MODE_COMPILATION = "compilation"

FAIL_BEFORE_COMPILATION_PATTERNS = (
    "*.bak",
    "*.backup",
    "*_old.*",
    "*_deprecated.*",
    "__pycache__/",
    ".pytest_cache/",
    "*_extracted/",
    "project_analysis_evidence/",
    "*_architecture_audit/",
    "*__active_snapshot.json",
    "*__bundle_manifest.json",
    "*__complete.json",
    "*__complete_runtime_trace.json",
    "*__exclusion_rules.json",
    "*__file_manifest.json",
    "*__reconstruction_payload.json",
    "*__validation_state.json",
)

DEVELOPMENT_ONLY_WARN_PATTERNS = (
    "workbench/",
    "workbench/bundle_manifest/",
)

PACKAGING_EXCLUDE_PATTERNS = (
    "workbench/",
    "project_analysis_evidence/",
    "*_architecture_audit/",
    "__pycache__/",
    ".pytest_cache/",
    "*.bak",
    "*.backup",
    "*_old.*",
    "*_deprecated.*",
    "*_extracted/",
    "*__active_snapshot.json",
    "*__bundle_manifest.json",
    "*__complete.json",
    "*__complete_runtime_trace.json",
    "*__exclusion_rules.json",
    "*__file_manifest.json",
    "*__reconstruction_payload.json",
    "*__validation_state.json",
)

GENERATED_INTENTIONAL_SOURCE_ALLOWLIST = (
    "architecture_manifest.json",
    "workflow_manifest.json",
)

SECRET_EXCLUDE_HINT_PATTERNS = (
    ".env",
    "*.pem",
    "*.key",
    "*secret*",
    "*token*",
    "*credential*",
)


@dataclass(frozen=True)
class BuildPolicyBaseline:
    """Immutable baseline policy for source and packaging classification."""

    fail_before_compilation: tuple[str, ...]
    development_only_warnings: tuple[str, ...]
    packaging_excludes: tuple[str, ...]
    generated_intentional_source_allowlist: tuple[str, ...]
    secret_exclude_hints: tuple[str, ...]


def _as_tuple(values: Iterable[str]) -> tuple[str, ...]:
    """Return values as a tuple of stripped non-empty strings."""
    return tuple(str(value).strip() for value in values if str(value).strip())


def get_build_policy_baseline() -> BuildPolicyBaseline:
    """Return the immutable Kanda Reasoner build policy baseline."""
    return BuildPolicyBaseline(
        fail_before_compilation=FAIL_BEFORE_COMPILATION_PATTERNS,
        development_only_warnings=DEVELOPMENT_ONLY_WARN_PATTERNS,
        packaging_excludes=PACKAGING_EXCLUDE_PATTERNS,
        generated_intentional_source_allowlist=(
            GENERATED_INTENTIONAL_SOURCE_ALLOWLIST
        ),
        secret_exclude_hints=SECRET_EXCLUDE_HINT_PATTERNS,
    )


def render_gitignore_baseline() -> str:
    """Return a suggested .gitignore baseline without writing it."""
    policy = get_build_policy_baseline()
    lines = [
        "# Kanda Reasoner storage policy baseline",
        "# Generated suggestion only. Review before writing to .gitignore.",
        "",
        "# Non-compilation debris",
    ]
    lines.extend(policy.fail_before_compilation)
    lines.extend(("", "# Packaging exclusions"))
    lines.extend(policy.packaging_excludes)
    lines.extend(("", "# Secret and credential hints"))
    lines.extend(policy.secret_exclude_hints)
    return "\n".join(dict.fromkeys(lines)) + "\n"


def render_buildignore_baseline() -> str:
    """Return a suggested packaging exclusion baseline without writing it."""
    policy = get_build_policy_baseline()
    lines = [
        "# Kanda Reasoner build exclusion baseline",
        "# Generated suggestion only. Review before writing build exclusions.",
        "",
    ]
    lines.extend(policy.packaging_excludes)
    lines.extend(policy.secret_exclude_hints)
    return "\n".join(dict.fromkeys(lines)) + "\n"


def describe_build_policy_baseline() -> dict[str, tuple[str, ...]]:
    """Return a copy-friendly dictionary representation of the policy."""
    policy = get_build_policy_baseline()
    return {
        "fail_before_compilation": tuple(policy.fail_before_compilation),
        "development_only_warnings": tuple(policy.development_only_warnings),
        "packaging_excludes": tuple(policy.packaging_excludes),
        "generated_intentional_source_allowlist": tuple(
            policy.generated_intentional_source_allowlist
        ),
        "secret_exclude_hints": tuple(policy.secret_exclude_hints),
    }


__all__ = [
    "BuildPolicyBaseline",
    "DEVELOPMENT_ONLY_WARN_PATTERNS",
    "FAIL_BEFORE_COMPILATION_PATTERNS",
    "GENERATED_INTENTIONAL_SOURCE_ALLOWLIST",
    "PACKAGING_EXCLUDE_PATTERNS",
    "POLICY_MODE_COMPILATION",
    "POLICY_MODE_DEV",
    "SECRET_EXCLUDE_HINT_PATTERNS",
    "describe_build_policy_baseline",
    "get_build_policy_baseline",
    "render_buildignore_baseline",
    "render_gitignore_baseline",
]
