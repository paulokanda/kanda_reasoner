"""Recognize and classify the bounded Kilo Code workspace contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = ["KiloWorkspaceRecord", "classify_verified_kilo_workspace"]


@dataclass(frozen=True)
class KiloWorkspaceRecord:
    """Return a classification name without importing the parent policy enum."""

    classification: str
    reason: str
    matched_rule: str


def _read_json_object(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _top_level_is_allowed(workspace: Path, policy: dict[str, Any]) -> bool:
    try:
        items = tuple(workspace.iterdir())
    except OSError:
        return False
    if any(item.is_symlink() for item in items):
        return False
    names = {item.name for item in items}
    required = {str(item) for item in policy.get("required_top_level_entries", [])}
    allowed = {str(item) for item in policy.get("allowed_top_level_entries", [])}
    return required.issubset(names) and names.issubset(allowed)


def _package_identity_is_valid(workspace: Path, policy: dict[str, Any]) -> bool:
    package = _read_json_object(workspace / "package.json")
    lockfile = _read_json_object(workspace / "package-lock.json")
    dependency_name = str(policy.get("dependency_name", "@kilocode/plugin"))
    if package is None or lockfile is None or set(package) != {"dependencies"}:
        return False
    dependencies = package.get("dependencies")
    if not isinstance(dependencies, dict) or set(dependencies) != {dependency_name}:
        return False
    dependency_version = dependencies.get(dependency_name)
    if not isinstance(dependency_version, str) or not dependency_version.strip():
        return False
    packages = lockfile.get("packages")
    if not isinstance(packages, dict):
        return False
    root_record = packages.get("")
    plugin_record = packages.get("node_modules/" + dependency_name)
    return (
        lockfile.get("name") == policy.get("lockfile_name", ".kilo")
        and lockfile.get("lockfileVersion")
        == int(policy.get("lockfile_version", 3))
        and isinstance(root_record, dict)
        and root_record.get("dependencies") == dependencies
        and isinstance(plugin_record, dict)
        and plugin_record.get("version") == dependency_version
    )


def _gitignore_identity_is_valid(workspace: Path, policy: dict[str, Any]) -> bool:
    try:
        ignored = {
            line.strip()
            for line in (workspace / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    except (OSError, UnicodeDecodeError):
        return False
    required = {str(item) for item in policy.get("required_gitignore_entries", [])}
    return required.issubset(ignored)


def _members_are_bounded(workspace: Path, policy: dict[str, Any]) -> bool:
    plan_suffixes = {
        str(item).casefold() for item in policy.get("allowed_plan_suffixes", [])
    }
    maximum = int(policy.get("maximum_files_inspected", 4096))
    inspected = 0
    try:
        for candidate in workspace.rglob("*"):
            if candidate.is_symlink():
                return False
            if not candidate.is_file():
                continue
            inspected += 1
            if inspected > maximum:
                return False
            local = candidate.relative_to(workspace)
            if local.parts[0] == "node_modules":
                continue
            if local.as_posix() in {".gitignore", "package.json", "package-lock.json"}:
                continue
            if local.parts[0] == "plans" and candidate.suffix.casefold() in plan_suffixes:
                continue
            return False
    except OSError:
        return False
    return True


def classify_verified_kilo_workspace(
    tool_root: Path,
    relative: str,
    raw_policy: object,
) -> KiloWorkspaceRecord | None:
    """Return a record only for the exact verified Kilo workspace shape."""
    if not isinstance(raw_policy, dict) or raw_policy.get("enabled") is not True:
        return None
    root_name = str(raw_policy.get("root_name", ".kilo"))
    if relative != root_name and not relative.startswith(root_name + "/"):
        return None
    workspace = tool_root / root_name
    if not workspace.is_dir() or workspace.is_symlink():
        return None
    if not _top_level_is_allowed(workspace, raw_policy):
        return None
    if not _package_identity_is_valid(workspace, raw_policy):
        return None
    if not _gitignore_identity_is_valid(workspace, raw_policy):
        return None
    if not _members_are_bounded(workspace, raw_policy):
        return None
    cache_prefix = root_name + "/node_modules"
    is_cache = relative == cache_prefix or relative.startswith(cache_prefix + "/")
    classification = str(
        raw_policy.get(
            "cache_classification" if is_cache else "evidence_classification",
            "CACHE" if is_cache else "GENERATED_TOOL_EVIDENCE",
        )
    )
    return KiloWorkspaceRecord(
        classification=classification,
        reason=str(raw_policy.get("reason", "Verified Kilo workspace local state.")),
        matched_rule="kilo_workspace_policy:" + root_name,
    )
