# project-path: kanda_reasoner_app/engineering_diagnostics/frozen_path_enrichment.py
"""Read-only Project Freeze Memory enrichment through its public box contract."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from kanda_reasoner_app.freeze_after_update import inspect_freeze_after_update_box

from .enrichment_models import DiagnosticFrozenPathEnrichment
from .fingerprinting import normalize_relative_path

__all__ = [
    "DiagnosticFreezeSnapshot",
    "build_diagnostic_freeze_snapshot",
    "classify_diagnostic_frozen_path",
    "related_project_paths_from_evidence",
]

_FREEZE_INDEX_RELATIVE = Path("frozen_features_memory") / "freeze_index.json"
_MAX_INDEX_BYTES = 16 * 1024 * 1024
_MAX_FREEZES = 10000
_RELATED_PATH_KEYS = frozenset(
    {
        "related_path",
        "related_paths",
        "owner_path",
        "target_path",
        "source_path",
        "implementation_path",
        "facade_path",
    }
)


@dataclass(frozen=True, slots=True)
class _ProtectedBinding:
    freeze_id: str
    protected_path: str
    active: bool


@dataclass(frozen=True, slots=True)
class DiagnosticFreezeSnapshot:
    """Prepared immutable public Freeze index snapshot for batch enrichment."""

    state: str
    bindings: tuple[_ProtectedBinding, ...] = ()
    evidence: tuple[str, ...] = ()


def _normalize_protected_path(value: object) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if not text:
        return ""
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts:
        return ""
    return "/".join(part for part in path.parts if part not in ("", "."))


def build_diagnostic_freeze_snapshot(
    project_root: str | Path,
) -> DiagnosticFreezeSnapshot:
    """Inspect and read the public Project Freeze index without writing files."""
    result = inspect_freeze_after_update_box(project_root)
    if not result.ok or result.box_root is None:
        return DiagnosticFreezeSnapshot(
            "UNKNOWN",
            evidence=(
                "freeze_box_status=" + result.status.value,
                "freeze_box_message=" + str(result.message or ""),
            ),
        )
    index_path = result.box_root / _FREEZE_INDEX_RELATIVE
    try:
        if not index_path.is_file():
            return DiagnosticFreezeSnapshot(
                "UNKNOWN",
                evidence=("freeze_index_missing=" + str(index_path),),
            )
        if index_path.stat().st_size > _MAX_INDEX_BYTES:
            return DiagnosticFreezeSnapshot(
                "UNKNOWN",
                evidence=("freeze_index_too_large=" + str(index_path),),
            )
        payload = json.loads(index_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return DiagnosticFreezeSnapshot(
            "UNKNOWN",
            evidence=("freeze_index_invalid=" + str(exc),),
        )
    if not isinstance(payload, Mapping) or payload.get("schema_version") != "1.0":
        return DiagnosticFreezeSnapshot(
            "UNKNOWN",
            evidence=("freeze_index_schema_invalid",),
        )
    freezes = payload.get("freezes")
    if not isinstance(freezes, list) or len(freezes) > _MAX_FREEZES:
        return DiagnosticFreezeSnapshot(
            "UNKNOWN",
            evidence=("freeze_index_freezes_invalid",),
        )
    bindings: list[_ProtectedBinding] = []
    for raw in freezes:
        if not isinstance(raw, Mapping):
            continue
        freeze_id = str(raw.get("freeze_id") or "").strip()
        if not freeze_id:
            continue
        status = str(raw.get("status") or "").strip().lower()
        superseded_by = str(raw.get("superseded_by") or "").strip()
        active = status == "frozen" and not superseded_by
        protected = raw.get("protected_paths")
        if not isinstance(protected, list):
            continue
        for value in protected:
            normalized = _normalize_protected_path(value)
            if normalized:
                bindings.append(_ProtectedBinding(freeze_id, normalized, active))
    ordered = tuple(
        sorted(
            set(bindings),
            key=lambda item: (item.protected_path, item.freeze_id, not item.active),
        )
    )
    return DiagnosticFreezeSnapshot(
        "READY",
        bindings=ordered,
        evidence=("freeze_index=" + str(index_path),),
    )


def _path_matches(relative_path: str, protected_path: str) -> bool:
    return relative_path == protected_path or relative_path.startswith(
        protected_path.rstrip("/") + "/"
    )


def _normalized_related_path(value: object) -> str:
    try:
        return normalize_relative_path(value)
    except Exception:
        return ""


def related_project_paths_from_evidence(
    evidence: Mapping[str, Any],
) -> tuple[str, ...]:
    """Extract only explicit path-bearing evidence fields for frozen impact."""
    output: list[str] = []
    for key, value in evidence.items():
        if str(key).strip().lower() not in _RELATED_PATH_KEYS:
            continue
        values: Iterable[object]
        if isinstance(value, (list, tuple, set, frozenset)):
            values = value
        else:
            values = (value,)
        for item in values:
            normalized = _normalized_related_path(item)
            if normalized and normalized not in output:
                output.append(normalized)
    return tuple(output)


def classify_diagnostic_frozen_path(
    snapshot: DiagnosticFreezeSnapshot,
    relative_path: str,
    *,
    related_paths: Iterable[str] = (),
) -> DiagnosticFrozenPathEnrichment:
    """Classify one finding path against a prepared public Freeze snapshot."""
    if snapshot.state != "READY":
        return DiagnosticFrozenPathEnrichment(
            "UNKNOWN",
            evidence=snapshot.evidence,
        )
    try:
        primary = normalize_relative_path(relative_path)
    except Exception as exc:
        return DiagnosticFrozenPathEnrichment(
            "UNKNOWN",
            evidence=(str(exc),),
        )
    normalized_related = tuple(
        path
        for value in related_paths
        if (path := _normalized_related_path(value)) and path != primary
    )
    active_primary: list[_ProtectedBinding] = []
    historical_primary: list[_ProtectedBinding] = []
    active_related: list[_ProtectedBinding] = []
    for binding in snapshot.bindings:
        if _path_matches(primary, binding.protected_path):
            if binding.active:
                active_primary.append(binding)
            else:
                historical_primary.append(binding)
            continue
        if binding.active and any(
            _path_matches(path, binding.protected_path)
            for path in normalized_related
        ):
            active_related.append(binding)
    selected = active_primary or active_related or historical_primary
    freeze_ids = tuple(sorted({item.freeze_id for item in selected}))
    protected = tuple(sorted({item.protected_path for item in selected}))
    if active_primary:
        status = "FROZEN"
    elif active_related:
        status = "TOUCHES_FROZEN"
    elif historical_primary:
        status = "HISTORICAL_FROZEN"
    else:
        status = "UNFROZEN"
    evidence = list(snapshot.evidence)
    evidence.append("primary_path=" + primary)
    if normalized_related:
        evidence.append("related_paths=" + ",".join(normalized_related))
    return DiagnosticFrozenPathEnrichment(
        status,
        governing_freeze_ids=freeze_ids,
        matched_protected_paths=protected,
        evidence=tuple(evidence),
    )
