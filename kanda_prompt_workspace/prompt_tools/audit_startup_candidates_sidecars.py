"""Sidecar discovery and validation helpers for startup prompt candidate audits."""

from __future__ import annotations
__all__: list[str] = []


import json
from pathlib import Path

from .audit_startup_candidates_models import (
    ALLOWED_SCAN_DIRS,
    ALLOWED_SIDECAR_KEYS,
    GENERATED_FILENAME_RE,
    MAX_CANDIDATE_SIZE_BYTES,
    MAX_NEW_CANDIDATES_WARNING,
    PROMPT_ID_RE,
    REQUIRED_SIDECAR_KEYS,
    SourceMapEntry,
    StartupCandidate,
    read_json_file,
    read_text_utf8_strict,
)
from .audit_startup_candidates_paths import (
    is_hidden_or_cache_path,
    is_relative_to_safe,
    normalize_rel_path,
)

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
