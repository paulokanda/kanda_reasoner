#!/usr/bin/env python3
"""
audit_startup_candidates.py

Auditor and human-confirmed updater for KANDA startup routing kernel candidates.

This tool scans approved prompt folders for explicit startup sidecar
metadata files and compares them with STARTUP_ROUTING_KERNEL_SOURCES.json.
When missing candidates are found, it explains them, asks the human for
explicit confirmation, updates STARTUP_ROUTING_KERNEL_SOURCES.json only
after a YES answer, and then runs sync_startup_routing_kernel_pack.py
--ensure-sync --yes.

Python: 3.10+
Platform: Windows compatible
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLS_DIR_NAME = "prompt_tools"
PROMPT_LIBRARY_DIR_NAME = "prompt_library"
SOURCE_MAP_FILENAME = "STARTUP_ROUTING_KERNEL_SOURCES.json"
REPORT_FILENAME = "STARTUP_ROUTING_KERNEL_SOURCES_UPDATE_CANDIDATE.md"
SYNC_SCRIPT_FILENAME = "sync_startup_routing_kernel_pack.py"

ALLOWED_SCAN_DIRS = (
    "prompt_library/ACTIVE_PROMPTS",
    "prompt_library/ROUTING",
)

MAX_CANDIDATE_SIZE_BYTES = 100 * 1024
MAX_NEW_CANDIDATES_WARNING = 5
MAX_STARTUP_SOURCES_WARNING = 20

GENERATED_FILENAME_RE = re.compile(r"^[0-9]{2}_[^\\/]+\.md$")
PROMPT_ID_RE = re.compile(r"^[a-z0-9_]+$")

REQUIRED_SOURCE_MAP_KEYS = {
    "load_order",
    "canonical_source",
    "generated_filename",
    "prompt_id",
    "load_mode",
    "role",
}

ALLOWED_SOURCE_MAP_KEYS = REQUIRED_SOURCE_MAP_KEYS

REQUIRED_SIDECAR_KEYS = {
    "startup_kernel_include",
    "startup_load_mode",
    "startup_generated_filename",
    "prompt_id",
    "startup_role",
}

ALLOWED_SIDECAR_KEYS = REQUIRED_SIDECAR_KEYS | {"canonical_source", "load_order"}


@dataclass(frozen=True)
class SourceMapEntry:
    load_order: int
    canonical_source: str
    generated_filename: str
    prompt_id: str
    load_mode: str
    role: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class StartupCandidate:
    canonical_source: str
    generated_filename: str
    prompt_id: str
    load_mode: str
    role: str
    md_path: Path
    sidecar_path: Path
    size_bytes: int
    optional_load_order: int | None


@dataclass
class AuditResult:
    source_map_errors: list[str]
    source_map_warnings: list[str]
    sidecar_warnings: list[str]
    candidate_errors: list[str]
    candidate_warnings: list[str]
    stale_entries: list[str]
    existing_candidates: list[StartupCandidate]
    missing_candidates: list[StartupCandidate]
    ignored_sidecars: list[str]
    source_map_sha256: str
    report_path: Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_text_utf8_strict(path: Path) -> str:
    # Accept UTF-8 with or without BOM. Windows PowerShell 5.1 and
    # some editors can write UTF-8 files with a BOM; that is still
    # valid UTF-8 for this workflow and should not break JSON parsing.
    return path.read_text(encoding="utf-8-sig")


def write_text_utf8(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def read_json_file(path: Path) -> Any:
    return json.loads(read_text_utf8_strict(path))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_rel_path(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def is_hidden_or_cache_path(path: Path) -> bool:
    hidden_or_cache_names = {".git", ".idea", "__pycache__", ".pytest_cache"}
    return any(part in hidden_or_cache_names or part.startswith(".") for part in path.parts)


def is_relative_to_safe(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def detect_workspace_root(script_path: Path, explicit_workspace: Path | None) -> Path:
    if explicit_workspace is not None:
        workspace = explicit_workspace.resolve()
    else:
        candidates = [
            script_path.parent.parent,
            Path.cwd(),
        ]
        workspace = next(
            (candidate.resolve() for candidate in candidates if is_valid_workspace(candidate)),
            script_path.parent.parent.resolve(),
        )

    if not is_valid_workspace(workspace):
        raise ValueError(
            "Workspace root could not be confirmed. Run from kanda_prompt_workspace "
            "or pass --workspace <path>. Expected prompt_library and prompt_tools."
        )
    return workspace


def is_valid_workspace(path: Path) -> bool:
    return (
        (path / PROMPT_LIBRARY_DIR_NAME).is_dir()
        and (path / TOOLS_DIR_NAME).is_dir()
        and (path / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME).is_file()
    )


def parse_source_map(source_map_path: Path) -> tuple[list[SourceMapEntry], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    raw = read_json_file(source_map_path)
    if not isinstance(raw, dict):
        raise ValueError("Source map must be a JSON object.")

    if "schema_version" not in raw:
        warnings.append("Source map has no schema_version field. Consider adding schema_version: 1 later.")

    sources = raw.get("startup_sources")
    if not isinstance(sources, list):
        raise ValueError("Source map must contain a startup_sources list.")

    entries: list[SourceMapEntry] = []
    seen_orders: dict[int, str] = {}
    seen_canonical: dict[str, str] = {}
    seen_generated: dict[str, str] = {}
    seen_prompt_ids: dict[str, str] = {}

    for index, item in enumerate(sources, start=1):
        label = f"startup_sources[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: entry must be a JSON object.")
            continue

        missing_keys = sorted(REQUIRED_SOURCE_MAP_KEYS - set(item.keys()))
        extra_keys = sorted(set(item.keys()) - ALLOWED_SOURCE_MAP_KEYS)
        if missing_keys:
            errors.append(f"{label}: missing required keys: {missing_keys}")
            continue
        if extra_keys:
            warnings.append(f"{label}: extra keys present: {extra_keys}")

        try:
            load_order = int(item["load_order"])
        except (TypeError, ValueError):
            errors.append(f"{label}: load_order must be an integer.")
            continue

        canonical_source = str(item["canonical_source"])
        generated_filename = str(item["generated_filename"])
        prompt_id = str(item["prompt_id"])
        load_mode = str(item["load_mode"])
        role = str(item["role"])

        if "\\" in canonical_source:
            warnings.append(f"{label}: canonical_source should use forward slashes: {canonical_source}")

        if "/" in generated_filename or "\\" in generated_filename:
            errors.append(f"{label}: generated_filename must not contain path separators: {generated_filename}")
        elif not generated_filename.endswith(".md"):
            errors.append(f"{label}: generated_filename must end with .md: {generated_filename}")
        elif not GENERATED_FILENAME_RE.match(generated_filename):
            warnings.append(
                f"{label}: generated_filename should be numbered like 08_name.md: {generated_filename}"
            )

        if load_mode != "always_startup":
            warnings.append(f"{label}: v1 expects load_mode always_startup, got {load_mode}")

        if not role.strip():
            errors.append(f"{label}: role must be non-empty.")

        if not prompt_id.strip():
            errors.append(f"{label}: prompt_id must be non-empty.")
        elif not PROMPT_ID_RE.match(prompt_id):
            warnings.append(
                f"{label}: prompt_id should be lowercase alphanumeric plus underscores: {prompt_id}"
            )

        if load_order in seen_orders:
            errors.append(
                f"{label}: duplicate load_order {load_order}; already used by {seen_orders[load_order]}"
            )
        seen_orders[load_order] = label

        canonical_key = canonical_source.replace("\\", "/")
        if canonical_key in seen_canonical:
            errors.append(
                f"{label}: duplicate canonical_source {canonical_key}; already used by {seen_canonical[canonical_key]}"
            )
        seen_canonical[canonical_key] = label

        if generated_filename in seen_generated:
            errors.append(
                f"{label}: duplicate generated_filename {generated_filename}; already used by {seen_generated[generated_filename]}"
            )
        seen_generated[generated_filename] = label

        if prompt_id in seen_prompt_ids:
            errors.append(
                f"{label}: duplicate prompt_id {prompt_id}; already used by {seen_prompt_ids[prompt_id]}"
            )
        seen_prompt_ids[prompt_id] = label

        entries.append(
            SourceMapEntry(
                load_order=load_order,
                canonical_source=canonical_key,
                generated_filename=generated_filename,
                prompt_id=prompt_id,
                load_mode=load_mode,
                role=role,
                raw=item,
            )
        )

    if entries:
        actual_orders = sorted(entry.load_order for entry in entries)
        expected_orders = list(range(1, len(entries) + 1))
        if actual_orders != expected_orders:
            errors.append(
                "load_order values must be contiguous starting at 1. "
                f"Expected {expected_orders}, got {actual_orders}."
            )

    return entries, errors, warnings


def detect_stale_entries(workspace_root: Path, entries: list[SourceMapEntry]) -> list[str]:
    stale: list[str] = []
    for entry in entries:
        source_path = workspace_root / entry.canonical_source
        if not source_path.exists():
            stale.append(
                f"{entry.generated_filename}: canonical_source missing: {entry.canonical_source}"
            )
    return stale


def allowed_scan_roots(workspace_root: Path) -> list[Path]:
    roots: list[Path] = []
    for rel in ALLOWED_SCAN_DIRS:
        path = workspace_root / rel
        if path.is_dir():
            roots.append(path)
    return roots


def sidecar_to_candidate(
    workspace_root: Path,
    sidecar_path: Path,
) -> tuple[StartupCandidate | None, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    label = normalize_rel_path(sidecar_path, workspace_root)

    if not sidecar_path.name.endswith(".meta.json"):
        warnings.append(f"{label}: ignored because sidecar name must end with .meta.json")
        return None, errors, warnings

    md_name = sidecar_path.name[: -len(".meta.json")] + ".md"
    md_path = sidecar_path.with_name(md_name)
    if not md_path.exists():
        warnings.append(f"{label}: paired markdown file not found: {md_name}")
        return None, errors, warnings

    try:
        _ = read_text_utf8_strict(md_path)
    except UnicodeDecodeError as exc:
        errors.append(f"{label}: paired markdown file is not valid UTF-8: {exc}")
        return None, errors, warnings

    try:
        raw = read_json_file(sidecar_path)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        warnings.append(f"{label}: invalid sidecar JSON or encoding: {exc}")
        return None, errors, warnings

    if not isinstance(raw, dict):
        warnings.append(f"{label}: sidecar must be a JSON object.")
        return None, errors, warnings

    if raw.get("startup_kernel_include") is not True:
        warnings.append(f"{label}: ignored because startup_kernel_include is not true.")
        return None, errors, warnings

    missing = sorted(REQUIRED_SIDECAR_KEYS - set(raw.keys()))
    extra = sorted(set(raw.keys()) - ALLOWED_SIDECAR_KEYS)
    if missing:
        errors.append(f"{label}: missing required sidecar keys: {missing}")
        return None, errors, warnings
    if extra:
        warnings.append(f"{label}: extra sidecar keys present: {extra}")

    canonical_source = normalize_rel_path(md_path, workspace_root)
    declared_canonical = raw.get("canonical_source")
    if declared_canonical is not None:
        declared = str(declared_canonical).replace("\\", "/")
        if declared != canonical_source:
            errors.append(
                f"{label}: canonical_source mismatch. Declared {declared}, inferred {canonical_source}."
            )

    load_mode = str(raw.get("startup_load_mode", ""))
    generated_filename = str(raw.get("startup_generated_filename", ""))
    prompt_id = str(raw.get("prompt_id", ""))
    role = str(raw.get("startup_role", ""))

    if load_mode != "always_startup":
        errors.append(f"{label}: startup_load_mode must be always_startup in v1.")

    if not GENERATED_FILENAME_RE.match(generated_filename):
        errors.append(
            f"{label}: startup_generated_filename must match NN_name.md: {generated_filename}"
        )

    if not PROMPT_ID_RE.match(prompt_id):
        errors.append(
            f"{label}: prompt_id must be lowercase alphanumeric plus underscores: {prompt_id}"
        )

    if not role.strip():
        errors.append(f"{label}: startup_role must be non-empty.")
    elif len(role) > 200:
        errors.append(f"{label}: startup_role must be 200 characters or less.")

    optional_load_order = None
    if "load_order" in raw:
        try:
            optional_load_order = int(raw["load_order"])
        except (TypeError, ValueError):
            errors.append(f"{label}: optional load_order must be an integer when present.")

    size_bytes = md_path.stat().st_size
    if size_bytes > MAX_CANDIDATE_SIZE_BYTES:
        warnings.append(
            f"{label}: candidate markdown is large ({size_bytes} bytes). "
            f"Recommended maximum is {MAX_CANDIDATE_SIZE_BYTES} bytes."
        )

    if errors:
        return None, errors, warnings

    return (
        StartupCandidate(
            canonical_source=canonical_source,
            generated_filename=generated_filename,
            prompt_id=prompt_id,
            load_mode=load_mode,
            role=role,
            md_path=md_path,
            sidecar_path=sidecar_path,
            size_bytes=size_bytes,
            optional_load_order=optional_load_order,
        ),
        errors,
        warnings,
    )


def find_sidecar_candidates(workspace_root: Path) -> tuple[list[StartupCandidate], list[str], list[str], list[str]]:
    candidates: list[StartupCandidate] = []
    errors: list[str] = []
    warnings: list[str] = []
    ignored: list[str] = []

    for root in allowed_scan_roots(workspace_root):
        for sidecar_path in sorted(root.rglob("*.meta.json")):
            rel_sidecar = normalize_rel_path(sidecar_path, workspace_root)
            if is_hidden_or_cache_path(sidecar_path.relative_to(workspace_root)):
                ignored.append(f"{rel_sidecar}: hidden/cache path ignored.")
                continue
            if not is_relative_to_safe(sidecar_path, workspace_root):
                errors.append(f"{rel_sidecar}: sidecar escapes workspace root.")
                continue
            candidate, item_errors, item_warnings = sidecar_to_candidate(workspace_root, sidecar_path)
            errors.extend(item_errors)
            warnings.extend(item_warnings)
            if candidate is not None:
                candidates.append(candidate)

    validate_candidate_set(candidates, errors, warnings)
    return candidates, errors, warnings, ignored


def validate_candidate_set(
    candidates: list[StartupCandidate],
    errors: list[str],
    warnings: list[str],
) -> None:
    seen_canonical: dict[str, str] = {}
    seen_generated: dict[str, str] = {}
    seen_prompt_ids: dict[str, str] = {}

    for candidate in candidates:
        if candidate.canonical_source in seen_canonical:
            errors.append(
                "Duplicate candidate canonical_source "
                f"{candidate.canonical_source}: {candidate.sidecar_path} and {seen_canonical[candidate.canonical_source]}"
            )
        seen_canonical[candidate.canonical_source] = str(candidate.sidecar_path)

        if candidate.generated_filename in seen_generated:
            errors.append(
                "Duplicate candidate startup_generated_filename "
                f"{candidate.generated_filename}: {candidate.sidecar_path} and {seen_generated[candidate.generated_filename]}"
            )
        seen_generated[candidate.generated_filename] = str(candidate.sidecar_path)

        if candidate.prompt_id in seen_prompt_ids:
            errors.append(
                "Duplicate candidate prompt_id "
                f"{candidate.prompt_id}: {candidate.sidecar_path} and {seen_prompt_ids[candidate.prompt_id]}"
            )
        seen_prompt_ids[candidate.prompt_id] = str(candidate.sidecar_path)

        if candidate.optional_load_order is not None:
            warnings.append(
                f"{candidate.canonical_source}: load_order is present in sidecar. "
                "v1 reports it only; the human source map remains authoritative."
            )

    if len(candidates) > MAX_NEW_CANDIDATES_WARNING:
        warnings.append(
            f"Many startup candidates detected ({len(candidates)}). Review carefully before adding any to startup."
        )


def compare_candidates_to_source_map(
    entries: list[SourceMapEntry],
    candidates: list[StartupCandidate],
) -> tuple[list[StartupCandidate], list[StartupCandidate], list[str]]:
    existing_by_canonical = {entry.canonical_source: entry for entry in entries}
    existing_by_generated = {entry.generated_filename: entry for entry in entries}
    existing_by_prompt_id = {entry.prompt_id: entry for entry in entries}

    existing_candidates: list[StartupCandidate] = []
    missing_candidates: list[StartupCandidate] = []
    warnings: list[str] = []

    for candidate in candidates:
        if candidate.canonical_source in existing_by_canonical:
            existing_candidates.append(candidate)
            continue

        conflicts: list[str] = []
        if candidate.generated_filename in existing_by_generated:
            conflicts.append(
                "generated_filename already exists in source map: "
                f"{candidate.generated_filename}"
            )
        if candidate.prompt_id in existing_by_prompt_id:
            conflicts.append(
                f"prompt_id already exists in source map: {candidate.prompt_id}"
            )

        if conflicts:
            warnings.append(
                f"{candidate.canonical_source}: conflict; not suggested. " + "; ".join(conflicts)
            )
        else:
            missing_candidates.append(candidate)

    return existing_candidates, missing_candidates, warnings


def suggested_next_load_order(entries: list[SourceMapEntry]) -> int:
    return max((entry.load_order for entry in entries), default=0) + 1


def suggested_next_filename_number(entries: list[SourceMapEntry]) -> int:
    numbers: list[int] = []
    for entry in entries:
        match = re.match(r"^([0-9]{2})_", entry.generated_filename)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def create_report(
    workspace_root: Path,
    source_map_path: Path,
    entries: list[SourceMapEntry],
    result: AuditResult,
) -> str:
    now = utc_now_iso()
    next_order = suggested_next_load_order(entries)
    next_number = suggested_next_filename_number(entries)

    lines: list[str] = []
    lines.append("# STARTUP_ROUTING_KERNEL_SOURCES Update Candidate Report")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"Workspace root: {workspace_root}")
    lines.append(f"Source map: {source_map_path}")
    lines.append(f"Source map SHA-256: {result.source_map_sha256}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Current source-map entries: {len(entries)}")
    lines.append(f"- Existing marked candidates already mapped: {len(result.existing_candidates)}")
    lines.append(f"- Missing marked candidates: {len(result.missing_candidates)}")
    lines.append(f"- Stale source-map entries: {len(result.stale_entries)}")
    lines.append(f"- Source-map errors: {len(result.source_map_errors)}")
    lines.append(f"- Candidate errors: {len(result.candidate_errors)}")
    lines.append(f"- Warnings: {len(result.source_map_warnings) + len(result.sidecar_warnings) + len(result.candidate_warnings)}")
    lines.append(f"- Suggested next load_order: {next_order}")
    lines.append(f"- Suggested next filename number: {next_number:02d}")
    lines.append("")
    lines.append("## Status meaning")
    lines.append("")
    lines.append("- NO_UPDATE_NEEDED means no marked candidate is missing from the source map.")
    lines.append("- UPDATE_CANDIDATE_FOUND means one or more marked candidates need human review.")
    lines.append("- AUDIT_ERRORS means source-map or candidate errors must be fixed before changes.")
    lines.append("")
    lines.append("## Source-map errors")
    lines.append("")
    append_items(lines, result.source_map_errors)
    lines.append("")
    lines.append("## Candidate errors")
    lines.append("")
    append_items(lines, result.candidate_errors)
    lines.append("")
    lines.append("## Source-map warnings")
    lines.append("")
    append_items(lines, result.source_map_warnings)
    lines.append("")
    lines.append("## Sidecar warnings")
    lines.append("")
    append_items(lines, result.sidecar_warnings)
    lines.append("")
    lines.append("## Candidate warnings")
    lines.append("")
    append_items(lines, result.candidate_warnings)
    lines.append("")
    lines.append("## Stale source-map entries")
    lines.append("")
    append_items(lines, result.stale_entries)
    lines.append("")
    lines.append("## Existing marked candidates already in source map")
    lines.append("")
    if result.existing_candidates:
        for candidate in result.existing_candidates:
            lines.append(f"- {candidate.prompt_id}: {candidate.canonical_source}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Missing startup candidates")
    lines.append("")
    if result.missing_candidates:
        for index, candidate in enumerate(result.missing_candidates, start=0):
            proposed_order = next_order + index
            lines.append(f"### {candidate.prompt_id}")
            lines.append("")
            lines.append(f"- canonical_source: `{candidate.canonical_source}`")
            lines.append(f"- generated_filename: `{candidate.generated_filename}`")
            lines.append(f"- prompt_id: `{candidate.prompt_id}`")
            lines.append(f"- load_mode: `{candidate.load_mode}`")
            lines.append(f"- role: `{candidate.role}`")
            lines.append(f"- sidecar: `{normalize_rel_path(candidate.sidecar_path, workspace_root)}`")
            lines.append(f"- size_bytes: {candidate.size_bytes}")
            lines.append(f"- suggested load_order if accepted: {proposed_order}")
            lines.append("")
            lines.append("Suggested JSON entry for manual review:")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(
                {
                    "load_order": proposed_order,
                    "canonical_source": candidate.canonical_source,
                    "generated_filename": candidate.generated_filename,
                    "prompt_id": candidate.prompt_id,
                    "load_mode": candidate.load_mode,
                    "role": candidate.role,
                },
                indent=2,
                ensure_ascii=False,
            ))
            lines.append("```")
            lines.append("")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Ignored sidecars")
    lines.append("")
    append_items(lines, result.ignored_sidecars)
    lines.append("")
    lines.append("## Required human workflow")
    lines.append("")
    lines.append("1. Review this report.")
    lines.append("2. If a missing candidate should be startup-loaded, manually edit STARTUP_ROUTING_KERNEL_SOURCES.json.")
    lines.append("3. Re-run this auditor until no unexpected missing candidates remain.")
    lines.append("4. Then run sync_startup_routing_kernel_pack.py --ensure-sync --yes.")
    lines.append("")
    return "\n".join(lines) + "\n"


def append_items(lines: list[str], items: list[str]) -> None:
    if items:
        for item in items:
            lines.append(f"- {item}")
    else:
        lines.append("- None")


def run_audit(workspace_root: Path, report_filename: str) -> tuple[int, str, Path, list[SourceMapEntry], AuditResult]:
    source_map_path = workspace_root / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME
    report_path = workspace_root / TOOLS_DIR_NAME / report_filename
    source_map_sha256 = sha256_file(source_map_path)

    entries, source_errors, source_warnings = parse_source_map(source_map_path)
    stale_entries = detect_stale_entries(workspace_root, entries)

    candidates: list[StartupCandidate] = []
    candidate_errors: list[str] = []
    sidecar_warnings: list[str] = []
    ignored_sidecars: list[str] = []
    candidate_warnings: list[str] = []
    existing_candidates: list[StartupCandidate] = []
    missing_candidates: list[StartupCandidate] = []

    if not source_errors:
        candidates, candidate_errors, sidecar_warnings, ignored_sidecars = find_sidecar_candidates(workspace_root)
        existing_candidates, missing_candidates, compare_warnings = compare_candidates_to_source_map(entries, candidates)
        candidate_warnings.extend(compare_warnings)

        if len(entries) + len(missing_candidates) > MAX_STARTUP_SOURCES_WARNING:
            candidate_warnings.append(
                "Adding all missing candidates would exceed the recommended startup source count "
                f"of {MAX_STARTUP_SOURCES_WARNING}."
            )

    result = AuditResult(
        source_map_errors=source_errors,
        source_map_warnings=source_warnings,
        sidecar_warnings=sidecar_warnings,
        candidate_errors=candidate_errors,
        candidate_warnings=candidate_warnings,
        stale_entries=stale_entries,
        existing_candidates=existing_candidates,
        missing_candidates=missing_candidates,
        ignored_sidecars=ignored_sidecars,
        source_map_sha256=source_map_sha256,
        report_path=report_path,
    )

    report = create_report(workspace_root, source_map_path, entries, result)
    write_text_utf8(report_path, report)

    if source_errors or candidate_errors:
        return 2, "AUDIT_ERRORS", report_path, entries, result
    if missing_candidates:
        return 1, "UPDATE_CANDIDATE_FOUND", report_path, entries, result
    return 0, "NO_UPDATE_NEEDED", report_path, entries, result


def load_source_map_object(source_map_path: Path) -> dict[str, Any]:
    raw = read_json_file(source_map_path)
    if not isinstance(raw, dict):
        raise ValueError("Source map must be a JSON object.")
    if not isinstance(raw.get("startup_sources"), list):
        raise ValueError("Source map must contain a startup_sources list.")
    return raw


def proposed_entry_for_candidate(candidate: StartupCandidate, load_order: int) -> dict[str, Any]:
    return {
        "load_order": load_order,
        "canonical_source": candidate.canonical_source,
        "generated_filename": candidate.generated_filename,
        "prompt_id": candidate.prompt_id,
        "load_mode": candidate.load_mode,
        "role": candidate.role,
    }


def explain_missing_candidates(workspace_root: Path, entries: list[SourceMapEntry], result: AuditResult) -> None:
    next_order = suggested_next_load_order(entries)
    print("")
    print("STARTUP CANDIDATES FOUND")
    print("These prompts have explicit .meta.json startup sidecars but are not in STARTUP_ROUTING_KERNEL_SOURCES.json.")
    print("Only answer YES if they should be loaded in every future startup ZIP.")
    print("")
    for index, candidate in enumerate(result.missing_candidates, start=0):
        proposed_order = next_order + index
        print(f"Candidate {index + 1}:")
        print(f"  canonical_source: {candidate.canonical_source}")
        print(f"  generated_filename: {candidate.generated_filename}")
        print(f"  prompt_id: {candidate.prompt_id}")
        print(f"  load_mode: {candidate.load_mode}")
        print(f"  role: {candidate.role}")
        print(f"  sidecar: {normalize_rel_path(candidate.sidecar_path, workspace_root)}")
        print(f"  size_bytes: {candidate.size_bytes}")
        print(f"  proposed load_order: {proposed_order}")
        print("  proposed source-map entry:")
        print(json.dumps(proposed_entry_for_candidate(candidate, proposed_order), indent=2, ensure_ascii=False))
        print("")


def ask_yes_no() -> bool:
    try:
        answer = input("Update STARTUP_ROUTING_KERNEL_SOURCES.json with these candidates and regenerate startup delivery? Type YES to proceed: ")
    except EOFError:
        print("No interactive answer was provided. No changes were applied.")
        return False
    return answer.strip() == "YES"


def atomic_write_text(path: Path, text: str) -> None:
    tmp_path = path.with_name(path.name + ".tmp")
    write_text_utf8(tmp_path, text)
    os.replace(tmp_path, path)


def update_source_map_with_candidates(
    workspace_root: Path,
    entries: list[SourceMapEntry],
    candidates: list[StartupCandidate],
) -> Path:
    source_map_path = workspace_root / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME
    original_text = read_text_utf8_strict(source_map_path)
    source_map = load_source_map_object(source_map_path)
    source_map.setdefault("schema_version", 1)
    sources = list(source_map["startup_sources"])
    next_order = suggested_next_load_order(entries)

    for index, candidate in enumerate(candidates, start=0):
        sources.append(proposed_entry_for_candidate(candidate, next_order + index))

    source_map["startup_sources"] = sources
    new_text = json.dumps(source_map, indent=2, ensure_ascii=False) + "\n"

    atomic_write_text(source_map_path, new_text)
    try:
        _new_entries, new_errors, _new_warnings = parse_source_map(source_map_path)
        if new_errors:
            raise ValueError("Updated source map failed validation: " + "; ".join(new_errors))
    except Exception:
        atomic_write_text(source_map_path, original_text)
        raise

    return source_map_path


def run_sync_generator(workspace_root: Path) -> int:
    sync_script = workspace_root / TOOLS_DIR_NAME / SYNC_SCRIPT_FILENAME
    if not sync_script.exists():
        print(f"SYNC FAILED: missing generator: {sync_script}")
        return 3

    command = [
        sys.executable,
        str(sync_script),
        "--ensure-sync",
        "--yes",
    ]
    print("")
    print("RUNNING STARTUP DELIVERY SYNC")
    print("Command: python .\\prompt_tools\\sync_startup_routing_kernel_pack.py --ensure-sync --yes")
    sys.stdout.flush()
    completed = subprocess.run(command, cwd=str(workspace_root), text=True, check=False)
    return int(completed.returncode)


def handle_interactive_update(
    workspace_root: Path,
    entries: list[SourceMapEntry],
    result: AuditResult,
) -> int:
    explain_missing_candidates(workspace_root, entries, result)
    if not ask_yes_no():
        print("UPDATE CANCELLED BY HUMAN")
        print("No source-map or delivery files were changed.")
        print("EXIT_CODE: 1")
        return 1

    try:
        updated_path = update_source_map_with_candidates(workspace_root, entries, result.missing_candidates)
    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print("SOURCE MAP UPDATE FAILED")
        print(f"ERROR: {exc}")
        print("EXIT_CODE: 3")
        return 3

    print("")
    print("SOURCE MAP UPDATE OK")
    print(f"Updated: {updated_path}")
    sys.stdout.flush()

    sync_code = run_sync_generator(workspace_root)
    if sync_code != 0:
        print("SYNC FAILED")
        print("STARTUP_ROUTING_KERNEL_SOURCES.json was updated, but startup delivery regeneration failed.")
        print(f"EXIT_CODE: {sync_code}")
        return sync_code

    print("")
    print("SYNC OK")
    print("STARTUP ROUTING KERNEL SOURCE MAP UPDATE COMPLETE")
    print("EXIT_CODE: 0")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit explicit startup routing kernel candidates and optionally update after YES confirmation."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace root containing prompt_library and prompt_tools.",
    )
    parser.add_argument(
        "--report-filename",
        default=REPORT_FILENAME,
        help="Report filename written inside prompt_tools.",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Report-only mode. Do not ask to update the source map.",
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Do not ask to update candidates; write report and return status only.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        workspace_root = detect_workspace_root(Path(__file__).resolve(), args.workspace)
        code, status, report_path, entries, result = run_audit(workspace_root, args.report_filename)

        print("STARTUP ROUTING KERNEL CANDIDATE AUDIT")
        print(f"Workspace root: {workspace_root}")
        print(f"Report: {report_path}")
        print(f"STATUS: {status}")
        print(f"EXIT_CODE: {code}")

        if status == "UPDATE_CANDIDATE_FOUND" and not args.report and not args.no_interactive:
            return handle_interactive_update(workspace_root, entries, result)

        return code

    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print("STARTUP ROUTING KERNEL CANDIDATE AUDIT")
        print("STATUS: AUDIT_FATAL_ERROR")
        print(f"ERROR: {exc}")
        print("EXIT_CODE: 2")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
