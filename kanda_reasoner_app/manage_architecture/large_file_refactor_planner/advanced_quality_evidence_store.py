# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_evidence_store.py
"""Durable Project-owned persistence for Advanced Quality Review evidence."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
from typing import Mapping
import uuid

from .advanced_quality_evidence_models import (
    EvidenceAuthorizationEvent,
    EvidenceAuthorizationState,
    QualityReviewRunRecord,
    evaluate_authorization_state,
)
from .advanced_quality_review_contract import AnalysisIdentity
from .workbench_project_support_paths import (
    daily_work_root,
    quality_evidence_root,
    quality_evidence_root_blockers,
)

__all__ = [
    "EvidencePersistenceReceipt",
    "append_evidence_authorization_event",
    "latest_evidence_authorization_state",
    "persist_quality_review_run",
    "quality_review_run_root",
    "verify_persisted_quality_review_run",
]


@dataclass(frozen=True)
class EvidencePersistenceReceipt:
    """Prove one immutable run was persisted under the selected Project Support."""

    run_id: str
    run_root: str
    manifest_path: str
    record_hash: str
    manifest_hash: str
    file_hashes: tuple[tuple[str, str], ...]

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready persistence receipt."""
        return {
            "run_id": self.run_id,
            "run_root": self.run_root,
            "manifest_path": self.manifest_path,
            "record_hash": self.record_hash,
            "manifest_hash": self.manifest_hash,
            "file_hashes": [list(item) for item in self.file_hashes],
        }



def quality_review_run_root(
    active_project_root: str | Path,
    record: QualityReviewRunRecord,
) -> Path:
    """Return deterministic immutable destination for one quality review run."""
    identity = record.analysis_identity
    card_component = _identity_component(
        "card",
        identity.project_card_identity,
    )
    target_component = _identity_component(
        "target",
        identity.target_relative_path,
    )
    return (
        quality_evidence_root(active_project_root)
        / card_component
        / target_component
        / ("baseline-" + identity.baseline_hash[:16])
        / ("preview-" + identity.preview_hash[:16])
        / "runs"
        / record.run_id
    )



def persist_quality_review_run(
    active_project_root: str | Path,
    record: QualityReviewRunRecord,
    *,
    raw_evidence: Mapping[str, bytes],
) -> EvidencePersistenceReceipt:
    """Persist one complete immutable evidence run using transient staging."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    final_root = quality_review_run_root(project_root, record).resolve(strict=False)
    blockers = quality_evidence_root_blockers(project_root, final_root)
    if blockers:
        raise ValueError("QUALITY_EVIDENCE_ROOT_BLOCKED:" + "|".join(blockers))
    if final_root.exists():
        raise FileExistsError("QUALITY_REVIEW_RUN_ALREADY_EXISTS:" + str(final_root))

    normalized_raw = _normalize_raw_evidence(raw_evidence)
    _validate_raw_references(record, normalized_raw)
    stage_parent = daily_work_root(project_root) / "quality_evidence_staging"
    stage_root = stage_parent / (
        record.run_id + "." + str(os.getpid()) + "." + uuid.uuid4().hex[:12]
    )
    if stage_root.exists():
        raise FileExistsError("QUALITY_EVIDENCE_STAGE_ALREADY_EXISTS:" + str(stage_root))
    stage_root.mkdir(parents=True, exist_ok=False)
    committed = False
    try:
        _write_run_payload(stage_root, record, normalized_raw)
        manifest = _build_manifest(stage_root, record)
        _write_json(stage_root / "manifest.json", manifest)
        final_root.parent.mkdir(parents=True, exist_ok=True)
        os.replace(stage_root, final_root)
        committed = True
        receipt = _build_receipt(final_root, record)
        blockers = verify_persisted_quality_review_run(project_root, receipt)
        if blockers:
            shutil.rmtree(final_root, ignore_errors=True)
            committed = False
            raise RuntimeError("QUALITY_EVIDENCE_VERIFY_FAILED:" + "|".join(blockers))
        return receipt
    finally:
        if not committed and stage_root.exists():
            shutil.rmtree(stage_root, ignore_errors=True)



def verify_persisted_quality_review_run(
    active_project_root: str | Path,
    receipt: EvidencePersistenceReceipt,
) -> tuple[str, ...]:
    """Verify ownership, manifest integrity, and every persisted payload hash."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    run_root = Path(receipt.run_root).expanduser().resolve(strict=False)
    blockers = list(quality_evidence_root_blockers(project_root, run_root))
    manifest_path = run_root / "manifest.json"
    if not manifest_path.is_file():
        blockers.append("QUALITY_EVIDENCE_MANIFEST_MISSING")
        return tuple(sorted(set(blockers)))
    if _file_hash(manifest_path) != receipt.manifest_hash:
        blockers.append("QUALITY_EVIDENCE_MANIFEST_HASH_MISMATCH")
        return tuple(sorted(set(blockers)))
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8", errors="strict"))
    except (UnicodeError, json.JSONDecodeError):
        blockers.append("QUALITY_EVIDENCE_MANIFEST_INVALID_UTF8_JSON")
        return tuple(sorted(set(blockers)))
    if manifest.get("run_id") != receipt.run_id:
        blockers.append("QUALITY_EVIDENCE_RUN_ID_MISMATCH")
    if manifest.get("record_hash") != receipt.record_hash:
        blockers.append("QUALITY_EVIDENCE_RECORD_HASH_MISMATCH")
    files = manifest.get("files", [])
    if not isinstance(files, list):
        blockers.append("QUALITY_EVIDENCE_MANIFEST_FILES_INVALID")
        return tuple(sorted(set(blockers)))
    for entry in files:
        if not isinstance(entry, dict):
            blockers.append("QUALITY_EVIDENCE_FILE_ENTRY_INVALID")
            continue
        relative_path = _safe_relative_path(str(entry.get("relative_path", "")))
        candidate = (run_root / relative_path).resolve(strict=False)
        if not _is_relative_to(candidate, run_root):
            blockers.append("QUALITY_EVIDENCE_FILE_PATH_ESCAPE")
            continue
        if not candidate.is_file():
            blockers.append("QUALITY_EVIDENCE_FILE_MISSING:" + relative_path)
            continue
        expected_hash = str(entry.get("sha256", ""))
        if _file_hash(candidate) != expected_hash:
            blockers.append("QUALITY_EVIDENCE_FILE_HASH_MISMATCH:" + relative_path)
    return tuple(sorted(set(blockers)))



def append_evidence_authorization_event(
    active_project_root: str | Path,
    record: QualityReviewRunRecord,
    *,
    current_identity: AnalysisIdentity,
    reason: str,
    event_id: str,
    created_at_utc: str | None = None,
) -> EvidenceAuthorizationEvent:
    """Append a stale-state event without rewriting immutable run evidence."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    run_root = quality_review_run_root(project_root, record).resolve(strict=False)
    blockers = quality_evidence_root_blockers(project_root, run_root)
    if blockers:
        raise ValueError("QUALITY_EVIDENCE_ROOT_BLOCKED:" + "|".join(blockers))
    if not (run_root / "manifest.json").is_file():
        raise FileNotFoundError("QUALITY_REVIEW_RUN_NOT_PERSISTED:" + str(run_root))
    prior_state = latest_evidence_authorization_state(run_root)
    evaluated = evaluate_authorization_state(record.analysis_identity, current_identity)
    new_state = (
        prior_state
        if prior_state == EvidenceAuthorizationState.INVALIDATED
        else evaluated
    )
    event = EvidenceAuthorizationEvent(
        schema_version="1.0",
        event_id=_safe_component(event_id, "EVENT_ID"),
        created_at_utc=created_at_utc or _utc_now_text(),
        run_id=record.run_id,
        evidence_identity_hash=record.analysis_identity.identity_hash,
        current_identity_hash=current_identity.identity_hash,
        prior_state=prior_state,
        new_state=new_state,
        reason=_required(reason, "AUTHORIZATION_EVENT_REASON_EMPTY"),
        superseding_preview_hash=(
            current_identity.preview_hash
            if new_state == EvidenceAuthorizationState.STALE
            else ""
        ),
    )
    event_root = run_root / "authorization_events"
    event_root.mkdir(parents=True, exist_ok=True)
    event_path = event_root / (event.event_id + ".json")
    if event_path.exists():
        raise FileExistsError("AUTHORIZATION_EVENT_ALREADY_EXISTS:" + str(event_path))
    _write_json_exclusive(event_path, event.to_dict())
    return event



def latest_evidence_authorization_state(
    run_root: str | Path,
) -> EvidenceAuthorizationState:
    """Derive current authorization state from append-only historical events."""
    root = Path(run_root).expanduser().resolve(strict=False)
    event_root = root / "authorization_events"
    if not event_root.is_dir():
        return EvidenceAuthorizationState.CURRENT
    events: list[tuple[str, EvidenceAuthorizationState]] = []
    for path in event_root.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8", errors="strict"))
            created = str(payload.get("created_at_utc", ""))
            state = EvidenceAuthorizationState(str(payload.get("new_state", "")))
        except (UnicodeError, json.JSONDecodeError, ValueError):
            raise ValueError("AUTHORIZATION_EVENT_INVALID:" + str(path))
        events.append((created + "\0" + path.name, state))
    if not events:
        return EvidenceAuthorizationState.CURRENT
    return sorted(events, key=lambda item: item[0])[-1][1]



def _write_run_payload(
    stage_root: Path,
    record: QualityReviewRunRecord,
    raw_evidence: Mapping[str, bytes],
) -> None:
    """Write exact UTF-8 JSON evidence and bounded raw evidence into staging."""
    _write_json(stage_root / "analysis_identity.json", record.analysis_identity.to_dict())
    _write_json(stage_root / "capabilities.json", [item.to_dict() for item in record.capabilities])
    _write_json(stage_root / "executions.json", [item.to_dict() for item in record.executions])
    _write_json(stage_root / "normalized_findings.json", [item.to_dict() for item in record.findings])
    _write_json(stage_root / "review_record.json", record.to_dict())
    for relative_path, data in raw_evidence.items():
        destination = stage_root / "raw" / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)



def _build_manifest(stage_root: Path, record: QualityReviewRunRecord) -> dict[str, object]:
    """Return manifest over every payload file except the manifest itself."""
    entries: list[dict[str, object]] = []
    for path in sorted(candidate for candidate in stage_root.rglob("*") if candidate.is_file()):
        relative = path.relative_to(stage_root).as_posix()
        entries.append(
            {
                "relative_path": relative,
                "sha256": _file_hash(path),
                "byte_size": path.stat().st_size,
            }
        )
    return {
        "schema_version": "1.0",
        "artifact_type": "advanced_quality_review_immutable_run_manifest",
        "feature_id": record.feature_id,
        "run_id": record.run_id,
        "record_hash": record.record_hash,
        "analysis_identity_hash": record.analysis_identity.identity_hash,
        "created_at_utc": record.created_at_utc,
        "files": entries,
    }



def _build_receipt(
    final_root: Path,
    record: QualityReviewRunRecord,
) -> EvidencePersistenceReceipt:
    manifest_path = final_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8", errors="strict"))
    file_hashes = tuple(
        sorted(
            (str(entry["relative_path"]), str(entry["sha256"]))
            for entry in manifest["files"]
        )
    )
    return EvidencePersistenceReceipt(
        run_id=record.run_id,
        run_root=str(final_root),
        manifest_path=str(manifest_path),
        record_hash=record.record_hash,
        manifest_hash=_file_hash(manifest_path),
        file_hashes=file_hashes,
    )



def _normalize_raw_evidence(raw_evidence: Mapping[str, bytes]) -> dict[str, bytes]:
    normalized: dict[str, bytes] = {}
    for relative_path, data in raw_evidence.items():
        path = _safe_relative_path(relative_path)
        if path in normalized:
            raise ValueError("RAW_EVIDENCE_PATH_DUPLICATE:" + path)
        if not isinstance(data, bytes):
            raise TypeError("RAW_EVIDENCE_MUST_BE_BYTES:" + path)
        normalized[path] = data
    return normalized



def _validate_raw_references(
    record: QualityReviewRunRecord,
    raw_evidence: Mapping[str, bytes],
) -> None:
    for finding in record.findings:
        reference = finding.raw_evidence_reference
        data = raw_evidence.get(reference.relative_path)
        if data is None:
            raise ValueError("RAW_EVIDENCE_REFERENCE_MISSING:" + reference.relative_path)
        digest = hashlib.sha256(data).hexdigest()
        if digest != reference.sha256:
            raise ValueError("RAW_EVIDENCE_REFERENCE_HASH_MISMATCH:" + reference.relative_path)
        if len(data) != reference.byte_size:
            raise ValueError("RAW_EVIDENCE_REFERENCE_SIZE_MISMATCH:" + reference.relative_path)



def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    path.write_bytes(text.encode("utf-8"))



def _write_json_exclusive(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    with path.open("xb") as handle:
        handle.write(text.encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())



def _safe_relative_path(value: str) -> str:
    text = str(value or "").replace("\\", "/").strip()
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("EVIDENCE_RELATIVE_PATH_INVALID:" + text)
    normalized = path.as_posix().lstrip("./")
    if not normalized:
        raise ValueError("EVIDENCE_RELATIVE_PATH_INVALID:" + text)
    return normalized



def _identity_component(prefix: str, value: str) -> str:
    text = str(value or "").strip()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    safe = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in text
    ).strip("_.-")[:48]
    return prefix + "-" + (safe or "identity") + "-" + digest



def _safe_component(value: str, label: str) -> str:
    text = _required(value, label + "_EMPTY")
    cleaned = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in text
    ).strip("_.-")
    if not cleaned:
        raise ValueError(label + "_INVALID")
    return cleaned[:96]



def _required(value: str, error: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(error)
    return text



def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()



def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(base.resolve(strict=False))
        return True
    except ValueError:
        return False



def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
