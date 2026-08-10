"""Read-only Preview and explicit quarantine for Tool-source captures.

Release 3 never moves an identified external-Project capture during package
installation or validation.  This module first records exact path, size, hash,
and destination evidence under Tool Support.  A separate call with an exact
human confirmation token performs the reversible quarantine operation.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_support_boundary import (
    canonical_tool_support_root,
)
from kanda_reasoner_app.source_hygiene.tool_archive_policy import (
    ToolArchivePolicyError,
    ToolPathClassification,
    classify_tool_source_path,
    iter_known_capture_records,
)

__all__ = [
    "CAPTURE_FEATURE_ID",
    "CaptureQuarantineError",
    "CaptureQuarantineRecord",
    "apply_capture_quarantine",
    "build_capture_quarantine_preview",
    "capture_quarantine_confirmation_token",
    "capture_quarantine_root",
    "restore_quarantined_captures",
]

CAPTURE_FEATURE_ID = "tool-source-and-archive-hygiene-v1"
_PREVIEW_FILENAME = CAPTURE_FEATURE_ID + "_capture_preview.json"
_RECEIPT_FILENAME = CAPTURE_FEATURE_ID + "_capture_quarantine_receipt.json"


class CaptureQuarantineError(RuntimeError):
    """Raised when Preview or quarantine evidence is unsafe or inconsistent."""


@dataclass(frozen=True)
class CaptureQuarantineRecord:
    """Describe one exact source capture and its Tool Support destination."""

    relative_path: str
    source_path: str
    size_bytes: int
    sha256: str
    classification: str
    destination_path: str
    source_exists: bool
    destination_exists: bool
    state: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def capture_quarantine_root(tool_root: str | Path) -> Path:
    """Return the durable Tool Support root for quarantined captures."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    support = canonical_tool_support_root(root)
    try:
        support.relative_to(root)
    except ValueError:
        pass
    else:
        raise CaptureQuarantineError(
            "TOOL_CAPTURE_QUARANTINE_INSIDE_TOOL_SOURCE:" + str(support)
        )
    return support / "tool_source_hygiene"


def capture_quarantine_confirmation_token() -> str:
    """Return the exact token required for capture movement."""
    return "QUARANTINE " + CAPTURE_FEATURE_ID


def _record_destination(base: Path, sha256_value: str, source: Path) -> Path:
    return (
        base
        / "quarantined_foreign_project_captures"
        / sha256_value
        / source.name
    )


def _build_record(
    tool_root: Path,
    base: Path,
    raw: dict[str, Any],
) -> CaptureQuarantineRecord:
    relative = str(raw.get("path", "")).replace("\\", "/").strip("/")
    expected_hash = str(raw.get("sha256", "")).strip().lower()
    expected_size = int(raw.get("size_bytes", -1))
    if not relative or len(expected_hash) != 64 or expected_size < 0:
        raise CaptureQuarantineError("KNOWN_CAPTURE_RECORD_INVALID")
    source = (tool_root / relative).resolve(strict=False)
    try:
        source.relative_to(tool_root)
    except ValueError as exc:
        raise CaptureQuarantineError(
            "KNOWN_CAPTURE_SOURCE_OUTSIDE_TOOL_ROOT:" + str(source)
        ) from exc
    try:
        decision = classify_tool_source_path(tool_root, source)
    except ToolArchivePolicyError as exc:
        raise CaptureQuarantineError(str(exc)) from exc
    if decision.classification is not ToolPathClassification.PROJECT_CAPTURE_FORBIDDEN:
        raise CaptureQuarantineError(
            "KNOWN_CAPTURE_CLASSIFICATION_MISMATCH:" + relative
        )

    destination = _record_destination(base, expected_hash, source)
    source_exists = source.is_file()
    destination_exists = destination.is_file()
    if source_exists:
        if source.stat().st_size != expected_size or _sha256_file(source) != expected_hash:
            raise CaptureQuarantineError(
                "KNOWN_CAPTURE_SOURCE_HASH_MISMATCH:" + relative
            )
    if destination_exists:
        if destination.stat().st_size != expected_size or _sha256_file(destination) != expected_hash:
            raise CaptureQuarantineError(
                "KNOWN_CAPTURE_DESTINATION_HASH_MISMATCH:" + str(destination)
            )
    if source_exists and not destination_exists:
        state = "READY_FOR_HUMAN_CONFIRMED_QUARANTINE"
    elif source_exists and destination_exists:
        state = "DUPLICATE_SOURCE_REMAINS_AFTER_PRIOR_COPY"
    elif not source_exists and destination_exists:
        state = "QUARANTINED"
    else:
        state = "CAPTURE_MISSING_FROM_SOURCE_AND_QUARANTINE"
    return CaptureQuarantineRecord(
        relative_path=relative,
        source_path=str(source),
        size_bytes=expected_size,
        sha256=expected_hash,
        classification=decision.classification.value,
        destination_path=str(destination),
        source_exists=source_exists,
        destination_exists=destination_exists,
        state=state,
    )


def build_capture_quarantine_preview(
    tool_root: str | Path,
) -> tuple[Path, tuple[CaptureQuarantineRecord, ...]]:
    """Write read-only migration evidence without changing Tool source."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    base = capture_quarantine_root(root)
    records = tuple(
        _build_record(root, base, raw)
        for raw in iter_known_capture_records(root)
    )
    if not records:
        raise CaptureQuarantineError("KNOWN_CAPTURE_PREVIEW_EMPTY")
    preview_path = base / "previews" / _PREVIEW_FILENAME
    payload = {
        "artifact_type": "tool_source_capture_quarantine_preview",
        "feature_id": CAPTURE_FEATURE_ID,
        "generated_at_utc": _utc_now(),
        "tool_root": str(root),
        "tool_support_root": str(canonical_tool_support_root(root)),
        "read_only_preview": True,
        "source_mutation_performed": False,
        "external_project_mutation_performed": False,
        "confirmation_required": capture_quarantine_confirmation_token(),
        "records": [asdict(record) for record in records],
    }
    _write_json(preview_path, payload)
    return preview_path, records


def _copy_then_remove(source: Path, destination: Path, expected_hash: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".copying")
    if temporary.exists():
        temporary.unlink()
    shutil.copy2(source, temporary)
    if _sha256_file(temporary) != expected_hash:
        temporary.unlink(missing_ok=True)
        raise CaptureQuarantineError(
            "CAPTURE_QUARANTINE_COPY_HASH_MISMATCH:" + str(source)
        )
    os.replace(temporary, destination)
    if _sha256_file(destination) != expected_hash:
        raise CaptureQuarantineError(
            "CAPTURE_QUARANTINE_DESTINATION_HASH_MISMATCH:" + str(destination)
        )
    source.unlink()


def apply_capture_quarantine(
    tool_root: str | Path,
    *,
    confirmation: str,
) -> tuple[Path, tuple[CaptureQuarantineRecord, ...]]:
    """Quarantine exact known captures after explicit human confirmation."""
    expected_confirmation = capture_quarantine_confirmation_token()
    if str(confirmation) != expected_confirmation:
        raise CaptureQuarantineError(
            "CAPTURE_QUARANTINE_EXPLICIT_CONFIRMATION_REQUIRED"
        )
    root = Path(tool_root).expanduser().resolve(strict=False)
    preview_path, before = build_capture_quarantine_preview(root)
    for record in before:
        source = Path(record.source_path)
        destination = Path(record.destination_path)
        if record.state == "QUARANTINED":
            continue
        if record.state == "DUPLICATE_SOURCE_REMAINS_AFTER_PRIOR_COPY":
            source.unlink()
            continue
        if record.state != "READY_FOR_HUMAN_CONFIRMED_QUARANTINE":
            raise CaptureQuarantineError(
                "CAPTURE_QUARANTINE_STATE_REJECTED:" + record.state
            )
        _copy_then_remove(source, destination, record.sha256)

    _, after = build_capture_quarantine_preview(root)
    if any(record.state != "QUARANTINED" for record in after):
        raise CaptureQuarantineError("CAPTURE_QUARANTINE_NOT_COMPLETE")
    receipt_path = capture_quarantine_root(root) / "receipts" / _RECEIPT_FILENAME
    _write_json(
        receipt_path,
        {
            "artifact_type": "tool_source_capture_quarantine_receipt",
            "feature_id": CAPTURE_FEATURE_ID,
            "written_at_utc": _utc_now(),
            "human_confirmation": expected_confirmation,
            "preview_path": str(preview_path),
            "external_project_mutation_performed": False,
            "records": [asdict(record) for record in after],
        },
    )
    return receipt_path, after


def restore_quarantined_captures(
    tool_root: str | Path,
) -> tuple[CaptureQuarantineRecord, ...]:
    """Restore exact source bytes while retaining durable quarantine evidence."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    base = capture_quarantine_root(root)
    before = tuple(
        _build_record(root, base, raw)
        for raw in iter_known_capture_records(root)
    )
    for record in before:
        source = Path(record.source_path)
        destination = Path(record.destination_path)
        if source.exists():
            if _sha256_file(source) != record.sha256:
                raise CaptureQuarantineError(
                    "CAPTURE_ROLLBACK_SOURCE_OCCUPIED:" + str(source)
                )
            continue
        if not destination.is_file() or _sha256_file(destination) != record.sha256:
            raise CaptureQuarantineError(
                "CAPTURE_ROLLBACK_QUARANTINE_MISSING:" + str(destination)
            )
        source.parent.mkdir(parents=True, exist_ok=True)
        temporary = source.with_name(source.name + ".restoring")
        shutil.copy2(destination, temporary)
        if _sha256_file(temporary) != record.sha256:
            temporary.unlink(missing_ok=True)
            raise CaptureQuarantineError(
                "CAPTURE_ROLLBACK_COPY_HASH_MISMATCH:" + str(source)
            )
        os.replace(temporary, source)
    return tuple(
        _build_record(root, base, raw)
        for raw in iter_known_capture_records(root)
    )
