# project-path: kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py
"""Deterministic project-path scope enrichment for diagnostic findings."""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path, PurePosixPath
import re
from typing import Mapping, Sequence

from kanda_reasoner_app.project_exclusion_path_matching import (
    file_rule_matches,
    folder_rule_matches,
)
from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
)

from .enrichment_models import DiagnosticScopeEnrichment
from .fingerprinting import normalize_relative_path

__all__ = [
    "DiagnosticScopePolicy",
    "build_diagnostic_scope_policy",
    "classify_diagnostic_scope",
]

_SCOPE_MARKER = re.compile(
    r"^\s*#\s*kanda:scope\s*=\s*"
    r"(active|test|fixture|prototype|generated|reference|deprecated|"
    r"workbench|snippet|temporary)\s*$",
    re.IGNORECASE,
)
_SCOPE_MARKER_MAX_BYTES = 1024 * 1024
_SCOPE_MARKER_MAX_LINES = 80

_EXACT_SEGMENTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("TEMPORARY", ("tmp", "temp", "temporary", "_delete_after_daily_work")),
    (
        "REFERENCE",
        (
            ".project_reference",
            "_project_reference",
            "reference",
            "references",
            "archive",
            "archives",
        ),
    ),
    ("WORKBENCH", ("workbench", "workbenches")),
    ("SNIPPET", ("snippet", "snippets")),
    ("FIXTURE", ("fixture", "fixtures", "testdata", "test_data")),
    ("TEST", ("test", "tests", "testing")),
    (
        "PROTOTYPE",
        (
            "prototype",
            "prototypes",
            "experimental",
            "experiments",
            "not_implemented_yet",
        ),
    ),
    ("GENERATED", ("generated", "autogen", "auto_generated", "codegen")),
)
_DEPRECATED_TOKENS = ("deprecated", "legacy", "oldies", "older", "obsolete")


@dataclass(frozen=True, slots=True)
class DiagnosticScopePolicy:
    """Prepared read-only policy used for deterministic batch classification."""

    project_root: Path
    exclusion_rules: Mapping[str, Sequence[str]]
    folder_rules: tuple[str, ...]
    file_rules: tuple[str, ...]
    excluded_extensions: frozenset[str]
    _directory_names: dict[str, frozenset[str]] = field(
        default_factory=dict,
        repr=False,
        compare=False,
    )
    _marker_cache: dict[str, str] = field(
        default_factory=dict,
        repr=False,
        compare=False,
    )
    _parent_excluded_cache: dict[str, bool] = field(
        default_factory=dict,
        repr=False,
        compare=False,
    )


def build_diagnostic_scope_policy(
    project_root: str | Path,
) -> DiagnosticScopePolicy:
    """Load the public Project exclusion policy once for batch enrichment."""
    root = Path(project_root).expanduser().resolve(strict=True)
    rules = load_reasoner_project_exclusion_rules(root)
    extensions = frozenset(
        text if text.startswith(".") else "." + text
        for value in rules.get("extensions", ())
        if (text := str(value).strip().lower())
    )
    return DiagnosticScopePolicy(
        project_root=root,
        exclusion_rules=rules,
        folder_rules=tuple(str(value) for value in rules.get("folders", ())),
        file_rules=tuple(str(value) for value in rules.get("files", ())),
        excluded_extensions=extensions,
    )


def _directory_names(
    policy: DiagnosticScopePolicy,
    directory: Path,
) -> frozenset[str]:
    key = str(directory)
    cached = policy._directory_names.get(key)
    if cached is not None:
        return cached
    try:
        with os.scandir(directory) as entries:
            names = frozenset(entry.name for entry in entries)
    except OSError:
        names = frozenset()
    policy._directory_names[key] = names
    return names


def _inline_marker(
    policy: DiagnosticScopePolicy,
    path: Path,
) -> str:
    key = str(path)
    cached = policy._marker_cache.get(key)
    if cached is not None:
        return cached
    if path.name not in _directory_names(policy, path.parent):
        return ""
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(policy.project_root)
        if resolved.stat().st_size > _SCOPE_MARKER_MAX_BYTES:
            policy._marker_cache[key] = ""
            return ""
        lines = resolved.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()
    except (OSError, ValueError):
        policy._marker_cache[key] = ""
        return ""
    marker = ""
    for line in lines[:_SCOPE_MARKER_MAX_LINES]:
        match = _SCOPE_MARKER.match(line)
        if match:
            marker = match.group(1).upper()
            break
    policy._marker_cache[key] = marker
    return marker


def _path_classification(relative_path: str) -> tuple[str, str]:
    lowered = relative_path.lower()
    parts = tuple(part for part in lowered.split("/") if part)
    filename = parts[-1] if parts else ""
    stem = PurePosixPath(filename).stem.lower()

    if (
        filename == "conftest.py"
        or filename.startswith("test_")
        or filename.endswith("_test.py")
    ):
        return "TEST", "test_filename"
    if any(token in part for part in parts for token in _DEPRECATED_TOKENS):
        return "DEPRECATED", "deprecated_path_token"
    if "not implemented yet" in lowered or "not-implemented-yet" in lowered:
        return "PROTOTYPE", "prototype_path_phrase"
    if ".generated." in filename or stem.endswith("_generated"):
        return "GENERATED", "generated_filename"
    for classification, candidates in _EXACT_SEGMENTS:
        if any(part in candidates for part in parts):
            return classification, "path_segment"
    if parts and parts[0].startswith("."):
        return "REFERENCE", "hidden_root_path"
    return "", ""


def _parent_excluded(
    policy: DiagnosticScopePolicy,
    parent_relative: str,
) -> bool:
    cached = policy._parent_excluded_cache.get(parent_relative)
    if cached is not None:
        return cached
    parts = tuple(part for part in parent_relative.lower().split("/") if part)
    excluded = bool(parts and parts[0].startswith("."))
    if not excluded:
        excluded = any(
            folder_rule_matches(
                parent_relative,
                rule,
                path_is_dir=True,
            )
            for rule in policy.folder_rules
        )
    policy._parent_excluded_cache[parent_relative] = excluded
    return excluded


def _excluded_relative_file(
    policy: DiagnosticScopePolicy,
    relative_path: str,
) -> bool:
    path = PurePosixPath(relative_path)
    parent_relative = path.parent.as_posix()
    if parent_relative == ".":
        parent_relative = ""
    if _parent_excluded(policy, parent_relative):
        return True
    filename = path.name
    if any(
        file_rule_matches(relative_path, filename, rule)
        for rule in policy.file_rules
    ):
        return True
    return path.suffix.lower() in policy.excluded_extensions


def classify_diagnostic_scope(
    policy: DiagnosticScopePolicy,
    relative_path: str,
) -> DiagnosticScopeEnrichment:
    """Classify one path without mutating Project source or policy state."""
    try:
        normalized = normalize_relative_path(relative_path)
    except Exception as exc:
        return DiagnosticScopeEnrichment(
            "UNKNOWN",
            "low",
            "invalid_relative_path",
            (str(exc),),
        )

    path = policy.project_root.joinpath(*normalized.split("/"))
    marker = _inline_marker(policy, path)
    if marker:
        return DiagnosticScopeEnrichment(
            marker,
            "high",
            "explicit_scope_marker",
            ("marker=# kanda:scope=" + marker.lower(),),
        )

    classification, reason = _path_classification(normalized)
    if classification:
        return DiagnosticScopeEnrichment(
            classification,
            "high",
            reason,
            ("relative_path=" + normalized,),
        )

    if _excluded_relative_file(policy, normalized):
        return DiagnosticScopeEnrichment(
            "UNKNOWN",
            "low",
            "project_exclusion_policy",
            (
                "relative_path=" + normalized,
                "active_policy_excluded=true",
            ),
        )
    return DiagnosticScopeEnrichment(
        "ACTIVE",
        "medium",
        "active_project_policy",
        (
            "relative_path=" + normalized,
            "active_policy_excluded=false",
        ),
    )
