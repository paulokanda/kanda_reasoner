# project-path: kanda_reasoner_app/freeze_hint_intake/frozen_matching.py
"""Frozen-feature matching helpers for freeze hint intake."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Mapping

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_project_freeze_after_update_dir,
    legacy_project_freeze_after_update_dir,
)

from .paths_io import _safe_slug

def _find_matching_frozen_feature(project_root: Path, record: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return a frozen feature match for the latest hint, if any.

    The local freeze writer should mark a hint used after Confirm and Write, but
    this function protects the workflow when project state is imperfect:
    - freeze_index.json may be missing the newest entry;
    - the entry file may exist even when the index is stale;
    - the saved hint may use underscores while the freeze ID uses hyphens.

    Detection therefore checks both freeze_index.json and entry/*.md files.
    """

    if not isinstance(record, Mapping):
        return None

    candidate_slugs = _candidate_feature_slugs_from_record(record)
    if not candidate_slugs:
        return None

    entry_match = _find_matching_frozen_feature_in_entry_files(
        project_root,
        candidate_slugs,
    )
    if entry_match is not None:
        return entry_match

    # freeze_index.json is derived exposure state, not write authority. A stale
    # index-only record must never consume a current freeze hint when no
    # canonical frozen entry exists for that feature.
    return None

def _candidate_feature_slugs_from_record(record: Mapping[str, Any]) -> set[str]:
    """Support candidate feature slugs from record behavior.
    
    Parameters
    ----------
    record : Mapping[str, Any]
        The record value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    hint = record.get("hint") if isinstance(record.get("hint"), Mapping) else {}
    form_inputs = record.get("form_inputs") if isinstance(record.get("form_inputs"), Mapping) else {}
    candidates = {
        _safe_slug(str(hint.get("feature_id") or "")),
        _safe_slug(str(hint.get("feature_title") or "")),
        _safe_slug(str(form_inputs.get("feature_title") or "")),
    }
    cleaned = {slug for slug in candidates if slug and slug != "freeze-hint"}
    return cleaned

def _find_matching_frozen_feature_in_index(project_root: Path, candidate_slugs: set[str]) -> dict[str, Any] | None:
    """Support find matching frozen feature in index behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    candidate_slugs : set[str]
        The candidate slugs value.
    
    Returns
    -------
    dict[str, Any] | None
        The mapped values.
    """
    
    freeze_root = analysis_project_freeze_after_update_dir(project_root)
    index_path = freeze_root / "frozen_features_memory" / "freeze_index.json"
    if not index_path.exists():
        legacy_index = legacy_project_freeze_after_update_dir(project_root) / "frozen_features_memory" / "freeze_index.json"
        index_path = legacy_index
    if not index_path.exists():
        return None

    try:
        index_data = json.loads(index_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None

    freezes = index_data.get("freezes") if isinstance(index_data, Mapping) else None
    if not isinstance(freezes, list):
        return None

    for item in freezes:
        if not isinstance(item, Mapping):
            continue
        if not _freeze_index_item_can_consume_hint(item):
            continue
        item_slugs = _freeze_index_item_slugs(item)
        if candidate_slugs.intersection(item_slugs):
            return dict(item)
    return None

def _freeze_index_item_can_consume_hint(item: Mapping[str, Any]) -> bool:
    """Support freeze index item can consume hint behavior.
    
    Parameters
    ----------
    item : Mapping[str, Any]
        The item value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    status = str(item.get("status") or "").strip().casefold()
    if status and status not in {"frozen", "active", "validated"}:
        return False
    superseded_by = str(item.get("superseded_by") or "").strip()
    return not superseded_by

def _freeze_index_item_slugs(item: Mapping[str, Any]) -> set[str]:
    """Support freeze index item slugs behavior.
    
    Parameters
    ----------
    item : Mapping[str, Any]
        The item value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    freeze_id = str(item.get("freeze_id") or "").strip()
    feature_title = str(item.get("feature_title") or item.get("title") or "").strip()
    entry_path = str(item.get("entry") or "").strip()
    slugs = {_safe_slug(freeze_id), _safe_slug(feature_title)}
    tail = _freeze_feature_tail_slug(freeze_id)
    if tail:
        slugs.add(tail)
    if entry_path:
        entry_stem = Path(entry_path).stem
        slugs.add(_safe_slug(entry_stem))
        entry_tail = _freeze_feature_tail_slug(entry_stem)
        if entry_tail:
            slugs.add(entry_tail)
    slugs.discard("freeze-hint")
    slugs.discard("")
    return slugs

def _find_matching_frozen_feature_in_entry_files(project_root: Path, candidate_slugs: set[str]) -> dict[str, Any] | None:
    """Support find matching frozen feature in entry files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    candidate_slugs : set[str]
        The candidate slugs value.
    
    Returns
    -------
    dict[str, Any] | None
        The mapped values.
    """
    
    freeze_root = analysis_project_freeze_after_update_dir(project_root)
    entries_root = freeze_root / "frozen_features_memory" / "entries"
    if not entries_root.exists() or not entries_root.is_dir():
        legacy_entries = legacy_project_freeze_after_update_dir(project_root) / "frozen_features_memory" / "entries"
        entries_root = legacy_entries
    if not entries_root.exists() or not entries_root.is_dir():
        return None

    for entry_file in sorted(entries_root.glob("freeze-*.md"), key=lambda item: item.name.lower()):
        if not entry_file.is_file():
            continue
        match = _entry_file_frozen_match(entry_file, candidate_slugs, project_root)
        if match is not None:
            return match
    return None

def _entry_file_frozen_match(entry_file: Path, candidate_slugs: set[str], project_root: Path) -> dict[str, Any] | None:
    """Support entry file frozen match behavior.
    
    Parameters
    ----------
    entry_file : Path
        The entry file value.
    candidate_slugs : set[str]
        The candidate slugs value.
    project_root : Path
        The project root path.
    
    Returns
    -------
    dict[str, Any] | None
        The mapped values.
    """
    
    try:
        text = entry_file.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return None

    head = text[:12000]
    slugs = {_safe_slug(entry_file.stem)}
    tail = _freeze_feature_tail_slug(entry_file.stem)
    if tail:
        slugs.add(tail)

    for pattern in (
        r"freeze_id:\s*[\"\']?([^\"\'\n]+)",
        r"feature_title:\s*[\"\']?([^\"\'\n]+)",
        r"title:\s*[\"\']?([^\"\'\n]+)",
        r'^#\s+(.+)$',
    ):
        for match in re.finditer(pattern, head, flags=re.MULTILINE):
            captured = match.group(1).strip().strip('"\'')
            if captured:
                slugs.add(_safe_slug(captured))
                tail = _freeze_feature_tail_slug(captured)
                if tail:
                    slugs.add(tail)

    # Do not infer frozen status from arbitrary body prose or validation
    # evidence. A freeze entry for one feature may mention another feature in
    # validation notes, protected-path summaries, or next-step text. Only the
    # entry filename, freeze_id, feature_title, title, or H1 heading may identify
    # the feature that the entry itself freezes. This prevents related frozen
    # repair entries from hiding the next current unconsumed patch ZIP.

    slugs.discard("freeze-hint")
    slugs.discard("")
    if not candidate_slugs.intersection(slugs):
        return None

    freeze_id = entry_file.stem
    freeze_id_match = re.search(r"freeze_id:\s*[\"\']?([^\"\'\n]+)", head)
    if freeze_id_match:
        freeze_id = freeze_id_match.group(1).strip().strip('"\'') or freeze_id

    rel_entry = entry_file
    try:
        rel_entry = entry_file.relative_to(project_root)
    except ValueError:
        pass

    return {
        "freeze_id": freeze_id,
        "status": "frozen",
        "entry": str(rel_entry).replace("\\", "/"),
        "source": "entry_file_scan",
    }

def _freeze_feature_tail_slug(freeze_id: str) -> str:
    """Return feature portion from freeze-YYYYMMDD-feature-id freeze IDs."""

    slug = _safe_slug(freeze_id)
    match = re.match(r"^freeze-[0-9]{8}-(.+)$", slug)
    if match:
        return match.group(1)
    return slug

def _same_feature_id_alias(left: Any, right: Any) -> bool:
    """Return True for equivalent feature IDs across underscore/hyphen slug styles.

    KANDA_FREEZE_HINT.json sidecars are normalized to safe slugs when saved
    (for example, freeze_tab_restore_v1 becomes freeze-tab-restore-v1), while
    validation markers and validation scripts often keep the original underscore
    feature_id. These are the same feature identity and must not block merging
    post-validation evidence into the project-local freeze hint intake record.
    """

    left_text = str(left or "").strip()
    right_text = str(right or "").strip()
    if not left_text or not right_text:
        return False
    if left_text == right_text:
        return True
    return _safe_slug(left_text) == _safe_slug(right_text)

def _same_feature_identity(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Return True when two freeze hints describe the same feature/patch."""

    left_id = str(left.get("feature_id") or "").strip()
    right_id = str(right.get("feature_id") or "").strip()
    left_patch = str(left.get("patch_name") or "").strip()
    right_patch = str(right.get("patch_name") or "").strip()
    if left_id and right_id and _same_feature_id_alias(left_id, right_id):
        if left_patch and right_patch:
            return left_patch == right_patch
        return True
    left_title = str(left.get("feature_title") or "").strip()
    right_title = str(right.get("feature_title") or "").strip()
    return bool(left_title and right_title and left_title == right_title and (not left_patch or not right_patch or left_patch == right_patch))
