"""Path, source-signature, slug, time, and JSON write helpers for freeze hint intake."""

from __future__ import annotations

__all__: list[str] = []


from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Mapping

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_project_freeze_after_update_dir,
)

from .models import (
    CONSUMED_NAME,
    HISTORY_REL,
    INTAKE_REL,
    LATEST_NAME,
    FreezeHintIntakeError,
    FreezeHintIntakePaths,
)

def build_freeze_hint_intake_paths(project_root: str | Path) -> FreezeHintIntakePaths:
    """Build external project-support paths for freeze hint intake."""

    root = _resolve_project_root(project_root)
    box_root = analysis_project_freeze_after_update_dir(root)
    intake_root = box_root / INTAKE_REL
    return FreezeHintIntakePaths(
        project_root=root,
        intake_root=intake_root,
        history_root=box_root / HISTORY_REL,
        latest_hint=intake_root / LATEST_NAME,
        consumed_hints=intake_root / CONSUMED_NAME,
    )

def _resolve_project_root(project_root: str | Path) -> Path:
    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise FreezeHintIntakeError(f"Project root is not a directory: {root}")
    if root.name == "project_freeze_ledger":
        raise FreezeHintIntakeError("Refusing project_freeze_ledger as active project root.")
    return root

def _default_staging_dir(project_root: Path) -> Path:
    anchor = project_root.anchor
    if anchor:
        return Path(anchor) / (project_root.name + "_delete_after_daily_work")
    return project_root.parent / (project_root.name + "_delete_after_daily_work")

def _source_signature(path: Path) -> dict[str, Any]:
    resolved = Path(path).expanduser().resolve()
    stat = resolved.stat()
    return {
        "source_path": str(resolved),
        "source_name": resolved.name,
        "source_mtime_ns": int(stat.st_mtime_ns),
        "source_size_bytes": int(stat.st_size),
    }

def _safe_mtime_ns(path: Path) -> int:
    try:
        return int(path.stat().st_mtime_ns)
    except OSError:
        return 0

def _history_filename(saved_at_utc: str, hint: Mapping[str, Any]) -> str:
    stamp = re.sub(r"[^0-9A-Za-z]+", "", saved_at_utc)[:15]
    feature = _safe_slug(str(hint.get("feature_id") or hint.get("feature_title") or "freeze-hint"))
    return stamp + "_" + feature + ".json"

def _safe_slug(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "freeze-hint"

def _coerce_mapping(value: Any) -> dict[str, Any]:
    """Return a dictionary for mapping-like values and tolerate legacy scalars.

    Earlier formulary-data records may contain fields such as
    ``"source": "formulary_data_zip"``.  Those records are valid historical
    intake state, but ``dict("formulary_data_zip")`` raises ValueError.  The
    intake contract must treat non-mapping source values as absent metadata, not
    crash the Freeze tab formulary.
    """

    if isinstance(value, Mapping):
        return dict(value)
    return {}

def _source_name(record: Mapping[str, Any]) -> str:
    source = _coerce_mapping(record.get("source"))
    name = str(source.get("source_name") or record.get("source_zip") or "").strip()
    if name:
        return name
    path_text = str(source.get("source_path") or "").strip()
    return Path(path_text).name if path_text else "unknown"

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _atomic_write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
